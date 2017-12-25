# coding=utf-8
from .workers import app
from downloader import parse_url
from page_parse import extract_position_detial_info,extract_position_list
from db import save_item

@app.task(ignore_result=True)
def downloader(url,meta,flag="list"):
    response = parse_url(url)
    if response is not None:
        if flag=="detail":
            app.send_task("tasks.downloader.parse_page_detail", args=(response, meta),queue="parse_page_detail",routing_key="for_page_detail")
        elif flag =="list":
            app.send_task("tasks.downloader.parse_page_list", args=(response, meta),queue="parse_page_list",routing_key="for_page_list")


@app.task(ignore_result=True)
def parse_page_list(resposne,meta):
    position_list, next_url = extract_position_list(resposne)
    if next_url is not None:
        app.send_task("tasks.downloader.downloader",args=(next_url,meta),queue="downloader_queue",routing_key="for_download")

    for position in position_list:
        meta["item"] = position
        app.send_task("tasks.downloader.downloader",args=(position["position_href"],meta,"detail"),queue="downloader_queue",routing_key="for_download")


@app.task(ignore_result=True)
def parse_page_detail(response,meta):
    item = meta.get("item",None)
    item = extract_position_detial_info(response,item)
    app.send_task("tasks.downloader.process_item",args=(item,),queue="item_queue",routing_key="for_save")

@app.task(ignore_result=True)
def process_item(item):
    save_item(item)

@app.task(ignore_result=True)
def execute_start_request():
    meta = {}
    start_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=python"
    meta["start_url"] = start_url
    app.send_task("tasks.downloader.downloader", args=(start_url, meta), queue="downloader_queue", routing_key="for_download")
