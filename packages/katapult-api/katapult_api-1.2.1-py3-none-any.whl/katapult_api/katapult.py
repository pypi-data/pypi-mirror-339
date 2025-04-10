from typing import Optional, Union
from urllib.parse import urljoin

from .client import Client, Response
from .enums import RequestEnums


class Katapult(Client):
    _CONCURRENT_RATE_LIMT = 99
    _BASE_URL = "https://{}.katapultpro.com/api/"

    def __init__(
        self,
        api_key: str,
        servername: str = "techserv",
        concurrent_rate_limit: int = 99,
    ):
        super().__init__(
            self._BASE_URL.format(servername), api_key, concurrent_rate_limit
        )

    async def job_lists(
        self, order_by_child: Optional[str] = None, equal_to: Optional[str] = None
    ) -> Response:
        return await self.request(
            "GET",
            self._build_url("jobs"),
            params={"orderByChild": order_by_child, "equalTo": equal_to},
        )

    async def job(self, job_id: str) -> Response:
        return await self.request(
            RequestEnums.GET.value, self._build_url(f"jobs/{job_id}")
        )

    async def jobs_in_folder(self, folder_path: Union[str, None] = None) -> Response:
        return await self.request(
            RequestEnums.GET.value,
            self._build_url("folders"),
            params={"folderPath": folder_path},
        )

    async def get_model_list(self) -> Response:
        return await self.request(RequestEnums.GET.value, self._build_url("models"))

    async def create_job(
        self,
        name: str,
        model: str,
        job_project_folder_path: Optional[str] = None,
        **kwargs,
    ) -> Response:
        body = {
            "name": name,
            "model": model,
            "jobProjectFolderPath": job_project_folder_path,
            **kwargs,
        }
        return await self.request(
            RequestEnums.POST.value, self._build_url("jobs"), json=body
        )

    async def write_job_data(self, jobid: str, nodes: dict, **kwargs):
        # essentially converts {"attribute":{"key1":"val1","key2":"val2"}} to
        # {"attributes":[{"attribute":"key1","value":"val1"},{"attribute":"key2","value":"val2"}]}
        fixed_nodes = {}
        for key, value in nodes.items():
            fixed_nodes[key] = value

            # fixed_nodes[key].update({"attributes":[
            #         {"attribute": attr_key, "value": attr_value}
            #         for attr_key, attr_value in value.get("attributes").items()
            #     ]})

        body = {"nodes": fixed_nodes, **kwargs}
        return await self.request(
            RequestEnums.PUT.value, self._build_url(f"jobs/{jobid}"), json=body
        )

    async def archive_job(self, jobid: str) -> Response:
        return await self.request(
            RequestEnums.PUT.value, self._build_url(f"jobs/{jobid}/archive")
        )

    async def create_node(
        self,
        jobid: str,
        latitude: float,
        longitude: float,
        attributes: Optional[dict] = None,
    ) -> Response:
        body = {
            "latitude": latitude,
            "longitude": longitude,
        }

        if attributes:
            body["attributes"] = [
                {"attribute": key, "value": value} for key, value in attributes.items()
            ]

        return await self.request(
            RequestEnums.POST.value, self._build_url(f"jobs/{jobid}/nodes"), json=body
        )

    async def update_node(
        self,
        jobid: str,
        nodeid: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        attributes: Optional[dict] = None,
    ) -> Response:
        return await self.request(
            RequestEnums.PATCH.value,
            self._build_url(f"jobs/{jobid}/nodes/{nodeid}"),
            json={
                "latitude": latitude,
                "longitude": longitude,
                "attributes": [
                    {"attribute": key, "value": value}
                    for key, value in attributes.items()
                ],
            },
        )

    async def delete_node(self, jobid: str, nodeid: str) -> Response:
        return await self.request(
            RequestEnums.DELETE.value, self._build_url(f"jobs/{jobid}/nodes/{nodeid}")
        )

    def _build_url(self, endpoint: str) -> str:
        return urljoin(self._base_url, endpoint)
