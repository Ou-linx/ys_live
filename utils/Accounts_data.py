from datetime import date
import json

from utils.tool import DatabaseConnector,Tools


class GetAccounts:
    @staticmethod
    def get_alldate():  # 获取全部账号信息
        guard_table = Tools.get_tables()['guard_table']
        acc_table = Tools.get_tables()['acc_table']
        sql = f"select * from {guard_table} left join {acc_table} on {guard_table}.uid = {acc_table}.bili_uid union select * from {guard_table} right join {acc_table} on {guard_table}.uid = {acc_table}.bili_uid"
        re = DatabaseConnector.data_results(sql)
        return re

    @staticmethod
    def seq_acc(data_list):      # 数据重新排序
        for a in range(len(data_list) - 1):
            for b in range(len(data_list) - 1 - a):
                if data_list[b + 1]['guard_no'] is None:
                    pass
                elif data_list[b]['guard_no'] is None or data_list[b]['guard_no'] > data_list[b + 1]['guard_no']:
                    data_list[b],data_list[b + 1] = data_list[b + 1],data_list[b]
        return data_list


    @staticmethod
    def get_acc_date(acc_id):  # 获取单个账号信息
        guard_table = Tools.get_tables()['guard_table']
        acc_table = Tools.get_tables()['acc_table']
        sql = f"select * from {guard_table} right join {acc_table} on {guard_table}.uid = {acc_table}.bili_uid where {acc_table}.id = {acc_id}"
        re = DatabaseConnector.data_results(sql)
        return re

    def __init__(self):
        self.more_acc = []
        self.tiedao_acc = []
        self.bili_acc = []
        self.off_acc = []
        self.boss_acc = []
        self.guard_noacc = []
        self.old_acc = []
        self.del_acc = []
        self.alldata = GetAccounts.get_alldate()


    def class_acc(self):        # 账号分类
        for ac in self.alldata:
            if ac["is_del"].__str__() == "1":
                self.del_acc.append(ac)     # 标记删除数据
            elif ac["bili_uid"].__str__() == str(Tools.get_config('bilibili')['uid']) or ac["good_friend"].__str__() == "666":   # 卖萌自己
                self.boss_acc.append(ac)
            elif ac["is_ok"] is None:
                self.guard_noacc.append(ac)         # 没有存账号的舰长
            elif ac["is_ok"] is not None:     # 卖萌自己以外的账号处理
                if ac["good_friend"].__str__() == "1" and ac["guard_no"] is not None:
                    ac["is_ok"] = None
                    self.more_acc.append(ac)    # 明确不打号的舰长
                elif ac["guard_no"] is None and ac["good_friend"].__str__() != "4":
                    ac["is_ok"] = None
                    self.old_acc.append(ac)       # 掉舰、保存账号
                elif ac['server'].__str__() == "0":
                    self.off_acc.append(ac)     # 官服
                elif ac['server'].__str__() == '1':
                    self.bili_acc.append(ac)    # B服
                elif ac['server'].__str__() == '5':
                    self.tiedao_acc.append(ac)  # 铁道
        # 重新按舰长列表排序进行排序
        self.more_acc = GetAccounts.seq_acc(self.more_acc)
        self.tiedao_acc = GetAccounts.seq_acc(self.tiedao_acc)
        self.bili_acc = GetAccounts.seq_acc(self.bili_acc)
        self.off_acc = GetAccounts.seq_acc(self.off_acc)
        self.guard_noacc = GetAccounts.seq_acc(self.guard_noacc)

    def replace_acc(self):      # 重新排列整合数据
        self.alldata = []
        self.alldata+=self.boss_acc      # 卖萌自己在最上面
        self.alldata+=self.bili_acc      # B服数量少，在官服上面
        self.alldata+=self.off_acc       # 官服
        self.alldata+=self.tiedao_acc    # 铁道
        self.alldata+=self.more_acc      # 不打号的舰长
        self.alldata+=self.guard_noacc   # 没存账号的舰长
        self.alldata+=self.old_acc       # 掉舰、仅保存的账号


    def rtn_acc(self):      # 结果输出
        GetAccounts.class_acc(self)
        GetAccounts.replace_acc(self)
        return json.dumps(self.alldata, default=GetAccounts.handle_date)

    @staticmethod   # sql结果中日期处理
    def handle_date(obj):
        if isinstance(obj, date):
            return obj.isoformat()


class SetAccounts:
    def __init__(self):
        self.acc_table = Tools.get_tables()['acc_table']
        self.insert_sql = f"insert into {self.acc_table} (`nick_name`,`bili_uid`,`username`,`password`,`info`,`server`,`good_friend`,`update_time`) values"
        self.update_sql = f"update {self.acc_table} set"

    # 增加舰长数据
    def add_acc(self,nick_name, bili_uid, username, password, info, server, good_friend=None):
        self.insert_sql = self.insert_sql+f"('{nick_name}','{bili_uid}','{username}','{password}','{info}','{server}','{good_friend}','{date.today()}')".replace("\'None\'","NULL")
        return DatabaseConnector.data_results(self.insert_sql)


    # 更新舰长数据
    def up_acc(self,up_data):
        end = ""
        for d in up_data:
            if d == "id":
                end = f"`update_time` = '{date.today()}' where id = {up_data[d]}"
            elif up_data[d] is None or up_data[d] == "" or d == "update_time":
                pass
            else:
                self.update_sql = self.update_sql + f" `{d}` = '{up_data[d]}',"
        self.update_sql = self.update_sql + end
        return DatabaseConnector.data_results(self.update_sql)

    def del_acc(self,ac_id):       # 删除舰长数据
        del_sql = self.update_sql + f" `is_del` = 1 where id = {ac_id}"
        return DatabaseConnector.data_results(del_sql)

    def set_state(self,ac_id):  # 更新打号状态，传入id，为0时更新全部；为其它时更新指定id下的值（0，1互换）
        if str(ac_id) == "0":
            state_sql = self.update_sql + f" `is_ok` = 0"
        else:
            state_sql = self.update_sql + f" `is_ok` = CASE WHEN is_ok = 0 THEN 1 WHEN is_ok = 1 THEN 0 END where id = {ac_id};"
        return DatabaseConnector.data_results(state_sql)

# a = Accounts.get_alldate()
# Accounts.seq_acc(a)
# if __name__ == '__main__':
#     a = GetAccounts()
#     print(a.rtn_acc())
# a = {"ac_id":2,"nick_name":"昵称", "username":"账号", "password":"密码", "update_time":"2022-11-01"}
# b = SetAccounts()
# # print(b.up_acc(a))
# b.set_state(1)