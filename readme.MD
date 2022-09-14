## 简介

这是一个模仿微软TODO的一个项目,当前只有网页端,使用`websocket`推送消息

## 适用人群

需要时间管理的个人或团队

## 功能

可以给代办事项:
1. 添加到期时间
2. 添加提醒
3. 添加重复周期

(待实现功能...)
通过不同的任务来管理一天的精力

多种方式提醒用户
- websocket
- 邮件
- 短信
- webhook


## 安装

运行及依赖环境

`python 3.10`,`node v16.14.0`

安装依赖

```
pip install -r requirements.txt
```

编译前端

```
cd html
npm install
npm run build
```

## 本地运行

运行`Django`

```
python manage.py runserver
```

运行定时服务

```
python websocket_server.py
```

运行前端

```
cd html
npm run dev
```

## 部署

`chrome`的`Notification`需要https协议

修改`html/.env.production`中的ws地址

## 展示

https://todo.iforj.com/myday

账号`test`,密码`test`