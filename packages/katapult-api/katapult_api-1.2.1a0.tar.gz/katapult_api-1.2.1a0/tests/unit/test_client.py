import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from aiohttp.web_exceptions import HTTPTooManyRequests

from katapult_api.client import Client
from katapult_api.enums import RequestEnums
from katapult_api.utils import task_handler


class TestClient(unittest.IsolatedAsyncioTestCase):
    TEST_API_KEY = "test_key"
    TEST_BASE_URL = "test_url"

    def get_mock_request(self, content: str = '{"body":"success"}', status: int = 200):
        """Returns a mock request method with customizable content and status"""

        async def mock_request(*args, **kwargs) -> tuple[str, str, int]:
            await asyncio.sleep(2)

            mock_response = AsyncMock()
            mock_response.content = content
            mock_response.headers = f'{{"content-length":{len(content)}}}'
            mock_response.status = status

            return mock_response.content, mock_response.headers, mock_response.status

        return mock_request

    def generate_mock_429(self):
        mock_429_response = MagicMock()
        mock_429_response.status = 429
        mock_429_response.headers = MagicMock()
        mock_429_response.headers.get.return_value = "2"
        mock_429_response.headers.__iter__ = lambda self: iter({})
        mock_429_response.headers.items = lambda: {}
        mock_429_response.text = MagicMock(return_value=asyncio.Future())
        mock_429_response.text.return_value.set_result("Rate limited")
        mock_429_response.reason = "Too Many Requests"
        mock_429_response.content_type = "application/json"
        return mock_429_response

    def generate_mock_200(self):
        mock_200_response = MagicMock()
        mock_200_response.status = 200
        mock_200_response.headers = MagicMock()
        mock_200_response.headers.__iter__ = lambda self: iter({})
        mock_200_response.headers.items = lambda: {}
        mock_200_response.text = MagicMock(return_value=asyncio.Future())
        mock_200_response.text.return_value.set_result("{'message':'success'}")
        return mock_200_response

    async def test_various_methods_and_responses(self):
        """Test multiple response scenarios across different HTTP methods"""
        test_cases = [
            # Success cases
            {
                "method": "GET",
                "content": '{"body":"success"}',
                "status": 200,
                "expected_status": 200,
            },
            {
                "method": "POST",
                "content": '{"body":"created"}',
                "status": 201,
                "expected_status": 201,
            },
            {
                "method": "PUT",
                "content": '{"body":"updated"}',
                "status": 200,
                "expected_status": 200,
            },
            {
                "method": "PATCH",
                "content": '{"body":"patched"}',
                "status": 200,
                "expected_status": 200,
            },
            {
                "method": "DEL",
                "content": '{"body":"deleted"}',
                "status": 204,
                "expected_status": 204,
            },
            # Failure cases
            {
                "method": "GET",
                "content": '{"error":"not found"}',
                "status": 404,
                "expected_status": 404,
            },
            {
                "method": "POST",
                "content": '{"error":"bad request"}',
                "status": 400,
                "expected_status": 400,
            },
            {"method": "PUT", "content": "", "status": 500, "expected_status": 500},
            {
                "method": "PATCH",
                "content": '{"message":"rate limit exceeded"}',
                "status": 429,
                "expected_status": 429,
            },
        ]

        client = Client(self.TEST_BASE_URL, self.TEST_API_KEY, 1)

        for case in test_cases:
            with self.subTest(
                method=case["method"], content=case["content"], status=case["status"]
            ):
                with patch.object(
                    client,
                    "_request",
                    side_effect=self.get_mock_request(
                        content=case["content"], status=case["status"]
                    ),
                ):
                    async with client:
                        response = await client.request(case["method"], "")

                self.assertEqual(response.status, case["expected_status"])
                self.assertEqual(response.content, case["content"])

    async def test_multiple_request(self):
        client = Client(self.TEST_BASE_URL, self.TEST_API_KEY, 1)

        param_list = [{"method": RequestEnums.GET.value, "url": ""} for _ in range(3)]

        with patch.object(client, "_request", side_effect=self.get_mock_request()):
            async with client:
                responses = await task_handler(client.request, param_list=param_list)

        for response in responses:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.content, '{"body":"success"}')

    async def test_return_429_when_max_retry(self):
        client = Client(self.TEST_BASE_URL, self.TEST_API_KEY, 1)

        with patch.object(
            client,
            "_request",
            side_effect=HTTPTooManyRequests(
                headers={"Retry-After": "0"},
                reason="Rate limited",
                text="Rate limited",
                content_type="application/json",
            ),
        ):
            async with client:
                response = await client.request("GET", "", max_retries=3)

        self.assertEqual(response.status, 429)
        self.assertEqual(response.content, "Rate limited")

    @patch("asyncio.sleep", return_value=None)
    async def test_retry_on_429(self, mock_sleep):
        client = Client(self.TEST_BASE_URL, self.TEST_API_KEY, 1)
        client._session = MagicMock()
        client._session.request = MagicMock()

        mock_429_response = self.generate_mock_429()
        mock_200_response = self.generate_mock_200()

        cm1 = AsyncMock()
        cm1.__aenter__.return_value = mock_429_response
        cm2 = AsyncMock()
        cm2.__aenter__.return_value = mock_429_response
        cm3 = AsyncMock()
        cm3.__aenter__.return_value = mock_200_response

        client._session.request.side_effect = [cm1, cm2, cm3]

        content, headers, status = await client._request("GET", "", max_retries=3)

        self.assertEqual(client._session.request.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)
        self.assertEqual(mock_sleep.call_args_list[0][0][0], 2)

        self.assertEqual(content, "{'message':'success'}")
        self.assertEqual(status, 200)

    async def test_session_cleanup(self):
        client = Client(self.TEST_BASE_URL, self.TEST_API_KEY, 1)

        with patch.object(client, "_request", side_effect=self.get_mock_request()):
            async with client:
                await client.request(RequestEnums.GET.value, "")

        self.assertEqual(client._session, None)


class TestClientConcurrency(unittest.IsolatedAsyncioTestCase):
    TEST_API_KEY = "test_key"
    TEST_BASE_URL = "test_url"
    SEMAPHORE_LIMIT = 10

    def setUp(self):
        self.active_requests = 0
        self.max_concurrent = 0

    async def mock_delayed_request(self, *args, **kwargs):
        """Mock request that simulates a delay to observe concurrency"""
        self.active_requests += 1  # Track how many requests are running
        self.max_concurrent = max(self.max_concurrent, self.active_requests)

        await asyncio.sleep(0.5)  # Simulate network delay

        self.active_requests -= 1  # Decrement active count when finished
        return '{"body":"success"}', "{}", 200

    async def test_concurrent_requests_respect_semaphore(self):
        """Ensure concurrent requests never exceed the set semaphore limit"""
        client = Client(self.TEST_BASE_URL, self.TEST_API_KEY, self.SEMAPHORE_LIMIT)
        param_list = [{"method": RequestEnums.GET.value, "url": ""} for _ in range(15)]

        self.active_requests = 0
        self.max_concurrent = 0  # Track the highest concurrent request count

        with patch.object(client, "_request", side_effect=self.mock_delayed_request):
            async with client:
                await task_handler(client.request, param_list=param_list)

        self.assertLessEqual(
            self.max_concurrent,
            self.SEMAPHORE_LIMIT,
            f"Exceeded max concurrency: {self.max_concurrent} > {self.SEMAPHORE_LIMIT}",
        )
