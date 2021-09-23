from bs4 import BeautifulSoup

import re
import requests

illegalParagraphClasses = {'asbox-body'}

startURL = "https://en.wikipedia.org/wiki/Advanced_Television_Systems_Committee"

def getValidLinks(seeAlso=True):
    response = requests.get(startURL)
    soup = BeautifulSoup(response.text, 'html.parser')

    allAnchors = set()

    bodyText = soup.find('div', attrs={"class": "mw-parser-output"})

    # Main body links
    paragraphs = bodyText.findAll('p')
    paragraphs = [p for p in bodyText.findAll('p') if not (p.has_attr('class') and set(p['class']).issubset(illegalParagraphClasses))]

    for p in paragraphs:
        anchors = p.findAll('a')

        anchors = [a['href'] for a in anchors if a['href'].find('#cite') == -1]
        allAnchors = allAnchors.union(set(anchors))
    
    # See Also links
    if seeAlso:
        seeAlsoSpan = bodyText.find('span', text="See also")
        seeAlso = seeAlsoSpan.parent
        seeAlsoList = seeAlso.findNextSibling().findAll('li')
        for li in seeAlsoList:
            anchors = li.findAll('a')

            anchors = [a['href'] for a in anchors if a['href'].find('#cite') == -1]
            allAnchors = allAnchors.union(set(anchors))

    # Navboxes
    navboxes = bodyText.findAll('div', attrs={"class": "navbox"})
    # print(navboxes)






    print(allAnchors)

def main():
    getValidLinks()

if __name__ == "__main__":
    main()