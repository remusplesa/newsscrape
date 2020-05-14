from datetime import datetime
from typing import List


class Article:
    def __init__(
            self,
            source: str,
            publish_date: str,
            title: str,
            img_source: str,
            tldr: str,
            keywords: List[str],
            bias: float
    ):
        self.set_source(source)
        self.set_publish_date(publish_date)
        self.set_title(title)
        self.set_img_source(img_source)
        self.set_tldr(tldr)
        self.set_keywords(keywords)
        self.set_bias(bias)
        self.clicks = 0
        self.reports = 0
        self.hidden = False
        self.collection_date = int(datetime.now().strftime('%Y%m%d'))

    def get_source(self):
        return self.source

    def set_source(self, src):
        # TODO validate src
        if not src:
            raise ValueError('Should exist & be a good link / source')
        self.source = src

    def get_publish_date(self):
        return self.publish_date

    def set_publish_date(self, date):
        # TODO validate date ?!
        if not date:
            raise ValueError('Date value should exist & be ok')
        self.publish_date = date

    def get_title(self):
        return self.title

    def set_title(self, t):
        # TODO validate title
        if not t:
            raise ValueError('Title should exist & be ok')
        self.title = t

    def get_img_source(self):
        return self.img_source

    def set_img_source(self, img_src):
        # TODO validate img src
        if not img_src:
            self.img_source = ''
        else:
            self.img_source = img_src

    def get_tldr(self):
        return self.tldr

    def set_tldr(self, text):
        if not text:
            raise ValueError('Tldr should have a value')
        if len(text) > 258:
            raise Warning(
                'Due to to author rights you can\'t store & use \
                more than 255 characters')
        self.tldr = text

    def set_get_keywords(self):
        return self.keywords

    def set_keywords(self, kw: List):
        if not len(kw) > 0:
            raise ValueError('Keywords list should not be empty')
        for item in kw:
            if type(item) is not str:
                raise ValueError('Keywords should be of type string')
        self.keywords = kw

    def get_bias(self):
        return self.bias

    def set_bias(self, value):
        if not value:
            raise ValueError('Bias should exist')
        if value > 1 or value <= 0:
            raise ValueError('Bias value should be in (0, 1]')
        self.bias = value
