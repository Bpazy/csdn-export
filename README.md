# csdn-export
导出CSDN博客并创建对应的Github Issue博客。  
通过本工具你既可以一次性导出所有博客，也可以指定某一篇要导出的博客。

# 使用
`python csdn-export.py --help`查看详细。

## 前提
```
$ pip install pipenv
$ pipenv install
```

## 例子
```
$ echo CSDN_COOKIE > cookie.txt 
$ pipenv run python csdn-export.py -u GITHUB_USERNAME -r GITHUB_REPO -t GITHUB_ACCESS_TOKEN -p CSDN_BLOG_MAX_PAGE -c CSDN_USERNAME -b BLOG_ID
```

## Variables
`GITHUB_ACCESS_TOKEN`: 在后面的网址中生成：https://github.com/settings/tokens  
`GITHUB_USERNAME`: 你的Github用户名  
`GITHUB_REPO`: 你的Github仓库名  
`CSDN_BLOG_MAX_PAGE`: 你的CSDN博客最大页码. 存在这个变量的原因是目前程序无法获取最大页码     
`CSDN_COOKIE`: 你的CSDN cookie，你可以在控制台中复制随便一个csdn请求的cookie。  
`CSDN_USERNAME`: 你的CSDN用户名  
`BLOG_ID`: 你的CSDN博客ID  


# 警告
不要对他人的仓库使用本工具!!!  
不要对他人的仓库使用本工具!!!  
不要对他人的仓库使用本工具!!!  
