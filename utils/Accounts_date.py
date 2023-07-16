from utils.tool import DatabaseConnector


class GetAccounts:
    @staticmethod
    def get_alldate():  # 获取全部账号信息
        sql = "select * from list_aa left join list_bb on list_aa.uid = list_bb.bili_uid union select * from list_aa right join list_bb on list_aa.uid = list_bb.bili_uid"
        re = DatabaseConnector.print_results(sql)
        return re

    @staticmethod
    def seq_acc(list):      # 数据重新排序
        for a in range(len(list)-1):
            for b in range(len(list)-1-a):
                if list[b+1]['guard_no'] is None:
                    pass
                elif list[b]['guard_no'] is None or list[b]['guard_no'] > list[b+1]['guard_no']:
                    list[b],list[b+1] = list[b+1],list[b]
        return list

    def __init__(self):
        self.more_acc = []
        self.tiedao_acc = []
        self.bili_acc = []
        self.off_acc = []
        self.boss_acc = []
        self.guard_noacc = []
        self.old_acc = []
        self.alldata = GetAccounts.get_alldate()


    def class_acc(self):        # 账号分类
        for ac in self.alldata:
            if ac["uid"].__str__() == "34055779" or ac["good_friend"].__str__() == "666":   # 卖萌自己
                self.boss_acc.append(ac)
            elif ac["is_ok"] is None:
                self.guard_noacc.append(ac)         # 没有存账号的舰长
            elif ac["is_ok"] is not None:     # 卖萌自己以外的账号处理
                if ac["good_friend"].__str__() == "1" and ac["guard_no"] is not None:
                    self.more_acc.append(ac)    # 明确不打号的舰长
                elif ac["guard_no"] is None and ac["good_friend"].__str__() != "4":
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


    def ret_acc(self):      # 结果输出
        GetAccounts.class_acc(self)
        GetAccounts.replace_acc(self)
        return self.alldata


# a = Accounts.get_alldate()
# Accounts.seq_acc(a)
if __name__ == '__main__':
    a = GetAccounts()
    print(a.ret_acc())