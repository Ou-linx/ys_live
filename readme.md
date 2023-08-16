账号表：

| 字段名         | 数据类型         | 备注                       |
|-------------|--------------|--------------------------|
| id          | int          | 自增主键                     |
| nick_name   | varchar(100) | 自定义名称                    |
| bili_uid    | int          |                          |
| username    | varchar(100) | 账号                       |
| password    | varchar(100) | 密码                       |
| info        | varchar(255) | 备注                       |
| server      | int          | 0=官服；1=B服；5=星铁           |
| good_friend | int          | 为1不打号；为4为额外接单；为666则是主播自己 |
| is_ok       | int          |                          |
| update_time | date         | 数据更新时间（手动录入则更新）          |
| is_del      | int          | 逻辑删除                     |

舰长表：

| 字段名         | 数据类型         | 备注   |
|-------------|--------------|------|
| b_id        | int          | 自增主键 |
| uid         | int          | uid  |
| guard_no    | int          | 舰长排名 |
| bili_name   | varchar(100) | 用户名  |
| guard_level | int          | 舰长等级 |
| medal_level | int          | 牌子等级 |
