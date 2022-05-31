from get_data import GetData
from database import Database


if __name__ == "__main__":

    gt = GetData()
    db = Database()

    gt.login()

    # goods_list = gt.get_all_data([1, 9], list(range(0, 5)))
    # sql = gt.process_data(goods_list)
    # db.insert_goods_data(sql=sql)

    gt.get_user_gtime(1)
    gt.visit_all_goods()


