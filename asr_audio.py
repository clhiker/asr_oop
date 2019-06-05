#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import hashlib
import urllib.request
import urllib.parse
import json
import base64
import time
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
import const
timer = time.perf_counter


class DemoError(Exception):
    pass


class Asr:

    def __init__(self, asr_factory=None):
        """asr_factory is our abstract factory.  We can set it at will."""
        self.asr_factory = asr_factory

    def getProduct(self, asr_way=''):
        """Creates and shows a asr using the abstract factory"""
        return self.asr_factory.getAsrProduct(asr_way)


class BaiduAsr:
    def __init__(self):
        pass
    def fetchToken(self):
        params = {'grant_type': 'client_credentials',
                  'client_id': const.API_KEY,
                  'client_secret': const.SECRET_KEY}
        post_data = urlencode(params)
        post_data = post_data.encode('utf-8')
        req = Request(const.TOKEN_URL, post_data)
        try:
            f = urlopen(req)
            result_str = f.read()
        except URLError as err:
            print('token http response http code : ' + str(err.code))
            result_str = err.read()

        result_str = result_str.decode()

        result = json.loads(result_str)
        if 'access_token' in result.keys() and 'scope' in result.keys():
            # print(SCOPE)
            if const.SCOPE and (const.SCOPE not in result['scope'].split(' ')):  # SCOPE = False 忽略检查
                raise DemoError('scope is not correct')
            # print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
            return result['access_token']
        else:
            raise DemoError(
                'MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

# Stuff that our factory makes
class BaiduAsrJson(BaiduAsr):
    def recognition(self, audio_file):        
        # 文件格式
        FORMAT = audio_file[-3:]  # 文件后缀只支持 pcm/wav/amr
        token = self.fetchToken()

        # speech_data = []
        with open(audio_file, 'rb') as speech_file:
            speech_data = speech_file.read()

        length = len(speech_data)
        if length == 0:
            raise DemoError('file %s length read 0 bytes' % audio_file)
        speech = base64.b64encode(speech_data)

        speech = str(speech, 'utf-8')
        params = {'dev_pid': const.DEV_PID,
                  'format': FORMAT,
                  'rate': const.RATE,
                  'token': token,
                  'cuid': const.CUID,
                  'channel': 1,
                  'speech': speech,
                  'len': length
                  }
        post_data = json.dumps(params, sort_keys=False)
        req = Request(const.ASR_URL, post_data.encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        try:
            begin = time.perf_counter()
            f = urlopen(req)
            result_str = f.read()
            # print ("Request time cost %f" % (timer() - begin))
        except URLError as err:
            # print('asr http response http code : ' + str(err.code))
            result_str = err.read()

        result_str = str(result_str, 'utf-8')

        result = result_str.split(',')
        if result[1][11:] == 'success."':
            text = result_str[result_str.find('[') + 2 : result_str.find(']') - 1]
            print(text)
            return text
        else:
            return ''

    def __str__(self):
        pass


class BaiduAsrRaw(BaiduAsr):

    def recognition(self, audio_file):
        # 文件格式
        FORMAT = audio_file[-3:]  # 文件后缀只支持 pcm/wav/amr
        token = self.fetchToken()

        """
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        opener = urllib2.build_opener(httpHandler)
        urllib2.install_opener(opener)
        """

        speech_data = []
        with open(audio_file, 'rb') as speech_file:
            speech_data = speech_file.read()
        length = len(speech_data)
        if length == 0:
            raise DemoError('file %s length read 0 bytes' % audio_file)

        params = {'cuid': const.CUID, 'token': token, 'dev_pid': const.DEV_PID}
        params_query = urlencode(params)

        headers = {
            'Content-Type': 'audio/' + FORMAT + '; rate=' + str(const.RATE),
            'Content-Length': length
        }

        url = const.ASR_URL + "?" + params_query
        # print("url is", url)
        # print("header is", headers)
        # print post_data
        req = Request(const.ASR_URL + "?" + params_query, speech_data, headers)
        try:
            begin = timer()
            f = urlopen(req)
            result_str = f.read()
            # print("Request time cost %f" % (timer() - begin))
        except  URLError as err:
            print('asr http response http code : ' + str(err.code))
            result_str = err.read()

        result_str = str(result_str, 'utf-8')

        result = result_str.split(',')
        if result[1][11:] == 'success."':
            text = result_str[result_str.find('[') + 2: result_str.find(']') - 1]
            # print(text)
            return text

    def __str__(self):
        pass


class XunFeiAsr:

    def recognition(self, audio_file):
        f = open(audio_file, 'rb')  # rb表示二进制格式只读打开文件
        file_content = f.read()
        # file_content 是二进制内容，bytes类型
        # 由于Python的字符串类型是str，在内存中以Unicode表示，一个字符对应若干个字节。
        # 如果要在网络上传输，或者保存到磁盘上，就需要把str变为以字节为单位的bytes
        # 以Unicode表示的str通过encode()方法可以编码为指定的bytes
        base64_audio = base64.b64encode(file_content)  # base64.b64encode()参数是bytes类型，返回也是bytes类型
        body = urllib.parse.urlencode({'audio': base64_audio})

        url = const.URL
        api_key = const.XUNFEI_API_KEY
        param = {"engine_type":const.ENGINE_TYPE , "aue":const.AUE }

        x_appid = const.X_APPID
        x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))  # 改('''')
        # 这是3.x的用法，因为3.x中字符都为unicode编码，而b64encode函数的参数为byte类型，
        # 所以必须先转码为utf-8的bytes
        x_param = str(x_param, 'utf-8')

        x_time = int(int(round(time.time() * 1000)) / 1000)
        x_checksum = hashlib.md5((api_key + str(x_time) + x_param).encode('utf-8')).hexdigest()  # 改
        x_header = {'X-Appid': x_appid,
                    'X-CurTime': x_time,
                    'X-Param': x_param,
                    'X-CheckSum': x_checksum}
        # 不要忘记url = ??, data = ??, headers = ??, method = ?? 中的“ = ”，这是python3
        req = urllib.request.Request(url=url, data=body.encode('utf-8'), headers=x_header, method='POST')
        result = urllib.request.urlopen(req)
        result = result.read().decode('utf-8')
        result = eval(result)
        result = result['data']
        return result

    def __str__(self):
        pass


# Factory classes
class BaiduAsrFactory:
    def getAsrProduct(self, asr_way):
        if asr_way == 'json':
            return BaiduAsrJson()
        if asr_way == 'raw':
            return BaiduAsrRaw()


class XunFeiAsrFactory:
    def getAsrProduct(self, asr_way=''):
        return XunFeiAsr()


# Create the proper family
def get_factory(factory):
    """Let's be dynamic!"""
    if factory == 'baidu':
        return BaiduAsrFactory()
    if factory == 'xunfei':
        return XunFeiAsrFactory()


def asr_recognition(company, way, resource):
    asr = Asr(get_factory(company))
    asr_product = asr.getProduct(way)
    return asr_product.recognition(resource)


if __name__ == '__main__':
    result = asr_recognition('xunfei', '', 'temp/pcm/test_b/1.pcm')
    print(result)
# are y'all readyI can't hear yousame