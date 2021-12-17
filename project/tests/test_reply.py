from app import main

def test_reply(test_app):
    response = test_app.get("/comments")
    assert response.status_code == 200
    for i in response.json():
        if "lol" in i["comment"].lower() or \
"patched" in i["comment"].lower() or "water" in i["comment"].lower():
           assert i["url"]
           assert i["title"]
           assert i["comment"]
           assert i["reply"]
           assert i["environment"] == "dev"
           assert i["testing"] == "False" or "True"
