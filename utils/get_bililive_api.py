from utils.tool import Tools, DatabaseConnector

# 注：**more均为接收配置文件多余参数的适应参数
class BiliLive:
    def __init__(self):
        self.conf = Tools.get_config('bilibili')

    @staticmethod
    def get_guard_sum(roomid=379598,uid=34055779,**more):    # 获取舰长数量
        url = f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid={roomid}&ruid={uid}&page_size=1&page=1"
        bda = Tools.get_json(url)
        guards = bda["data"]["info"]["num"]
        print(guards)
        return guards


    @staticmethod
    def get_fans_sum(uid=34055779,**more):    # 获取粉丝数量
        url = f"https://api.bilibili.com/x/relation/stat?vmid={uid}"
        bda = Tools.get_json(url)
        print(bda)
        fans = bda["data"]["follower"]
        print(fans)
        return fans


    @staticmethod
    def get_guard_list(roomid=379598, uid=34055779,**more):    # 获取舰长信息
        url = f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid={roomid}&ruid={uid}&page_size=29&page=1"
        print(url)
        bilidata = Tools.get_json(url)
        jztop = bilidata["data"]["top3"]
        jzlist = bilidata["data"]["list"]
        jz = jztop + jzlist
        if bilidata["data"]["info"]["page"]:  # b站接口限制单页数量，超过一页的数据获取
            for a in range(1, (bilidata["data"]["info"]["page"])):
                url = f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid={roomid}&ruid={uid}&page_size=29&page={a + 1}"
                bilidata = Tools.get_json(url)
                jz1 = bilidata["data"]["list"]
                jz = jz + jz1
        # uid:B站uid，rank:舰长排名，username:用户名，guard_level:舰长等级，medal_info[medal_level]: 粉丝牌等级
        # print(jz)
        return jz


    @staticmethod
    def save_guard():    # 保存舰长信息
        guard_table = Tools.get_tables()['guard_table']
        jzs = BiliLive.get_guard_list(**Tools.get_config('bilibili'))
        DatabaseConnector.data_results(f"update {guard_table} set `guard_no` = NULL WHERE `guard_no` IS NOT NULL")
        DatabaseConnector.data_results(f"ALTER TABLE {guard_table} AUTO_INCREMENT = 1;")  # 修正自增起点
        for jz_list in jzs:
            sql = f"""INSERT INTO {guard_table} (uid, bili_name, guard_no, guard_level, medal_level)
VALUES ('{jz_list["uid"]}', '{jz_list["username"]}', '{jz_list["rank"]}', '{jz_list["guard_level"]}', '{jz_list["medal_info"]["medal_level"]}')
ON DUPLICATE KEY UPDATE
  bili_name = IF(VALUES(bili_name) = bili_name, bili_name, VALUES(bili_name)),
  guard_no = IF(VALUES(guard_no) = guard_no, guard_no, VALUES(guard_no)),
  guard_level = IF(VALUES(guard_level) = guard_level, guard_level, VALUES(guard_level)),
  medal_level = IF(VALUES(medal_level) = medal_level, medal_level, VALUES(medal_level));
"""
            re = DatabaseConnector.data_results(sql)
            print(re)


# BiliLive.save_guard()
