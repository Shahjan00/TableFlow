import requests

url = "http://127.0.0.1:8000/orders/"  # change this to your API endpoint

data = {
  "shop": 1,
  "table": 1,
  "items": [
    {"menu_item": 2, "quantity": 2},
    {"menu_item": 1, "quantity": 1}
  ]
}

response = requests.get(url)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())