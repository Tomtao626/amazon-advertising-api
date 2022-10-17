# 初始化model模型到database
from db.RankGoods import RankGoods, RankHistory
from db.basemodel import _mdb

# create new table

tables = [RankGoods, RankHistory]
_mdb.drop_tables(tables)

_mdb.drop_tables(tables)
_mdb.create_tables(tables)
_mdb.commit()
