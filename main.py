from get_data import GetData
from database import Database


if __name__ == "__main__":

    # 帅娃: 15928446489    75337511

    gt = GetData()
    db = Database()

    gt.login()

    # goods_list = gt.get_all_data([1, 9], list(range(0, 5)))
    # sql = gt.process_data(goods_list)
    # db.insert_goods_data(sql=sql)

    gt.get_user_gtime(1)
    gt.visit_all_goods(1, [0, 12000], 1.3)    # 抢几幅、价格区间、延迟几秒


