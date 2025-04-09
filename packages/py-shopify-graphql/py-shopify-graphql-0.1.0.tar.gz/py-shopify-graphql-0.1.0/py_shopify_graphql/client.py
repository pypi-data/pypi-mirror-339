import requests
from .exceptions import GraphqlException


class GraphqlService:
    def __init__(self, shop_domain: str, access_token: str):
        if not shop_domain or not access_token:
            raise ValueError("Shop domain and access token must be provided.")

        self.shop_domain = shop_domain
        self.access_token = access_token
        self.base_url = f"https://{self.shop_domain}/admin/api/2025-01/graphql.json"
        self.headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json",
        }

    def graphql_query_thalia(self, query: str, variables: dict = None) -> dict:
        payload = {
            "query": query,
            "variables": variables or {}
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                error_response = response.json()
                errors = error_response.get("errors", ["Unknown error"])
            except Exception:
                errors = ["Unknown error during error parsing"]

            raise GraphqlException(
                "Shopify API request failed",
                response.status_code,
                errors,
                http_err
            )
        except requests.exceptions.RequestException as e:
            raise GraphqlException("Network error occurred", 0, ["Network error"], e)
