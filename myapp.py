import requests

url = "http://127.0.0.1:8000/shops/tables/"

data = {
    "shop": 1,
    "table_name": "Table 1"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())