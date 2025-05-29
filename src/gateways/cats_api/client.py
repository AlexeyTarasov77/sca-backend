import httpx

from gateways.contracts import ICatsAPIClient


class CatsAPIClient(ICatsAPIClient):
    def __init__(self, req_client: httpx.AsyncClient):
        self._base_url = "https://api.thecatapi.com/v1"
        self._req_client = req_client

    async def get_all_breeds(self) -> list[str]:
        resp = await self._req_client.get(self._base_url + "/breeds")
        resp.raise_for_status()
        breeds_data = resp.json()
        return [breed["name"] for breed in breeds_data]
