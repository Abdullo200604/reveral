import json

def load():
    with open("users.json", "r") as file:
        data = json.load(file)

    return data

def write(data):
    with open("users.json", "w") as file:
        json.dump(data, file, indent=4)