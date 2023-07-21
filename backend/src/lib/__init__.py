import os
import sys
import json

lib_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
src_path = os.path.abspath(os.path.join(lib_path, os.path.pardir))
backend_path = os.path.abspath(os.path.join(src_path, os.path.pardir))
conf_path = os.path.abspath(os.path.join(backend_path, 'conf'))
conf_file = os.path.abspath(os.path.join(conf_path, 'conf.json'))

if lib_path not in sys.path:
    sys.path.append(lib_path)
if conf_path not in sys.path:
    sys.path.append(conf_path)
    
# 리얼 서버 : "REAL", 스테이징 서버 : "STAGE", 개발 서버 : "DEV"
ENV = "DEV"

with open(conf_file, "rt") as f:
    conf = json.load(f)

MYSQL_CONNECTION = conf["mysql_connection"][ENV]
ENCRYTION_KEY = conf["encryption_key"][ENV]


