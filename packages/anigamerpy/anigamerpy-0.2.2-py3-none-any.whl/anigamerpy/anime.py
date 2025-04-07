from .response import searchanime, newanime, allanime, myanime

class Anime:
    def __init__(self):
        pass

    def search_anime(self, keyword: str):
        return searchanime.SearchResponse(keyword=keyword)
    
    def new_anime(self):
        return newanime.NewAnimeResponse()
    
    def all_anime(self, tags:list = [], category:int = None, target:int = None, sort:int = None, page:int = None):
        return allanime.AllAnimeResponse(tags=tags, category=category, target=target, sort=sort, page=page)
    
    def my_anime(self, cookie:str = None, username:str = None, password:str = None, sort:int = None):
        if cookie != None and username == None and password == None:
            return myanime.MyAnime().loggin_by_cookie(cookie=cookie, sort=sort)
        elif cookie == None and username != None and password != None:
            return myanime.MyAnime().loggin_by_username_and_password(username=username, password=password, sort=sort)
        else:
            return 'You can only use cookie or username and password.(Choose one method to loggin)'