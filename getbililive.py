from Utils import Tools

# 注：**more均为接收配置文件多余参数的适应参数
class BiliLive:
    @staticmethod
    def get_guard_sum(roomid,uid,**more):    # 获取舰长数量
        url = f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid={roomid}&ruid={uid}&page_size=1&page=1"
        bda = Tools.get_json(url)
        print(bda)
        guards = bda["data"]["info"]["num"]
        print(guards)


    @staticmethod
    def get_fans_sum(uid,**more):    # 获取粉丝数量
        url = f"https://api.bilibili.com/x/relation/followers?vmid={uid}"
        bda = Tools.get_json(url,cookie=Tools.cookie_set())
        print(bda)
        fans = bda["data"]["total"]
        print(fans)

BiliLive.get_guard_sum(**Tools.get_config('bilibili'))
# BiliLive.get_fans_sum(**Tools.get_config('bilibili'))