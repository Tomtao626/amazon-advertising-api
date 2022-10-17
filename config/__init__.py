import toml
from typing import List, AnyStr

config_path = "config/conf.toml"


def read_conf(conf_type: AnyStr, conf_path: AnyStr = config_path) -> List:
    """
    read conf
    :param conf_type: 配置类型
    :param conf_path: 配置文件地址
    :return: []
    """
    conf_reader = toml.load(conf_path)['conf'][conf_type]
    return conf_reader

