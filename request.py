import requests


url = "http://127.0.0.1:8000/uploads"

file = open("housing.csv", "rb")

# response = requests.get(url)
# print(response.json())

response = requests.post(url, files={"file": file})
print(response.json())
