<h2>自用打号列表6.0版本更新</h2>
<hr>
更新内容：
<br>
1、修改框架为django框架<br>
2、新增登录功能（调用django内置验证）实现多用户<br>
3、更好看的前端设计（放弃VUE，使用普通js配合bootstrap）<br>
4、优化部分逻辑，例如限制从bilibili拉取速度
<hr>
计划更新/待完成：<br>
1、单点登录及登录过期和登录延期功能（协商中）<br>
2、修改账号信息的前端（没人用，才不是忘记写了）<br>
3、admin账号的管理页面（不准备用内置admin）<br>
4、账号注册（admin功能，暂不准备对外开放）<br>
5、针对单个账号的外链功能<br>
<br>
6、静态资源暂时就用django来提供，完善后统一由nginx分发