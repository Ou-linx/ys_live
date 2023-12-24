# 指定基础镜像
FROM python:3.10-alpine
LABEL maintainer="admin@xuanol.com"

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories && apk add --no-cache tzdata

RUN apk add --no-cache pkgconf mysql-dev

RUN apk add --no-cache build-base mariadb-connector-c-dev

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com

# 设置工作目录
WORKDIR /app

# 复制应用程序文件到容器
COPY requirements.txt /app

# 运行命令来安装依赖项等
RUN pip3 install -r requirements.txt

# 指定容器启动时要执行的命令
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
