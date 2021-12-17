def test_comment(test_app):
    response = test_app.get("/comments")
    assert response.status_code == 200
    for i in response.json():
        assert i["url"]
        assert i["title"]
        assert i["comment"]
        assert i["environment"] == "dev"
        assert i["testing"] == "False" or "True"
