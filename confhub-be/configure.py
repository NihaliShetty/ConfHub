import requests

print("Updating database (see the server logs)")
res = requests.post("http://localhost:5000/admin/update-datasets")
print(res.status_code)
print(res.json())