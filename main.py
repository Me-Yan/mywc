from get_data import GetData
from database import Database


if __name__ == "__main__":

    flag = 2    # 1:表示查询商品  2:表示抢购

    gt = GetData()
    db = Database()

    gt.login()

    if flag == 1:
        goods_list = gt.get_all_data([1, 9], list(range(0, 5)))
        sql = gt.process_data(goods_list)
        db.insert_goods_data(sql=sql)
    elif flag == 2:
        gt.get_user_gtime()
        gt.visit_all_goods(1, [0, 30000], 2)    # 抢几幅、价格区间、延迟几秒


