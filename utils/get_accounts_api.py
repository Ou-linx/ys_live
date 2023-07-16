import json

from utils.tool import DatabaseConnector,Tools

class GetAccountsApi:
    @staticmethod
    def get_alldate():  # 获取全部账号信息
        sqlFullStr = " SELECT * FROM list_member LEFT JOIN list_account ON list_member.uid = list_account.member_uid"
        sqlFullStr += " UNION"
        sqlFullStr += " SELECT * FROM list_member RIGHT JOIN list_account ON list_member.uid = list_account.member_uid"
        sqlFullStr += " ORDER BY guard_no DESC, medal_level DESC,server_name DESC "
        result = DatabaseConnector.print_results(sqlFullStr)
        return result

    def __init__(self):
        self.alldata = GetAccountsApi.get_alldate()
        # 原神标签页
        self.genshen.maimeng = []
        self.genshen.member = []
        self.genshen.oldmember = []
        self.genshen.nomember = []
        # 崩坏3rd标签页
        self.hongkai3.maimeng = []
        self.hongkai3.member = []
        self.hongkai3.oldmember = []
        self.hongkai3.nomember = []
        # 星穹铁道标签页
        self.starrail.maimeng = []
        self.starrail.member = []
        self.starrail.oldmember = []
        self.starrail.nomember = []
        # 原始设计列表
        # self.boss_acc      # 卖萌自己在最上面
        # self.bili_acc      # B服数量少，在官服上面
        # self.off_acc       # 官服
        # self.tiedao_acc    # 铁道
        # self.more_acc      # 不打号的舰长
        # self.guard_noacc   # 没存账号的舰长
        # self.old_acc       # 掉舰、仅保存的账号

    def class_acc(self):        # 账号分类
        for rowdata in self.alldata:
            # 卖萌自己
            if rowdata["uid"].__str__() == str(Tools.get_config('bilibili')['uid']) or rowdata["nickname"].__str__() == "卖萌":
                if rowdata["is_genshin"]:
                    # 原神
                    self.genshen.maimeng.append(rowdata)
                elif rowdata["is_starrail"]:
                    # 星铁
                    self.hongkai3.maimeng.append(rowdata)
                elif rowdata["is_honkai3"]:
                    # 崩坏3
                    self.starrail.maimeng.append(rowdata)
            # 舰长
            elif rowdata["guard_no"] is not None:
                if rowdata["is_genshin"]:
                    # 原神
                    self.genshen.member.append(rowdata)
                elif rowdata["is_starrail"]:
                    # 星铁
                    self.hongkai3.member.append(rowdata)
                elif rowdata["is_honkai3"]:
                    # 崩坏3
                    self.starrail.member.append(rowdata)
            # 过期舰长：无排名、有biliuid
            elif rowdata["guard_no"] is None and uid is not None:
                if rowdata["is_genshin"]:
                    # 原神
                    self.genshen.oldmember.append(rowdata)
                elif rowdata["is_starrail"]:
                    # 星铁
                    self.hongkai3.oldmember.append(rowdata)
                elif rowdata["is_honkai3"]:
                    # 崩坏3
                    self.starrail.oldmember.append(rowdata)
            # 非舰长：无排名、无biliuid
            elif rowdata["guard_no"] is None and uid is None:
                if rowdata["is_genshin"]:
                    # 原神
                    self.genshen.nomember.append(rowdata)
                elif rowdata["is_starrail"]:
                    # 星铁
                    self.hongkai3.nomember.append(rowdata)
                elif rowdata["is_honkai3"]:
                    # 崩坏3
                    self.starrail.nomember.append(rowdata)
            # 不打号舰长（暂时过滤
			# if rowdata["guard_no"] is not None and rowdata["is_genshin"] = 0 and rowdata["is_starrail"] = 0 and rowdata["is_honkai3"] = 0:
			# 无账号舰长（暂时过滤
			# if rowdata["guard_no"] is not None and rowdata["is_genshin"] is None and rowdata["is_starrail"] is None and rowdata["is_honkai3"] is None:
            # 仅保存账号（暂时过滤
			# if rowdata["guard_no"] is None and rowdata["is_genshin"] = 0 and rowdata["is_starrail"] = 0 and rowdata["is_honkai3"] = 0:

    def rtn_acc(self):      # 结果输出
        GetAccounts.class_acc(self)
        return json.dumps(self)


# a = Accounts.get_alldate()
# Accounts.seq_acc(a)
# if __name__ == '__main__':
#     a = GetAccounts()
#     print(a.rtn_acc())