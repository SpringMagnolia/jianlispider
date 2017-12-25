# coding=utf-8
from tasks.workers import app

def execute_start_request():
    meta = {}
    start_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=python"
    meta["start_url"] = start_url
    app.send_task("tasks.downloader.downloader", args=(start_url, meta), queue="downloader_queue", routing_key="for_download")

if __name__ == '__main__':
    execute_start_request()