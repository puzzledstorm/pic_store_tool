import unittest
from pprint import pprint
import requests
from urllib.parse import urlencode

HOST = "127.0.0.1"
PORT = "12769"


def send_req(uri="/", body=None, params=None, method="POST", content_type="application/json"):
    url = f"http://{HOST}:{PORT}{uri}"
    if not hasattr(requests, method):
        raise AttributeError(f"requests doesn't has attribute {method}")
    headers = {"Content-Type": content_type}
    if body is None:
        body = {}
    if params is None:
        params = {}
    try:

        response = getattr(requests, method.lower())(url=url, json=body, params=urlencode(params), headers=headers)
        if response.status_code != 200:
            error_info = f"status_code:{response.status_code}, response_text: {response.text}"
            raise Exception(error_info)
        # print(response.json())
        return response.json()
    except Exception as e:
        # print(traceback.format_exc())
        raise e


def test_signatures():
    uri = "/"
    body = {}
    method = "get"
    result = send_req(uri=uri, body=body, method=method)
    pprint(result)


def test_add():
    uri = "/add"
    body = {
        "ID": "04f74f9716f047d2b14f4d5a8733851e", "name": "张三",
        "signature_list": [
            {"picture_path": "https://z3.ax1x.com/2021/09/01/h0UKpj.jpg", "picture_id": "1"},
            {"picture_path": "https://z3.ax1x.com/2021/09/01/h0UKpj.jpg", "picture_id": "2"}
        ]
    }
    method = "post"
    result = send_req(uri=uri, body=body, method=method)
    pprint(result)


def test_delete():
    uri = "/delete"
    body = {"ID": "04f74f9716f047d2b14f4d5a8733851e", "picture_id_list": ["1"]}
    method = "post"
    result = send_req(uri=uri, body=body, method=method)
    pprint(result)


def test_delete_all():
    uri = "/delete_all"
    body = {"ID": "04f74f9716f047d2b14f4d5a8733851e"}
    method = "post"
    result = send_req(uri=uri, body=body, method=method)
    pprint(result)


if __name__ == '__main__':
    test_signatures()
    test_add()
    test_delete()
    test_delete_all()
    test_signatures()