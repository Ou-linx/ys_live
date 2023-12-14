import requests


class AccTool:
    @staticmethod
    def set_reacc_json(sel_data):
        res_json = {
            "guard_id": sel_data.guard_id.id,  # 舰长表id
            "guard_bili_uid": sel_data.guard_id.bili_uid,  # 舰长b站uid
            "guard_bili_name": sel_data.guard_id.Bili_name,  # B站用户名
            "guard_nick_name": sel_data.nickname_set.all(),  # 舰长自定义名称
            # "guard_rank": sel_data.guard_id.guard_rank,  # 排行榜
            "guard_level": sel_data.guard_id.guard_level,  # 舰长等级
            # "guard_medal_level": sel_data.guard_id.guard_medal,  # 粉丝牌等级
            "acc_id": sel_data.id,  # 账号id
            "username": sel_data.game_acc,  # 用户名
            "password": sel_data.game_pass,  # 密码
            "info": sel_data.info,  # 备注
            "game_class": sel_data.game_class,  # 账号分类
            "good_friend": sel_data.free,  # 不打号标注
            "update_time": sel_data.update_time,  # 更新时间
            "is_ok": sel_data.is_ok,  # 打号完成标志
        }
        print(res_json)
        return res_json

    @staticmethod
    def res_json_msg(code="500", msg="server error"):
        json_message = {
            "code": code,
            "msg": msg,
        }
        return json_message

    @staticmethod
    def get_room_guard(roomid=379598, uid=34055779):
        url = (f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?"
               f"roomid={roomid}&ruid={uid}&page_size=29&page=1")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/118.0.0.0 Safari/537.36'
        }
        bilidata = requests.get(url, headers=headers, verify=False).json()
        jztop, jzlist = bilidata["data"]["top3"], bilidata["data"]["list"]
        alljz = jztop + jzlist
        if bilidata["data"]["info"]["page"]:  # b站接口限制单页数量，超过一页的数据获取
            for pagelist in range(1, (bilidata["data"]["info"]["page"])):
                url = (f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?"
                       f"roomid={roomid}&ruid={uid}&page_size=29&page={pagelist + 1}")
                bilidata = requests.get(url, headers=headers, verify=False).json()
                jz1 = bilidata["data"]["list"]
                alljz += jz1
        guard_list = []
        for i in alljz:
            uid, rank, username, guard_level, medal_level = i['uid'], i['rank'], i['username'], i['guard_level'], \
                i['medal_info']['medal_level']
            user_profile = {
                "bili_uid": uid,
                "guard_rank": rank,
                "Bili_name": username,
                "guard_level": guard_level,
                "guard_medal": medal_level,
            }
            guard_list.append(user_profile)
        # uid:B站uid，rank:舰长排名，username:用户名，guard_level:舰长等级，medal_info[medal_level]: 粉丝牌等级
        # print(jz)
        return guard_list


