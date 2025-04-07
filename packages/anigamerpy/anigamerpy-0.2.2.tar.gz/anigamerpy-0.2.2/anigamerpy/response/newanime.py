from bs4 import BeautifulSoup
import requests

from .error import ErrorType

class NewAnime:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
        }
        self.base_url = 'https://ani.gamer.com.tw/'
        self.result = []
    
    def get_new_anime(self):
        req = requests.get(self.base_url, headers=self.headers)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'html.parser')
            new_anime_item = soup.select_one('.timeline-ver > .newanime-block')
            anime_items = new_anime_item.select('.newanime-date-area:not(.premium-block)') #移除付費比例
            for anime_item in anime_items:
                anime_name = anime_item.select_one('.anime-name').text.strip()
                anime_watch_number = anime_item.select_one('.anime-watch-number > p').text.strip()
                anime_episode = anime_item.select_one('.anime-episode').text.strip()
                anime_href = anime_item.select_one('a.anime-card-block').get('href')
                anime_pic = anime_item.select_one('.anime-blocker > img')['data-src']
                self.ndata = {
                    'name': anime_name,
                    'watch_count': anime_watch_number,
                    'episode': anime_episode,
                    'href': anime_href,
                    'image': anime_pic
                }
                self.result.append(self.ndata)
            if anime_name == '':
                return ErrorType.no_result()
        else:
            return ErrorType.status_error(str(req.status_code))
        return self.result
    
class NewAnimeResponse:
    def __init__(self):
        self.data = NewAnime().get_new_anime()