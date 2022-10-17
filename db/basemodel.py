import logging
import datetime
import random
import time
from lib.__init__ import _mdb
from peewee import CharField, IntegerField
from playhouse.signals import Model, post_save

logger = logging.getLogger(__name__)


class CommonBase(Model):
    class Meta:
        database = _mdb


class BaseModel(CommonBase):
    show_id = CharField(max_length=32, verbose_name='展示ID', help_text="展示ID", default='')
    add_time = IntegerField(verbose_name='添加时间', help_text='添加时间', index=True, default=0)
    upd_time = IntegerField(verbose_name='更新时间', help_text='更新时间', default=0)

    def get_id_by_show_id(self, showId):
        '''
        根据showid获取真实id值
        :param showId: type string 自动增长列id值
        :return:
        '''
        i = showId[len(showId) - 1]
        j = showId[0:len(showId) - 1]
        k = (int(j) - int(i) - 10000) / int(i)
        return int(k)

    def set_show_id_by_id(self, id):
        '''
        设置showid
        :param id: 真实id
        :return:
        '''
        a = random.randint(1, 9)
        b = a * int(id) + 10000 + a
        j = str(b) + str(a)
        return j

    def to_dict(self, keys):
        data = {}
        for key in keys:
            value = getattr(self, key)
            if isinstance(value, datetime.datetime):
                data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                data[key] = value
        # data = {key:getattr(self,key) for key in keys}
        return data

    @classmethod
    def change_org(cls, org_id):
        return cls

    @classmethod
    def get_id_by_show_id(cls, showId):
        '''
        根据showid获取真实id值
        :param showId: type string 自动增长列id值
        :return:
        '''
        showId = str(showId)

        if not showId:
            return 0

        i = showId[len(showId) - 1]
        j = showId[0:len(showId) - 1]
        k = int((int(j) - int(i) - 10000) / int(i))
        return k

    @classmethod
    def set_show_id_by_id(self, id):
        '''
        设置showid
        :param id: 真实id
        :return:
        '''
        a = random.randint(1, 9)
        b = a * int(id) + 10000 + a
        j = str(b) + str(a)
        return j

    def _dict_(self, keys):
        data = {key: getattr(self, key) for key in keys}
        return data


@post_save(sender=BaseModel)
def on_save_handler(model_class, instance, created):
    """
    自动填充show_id
    自动发更新时间
    :param model_class:
    :param instance:
    :param created:
    :return:
    """
    if not instance.show_id:
        model_class.update({model_class.show_id: model_class.set_show_id_by_id(instance.id)}).where(
            model_class.id == instance.id).execute()
        if hasattr(instance, 'add_time'):
            model_class.update({model_class.add_time: int(time.time())}).where(
                model_class.id == instance.id).execute()
        if hasattr(instance, 'upd_time'):
            model_class.update({model_class.upd_time: int(time.time())}).where(
                model_class.id == instance.id).execute()
    else:
        model_class.update({model_class.upd_time: int(time.time())}).where(model_class.id == instance.id).execute()
