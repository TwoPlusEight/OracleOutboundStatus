## 项目描述
`frontend`为甲骨文批量查询的主要页面, 用于将后端提供的数据展示出来  
仅用作简单演示

`backend`为后端, 用于处理账号数据并编组提供给前端显示  
可以获取所有账号的机器的出站流量, 存储桶的流量, 账号的创建时间(默认以第一个订阅为注册时间, 多个订阅的情况请根据需要修改 ./backend/oracle/subscription.py 文件以适应)

具体请查看 [TwoPlusEight/OracleOutboundStatus/blob/master-previous/backend/readme.md](https://github.com/TwoPlusEight/OracleOutboundStatus/blob/master-previous/backend/readme.md)

## ?
可以直接下载backend进行部署, 设置域名解析与反代来进行访问
