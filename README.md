# csdn-export
export csdn blog and create github issue blog.

# Usage
`python csdn-export.py --help` for details.

## Premise
1. pip install -r requirements.txt

## Demo
1. echo CSDN_COOKIE > cookie.txt
2. python csdn-export.py -u GITHUB_USERNAME -r GITHUB_REPO -t GITHUB_ACCESS_TOKEN -p CSDN_BLOG_MAX_PAGE

## Variables
`GITHUB_ACCESS_TOKEN`: Generate under here, https://github.com/settings/tokens  
`GITHUB_USERNAME`: Your Github username.  
`GITHUB_REPO`: Your Github repository.  
`CSDN_BLOG_MAX_PAGE`: Your CSDN blog max page. It exists because the program cannot get the maximum page number now.   
`CSDN_COOKIE`: CSDN cookie. You can find it in CSDN Ajax.  


# Warning
DO NOT USE THE TOOL FOR OTHERS REPO!!!  
DO NOT USE THE TOOL FOR OTHERS REPO!!!  
DO NOT USE THE TOOL FOR OTHERS REPO!!!  
