# # baidu
# API_KEY = 'pRk3b9KxqMYG2tYyeQCl5Rzs'
# SECRET_KEY = '5sLg6Tsus2YDTFqpfslPj5QTiIkQLjPK'
# CUID = '123456PYTHON'
# # 采样率
# RATE = 16000  # 固定值
# # 免费版
# # 1537 表示识别普通话，使用输入法模型。
# # 1536表示识别普通话，使用搜索模型。根据文档填写PID，选择语言及识别模型
# # 1737 是英语
# DEV_PID = 1737
# ASR_URL = 'http://vop.baidu.com/server_api'
# SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有
# TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
#
#
# # xunfei
# XUNFEI_API_KEY = 'eb61a04dc978469e8a422f308680ffe0'
# URL = 'http://api.xfyun.cn/v1/service/v1/iat'
# ENGINE_TYPE = "sms-en16k"
# AUE = "raw"
# X_APPID = '5cd56b32'

import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
BAIDU_CONFIG = 'baidu'
# baidu
API_KEY     = config.get(BAIDU_CONFIG, 'API_KEY')
SECRET_KEY  = config.get(BAIDU_CONFIG, 'SECRET_KEY')
CUID        = config.get(BAIDU_CONFIG, 'CUID')
# 采样率
RATE        = int(config.get(BAIDU_CONFIG, 'RATE'))
# 免费版
# 1537 表示识别普通话，使用输入法模型。
# 1536表示识别普通话，使用搜索模型。根据文档填写PID，选择语言及识别模型
# 1737 是英语
DEV_PID     = int(config.get(BAIDU_CONFIG, 'DEV_PID'))
ASR_URL     = config.get(BAIDU_CONFIG, 'ASR_URL')
SCOPE       = config.get(BAIDU_CONFIG, 'SCOPE')
TOKEN_URL   = config.get(BAIDU_CONFIG, 'TOKEN_URL')


# xunfei
XUNFEI_CONFIG   = 'xunfei'
XUNFEI_API_KEY  = config.get(XUNFEI_CONFIG, 'XUNFEI_API_KEY')
URL             = config.get(XUNFEI_CONFIG, 'URL')
ENGINE_TYPE     = config.get(XUNFEI_CONFIG, 'ENGINE_TYPE')
AUE             = config.get(XUNFEI_CONFIG, 'AUE')
X_APPID         = config.get(XUNFEI_CONFIG, 'X_APPID')
