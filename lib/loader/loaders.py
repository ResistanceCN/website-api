from .user import UserLoader
from .article import ArticleLoader
from .user_articles import UserArticlesLoader


class Loaders:
    def __init__(self):
        self.user = UserLoader()
        self.article = ArticleLoader()
        self.user_articles = UserArticlesLoader()
