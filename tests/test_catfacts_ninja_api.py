import conftest

service = "catfacts"


def test_get_facts():
    response = conftest.api_request(
        service, "get",
        url="/facts"
    )

    assert response.status_code == 200
    assert len(response.json()['data']) == 10


def test_get_facts_limit():
    limit = 2

    response = conftest.api_request(
        service, "get",
        url="/facts",
        params={'limit': {limit}}
    )

    assert response.status_code == 200
    assert len(response.json()['data']) == limit


def test_max_length_fact():
    max_length = 100

    response = conftest.api_request(
        service, "get",
        url="/fact",
        params={"max_length": max_length}
    )

    assert response.json()['length'] <= 100