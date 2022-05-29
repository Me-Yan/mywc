from get_data import GetData
from database import Database


if __name__ == "__main__":

    gt = GetData()
    db = Database()

    token, session = gt.login()

    goods_list = gt.get_all_data(token, session, [1, 9], list(range(0, 5)))

    sql = gt.process_data(goods_list)

    print(sql)
    db.insert_goods_data(sql=sql)


