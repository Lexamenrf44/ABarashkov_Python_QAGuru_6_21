import os
import json
import allure

from allure_commons.types import AttachmentType
from curlify import to_curl
from requests import sessions


def load_json_schema(name: str):
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schemas', name)
    return schema_path


def response_schema(file_path):
    with open(file_path, encoding='utf8') as file:
        schema = json.loads(file.read())
    return schema


def api_request(service, method, url, **kwargs):
    base_url = {"reqres": "https://reqres.in", "catfacts": "https://catfact.ninja"}
    new_url = base_url[service] + url
    with allure.step(f"{method.upper()} {new_url}"):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)

            allure.attach(body=message.encode("utf-8"),
                          name="Curl",
                          attachment_type=AttachmentType.TEXT,
                          extension='txt')

        if not response.content:
            allure.attach(body='empty response',
                          name='Empty Response',
                          attachment_type=AttachmentType.TEXT,
                          extension='txt')
        else:
            allure.attach(body=json.dumps(response.json(), indent=4).encode("utf-8"),
                          name="Response Json",
                          attachment_type=AttachmentType.JSON,
                          extension='json')
    return response
