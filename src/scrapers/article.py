from datetime import datetime

class Article:
    def __init__(self, source: str, publish_date: str, title: str, img_source: str, tldr: str, bias: float):
        self.source = source
        self.publish_date = publish_date
        self.title = title
        self.img_source = img_source
        self.tldr = tldr
        self.bias = bias
        self.clicks = 0
        self.reports = 0
        self.hidden = False
        self.collection_date = datetime.now().strftime('%d%m%Y')
