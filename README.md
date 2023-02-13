# pic_store_tool

## 简单介绍
pic_store_tool根据用户id和用户名以及图片来存储。提供查询图片存储接口，根据特定用户删除特定图片接口，删除某个用户所有存储的图片接口。

## 依赖
```
Flask
Flask-RESTful
SQLAlchemy

数据库
sqlite
```
### ps
导出当前项目的req
虚拟环境： 
```
pip freeze > requirements.txt
```
本机环境：
```
pip install pipreqs
pipreqs . --encoding=utf8 --force
```