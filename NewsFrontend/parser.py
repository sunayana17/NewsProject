import abc
import urllib.request
from xml.dom.minidom import parseString


class AbstractNewsParser(object, metaclass=abc.ABCMeta):
    def __init__(self):

        # Restrict creating abstract class instance
        if self.__class__ is AbstractNewsParser:
            raise TypeError('Abstract class cannot be instantiated')

    def print_latest_news(self):
        """ A Template method, returns 3 latest news for every
    news website """
        url = self.get_url()
        raw_content = self.get_raw_content(url)
        content = self.parse_content(raw_content)
        cropped = self.content_crop(content)

        for item in cropped:
            print('Title: ', item['title'])
            print('Content: ', item['content'])
            print('Link: ', item['link'])
            print('Published ', item['published'])
            print('Id: ', item['id'])

    @abc.abstractmethod
    def get_url(self):
        pass

    def get_raw_content(self, url):
        return urllib.request.urlopen(url).read()

    @abc.abstractmethod
    def parse_content(self, content):
        pass

    def content_crop(self, parsed_content, max_items=3):
        return parsed_content[:max_items]


class YahooNewsParser(AbstractNewsParser):
    def get_url(self):
        return 'https://news.yahoo.com/rss/'

    def parse_content(self, raw_content):
        yahoo_parsed_content = []
        dom = parseString(raw_content)

        for node in dom.getElementsByTagName('item'):
            yahoo_parsed_item = {}
            try:
                yahoo_parsed_item['title'] = node.getElementsByTagName('title')[0]. \
                    childNodes[0].nodeValue
            except IndexError:
                yahoo_parsed_item['title'] = None

            try:
                yahoo_parsed_item['content'] = node.getElementsByTagName('description')[0]. \
                    childNodes[0].nodeValue
            except IndexError:
                yahoo_parsed_item['content'] = None

            try:
                yahoo_parsed_item['link'] = node.getElementsByTagName('link')[0]. \
                    childNodes[0].nodeValue
            except IndexError:
                yahoo_parsed_item['link'] = None

            try:
                yahoo_parsed_item['id'] = node.getElementsByTagName('guid')[0]. \
                    childNodes[0].nodeValue
            except IndexError:
                yahoo_parsed_item['id'] = None

            try:
                yahoo_parsed_item['published'] = node.getElementsByTagName('pubDate')[0]. \
                    childNodes[0].nodeValue
            except IndexError:
                yahoo_parsed_item['published'] = None

            yahoo_parsed_content.append(yahoo_parsed_item)

        return yahoo_parsed_content


class GoogleNewsParser(AbstractNewsParser):
    def get_url(self):
        return 'https://news.google.com/atom'

    def parse_content(self, raw_content):
        google_parsed_content = []
        dom = parseString(raw_content)

        for node in dom.getElementsByTagName('entry'):
            google_parsed_item = {}

            try:
                google_parsed_item['title'] = node.getElementsByTagName('title')[0]. \
                    childNodes[0].nodeValue
            except IndexError:
                google_parsed_item['title'] = None

            try:
                google_parsed_item['content'] = node.getElementsByTagName('content')[0]. \
                    childNodes[0].nodeValue
            except IndexError:
                google_parsed_item['content'] = None

            try:
                google_parsed_item['link'] = node.getElementsByTagName('href')[0]. \
                    childNodes[0].nodeValue
            except IndexError:
                google_parsed_item['link'] = None

            try:
                google_parsed_item['id'] = node.getElementsByTagName('id')[0]. \
                    childNodes[0].nodeValue
            except IndexError:
                google_parsed_item['id'] = None

            try:
                google_parsed_item['published'] = node.getElementsByTagName('title')[0]. \
                    childNodes[0].nodeValue
            except IndexError:
                google_parsed_item['published'] = None

            google_parsed_content.append(google_parsed_item)

        return google_parsed_content


class NewsParser(object):
    def get_latest_news(self):
        yahoo = YahooNewsParser()
        print('Yahoo: \n', yahoo.print_latest_news())
        print()
        print()
        google = GoogleNewsParser()
        print('Google: \n', google.print_latest_news())


if __name__ == '__main__':
    newsParser = NewsParser()
    newsParser.get_latest_news()
