import asr_audio
from concurrent.futures import ThreadPoolExecutor
import os
import functools


# 策略模式将因为并行而乱序的字幕重新排序
def sortStrategy(x, y):
    if x[0] < y[0]:
        return -1
    else:
        return 1


def asrAudio(audio_file):
    return audio_file


class AsrPool:
    def __init__(self, company, way):
        # 创建一个最大可容纳2个task的线程池
        self.pool = ThreadPoolExecutor(max_workers=200)
        self.company = company
        self.way = way
        self.result_list = []

    def beginRecongition(self, audio_file, key):
        result = asr_audio.asr_recognition(self.company, self.way, audio_file)
        self.result_list.append((key, result))

    def asrRun(self, pcm_dir):
        audio_list = os.listdir(pcm_dir)
        print(len(audio_list))
        count = 0
        for item in audio_list:
            # 需要识别的文件
            audio_file = pcm_dir + os.sep + item  # 只支持 pcm/wav/amr
            self.pool.submit(self.beginRecongition, audio_file, count)
            count += 1

    def getResultList(self, subtitle_num):
        print(str(round(len(self.result_list) / subtitle_num * 100)) + '%')
        if len(self.result_list) == subtitle_num:
            return sorted(self.result_list, key=functools.cmp_to_key(sortStrategy))
        else:
            return ''


# if __name__ == '__main__':
#     asr_pool = AsrPool('baidu', 'json')
#     asr_pool.asrRun('')
#     while True:
#         result_list = asr_pool.getResultList(30)
#         if result_list != '':
#             break