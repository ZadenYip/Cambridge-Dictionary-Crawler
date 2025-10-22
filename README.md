# 剑桥字典爬虫（Cambridge Dictionary crawler）**施工中（Work in progress）**

## 使用方式（Usage）
首先克隆仓库 `git clone XXX`<br>
First, clone the repository `git clone XXX`<br>

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

注意：由于使用了 scrapy-deltafetch 中间件，重复运行时不会重复爬取已经爬取过的页面。如果有需要重新爬取所有页面，可以删除与 camb_dict_crawler同级的文件夹 .scrapy下的 deltafetch 文件夹<br>
Note: Since the scrapy-deltafetch middleware is used, pages that have already been crawled will not be re-crawled when run repeatedly. If you need to re-crawl all pages, you can delete the deltafetch folder under the .scrapy folder at the same level as camb_dict_crawler<br>

### 导出文件
爬取结果会导出为 JSON Lines 格式的文件，分别为 successful_items.jl 和 error_items.jl，存放在 camb_dict_crawler 文件夹下<br>
The crawling results will be exported as JSON Lines format files, namely successful_items.jl and error_items.jl, stored in the camb_dict_crawler folder<br>

## 项目说明（Project Description）
使用 Scrapy 作为库进行爬取。scrapy-fake-useragent 和 scrapy-deltafetch 为中间件。<br>
Using Scrapy as the library for crawling. scrapy-fake-useragent and scrapy-deltafetch are used as middlewares.<br>
- scrapy-fake-useragent 用于随机生成 User-Agent，防止被反爬虫机制阻挡<br>
- scrapy-fake-useragent is used to randomly generate User-Agent to prevent being blocked by anti-crawling mechanisms<br>
- scrapy-deltafetch 用于避免重复下载已经爬取过的页面<br>
- scrapy-deltafetch is used to avoid re-downloading pages that have already been crawled<br>