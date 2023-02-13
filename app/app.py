import logging
import sys
from os import path
# sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from flask import Flask
from flask_restful import Api
from config import get_config

if __name__ == '__main__':
    from signature_api.resources import SignatureResource, DeleteSignatureResource,\
        DeleteAllSignatureResource, SIGNATURE_ENDPOINT, ADD_SIGNATURE_ENDPOINT, \
        DELETE_SIGNATURE_ENDPOINT, DELETE_ALL_SIGNATURE_ENDPOINT
else:
    from .signature_api.resources import SignatureResource, DeleteSignatureResource, \
        DeleteAllSignatureResource, SIGNATURE_ENDPOINT, ADD_SIGNATURE_ENDPOINT, \
        DELETE_SIGNATURE_ENDPOINT, DELETE_ALL_SIGNATURE_ENDPOINT


def create_app():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[logging.FileHandler("signature_api.log"), logging.StreamHandler()],
    )

    app = Flask(__name__)

    api = Api(app)
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

    api.add_resource(SignatureResource, SIGNATURE_ENDPOINT, ADD_SIGNATURE_ENDPOINT)
    api.add_resource(DeleteSignatureResource, DELETE_SIGNATURE_ENDPOINT)
    api.add_resource(DeleteAllSignatureResource, DELETE_ALL_SIGNATURE_ENDPOINT)
    return app


if __name__ == "__main__":
    app = create_app()
    port = get_config().get("port", 12769)
    app.run(host="0.0.0.0", port=port)
