# coding=utf-8
from lxml import etree

def load_response(response,back="element"):
    if back=="str":
        html = response.content.decode()
    else:
        html = etree.HTML(response.content.decode())
    return html

