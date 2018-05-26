import urllib2
import re
from bs4 import BeautifulSoup

def crawl_init():
    req = urllib2.Request('http://finance.ifeng.com')
    req.add_header('User-Agent','Mozilla/5.0 (X11;Ubuntu;Linux x86_64;rv:31.0) Gecko/20100101 Firefox/31.0')
    req.add_header('Referer','http://finance.ifeng.com')
    resp = urllib2.urlopen(req)
    return resp.read()

def make_data():
    html = crawl_init()
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.findAll('div', {'class': 'box_hot01 clearfix'})
    pack_list = []
    for data in datas:
        passage_title = data.find('h2').a.string
        passage_url = data.find('h2').a['href']
        image_url = data.find('img').get('src')
        little_passages = data.findAll('li')

        pack_data = {}
        pack_data['little_passages'] = []
        for little_passage in little_passages:
            l_p = {}
            l_p['little_passage_title'] = little_passage.a.string
            l_p['little_passage_url'] = little_passage.a['href']
            pack_data['little_passages'].append(l_p)
        pack_data['passage_title'] = passage_title
        pack_data['passage_url'] = passage_url
        pack_data['image_url'] = image_url
        pack_list.append(pack_data)
    return pack_list

if __name__ == '__main__':
    make_data()

