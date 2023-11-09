from news_feed.models import Topic


def create_site():
    print("Function create_site() needs implementation!")
    pass


def create_topic(name, description):
    c = Topic.objects.create(name=name, description=description)
    return c
