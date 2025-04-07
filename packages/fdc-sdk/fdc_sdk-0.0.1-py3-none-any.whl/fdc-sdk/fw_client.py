import requests
import json
import math

class FWClient:
    def __init__(self, base_url="", org="", secret_key=""):
        self.base_url = base_url.rstrip("/")
        self.org = org
        self.secret_key = secret_key
        self.headers = {
            "Authorization": f"Bearer {secret_key}",
            "X-Organization": org,
            "Content-Type": "application/json"
        }

    def list_all_entities(self, layer="BRONZE", q="", sort_by="updated_at", sort_order="asc"):
        try:
            # Step 1: Fetch the total entity count
            count_response = requests.get(
                f"{self.base_url}/master/api/entities/fetch-count/",
                headers=self.headers,
                params={"modal_type": layer.upper()}
            )
            count_response.raise_for_status()
            entity_count = count_response.json().get("data", {}).get(layer.lower(), {}).get("count", 0)

            if entity_count == 0:
                print("No entities found.")
                return []

            # Step 2: Fetch all entities in a single call
            params = {
                "page": 1,
                "page_size": entity_count,
                "q": q,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "modal_type": layer.upper()
            }
            print(params)
            response = requests.get(
                f"{self.base_url}/master/api/entities/",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            # print(response.json())
            results = response.json().get("data", {}).get("entities",[])
            print(f"Fetched {len(results)} entities:")
            # print(json.dumps(results, indent=2))
            return results

        except requests.RequestException as e:
            print(f"Error fetching entity list: {e}")
            return []

    def create_silver_entity(self, entity_name,sql_query):
        try:
            entity_payload = {
                "entity_name":entity_name,
                "sql_query": sql_query
            }
            print(entity_payload)
            response = requests.post(
                f"{self.base_url}/aggregator/api/v2/entities/silver-entity/",
                json=entity_payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # raise FWSDKException("Error creating silver entity") from e
            print(e)

    def create_gold_entity(self, entity_name,sql_query):
        try:
            entity_payload = {
                entity_name,
                sql_query
            }
            response = requests.post(
                f"{self.base_url}/aggregator/api/v2/entities/gold-entity/",
                json=entity_payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # raise FWSDKException("Error creating silver entity") from e
            print(e)
    def delete_entity(self, entity_name: str):
        try:
            response = requests.delete(
                f"{self.base_url}/api/entities/{entity_name}",
                headers=self.headers
            )
            response.raise_for_status()
            return {"message": f"Entity '{entity_name}' deleted successfully"}
        except requests.RequestException as e:
            # raise FWSDKException(f"Error deleting entity '{entity_name}'") from e
            print(e)

    def disable_schedule(self, entity_name: str):
        try:
            response = requests.post(
                f"{self.base_url}/api/entities/{entity_name}/disable-schedule",
                headers=self.headers
            )
            response.raise_for_status()
            return {"message": f"Schedule disabled for entity '{entity_name}'"}
        except requests.RequestException as e:
            # raise FWSDKException(f"Error disabling schedule for '{entity_name}'") from e
            print(e)
            
