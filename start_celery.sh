#!/bin/sh
celery -A tasks.workers -Q parse_page_list,parse_page_detail,downloader_queue,item_queue worker -l info -c 1

#启动一个parse_page_list
# celery -A tasks.workers -Q parse_page_list worker -l info -c 1 -n page_list

#启动一个 parse_page_detail
# celery -A tasks.workers -Q parse_page_detail worker -l info -c 1 -n page_detail

#启动一个 downloader_queue,4个并发，节点名字为downloader，-l log登记为info
# celery -A tasks.workers -Q downloader_queue worker -B -l info -c 4 -n downloader

#启动一个 item_queue,1个并发，节点名字为downloader
# celery -A tasks.workers -Q item_queue worker -l info -c 1 -n item



