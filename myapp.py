import requests

url = "http://127.0.0.1:8000/orders/order/24b5a4bb-2882-4431-a011-f87c0010f3e4/"

data = {
    
  "items": [
    { "menu_item": 1, "quantity": 2 },
    { "menu_item": 2, "quantity": 1 }
  ]

}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())