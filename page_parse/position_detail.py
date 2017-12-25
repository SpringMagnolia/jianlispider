# coding=utf-8
from .load_response import load_response
from loger import page_detail_logger

def extract_position_detial_info(response,item):
    html = load_response(response)
    item["job_publish_date"] = html.xpath("//li[@id='liJobPublishDate']/text()")
    item["job_publish_date"] = item["job_publish_date"][0] if len(item["job_publish_date"])>0 else None
    item["position_detial"]=html.xpath("//p[@class='mt20']/text()")
    item["position_detial"] = item["position_detial"] if len(item["position_detial"])>0 else None
    if item["position_detial"] is None:
        item["position_detial"] = html.xpath("//div[@class='tab-inner-cont']/p/text()")
    page_detail_logger.info("job的发布日期:{},url:{}".format(item["job_publish_date"],response.url))
    return item


if __name__ == '__main__':
    import  requests
    url = "https://xiaoyuan.zhaopin.com/job/CC000116133J90000261000"
    response = requests.get(url)
    from lxml import etree
    html = etree.HTML(response.content.decode())
    item = {}
    item["job_publish_date"] = html.xpath("//li[@id='liJobPublishDate']/text()")
    item["position_detial"]=html.xpath("//p[@class='mt20']/text()")

    print(item)

