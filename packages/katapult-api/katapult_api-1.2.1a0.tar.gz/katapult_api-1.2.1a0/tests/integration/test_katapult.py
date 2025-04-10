import asyncio
import gc
import unittest
import uuid

from katapult_api.katapult import Katapult
from tests.settings import KATAPULT_API_KEY, TEST_DIR_PATH


class TestKatapultAPI(unittest.IsolatedAsyncioTestCase):
    MODEL = "techserv"

    def get_test_name(self):
        return f"TEST-{uuid.uuid4()}"

    async def asyncSetUp(self):
        self.katapult = Katapult(KATAPULT_API_KEY, "techserv")
        self.test_job_id = None
        self.test_job_name = None
        await self.katapult.start_session()

    async def asyncTearDown(self):
        if self.test_job_id:
            await self.katapult.archive_job(self.test_job_id)
        await self.katapult.close_session()

        gc.collect()
        await asyncio.sleep(0.1)

    async def create_test_job(self) -> None:
        # It's important to make sure names are unique since even archived names can result in a collision and failure to make a job.
        self.test_job_name = self.get_test_name()
        response = await self.katapult.create_job(
            self.test_job_name,
            TestKatapultAPI.MODEL,
            TEST_DIR_PATH,
        )
        if response.status == 200:
            self.test_job_id = response.json().get("jobId")
        else:
            raise RuntimeError(
                f"Failed to create test job. Status: {response.status}, Body: {response.content}"
            )

    async def test_get_job_list(self):
        response = await self.katapult.job_lists()

        self.assertEqual(response.status, 200)

        response_json = response.json()

        self.assertIsNotNone(response_json)

        first_item_key = next(iter(response_json))

        self.assertIn("name", response_json.get(first_item_key))
        self.assertIn("status", response_json.get(first_item_key))

    async def test_get_job(self):
        await self.create_test_job()
        response = await self.katapult.job(self.test_job_id)
        response_json = response.json()

        self.assertEqual(response.status, 200)
        self.assertEqual(response_json.get("name"), self.test_job_name)

    async def test_get_model_list(self):
        response = await self.katapult.get_model_list()

        self.assertEqual(response.status, 200)

        response_json = response.json()

        self.assertIsNotNone(response_json)

        self.assertIn("label", response_json[0])
        self.assertIn("value", response_json[0])

    async def test_create_job(self):
        test_job_name = self.get_test_name()
        create_job_response = await self.katapult.create_job(
            test_job_name,
            TestKatapultAPI.MODEL,
            TEST_DIR_PATH,
        )

        self.assertEqual(create_job_response.status, 200)

        job_id = create_job_response.json().get("jobId")
        job_response = await self.katapult.job(job_id)

        self.assertEqual(test_job_name, job_response.json().get("name"))

        await self.katapult.archive_job(job_id)

    async def test_write_job_data(self):
        await self.create_test_job()

        create_node_response = await self.katapult.create_node(
            self.test_job_id, 29.0817046, -98.8429946
        )
        existing_node_id = create_node_response.json().get("key")

        job_response = await self.katapult.job(self.test_job_id)
        self.assertEqual(job_response.status, 200)
        job = job_response.json()
        self.assertEqual(job.get("name"), self.test_job_name)
        self.assertIn(existing_node_id, job.get("nodes"))

        updated_name = f"{self.test_job_name}-updated"
        updated_nodes = {
            "node_1": {
                "latitude": 30.0817046,
                "longitude": -97.8429946,
                # "attributes": {"street": "Main St"}
            },
            "node_2": {
                "latitude": 30.0820167,
                "longitude": -97.8436502,
                # "attributes":{"street": "Live Oak St"}
            },
        }

        # Need to provide name otherwise you will get an error on katapult and map_styles are needed to see poles on there as well.
        # Otherwise, it will still technically exist and show up in the job response when querying for the job data itself (but won't have a name).
        # Fairly certain that this method does a complete update to a job going as far as removing items that are not found in the passed parameters.
        write_job_data_response = await self.katapult.write_job_data(
            self.test_job_id,
            nodes=updated_nodes,
            name=updated_name,
            map_styles="AEP_Default",
        )

        self.assertEqual(write_job_data_response.status, 200)

        job_response = await self.katapult.job(self.test_job_id)

        self.assertEqual(job_response.status, 200)

        job = job_response.json()

        self.assertEqual(job.get("name"), updated_name)

        nodes = job.get("nodes")

        self.assertNotIn(existing_node_id, nodes)

        for key, value in updated_nodes.items():
            self.assertIn(key, nodes)
            self.assertEqual(value.get("latitude"), nodes.get(key).get("latitude"))
            self.assertEqual(value.get("longitude"), nodes.get(key).get("longitude"))

    async def test_create_node(self):
        await self.create_test_job()

        create_node_response = await self.katapult.create_node(
            self.test_job_id, 30.0817046, -97.8429946, {"street": "Main St"}
        )
        create_node_response_json = create_node_response.json()

        self.assertEqual(create_node_response.status, 200)

        job_response = await self.katapult.job(self.test_job_id)

        self.assertIn(
            create_node_response_json.get("key"), job_response.json().get("nodes")
        )

    async def test_update_node(self):
        await self.create_test_job()

        create_node_response = await self.katapult.create_node(
            self.test_job_id, 30.0819157, -97.8434061, {"street": "Main St"}
        )
        node_id = create_node_response.json().get("key")

        updated_street_name = "Live Oak St"
        updated_lat = 30.0820167
        updated_lon = -97.8436502

        new_attribute_town = "Buda"
        update_node_response = await self.katapult.update_node(
            self.test_job_id,
            node_id,
            updated_lat,
            updated_lon,
            {"street": updated_street_name, "town": new_attribute_town},
        )

        # the updated node response doesn't return the updated lat/long but job response does
        job_response = await self.katapult.job(self.test_job_id)
        job = job_response.json()

        updated_node_id = list(job.get("nodes").keys())[0]
        node = job.get("nodes").get(updated_node_id)

        self.assertEqual(update_node_response.status, 200)
        self.assertEqual(node_id, updated_node_id)

        attributes = node.get("attributes")

        self.assertIn(new_attribute_town, attributes.get("town").values())
        self.assertIn(updated_street_name, attributes.get("street").values())
        self.assertEqual(updated_lat, node.get("latitude"))
        self.assertEqual(updated_lon, node.get("longitude"))

    async def test_delete_node(self):
        await self.create_test_job()

        create_node_response = await self.katapult.create_node(
            self.test_job_id, 30.0819157, -97.8434061, {"street": "Main St"}
        )
        node_id = create_node_response.json().get("key")

        job_response = await self.katapult.job(self.test_job_id)
        self.assertIn(node_id, job_response.json().get("nodes"))

        delete_node_response = await self.katapult.delete_node(
            self.test_job_id, node_id
        )
        self.assertEqual(delete_node_response.status, 200)

        job_response = await self.katapult.job(self.test_job_id)
        self.assertNotIn("nodes", job_response.json())
