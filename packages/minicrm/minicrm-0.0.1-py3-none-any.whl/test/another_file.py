from ..minicrm_api import MiniCrmClient

client = MiniCrmClient(76354, "aaa")

adatlapok = client.get_request(endpoint="Project", query_params={"Serial_Number": "2024/0043/CIT"})
print(adatlapok.json())
