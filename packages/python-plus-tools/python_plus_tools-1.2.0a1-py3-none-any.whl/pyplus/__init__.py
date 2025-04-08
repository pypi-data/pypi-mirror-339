'''
The python Plus - Pyplus
================
the python's plus library.\n
'''

from .tools.update import *
from .tools.update import get_update_from_toml, upload
from . import science ,tools
from site import getsitepackages

__all__=["science" ,"tools" ,
         "ALL" ,"NEW" ,"WILL" ,
         "get_update" ,"get_version_update_time" ,"get_news_update_time" ,"get_new" ,"get_all" ,"get_will" ,"get_version",
        ]

update_data = get_update_from_toml(getsitepackages()[1] + "\\pyplus\\update.toml", write_to_info=False)['release']['main']

upload(update_data['version'], update_data['update_info'], update_data['update_time'])