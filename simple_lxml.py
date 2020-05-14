
#
# from lxml import html
#
#
# dom = html.fromstring('''
# <html>
#     <head></head>
#     <body>
#         <div title="buyer-name">William Sanchez</div>
#         <span class="item-price">$299.95</span>
#         <div num=1 attr=7>
#             Div #1 text
#             <div num=2 attr=7>
#                 Div #2 text
#                 <a href="http://google.com/">Google</a>
#             </div>
#         </div>
#         <span id=spanid>SPAM</span>
#     </body>
# </html>
# ''')
#
# print('dom.text: ', dom.text)
# print('dom.text_content', dom.text_content())
#
# divs = dom.cssselect('div')
# print('list of divs: ', divs)
# for d in divs:
#     print('div text: ', d.text)
#
# by_id = dom.get_element_by_id(id="spanid")
# print('html of id element: ', html.tostring(by_id))
#
# divs = dom.cssselect('div[num="2"],div[attr="7"]')
# print('multi divs: ', divs)
# for d in divs:
#     print('div with num="2"', d.text)
#
# divs = dom.cssselect('div[num="2"] > a')
# print('', divs)
# for d in divs:
#     print('link in div with num="2"', d.text)
#
#
# exit()


# third-party
import requests
from lxml import html


r = requests.get('http://frs24.ru/st/vitaminy-v-ovoschah-i-fruktah-tablica/')
print('response: ', r.status_code, 'encoding: ', r.encoding)
r.encoding = 'cp1251'
dom = html.fromstring(r.text)


# get html of element with id
try:
    print(html.tostring(dom.get_element_by_id(id="noname")))
except Exception as e0:
    print('get_element_by_id: ', e0)


# list all links on page
for l in dom.iterlinks():
    print(l)


# find all tables and all rows
tbls = dom.cssselect('table[class=skl]')
for t in tbls:
    for row in t.cssselect('TR'):
        print([td.text_content() for td in row.cssselect('TD')])

data = []
colnames = []
for t in tbls:
    for row in t.cssselect('TR'):
        if not colnames:
            colnames = [td.text_content() for td in row.cssselect('TD')]
            continue
        d = dict([
            (colnames[i], td.text_content()) for i, td in enumerate(
                row.cssselect('TD'))
        ])
        data.append(d)

print(colnames)
print(data)



# https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.read_html.html
# tables = pandas.read_html('http://frs24.ru/st/vitaminy-v-ovoschah-i-fruktah-tablica/', header=0)