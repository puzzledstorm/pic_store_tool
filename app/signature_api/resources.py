import logging
from flask import request
from flask_restful import Resource, abort, fields, marshal_with
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

if __name__ == "__main__":
    from api import API
else:
    from .api import API

SIGNATURE_ENDPOINT = "/"
ADD_SIGNATURE_ENDPOINT = "/add"
DELETE_SIGNATURE_ENDPOINT = "/delete"
DELETE_ALL_SIGNATURE_ENDPOINT = "/delete_all"

logger = logging.getLogger(__name__)
api = API()

resource_fields = {
    'signature_id': fields.String,
    'pic_id': fields.String,
    'pic_path': fields.String,
    'pic_feature': fields.String,
    'create_datetime': fields.String,
    # 'uri': fields.Url()
}

success_return = {
    "code": 0,
    "msg": "ok"
}


class SignatureResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        all_signatures = api.query_all_signatures()
        return all_signatures, 200

    def post(self):
        try:
            body = request.get_json()
        except Exception as e:
            return {
                       "code": 2,
                       "msg": f"please add Headers Content-Type: application/json, error info: {e}"
                   }, 400

        if body is None:
            return {
                       "code": 2,
                       "msg": f"json body need be not null, but got json {body}"
                   }, 400

        # user info
        ID = body.get("ID")
        name = body.get("name")
        logger.info(f"get ID --- {ID},name --- {name}")

        # signatures_info
        signature_list = body.get("signature_list")
        total_add_number = len(signature_list)
        success_add_number = 0
        failed_add_number = 0
        failed_add_picture = []

        # 1.查询到用户直接创建签名 2.查询不到用户新建用户并创建签名
        user = api.query_user_by_ID(ID)
        if not user:
            api.add_user(ID, name)
            logger.info(f"create user by ID {ID}, name {name}")
        user = api.query_user_by_ID(ID)
        user_id = user.user_id
        name = user.name
        logger.info(f"insert signature by user_id {user_id}")
        for signature in signature_list:
            picture_path = signature.get("picture_path")
            picture_id = signature.get("picture_id")
            try:
                api.add_signature(user_id=user_id, pic_id=picture_id, pic_path=picture_path)
                success_add_number += 1
            except Exception as e:
                failed_add_number += 1
                failed_add_picture.append({
                    "picture_path": picture_path,
                    "picture_id": picture_id,
                    "failed_msg": f"add signature pic failed, error info: {e}"
                })

        result = {
            "ID": ID,
            "name": name,
            "total_add_number": total_add_number,
            "success_add_number": success_add_number,
            "failed_add_number": failed_add_number,
            "failed_add_picture": failed_add_picture
        }
        return_result = {**success_return, **dict(result=result)}
        return return_result


class DeleteSignatureResource(Resource):
    def post(self):
        try:
            body = request.get_json()
        except Exception as e:
            return {
                       "code": 2,
                       "msg": f"please add Headers Content-Type: application/json, error info: {e}"
                   }, 400

        if body is None:
            return {
                       "code": 2,
                       "msg": f"json body need not null, but got json {body}"
                   }, 400

            # user info
        ID = body.get("ID")
        picture_id_list = body.get("picture_id_list")
        logger.info(f"get ID --- {ID}, picture_id_list --- {picture_id_list}")
        user = api.query_user_by_ID(ID)
        if user:
            user_id = user.user_id
            try:
                for pic_id in picture_id_list:
                    api.delete_signature_by_pic_id(user_id, pic_id)
                return {
                        "code": 0,
                        "msg": "签名删除成功"
                    }
            except Exception as e:
                return {
                    "code": 2,
                    "msg": f"签名删除失败，error info: {e}"
                }
        else:
            return {
                "code": 2,
                "msg": f"未查询到ID {ID} 的用户"
            }


class DeleteAllSignatureResource(Resource):
    def post(self):
        try:
            body = request.get_json()
        except Exception as e:
            return {
                       "code": 2,
                       "msg": f"please add Headers Content-Type: application/json, error info: {e}"
                   }, 400

        if body is None:
            return {
                       "code": 2,
                       "msg": f"json body need not null, but got json {body}"
                   }, 400

        # user info
        ID = body.get("ID")
        logger.info(f"get ID --- {ID}")
        user = api.query_user_by_ID(ID)
        if user:
            user_id = user.user_id
            logger.info(f"delete all signatures by user_id {user_id}")
            try:
                api.delete_signatures(user_id)

                return {
                    "code": 0,
                    "msg": "签名删除成功"
                }
            except Exception as e:
                return {
                    "code": 2,
                    "msg": f"签名删除失败，error info: {e}"
                }
        else:
            return {
                "code": 2,
                "msg": f"未查询到ID {ID} 的用户"
            }
