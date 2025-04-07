from bs4 import BeautifulSoup
import requests

from .error import ErrorType

class Search:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
        }
        self.base_url = 'https://ani.gamer.com.tw/search.php?keyword='
        self.result = []
    
    def search_anime(self, keyword: str):
        req = requests.get(self.base_url + keyword, headers=self.headers)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'html.parser')
            search_anime_item = soup.select_one('.animate-theme-list > .theme-list-block')
            search_items = search_anime_item.select('.theme-list-main')
            for search_item in search_items:
                anime_name = search_item.select_one('.theme-name').text.strip()
                anime_watch_number = search_item.select_one('.show-view-number > p').text.strip()
                anime_episode = search_item.select_one('.theme-number').text.strip()
                anime_year = search_item.select_one('.theme-time').text.strip()
                anime_href = search_item.get('href')
                anime_pic = search_item.select_one('.theme-img')['data-src']
                anime_tags = []
                if search_item.select_one('.color-bilingual') != None:
                    anime_both_tag = search_item.select_one('.color-bilingual').text.strip()
                    anime_tags.append(anime_both_tag)
                else:
                    pass
                if search_item.select_one('.color-paid') != None:
                    anime_paid_tag = search_item.select_one('.color-paid').text.strip()
                    anime_tags.append(anime_paid_tag)
                else:
                    pass
                if search_item.select_one('.color-R18') != None:
                    anime_age_tag = search_item.select_one('.color-R18').text.strip()
                    anime_tags.append(anime_age_tag)
                else:
                    pass
                self.sdata = {
                    'name': anime_name,
                    'watch_count': anime_watch_number,
                    'episode': anime_episode,
                    'years': anime_year,
                    'href': anime_href,
                    'image': anime_pic,
                    'tags': anime_tags
                }
                self.result.append(self.sdata)
            if anime_name == '':
                return ErrorType.no_result()
        else:
            return ErrorType.status_error(str(req.status_code))
        return self.result
    
class SearchResponse:
    def __init__(self, keyword: str):
        self.data = Search().search_anime(keyword=keyword)