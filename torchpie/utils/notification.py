import requests
from typing import List, Dict, Union


def notify_by_wechat(sckey: Union[str, List[str]], text: str, desp: str = ''):
    '''
    desp will no be shown now.
    '''
    if type(sckey) == str:
        sckey = [sckey]

    data = {
        'text': text,
        'desp': desp,
    }

    for key in sckey:
        requests.post(f'https://sc.ftqq.com/{sckey}.send', data=data)
