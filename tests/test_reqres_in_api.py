import jsonschema
import conftest

service = "reqres"
create_user_schema = conftest.response_schema(conftest.load_json_schema('create_user_response_schema.json'))
single_user_schema = conftest.response_schema(conftest.load_json_schema('get_single_user_response_schema.json'))
users_list_schema = conftest.response_schema(conftest.load_json_schema('get_users_list_response_schema.json'))
register_user_schema = conftest.response_schema(conftest.load_json_schema('register_user_response_schema.json'))
update_user_schema = conftest.response_schema(conftest.load_json_schema('update_user_response_schema.json'))


def test_get_users_list_by_page():
    page = 2

    response = conftest.api_request(
        service, "get",
        url="/api/users",
        params={"page": page}
    )

    jsonschema.validators.validate(instance=response.json(), schema=users_list_schema)

    assert response.status_code == 200
    assert response.json()['page'] == page


def test_get_users_list_data_by_per_page():
    per_page = 6

    response = conftest.api_request(
        service, "get",
        url="/api/users",
        params={"per_page": per_page}
    )

    jsonschema.validators.validate(instance=response.json(), schema=users_list_schema)

    assert response.status_code == 200
    assert response.json()['per_page'] == per_page
    assert len(response.json()['data']) == per_page


def test_positive_get_single_user_data_by_id():
    id = 1

    response = conftest.api_request(
        service, "get",
        url="/api/users",
        params={"id": id}
    )

    jsonschema.validators.validate(instance=response.json(), schema=single_user_schema)

    assert response.status_code == 200
    assert response.json()['data']['id'] == id


def test_negative_get_single_user_data_by_id():
    id = 23

    response = conftest.api_request(
        service, "get",
        url="/api/users",
        params={"id": id}
    )

    assert response.status_code == 404


def test_get_users_list_response_format():
    response = conftest.api_request(
        service, "get",
        url="/api/users"
    )

    jsonschema.validators.validate(instance=response.json(), schema=users_list_schema)


def test_patch_user_format_json():
    payload = {
        "name": "Alexander",
        "job": "QAGuru"
    }

    response = conftest.api_request(
        service, "patch",
        url="/api/users/2",
        json=payload
    )

    assert response.status_code == 200
    jsonschema.validators.validate(instance=response.json(), schema=update_user_schema)
    assert response.json()['name'] == payload['name']
    assert response.json()['job'] == payload['job']


def test_put_user_format_json():
    payload = {
        "name": "Alexander",
        "job": "QAGuru"
    }

    response = conftest.api_request(
        service, "put",
        url="/api/users/2",
        json=payload
    )

    assert response.status_code == 200
    jsonschema.validators.validate(instance=response.json(), schema=update_user_schema)
    assert response.json()['name'] == payload['name']
    assert response.json()['job'] == payload['job']


def test_delete_user_by_id():
    id = 2

    response = conftest.api_request(
        service, "delete",
        url="/api/users/2",
        params={"id": id}
    )

    assert response.status_code == 204


def test_create_user_format_json():
    payload = {
        "name": "Alexander",
        "job": "QAGuru"
    }

    response = conftest.api_request(
        service, "post",
        url="/api/users",
        json=payload
    )

    assert response.status_code == 201
    jsonschema.validators.validate(instance=response.json(), schema=create_user_schema)
    assert response.json()['name'] == payload['name']
    assert response.json()['job'] == payload['job']


def test_register_user_format_json():
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }

    response = conftest.api_request(
        service, "post",
        url="/api/register",
        json=payload
    )

    assert response.status_code == 200
    jsonschema.validators.validate(instance=response.json(), schema=register_user_schema)
