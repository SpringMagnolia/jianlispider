# coding=utf-8
from .load_response import load_response
from loger import page_list_logger

def extract_position_list(response):
    html = load_response(response)
    table_list = html.xpath("//div[@class='newlist_list_content']/table[@class='newlist']")
    position_list = []
    for table in table_list:
        item = {}
        item["position_title"] = table.xpath("./tr[1]/td[1]/div/a/text()")[0] if len(table.xpath("./tr/td[1]/div/a/text()"))>0 else None
        item["position_href"] = table.xpath("./tr[1]/td[1]/div/a/@href")[0] if len(table.xpath("./tr/td[1]/div/a/@href"))>0 else None
        item["company_name"] = table.xpath("./tr[1]/td[@class='gsmc']/a/text()")
        item["company_name"] = item["company_name"][0] if len(item["company_name"])>0 else None
        position_list.append(item)
        page_list_logger.info(item)
    #下一页
    next_url = html.xpath("//a[@class='next-page']/@href")
    next_url = next_url[0] if len(next_url)>0 else None
    page_list_logger.info(next_url)
    return position_list,next_url