def test_create_comments(authorized_client):
    res = authorized_client.post("/comments/")
    assert res.status_code == 200
    assert res.json().get('message') == "Succesfully stored comments in database"


def test_all_comments(authorized_client, test_comments):
    res = authorized_client.get("/comments/allcomments")
    assert len(res.json()) == len(test_comments)
    assert res.status_code == 200