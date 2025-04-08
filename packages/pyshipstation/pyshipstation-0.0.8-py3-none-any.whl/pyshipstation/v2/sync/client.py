import requests

from pyshipstation.v2.models.inventory_response import InventoryResponse


class ShipStationClientV2:
    BASE_URL = "https://api.shipstation.com/v2"

    def __init__(
        self,
        api_key: str,
        timeout: int = 10,
    ):
        self.api_key = api_key
        self.timeout = timeout

    def list_sku_inventory_levels(self) -> InventoryResponse:
        """
        https://docs.shipstation.com/openapi/inventory/getinventorylevels
        """
        headers = {"api-key": self.api_key}
        response = requests.get(
            url=f"{self.BASE_URL}/inventory", headers=headers, timeout=self.timeout
        )
        response.raise_for_status()

        data = response.json()
        inventory_response = InventoryResponse.model_validate(data)
        return inventory_response
