# coding=utf-8

import sys
import json
import base64
import time
import os
import subprocess
from pydub import AudioSegment
from pydub.silence import split_on_silence


# def getVideo():
#     video_path = './resource/video/test_a.mkv'
#     return video_path
#
#
# # 音轨分离
# def separateAudio():
#     video_path = getVideo()
#     audio_path = './resource/audio/test_a.mp3'
#     temp_path = './resource/audio/test_a.m4a'
#     command = 'ffmpeg -i ' + video_path \
#               + ' -vn -y -acodec copy '\
#               + temp_path
#     subprocess.call(command, shell=True)
#     command = 'ffmpeg -i ' + temp_path + ' -acodec libmp3lame -ab 128k ' + audio_path
#     subprocess.call(command, shell=True)
#     os.remove(temp_path)
#     return audio_path
#
#
# def match_target_amplitude(aChunk, target_dBFS):
#     ''' Normalize given audio mp3 '''
#     change_in_dBFS = target_dBFS - aChunk.dBFS
#     return aChunk.apply_gain(change_in_dBFS)
#
#
# def cutAudio():
#     # # 静音切割
#     # # audio_path = separateAudio()
#     # audio_path = './resource/audio/test_a.mp3'
#     # song = AudioSegment.from_mp3(audio_path)
#     # # split track where silence is 2 seconds or more and get chunks
#     # chunks = split_on_silence(song,
#     #                           # must be silent for at least 2 seconds or 2000 ms
#     #                           min_silence_len=50,
#     #                           # consider it silent if quieter than -16 dBFS
#     #                           # Adjust this per requirement
#     #                           silence_thresh=-10
#     #                           )
#     #
#     # # Process each mp3 per requirements
#     # for i, chunk in enumerate(chunks):
#     #     # Create 0.5 seconds silence mp3
#     #     silence_chunk = AudioSegment.silent(duration=500)
#     #     # Add 0.5 sec silence to beginning and end of audio mp3
#     #     audio_chunk = silence_chunk + chunk + silence_chunk
#     #     # Normalize each audio mp3
#     #     normalized_chunk = match_target_amplitude(audio_chunk, -20.0)
#     #     # Export audio mp3 with new bitrate
#     #     print("exporting mp3{0}.mp3".format(i))
#     #     normalized_chunk.export("../audio/mp3/{0}.mp3".format(i), bitrate='192k', format="mp3")
#     #
#     # mp3_path = './resource/audio/mp3'
#     # return mp3_path
#
#     # 线性切割
#     audio_path = separateAudio()
#     linear_trunk = AudioSegment.from_mp3(audio_path)  # 打开mp3文件
#     sound_time = round(linear_trunk.duration_seconds)
#     print(sound_time)
#     sound_len = sound_time // 30
#     for i in range(sound_len):
#         linear_trunk[i * 30000: (i+1) * 30000].export(
#             "./resource/audio/mp3/{0}.mp3".format(i), bitrate='192k', format="mp3")
#         print(i*30 / sound_time)
#         # 切割前17.5秒并覆盖保存
#
#     mp3_path = './resource/audio/mp3'
#     return mp3_path
#
# def convert(mp3_path, pcm_path):
#     error = subprocess.call(['ffmpeg', '-y',  '-i', mp3_path,
#                              '-acodec', 'pcm_s16le',
#                              '-f', 's16le',
#                              '-ac', '1',
#                              '-ar', '16000', pcm_path])
#     print(error)
#     if error:
#         return 0
#
#
# def mp32pcm():
#     mp3_home_path = cutAudio()
#     pcm_home_path = './resource/audio/pcm'
#     mp3_list = os.listdir(mp3_home_path)
#     count = 0
#     for item in mp3_list:
#         mp3_path = mp3_home_path + os.sep + item
#         pcm_path = pcm_home_path + os.sep + str(count) + '.pcm'
#         convert(mp3_path, pcm_path)
#         count += 1
#
#     return pcm_home_path


IS_PY3 = sys.version_info.major == 3

if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    timer = time.perf_counter
else:
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode
    if sys.platform == "win32":
        timer = time.clock
    else:
        # On most other platforms the best timer is time.time()
        timer = time.time

API_KEY = 'pRk3b9KxqMYG2tYyeQCl5Rzs'
SECRET_KEY = '5sLg6Tsus2YDTFqpfslPj5QTiIkQLjPK'



CUID = '123456PYTHON'
# 采样率
RATE = 16000  # 固定值

DEV_PID = 1737  # 1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型。根据文档填写PID，选择语言及识别模型
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有


class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode( 'utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        # print(SCOPE)
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        # print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

"""  TOKEN end """


def asrAudio(audio_file):
    token = fetch_token()
    # 文件格式
    FORMAT = audio_file[-3:]  # 文件后缀只支持 pcm/wav/amr

    with open(audio_file, 'rb') as speech_file:
        speech_data = speech_file.read()

    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % audio_file)
    speech = base64.b64encode(speech_data)
    if (IS_PY3):
        speech = str(speech, 'utf-8')
    params = {'dev_pid': DEV_PID,
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)
    # print post_data
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read()
        # print ("Request time cost %f" % (timer() - begin))
    except URLError as err:
        # print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    if (IS_PY3):
        result_str = str(result_str, 'utf-8')
    print(result_str)


if __name__ == '__main__':
    home_path = '../resource/audio/pcm'
    audio_list = os.listdir(home_path)
    for item in audio_list:
        # 需要识别的文件
        audio_file = home_path + os.sep + item  # 只支持 pcm/wav/amr
        asrAudio(audio_file)