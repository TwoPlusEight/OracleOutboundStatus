## 甲骨文云批量查询流量后端
### 用处
用于未来将会开发的前端, 展示所有甲骨文账号对应实例以及总流量, 数据来源于甲骨文API
### 使用
开发测试的环境为 Python3.11

使用时需要安装Python  
>Debian/Ubuntu  
1. 安装Python (Debian11/12, Ubuntu20/22可以跳过此步)
```bash
apt install python
```
2. 安装pip(如果没有的情况下)  
你也可以根据此文章的教材来[安装pip](https://pip.pypa.io/en/stable/installation/#supported-methods)
```bash
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```
3. 克隆项目到本地
```bash
git clone https://github.com/TwoPlusEight/OracleStatusBackend
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
7. 启动
```bash
python main.py
```