## celery的demo

#### 简介
- celery是一个`任务队列`,同时也`支持任务调度`，强大的生产者消费者模型
- backend `Results are not enabled by default. In order to do remote procedure calls or keep track of task results in a database`
- broker `a message transport`
- main.py中实现把第一个url地址放入downloader的队列中
- 整个程序在tasks中的worker中实现了每隔两分钟吧start_url放入downloader中
- 在tasks中定义的任务，都是调用的其他文件夹中的方法
- 可以通过celery flower来实现对当前多有节点的队列的监控，`flower -A tasks.workers --port=5555`


#### 注意
- 启动worker的时候如果需要使用celerybeat的定时功能，需要加上`-B`的参数
    - 启动一个 downloader_queue,-A app的位置,-Q 指定启动的队列,worker 消费者,-c 4个并发,-B 启动该队列的celerybeaet，-n 节点名字为downloader，-l log等级为info
    `celery -A tasks.workers -Q downloader_queue worker -B -l info -c 4 -n downloader`
- log中使用dictConfig的方式添加日志，格式比较清晰，后续可以使用该方式来设置日志
- 实例化celery的app的时候，使用include的方式，能够让celery自动的从`tasks.downloader`中寻找tasks，方便
- 在tasks中传递了resposne对象，不能使用json的序列化方式，选择`pickle`的方式
- 在app.conf.update(`'CELERYBEAT_SCHEDULE'`)中能够实现celerybeat的定时任务功能，如果是定时执行，比如某天的某小时，可以使用crontab的方式来完成
- 在task中，都是用`app.send_task("**task", args=(response,),queue="parse_page_list",routing_key="for_page_list")
`来把结果交给一个task去完成，同时使用queue和routing_key的方式来，能够把当前任务队列中的内容传递到另一个任务队列，celery能够自动的寻找queue和routing_key匹配的队列去接收任务

#### 本代码可以加强的地方
- 数据库存入时候的去重
- 请求的时候对cookie，headers的处理，refer的处理，代理ip的处理


#### 使用体会
- 使用celery能够轻松的帮助我们完成一个大型的分布式爬虫，但是如果和scrapy或者是scrapy_redis相比的话，整个程序会变得很凌乱
- 后续的框架，可以使用celery来完成一些细节功能的异步调用，但是目前感觉在纯粹的依靠celery来完成一个分布式的爬虫，没戏



------------------
#### 发现selenium grid能够实现在多个浏览器的分布式，下一步来研究下