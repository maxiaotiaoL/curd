from crm import models

class AutoSale(object):
    users = None
    iter_users = None
    reset_status = False
    roll_backlist = []

    @classmethod
    def fetch_users(cls):
        sales = models.SaleRank.objects.all().order_by('-weight')

        ret = []
        count = 0
        while True:
            flag = False
            for row in sales:
                if count < row.num:
                    ret.append(row.user_id)
                    flag = True
            count += 1
            if not flag:
                break

        # ret = []
        # temp = []  # [[6, 6, 6, 6], [14, 14], [15, 15]]
        # for sale_obj in sales:
        #     temp.append([sale_obj.user_id for _ in range(sale_obj.num)])
        #
        # flag = 0  # 标识几个列表被取空
        # while flag < len(temp):
        #     for sale_list in temp:
        #         if sale_list:
        #             ret.append(sale_list.pop())
        #         else:
        #             flag += 1

        cls.users = ret


    @classmethod
    def get_sale_id(cls):
        if cls.roll_backlist:
            return cls.roll_backlist.pop()

        if not cls.users:
            cls.fetch_users()

        if not cls.users:  # 如果没有课程顾问，则返回None
            return None

        if not cls.iter_users:
            cls.iter_users = iter(cls.users)

        try:
            user_id = next(cls.iter_users)
        except StopIteration as e:
            if cls.reset_status:
                cls.fetch_users()
                cls.reset_status = False
            cls.iter_users = iter(cls.users)
            user_id = cls.get_sale_id()
        except Exception as e:
            print(str(e))

        return user_id

    @classmethod
    def reset(cls):
        cls.reset_status = True

    @classmethod
    def rollback(cls,sale_id):
        cls.roll_backlist.insert(0,sale_id)