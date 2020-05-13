from datetime import datetime
from typing import List

class Article:
    def __init__(self, source: str, publish_date: str, title: str, img_source: str, tldr: str, keywords: List[str], bias: float):
        self.source = source
        self.publish_date = publish_date
        self.title = title
        self.img_source = img_source
        self.tldr = tldr
        self.keywords = keywords
        self.bias = bias
        self.clicks = 0
        self.reports = 0
        self.hidden = False
        self.collection_date = int(datetime.now().strftime('%Y%m%d'))

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, src):
        # TODO validate src
        if not src : raise ValueError('Should exist & be a good link / source')
        self._source = src

    @property
    def publish_date(self):
        return self._publish_date
    
    @publish_date.setter
    def publish_date(self, date):
        # TODO validate date ?!
        if not date: raise ValueError('Date value should exist & be ok')
        self._publish_date = date

    @property
    def title(self):  
        return self._title
    
    @title.setter 
    def title(self, t):
        # TODO validate title
        if not t: raise ValueError('Title should exist & be ok')
        self._title = t

    @property
    def img_source(self):
        return self._img_source

    @img_source.setter
    def img_source(self, img_src):
        # TODO validate img src
        if not img_src: raise ValueError('Image source should exist & be ok')
        self._img_source = img_src

    @property
    def tldr(self):
        return self._tldr 
    
    @tldr.setter 
    def tldr(self, text):
        if not text: raise ValueError('Tldr should have a value')
        if len(text) > 258:
            raise Warning('Due to to author rights you cant store & use more than 255 characters')
        self._tldr = text

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, kw: List):
        if not len(kw) > 0: raise ValueError('Keywords list should not be empty')
        for item in kw: 
            if type(item) is not str: 
                raise ValueError('Keywords should be of type string')
        self._keywords = kw

    @property
    def bias(self):
        return self._bias 

    @bias.setter 
    def bias(self, value):
        if not value: raise ValueError('Bias should exist')
        if value > 1 or value <= 0: raise ValueError('Bias value should be in (0, 1]')
        self._bias = value