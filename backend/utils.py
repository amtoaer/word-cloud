import collections
import logging
import requests
from wordcloud import WordCloud
from jieba import lcut, setLogLevel
from bs4 import BeautifulSoup


def request(URLs: tuple) -> str:
    headers = {
        'User Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    content_all = ''
    for URL in URLs:
        try:
            resp = requests.get(url=URL, headers=headers)
            text = resp.text
            # Speculate coding
            if resp.encoding == 'ISO-8859-1':
                encodings = requests.utils.get_encodings_from_content(
                    text)
                if encodings:
                    encoding = encodings[0]
                    text = resp.content.decode(encoding=encoding)
            soup = BeautifulSoup(text, 'html.parser')
            for hyperlink in soup.find_all('a'):
                try:
                    content_all += hyperlink.string
                except:
                    continue
        except:
            print('{}请求失败'.format(URL))
    return content_all.replace('\r', '').replace('\n', '').replace('\u3000', '')


def generate_image_and_top10(content: str) -> tuple:
    setLogLevel(logging.CRITICAL)
    word_list = [item for item in lcut(content) if len(item) > 1]
    word_count = collections.Counter(word_list)
    top_10 = word_count.most_common(10)
    word_cloud = WordCloud(
        font_path='./font/NotoSansCJKsc-Regular.otf', background_color='white')
    word_cloud.generate_from_frequencies(word_count)
    return (word_cloud.to_image(), top_10)


def handleURLs(URLs: tuple) -> tuple:
    return generate_image_and_top10(request(URLs))
