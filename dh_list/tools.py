class AccTool:
    @staticmethod
    def set_reacc_json(sel_data):
        res_json = {
            "guard_id": sel_data.guard_id.id,  # 舰长表id
            "guard_bili_uid": sel_data.guard_id.bili_uid,  # 舰长b站uid
            "guard_bili_name": sel_data.guard_id.Bili_name,  # B站用户名
            "guard_nick_name": sel_data.guard_id.nick_name,  # 舰长自定义名称
            "guard_rank": sel_data.guard_id.guard_rank,  # 排行榜
            "guard_level": sel_data.guard_id.guard_level,  # 舰长等级
            "guard_medal_level": sel_data.guard_id.guard_medal,  # 粉丝牌等级
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
