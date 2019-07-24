#! python 

import re
from bs4 import BeautifulSoup as bfs
from copy import copy
import sys
from getopt import gnu_getopt, GetoptError

HELP_MSG = 'preprocess.py <HTML file> -s <CSS file> -o <Target HTML file>'

def getargs(args):
    origin_file = ''
    css_file = 'whu-cs-report.css'
    output_file = ''
    try:
        opts, iargs = gnu_getopt(args[1:], 's:o:h',['style=','output=','help'])
    except GetoptError:
        print('Parse Error! Type "{} -h" to get help'.format(args[0]))
        sys.exit(2)

    for opt, arg in opts:
        if opt in ['-h','--help'] :
            print(HELP_MSG)
            sys.exit(0)
        elif opt in ['-s', '--style']:
            css_file = arg
        elif opt in ['-o', '--output']:
            output_file = arg
        else:
            print('unknown argumnet "{}". Type "{} -h" to get help'.format(opt,args[0]))

    if len(iargs) != 0 :
        origin_file = iargs[0]
    else:
        print('Please specify an html file! Type "{} -h" to get help'.format(args[0]))
        sys.exit(2)

    if output_file == '' :
        output_file = origin_file[:-5] + '_processed' + '.html'
    return origin_file, css_file, output_file

def main(args):
    origin_file, css_file, output_file = getargs(args)

    origin_html = ''
    custom_css = ''
    with open(origin_file, encoding='utf-8') as f:
        origin_html = f.read()
    with open(css_file, encoding='utf-8') as f:
        custom_css = f.read()

    # 将生成的html里有改动的custom CSS换成原版
    pat = r'\.custom-css-head.*\n(.+\n)+'
    new_html = re.sub(pat, custom_css, origin_html)

    # 将class为table-caption的div转成表标题
    soup = bfs(new_html, 'lxml')
    for tbltitle in soup.select('.table-caption'):
        cap = copy(tbltitle)
        del cap['class']
        cap.name = 'caption'
        tbltitle.next_sibling.table.insert(0,cap)
        tbltitle.decompose()

    # 匹配目录和各级标题的ID
    cnt = 1;
    for toc_a in soup.select('.md-toc-h2 a'):
        dest = soup.select('a[name="{}"]'.format(toc_a['href'][1:]))[0]
        dest['id'] = 'h2-{}'.format(cnt)
        toc_a['href'] = '#h2-{}'.format(cnt)
        cnt += 1
    cnt = 1;
    for toc_a in soup.select('.md-toc-h3 a'):
        dest = soup.select('a[name="{}"]'.format(toc_a['href'][1:]))[0]
        dest['id'] = 'h3-{}'.format(cnt)
        toc_a['href'] = '#h3-{}'.format(cnt)
        cnt += 1

    # BeautifulSoup会把 \3000 转成 À0 ，这里转回来
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup).replace('À0',r'\3000'))

if __name__ == '__main__':
    main(sys.argv)
