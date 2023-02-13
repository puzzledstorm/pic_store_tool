import base64
import cv2
import numpy as np
import requests
import yaml
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import os.path as osp
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == "__main__":
    from model import Base, Signature, User
    from utils import get_unique_str, get_cur_time
else:
    from .model import Base, Signature, User
    from .utils import get_unique_str, get_cur_time


class API(object):
    def __init__(self):
        signature_db = self.init_config()
        self.engine = self.init_engine(signature_db)

    @staticmethod
    def check_config(config):
        key = "signature_db"
        if key not in config.keys():
            raise ValueError(f"Configuration file is missing key {key}")
        if config["signature_db"] is None:
            raise ValueError(f"please config {key} field")

    def init_config(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = base_path + os.sep + 'config' + os.sep + 'config.yaml'
        # print(config_path)
        if not osp.exists(config_path):
            raise FileExistsError

        with open(config_path, 'r', encoding="utf-8") as f:
            config = yaml.safe_load(f.read())
            signature_db = config["signature_db"]
            print(signature_db)
            return signature_db

    def init_engine(self, db_path=None):
        # 数据库表初始化
        if not db_path:
            basedir = osp.abspath(osp.dirname(osp.dirname(__file__))) + os.sep + "database"
            if not osp.exists(basedir):
                os.makedirs(basedir)
            # print(basedir)
            database_name = 'signature.db?check_same_thread=False'
            database_url = 'sqlite:///' + osp.join(basedir, database_name)
        else:
            basedir = osp.dirname(db_path)
            if not osp.exists(basedir):
                os.makedirs(basedir)
            database_url = 'sqlite:///' + db_path + "?check_same_thread=False"

        print(f"database_url: {database_url}")
        # 创建engine，即数据库驱动信息
        engine = create_engine(url=database_url)

        # 创建表, checkfirst=True即如果数据库存在则不再创建
        Base.metadata.create_all(engine, checkfirst=True)

        return engine

    def add_user(self, ID, name, *args, **kwargs):
        with Session(self.engine) as session:
            user = User(ID=ID, name=name)
            print(f"add user: {user}")
            session.add(user)
            session.commit()

    def query_user_by_ID(self, ID, *args, **kwargs):
        with Session(self.engine) as session:
            user = session.query(User).filter(User.ID == ID).first()
            return user

    def add_signature(self, user_id, *args, **kwargs):
        with Session(self.engine) as session:
            sig = Signature(
                pic_id=kwargs.get("pic_id") or "pic_id" + get_unique_str(),
                pic_path=kwargs.get("pic_path") or "pic_path" + get_unique_str(),
                pic_feature=self.pic_to_base64(kwargs.get("pic_path")),
                create_datetime=get_cur_time(),
                user_id=user_id
            )
            print(f"add signature: {sig}")
            session.add(sig)
            session.commit()

    def delete_signatures(self, user_id, *args, **kwargs):
        with Session(self.engine) as session:
            session.query(Signature).filter(Signature.user_id == user_id).delete()
            session.commit()

    def query_all_signatures(self):
        with Session(self.engine) as session:
            signatures = session.query(Signature).all()
            return signatures

    def query_signature_by_user_id(self, user_id):
        with Session(self.engine) as session:
            signatures = session.query(Signature).filter(Signature.user_id == user_id).all()
            return signatures

    def delete_signature_by_pic_id(self, user_id, pic_id):
        with Session(self.engine) as session:
            session.query(Signature).filter(Signature.user_id == user_id, Signature.pic_id == pic_id).delete()
            session.commit()

    def pic_to_base64(self, image):
        # image = "image/" + "张三.png"
        # image = image_dir + "colorful_sky.jpg"
        if image.startswith("http"):
            r = requests.get(image, verify=False)
            base64_image = base64.b64encode(r.content)
        else:
            with open(image, 'rb') as f:
                image = f.read()
                base64_image = base64.b64encode(image)
        return base64_image

    def base64_to_pic(self, pic_feature):
        str_encode = base64.b64decode(pic_feature)
        image = np.fromstring(str_encode, np.uint8)
        img_decode = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # cv2.imwrite(f"image/verify.png", img_decode)
        # print(type(image))
        return img_decode

    def insert_data(self):
        # 添加数据流程 by ID -> find User.user_id -> insert signature with user_id
        try:
            # user
            ID = get_unique_str()
            # ID = "0cca9ae212c247ce938ed271a550e197"
            name = "张三"
            self.add_user(ID, name)
            # signatures
            user = self.query_user_by_ID(ID)
            if user:
                user_id = user.user_id
                print(user_id)
                self.add_signature(user_id, pic_path="image/gray.png")
            else:
                print(f"未查询到ID {ID}的用户")
        except IntegrityError as e:
            print(f"Integrity Error, this ID is already in the database. Error: {e}.")

    def get_pics_by_ID(self, ID):
        # 根据ID查询users表获取users.user_id
        user = self.query_user_by_ID(ID)
        if user:
            user_id = user.user_id
            name = user.name
            print(f"查询到用户ID {ID}的用户user_id: {user_id}, name: {name}")
            # 根据users.user_id查询signatures
            signatures = self.query_signature_by_user_id(user_id=user_id)
            pics = []
            for sig in signatures:
                pic_feature = sig.pic_feature
                pic = self.base64_to_pic(pic_feature)
                pics.append(pic)
            # print(pics)
            return pics, name

        else:
            print(f"未查询到ID {ID}的用户")
            return [], None


def main():
    api = API()
    api.insert_data()
    # ID = "0cca9ae212c247ce938ed271a550e197"
    # pics, name = api.get_pics_by_ID(ID)
    # for pic in pics:
    #     print(pic.shape)
    #     image = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    #     test_gray = cv2.resize(image, (220, 155), cv2.INTER_LINEAR)
    #     cv2.imwrite(f"image/gray.png", test_gray)
    #     print(test_gray.shape)


if __name__ == '__main__':
    main()

