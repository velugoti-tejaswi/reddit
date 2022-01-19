#def test_create_votes(authorized_client):
#    res = authorized_client.post("/vote/")
#    assert res.status_code == 201
#    assert res.json().get('message') == "Voted successfully..."


def test_all_votes(authorized_client, test_votes):
    res = authorized_client.get("/vote/getvotes")
    assert len(res.json()) == len(test_votes)
    assert res.status_code == 200