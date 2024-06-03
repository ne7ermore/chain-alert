import logging
from logging.handlers import RotatingFileHandler

import uuid
import json

import requests

from secret import *

symbols = '["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","DOGEUSDT","ADAUSDT","SHIBUSDT","AVAXUSDT","LINKUSDT","DOTUSDT","NEARUSDT","MATICUSDT","PEPEUSDT","UNIUSDT","FETUSDT","APTUSDT","RNDRUSDT","HBARUSDT","IMXUSDT","ATOMUSDT","FILUSDT","WIFUSDT","ARBUSDT","TAOUSDT","OPUSDT","ARUSDT","MKRUSDT","SUIUSDT","INJUSDT","THETAUSDT","FTMUSDT","RUNEUSDT","LDOUSDT","TIAUSDT","PYTHUSDT","SEIUSDT","AAVEUSDT","ALGOUSDT","GALAUSDT","JUPUSDT","STRKUSDT","FLOWUSDT","ENAUSDT","AXSUSDT","WUSDT","PENDLEUSDT","SANDUSDT","SNXUSDT","BOMEUSDT","MINAUSDT","ORDIUSDT","DYMUSDT","RDNTUSDT","CKBUSDT","AEVOUSDT","LPTUSDT","AXLUSDT","ETHFIUSDT","DYDXUSDT","ZRXUSDT","METISUSDT","SSVUSDT","JTOUSDT","IDUSDT","PEOPLEUSDT","ALTUSDT","ARKMUSDT","COSUSDT","AGLDUSDT","BEAMXUSDT","RIFUSDT","POLYXUSDT","BLURUSDT","STXUSDT","DUSKUSDT","SYSUSDT","SAGAUSDT","CREAMUSDT","BBUSDT","TNSRUSDT","ENSUSDT"]'

RATIO = 2

BIAN_API = "https://fapi.binance.com"

def configure_logger(file_name):
    """配置日志记录器"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    
    # 创建 RotatingFileHandler 实例，设置日志文件的最大大小和最大数量
    handler = RotatingFileHandler(file_name, maxBytes=10*1024*1024, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

def sned_alerts_to_dc(logger, content, channel_id):
    msg = {
        "content": content,
        "nonce": str(uuid.uuid4())[:25],
        "tts": False
    }
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'    

    headers = {
        "Authorization": authorizations["nevermore"],
        "Content-Type": "application/json",
        "User-Agent": ""
    }

    logger.info(f"channel: {channel_id}")
    try:
        res = requests.post(url=url, headers=headers, data=json.dumps(msg))
        res.raise_for_status()  
    except requests.RequestException as e:
        logger.error(e)