import os
import requests as rq
import json as js, re as rx
try:
    from fb_atm import Page as Pg
except:
    os.system('pip install fb-atm')

class scrape(Pg):
    def __init__(self):
        super().__init__()
    
    def post_id(self, _UrZ1):
        try:
            _TyX6 = rq.get(_UrZ1, headers=self.headers_web).text
            _PtN5 = rx.search('"post_id":"(.*?)"', str(_TyX6))
            return _PtN5.group(1) if _PtN5 else None
        except Exception:
            try:
                _PtN6 = rx.search('story_fbid=(.*?)&', str(_TyX6))
                return _PtN6.group(1) if _PtN6 else None
            except Exception:
                try:
                    _PtN7 = rx.search('"photo_id":"(.*?)"', str(_TyX6))
                    return _PtN6.group(1) if _PtN7 else None
                except Exception:
                    return None
       