from Utils import Tools

# 注：**more均为接收配置文件多余参数的适应参数
class BiliLive:
    @staticmethod
    def get_guard_sum(roomid=379598,uid=34055779,**more):    # 获取舰长数量
        url = f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid={roomid}&ruid={uid}&page_size=1&page=1"
        bda = Tools.get_json(url)
        print(bda)
        guards = bda["data"]["info"]["num"]
        print(guards)
        return guards


    @staticmethod
    def get_fans_sum(uid=34055779,**more):    # 获取粉丝数量
        url = f"https://api.bilibili.com/x/relation/followers?vmid={uid}"
        bda = Tools.get_json(url,cookie=Tools.cookie_set())
        print(bda)
        fans = bda["data"]["total"]
        print(fans)
        return fans


    @staticmethod
    def get_guard_list(roomid=379598, uid=34055779):
        url = f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid={roomid}&ruid={uid}&page_size=29&page=1"
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
        print(jz)
        return jz


class Accounts:
    @staticmethod
    def get_guard_accounts():
        sql = "select * from "


BiliLive.get_guard_list()