from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BLOB, ForeignKey
from sqlalchemy.orm import relationship

# 数据表的基类（定义表结构用）
Base = declarative_base()


# 定义signature表
class Signature(Base):
    __tablename__ = 'signatures'
    # signature_id name pic_id pic_path pic_feature
    signature_id = Column(Integer, primary_key=True, autoincrement=True)
    pic_id = Column(String())
    pic_path = Column(String())
    pic_feature = Column(BLOB())
    create_datetime = Column(String())

    user_id = Column(Integer, ForeignKey('users.user_id'))  # 外键

    def __repr__(self):
        return "<Signature(signature_id='%s', pic_id='%s', pic_path='%s', pic_feature='%s', " \
               "create_datetime='%s'>" % (self.signature_id, self.pic_id, self.pic_path,
                                          self.pic_feature, self.create_datetime)


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    ID = Column(String(), unique=True, index=True)
    name = Column(String())
    signatures = relationship("Signature", backref='User', lazy='dynamic')

    def __repr__(self):
        return "<User(user_id='%s',ID='%s',name='%s')>" % (self.user_id, self.ID, self.name)




