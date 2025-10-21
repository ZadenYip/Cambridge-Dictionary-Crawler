# 剑桥字典爬虫（Cambridge Dictionary crawler）**施工中（Work in progress）**

## 使用方式（Usage）
首先克隆仓库 `git clone XXX`<br>
First, clone the repository `git clone XXX`<br>

<em>接下来安装虚拟环境 venv `python -m venv ./.venv`（可选）</em><br>
<em>Next, install the virtual environment venv `python -m venv ./.venv` (optional)</em><br>

### 虚拟环境安装（可选）（Virtual Environment Installation (Optional)）
```shell
python -m venv ./.venv
```
安装完成后，激活虚拟环境<br>
After installation, activate the virtual environment<br>

Windows：
```
source ./.venv/Scripts/activate 
```
Linux：
```shell
source ./.venv/bin/activate
```

### 依赖安装与运行（Dependency Installation and Execution）
安装依赖 `pip install -r requirements.txt`<br>
install the dependencies `pip install -r requirements.txt`<br>


```shell
cd ./camb_dict_crawler
scrapy crawl camb_dict_spider
```