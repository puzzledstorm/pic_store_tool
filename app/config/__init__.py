import os.path as osp
import yaml

here = osp.split(osp.realpath(__file__))[0]


# 获取config配置文件
def get_config():
    config_name = "config.yaml"
    config_file = osp.join(here, config_name)
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

