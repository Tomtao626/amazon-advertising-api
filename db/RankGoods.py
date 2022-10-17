#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 6:02 下午
# @Author : admin
# @Software: PyCharm
# @File: RankGoods.py


from db.basemodel import BaseModel
from peewee import CharField, IntegerField, BooleanField

# ['标题', 'AsinId', '页面位置', '价格', '广告', '自然位置', '评论数', '评分']


class RankGoods(BaseModel):
    """
    rank goods
    """
    status = BooleanField(default=True, verbose_name='状态（1启用,0禁用')
    title = CharField(max_length=60, default='', verbose_name='标题', help_text='标题')
    price = CharField(max_length=60, default='', verbose_name='价格', help_text='价格')
    url = CharField(max_length=128, default='', verbose_name='url', help_text='url')
    asin_id = CharField(max_length=60, default='', verbose_name='商品asin编码', help_text='商品asin编码', index=True)
    is_sponsor = BooleanField(default=False, verbose_name='是否有广告推荐')
    score = CharField(max_length=2048, default='', verbose_name='评分', help_text='评分')
    comment_count = CharField(max_length=2048, default='', verbose_name='评论数', help_text='评论数')
    is_delete_time = IntegerField(default=0, verbose_name='是否已删除（0否, 大于0删除时间）', help_text='是否已删除（0否, 大于0删除时间）')

    class Meta:
        table_name = 'rank_goods'
        verbose_name = '商品排行'

    def _to_dict(self):
        keys = ['status', 'title', 'price', 'asin_id', 'is_sponsor', 'score', 'comment_count', 'is_delete_time']
        return self.to_dict(keys)


class RankHistory(BaseModel):
    """
    rank history
    """
    rank_good_id = CharField(max_length=60, default='', verbose_name='商品排行id', help_text='商品排行id', index=True)
    total = IntegerField(default=0, verbose_name='次数', help_text='次数')
    status = BooleanField(default=True, verbose_name='状态（1正常,0禁止登录')
    keyword = CharField(max_length=60, default='', verbose_name='关键词', help_text='关键词')
    bid_price = CharField(max_length=60, default='', verbose_name='bid价格', help_text='bid价格')
    last_page_num = IntegerField(default=0, verbose_name='上次页面位置', help_text='上次页面位置')
    page_num = IntegerField(default=0, verbose_name='页面位置', help_text='页面位置')
    is_sponsor = BooleanField(default=False, verbose_name='是否有广告推荐')
    check_time = CharField(max_length=256, default='', verbose_name='抓取时间', help_text='抓取时间')
    is_delete_time = IntegerField(default=0, verbose_name='是否已删除（0否, 大于0删除时间）', help_text='是否已删除（0否, 大于0删除时间）')

    class Meta:
        table_name = 'rank_history'
        verbose_name = '排行历史'

    def _to_dict(self):
        keys = ['rank_good_id', 'total', 'status', 'keyword', 'bid_price', 'last_page_num', 'page_num', 'is_sponsor']
        return self.to_dict(keys)
