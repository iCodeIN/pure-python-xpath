import bs4 as bs
import requests

from xpath_bs import XPATH

if __name__ == '__main__':

    # do HTTP GET request
    req = requests.get('http://www.unsplash.com')

    # get HTML string
    html_string = req.content

    # build bs document
    doc = bs.BeautifulSoup(html_string, 'html.parser')

    # apply xpath
    val = XPATH.xpath("//img[@src > 'https://images.unsplash' and @src < 'https://j']/@src", doc)

    for x in val:
        print(x)