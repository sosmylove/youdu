这是公司的一个自动更新小说章节的程序
1 upload_book_youdu 这是主体程序
2 upload_book_sql 这是存储sql语句的code
3 schedule_text.py 这是定时器的一个调度程序，设定好时间启动，就会调用主体程序去对应的网站采集新增加的章节
4 cache_clear.py   这个是清理内容中夹杂的特殊字符或者多余的文字内容，以及清理书籍对应的马甲包在redis中的缓存
5 api_requests.py  这是一个封装的请求文件，包含了断开连接重新请求的方法

需要：
    1 安装python3的环境
    2 安装微软云存储的包azure
    3 配置对应的mysql数据库表
    4 需要配置环境变量的微软云的秘钥，上传数据
    5 配置接口拿到需要更新的书籍的链接.这个本来在代码里有设置，囿于公司机密就删掉咯.
