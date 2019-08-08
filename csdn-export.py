import argparse
import codecs
import json
import re

import requests
from bs4 import BeautifulSoup


def create_issue(title, body, token, username, repo):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'token %s' % token
    }
    params = {
        'title': title,
        'body': body
    }
    r = requests.post(
        'https://api.github.com/repos/%s/%s/issues' % (username, repo), headers=headers, json=params)
    if r.status_code > 300:
        print('error %s', r.text)
        return False
    return True


def make_sure_create_issue(title, body, token, username, repo, times=0):
    try:
        created = create_issue(title, body, token, username, repo)
    except ConnectionError as err:
        if times + 1 >= 3:
            raise ConnectionError(err)
        created = make_sure_create_issue(title, body, token, username, repo, times + 1)
    return created


base_csdn = 'https://blog.csdn.net/{username}/article/list/{page}'
base_csdn_detail = 'https://blog.csdn.net/{username}/article/details/{blog_id}'
base_csdn_markdown = 'https://mp.csdn.net/mdeditor/getArticle?id={articleId}'


def get_csdn_page(username):
    url = base_csdn.replace('{username}', username).replace('{page}', '1')
    print(requests.get(url).text)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    page_htmls = soup.select('li[data-page]')
    print(page_htmls)
    return list(map(lambda x: x.attrs['data-page'], page_htmls))[-1]


def query_csdn_article_urls(page_num, username):
    url = base_csdn.replace('{username}', username).replace('{page}', str(page_num))
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    article_htmls = soup.select('h4 > a')

    # 过滤掉文章列表的广告
    return filter(lambda x: username in x, map(lambda x: x.attrs['href'], article_htmls))


class CsdnException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def read_cookie():
    with open('cookie.txt') as file:
        return file.read()


cookie = read_cookie()


def get_csdn_markdown(article_id):
    headers = {
        'authority': 'mp.csdn.net',
        'method': 'GET',
        'path': '/mdeditor/getArticle?id=%s' % article_id,
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-HK;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'referer': 'https://mp.csdn.net/mdeditor/%s' % article_id,
        'user-agent': 'Mozilla/ 5.0(Windows; NT; 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like; Gecko) Chrome / '
                      '73.0; .3683; .103; Safari / 537.36',
    }
    r = requests.get(base_csdn_markdown.replace('{articleId}', article_id), headers=headers)
    ret = json.loads(r.text)
    if ret['error']:
        raise CsdnException('%s 请检查Cookie是否设置, article_id: %s' % (ret['error'], article_id))
    return ret['data']


def extract_csdn_article_id(article_url):
    # https://blog.csdn.net/hanziyuan08/article/details/88954091
    pattern = re.match(
        r'https://blog.csdn.net/.+?/article/details/(\d+)', article_url)
    if not pattern:
        return ''
    return pattern.group(1)


def save_file(filename, file_content):
    filename = re.sub(r'[/:*?"<>|]', " ", filename)
    with codecs.open('blog/' + filename, 'w', 'utf-8') as file:
        file.write(file_content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help="github personal access token")
    parser.add_argument('-p', '--page', type=int, help="csdn blog max page")
    parser.add_argument('-u', '--username', help="github account username")
    parser.add_argument('-c', '--csdnusername', help="csdn account username")
    parser.add_argument('-b', '--csdnblogids', help="csdn blog ids", nargs='*')
    parser.add_argument('-r', '--repo', help="github account repo")
    args = parser.parse_args()

    all_article_urls = []
    # 取出所有文章
    if args.page:
        for page in range(1, args.page + 1):
            for articleUrl in query_csdn_article_urls(page, args.csdnusername):
                all_article_urls.append(articleUrl)

    # 指定文章ID
    if args.csdnblogids:
        for blog_id in args.csdnblogids:
            all_article_urls.append(
                base_csdn_detail.replace('{username}', args.csdnusername).replace('{blog_id}', blog_id))

    # 按照文章发表时间创建issue，最早的文章先创建issue
    for articleUrl in reversed(all_article_urls):
        article_id = extract_csdn_article_id(articleUrl)
        markdown_article = get_csdn_markdown(article_id)
        print(markdown_article)
        # save_file(markdownArticle['title'] + '.md', markdownArticle['markdowncontent'])
        success = make_sure_create_issue(markdown_article['title'], markdown_article['markdowncontent'], args.token,
                                         args.username, args.repo)
        if not success:
            print('Article migration failed: %s' % articleUrl)
