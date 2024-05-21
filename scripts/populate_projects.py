import requests
from datetime import datetime

API_URL = "http://localhost:5001"

RESOURCE_TAGS = [
    {
        "name": "resource_tag1"
    },
    {
        "name": "resource_tag2"
    }
]

EVENT_TAGS = [
    {
        "name": "event_tag1"
    },
    {
        "name": "event_tag2"
    }
]

EVENTS = [
    {
        "title": "event1",
        "event_date": datetime.now(),
        "event_place": "Toulouse"
    },
    {
        "title": "event2",
        "event_date": datetime.now(),
        "event_place": "Toulouse"
    },
    {
        "title": "event3",
        "event_date": datetime.now(),
        "event_place": "Toulouse"
    },
    {
        "title": "event4",
        "event_date": datetime.now(),
        "event_place": "Toulouse"
    },
    {
        "title": "event5",
        "event_date": datetime.now(),
        "event_place": "Toulouse"
    }
]

RESOURCES = [
    {
        'title': "resource1",
        "resource_type": "image",
        "uploaded_at": datetime.now(),
        "user_name": "ioqt",
        "source_date": datetime.now(),
        "source_place": "Toulouse",
        "source_place_type": "zone",
        "description": "description de resource 1",
        "file_path": "README.md"
    }
]

USERS = [
    {
        "username": "ioqt",
        "email": "test@gmail.com",
        "password": "test"
    },
    {
        "username": "dummy",
        "email": "nope@nope.nope",
        "password": "test"
    }
]

for user in USERS:
    res = requests.post(API_URL+"/users", json=user)
    print(res.content)
    print(res.json()["message"])
    if res.status_code == 403:
        id = res.json()["id"]
        res = requests.request("PUT", API_URL+f"/users/{id}", json=user)
        print(res.json()["message"])

credentials = {
    "username": "ioqt",
    "password": "test"
}

res = requests.post(API_URL+"/login", json=credentials)

token = res.json()["access_token"]
print(token)

requests = requests.Session()
requests.headers.update({'Authorization': f'Bearer {token}'})


# CLEAR ALL
response = requests.get(f"{API_URL}/resource_tags")
if response.status_code == 200:
    tags = response.json()
else:
    print(f"Failed to retrieve resource_tags. Status code: {response.status_code}")

for tag in tags:
    response = requests.delete(f"{API_URL}/resource_tags/{tag['id']}")
    if response.status_code == 200:
        print(f"resource_tag {tag['id']} deleted successfully.")
    else:
        print(f"Failed to delete resource_tag {tag['id']}. Status code: {response.status_code}")

response = requests.get(f"{API_URL}/event_tags")
if response.status_code == 200:
    tags = response.json()
else:
    print(f"Failed to retrieve event_tags. Status code: {response.status_code}")

for tag in tags:
    response = requests.delete(f"{API_URL}/event_tags/{tag['id']}")
    if response.status_code == 200:
        print(f"event_tag {tag['id']} deleted successfully.")
    else:
        print(f"Failed to delete event_tag {tag['id']}. Status code: {response.status_code}")

# CREATE ALL
for tag in RESOURCE_TAGS:
    res = requests.post(API_URL+"/resource_tags", json=tag)
    if res.status_code == 201:
        print(res.json())
    else:
        print(res.content)

for tag in EVENT_TAGS:
    res = requests.post(API_URL+"/event_tags", json=tag)
    if res.status_code == 201:
        print(res.json())
    else:
        print(res.json()["message"])

for event in EVENTS:
    res = requests.post(API_URL+"/resource_events", json=event)
    if res.status_code == 201:
        print(res.json()["message"])
    else:
        print(res.json())

for resource in RESOURCES:
    f = resource["file_path"].read()
    res = requests.post(API_URL+"/resources", data=resource, files=f.write())
    if res.status_code == 201:
        print(res.json()["message"])
    else:
        print(res.json())
    f.close()
