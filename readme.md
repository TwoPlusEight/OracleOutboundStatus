# 提示
本项目仅达到**能用就行**的程度, 不要要求太高, 因为能力有限  
~~仅充当融合怪的角色~~  
没有系统化的学习, 部分命名可能比较糟糕, 敬请谅解
## 甲骨文云批量查询流量后端(包括前端网页)
### 用处
展示所有甲骨文账号对应实例以及总流量, 数据来源于甲骨文API  
间隔固定时间(默认45分钟一次)刷新流量  
示例: [甲骨文云流量](https://oracle-cloud.twopluseight.net/)  
![1707840507805.png](https://img10.360buyimg.com/babel/jfs/t20260213/132044/32/39473/83260/65cb9402F7b8eb5d7/a96d9b8a005a3aad.png)
### 使用
开发测试的环境为 Python3.11

使用时需要安装Python  
>Debian/Ubuntu  
1. 安装Python (Debian11/12, Ubuntu20/22可以跳过此步)
```bash
apt install python
```
2. 安装pip(如果没有的情况下)  
你也可以根据此文章的教程来[安装pip](https://pip.pypa.io/en/stable/installation/#supported-methods)
```bash
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```
3. 克隆项目到本地
```bash
git clone https://github.com/TwoPlusEight/OracleOutboundStatus
cd ./OracleStatusBackend
```
4. 安装并创建虚拟环境(可跳过)
```bash
pip install venv
python -m venv ./venv
```
5. 安装依赖
> 虚拟环境
```bash
./venv/Script/activate
pip install -r ./requirements.txt
```
> 非虚拟环境
```bash
pip install -r ./requirements.txt
```
6. 创建`configs`并上传甲骨文API文件至此文件夹  
配置文件的文件名称必须为.conf(在不修改代码的情况下)  
文件第一行必须为[]开始且不为空  
最终网页左侧列表的账号标题为配置文件[]中的标题
7. 启动
```bash
python main.py
```
8. nginx反向代理
```
location / {
        proxy_pass http://localhost:15048/;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection upgrade;
        proxy_set_header Accept-Encoding gzip;
    }
```

## 更改
您可以根据static文件夹中的json来编写新的页面
