from bs4 import BeautifulSoup
import requests, json, codecs

from .error import ErrorType

class AllAnime:
    def __init__(self):
        self.base_url = 'https://ani.gamer.com.tw/animeList.php?'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }
        self.result = []
        self.json_data = json.load(codecs.open("./anigamerpy/json/allanime_data.json", "r", "utf-8"))
    
    def id2name(self, type:str, id:int):
        return self.json_data[type][id]["name"]
    
    def combine_url(self, tags:list = [], category:int = None, target:int = None, sort:int = None, page:int = None):
        if tags != []:
            self.base_url += "tags="
            if len(tags) == 1:
                type_name = AllAnime().id2name("tags", tags[0])
                self.base_url += "{}&".format(type_name)
            elif len(tags) >= 2 and len(tags) <= 5:
                for i in range(len(tags)):
                    type_name = AllAnime().id2name("tags", tags[i])
                    self.base_url += "{}%2C".format(type_name)
                    if i == len(tags) - 1:
                        self.base_url = self.base_url[:-3] + "&"
            else:
                return ErrorType.over_limit()
        if category != None:
            if category in [0, 1, 2, 3, 4]:
                self.base_url += "category="
                type_name = AllAnime().id2name("category", category)
                self.base_url += "{}&".format(type_name)
            else:
                return ErrorType.no_limit()
        if target != None:
            if target in [0, 1, 2]:
                self.base_url += "target="
                type_name = AllAnime().id2name("target", target)
                self.base_url += "{}&".format(type_name)
            else:
                return ErrorType.no_limit()
        if sort != None:
            if sort == 1:
                self.base_url += "sort={}&".format(str(sort))
            elif sort == 2:
                self.base_url += "sort={}&".format(str(sort))
            else:
                return ErrorType.no_limit()
        if page != None:
            self.base_url += "page={}".format(str(page))
        return AllAnime().get_anime(url=self.base_url)
    
    def get_anime(self, url):
        req = requests.get(url, headers=self.header)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'html.parser')
            all_anime_items = soup.select_one('.animate-theme-list > .theme-list-block')
            anime_items = all_anime_items.select('.theme-list-main')
            if anime_items == '':
                return ErrorType.no_result()
            for anime_item in anime_items:
                anime_name = anime_item.select_one('.theme-name').text.strip()
                anime_watch_number = anime_item.select_one('.show-view-number > p').text.strip()
                anime_episode = anime_item.select_one('.theme-number').text.strip()
                anime_year = anime_item.select_one('.theme-time').text.strip()
                anime_href = anime_item.get('href')
                anime_pic = anime_item.select_one('.theme-img')['data-src']
                anime_tags = []
                if anime_item.select_one('.color-bilingual') != None:
                    anime_both_tag = anime_item.select_one('.color-bilingual').text.strip()
                    anime_tags.append(anime_both_tag)
                else:
                    pass
                if anime_item.select_one('.color-paid') != None:
                    anime_paid_tag = anime_item.select_one('.color-paid').text.strip()
                    anime_tags.append(anime_paid_tag)
                else:
                    pass
                if anime_item.select_one('.color-R18') != None:
                    anime_age_tag = anime_item.select_one('.color-R18').text.strip()
                    anime_tags.append(anime_age_tag)
                else:
                    pass
                self.alldata = {
                    'name': anime_name,
                    'watch_count': anime_watch_number,
                    'episode': anime_episode,
                    'years': anime_year,
                    'href': anime_href,
                    'image': anime_pic,
                    'tags': anime_tags
                }
                self.result.append(self.alldata)
        else:
            return ErrorType.status_error(str(req.status_code))
        return self.result
    
class AllAnimeResponse:
    def __init__(self, tags:list = [], category:int = None, target:int = None, sort:int = None, page:int = None):
        self.data = AllAnime().combine_url(tags=tags, category=category, target=target, sort=sort, page=page)