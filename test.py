import json
file_path = "data.json"
with open(file_path, "r") as file:
    data = json.load(file)
print(data[0]["VOIES"])
