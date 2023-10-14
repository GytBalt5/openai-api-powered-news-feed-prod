from news_feed.models import Category


def create_site():
    print("Function create_site() needs implementation!")
    pass


def create_category(name, description):
    c = Category.objects.create(name=name, description=description)
    return c
