#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
"""
设计模式——命令模式
命令模式(Command Pattern):将请求封装成对象，从而使可用不同的请求对客户进行参数化；
对请求排队或记录请求日志，以及支持可撤消的操作.
"""

import ergodic_video
import cut_audio
import asr_threadpool
import ffmpeg_tools
import os
import time
import shutil


# 命令类
class Command(object):
    def __init__(self, receiver):
        self.receiver = receiver


# 执行接收者的操作
class ConcreteCommand1(Command):
    def execute(self):
        self.receiver.getVideo()


class ConcreteCommand2(Command):
    def execute(self):
        self.receiver.video2Audio()


class ConcreteCommand3(Command):
    def execute(self):
        self.receiver.cutAudio()


class ConcreteCommand4(Command):
    def execute(self):
        self.receiver.normalizateAudio()


class ConcreteCommand5(Command):
    def execute(self):
        self.receiver.asrAudio()


class ConcreteCommand6(Command):
    def execute(self):
        self.receiver.clearTemp()


# 接收命令
class Invoker(object):

    def __init__(self):
        self.command = ''

    def excutecommand(self, command):
        command.execute()


# 具体执行类
class Receiver(object):
    def __init__(self, video_path, args):
        self.video_path = video_path
        self.args = args
        self.video_list = []
        self.audio_list = []
        self.audio_path = 'temp'
        self.mp3_path = 'temp/mp3'
        self.mp3_dir_list = []
        self.pcm_path = 'temp/pcm'
        self.tools = ffmpeg_tools.Tools()
        self.subtitle_list = []
        self.initTempPath()

    def initTempPath(self):
        if not os.path.exists(self.audio_path):
            os.mkdir(self.audio_path)
        if not os.path.exists(self.mp3_path):
            os.mkdir(self.mp3_path)
        if not os.path.exists(self.pcm_path):
            os.mkdir(self.pcm_path)

    def getVideo(self):
        print("执行请求1")
        read_file = ergodic_video.VideoList()
        read_file.readArgs(self.video_path, self.args)
        self.video_list = read_file.getVideoList()
        self.subtitle_list = read_file.getSubtitleList()

    def video2Audio(self):
        print("执行请求2")
        for item in self.video_list:
            video_name = item[item.rfind(os.sep) + 1: item.find('.')]
            audio_path = item[: item.rfind(os.sep)] + os.sep + video_name + '.mp3'
            if os.path.exists(audio_path):
                os.remove(audio_path)
            self.audio_list.append(audio_path)
            self.tools.separateAudio(item, audio_path)

    def cutAudio(self):
        print("执行请求3")
        factory = cut_audio.CutFactory()
        key = 0

        for item in self.audio_list:
            name = item[item.rfind(os.sep) + 1: item.find('.')]
            mp3_file = item
            mp3_name = name
            mp3_dir = self.mp3_path + os.sep + mp3_name
            if not os.path.exists(mp3_dir):
                os.mkdir(mp3_dir)
            cut_product = factory.getCutProduct(mp3_file, mp3_dir, 'linear')
            cut_product.cut()
            self.subtitle_list[key].append(cut_product.getCutTimeList())
            self.mp3_dir_list.append(mp3_dir)
            key += 1

    def normalizateAudio(self):
        print("执行请求4")
        for mp3_dir_path in self.mp3_dir_list:
            dir_name = mp3_dir_path[mp3_dir_path.rfind(os.sep) + 1 :]
            pcm_dir = self.pcm_path + os.sep + dir_name
            if not os.path.exists(pcm_dir):
                os.mkdir(pcm_dir)

            mp3_list = os.listdir(mp3_dir_path)
            for item in mp3_list:
                file_name = item[: item.find('.')]
                mp3_path = mp3_dir_path + os.sep + item
                pcm_path = pcm_dir + os.sep + file_name + '.pcm'
                self.tools.mp32pcm(mp3_path, pcm_path)

    def asrAudio(self):
        print("执行请求5")
        key = 0
        pcm_list = os.listdir(self.pcm_path)
        for item in pcm_list:
            pcm_dir = self.pcm_path + os.sep + item
            asr_pool = asr_threadpool.AsrPool('baidu', 'json')
            asr_pool.asrRun(pcm_dir)
            split_num = len(os.listdir(pcm_dir))
            while True:
                # 返回的是以1,2,3...开头的list
                result_list = asr_pool.getResultList(split_num)
                if result_list != '':
                    break
                time.sleep(1)

            self.keepSubtitle(result_list, key)
            key += 1

    def keepSubtitle(self, result_list, key):
        keep_path = self.subtitle_list[key][0]
        time_list = self.subtitle_list[key][1]
        with open(keep_path, 'wt') as f:
            count = 0
            for item in time_list:
                f.write(str(count + 1))
                f.write('\n')
                f.write(item[0] + ' --> ' + item[1])
                f.write('\n')
                f.write('{\\fs5}\n')
                f.write(result_list[count][1])
                f.write('\n')
                f.write('\n')
                count += 1

    def clearTemp(self):
        shutil.rmtree(self.audio_path)
        # os.removedirs(self.audio_path)


if __name__ == "__main__":
    # 创建需要执行的命令
    video_path = input('video_path')
    args = input('args')
    # 创建命令接收者
    receive = Receiver(video_path, args)
    # 绑定要执行的命令
    video           = ConcreteCommand1(receive) # 获取源视频路径
    separate        = ConcreteCommand2(receive) # 从视频中分离音轨
    cut             = ConcreteCommand3(receive) # 切割音频
    normalization   = ConcreteCommand4(receive) # 标准化音频
    asr             = ConcreteCommand5(receive) # 对音频进行识别
    clear           = ConcreteCommand6(receive) # 清临时文件
    # 创建调用者
    invoker = Invoker()
    # 调用者调用命令
    invoker.excutecommand(video)
    invoker.excutecommand(separate)
    invoker.excutecommand(cut)
    invoker.excutecommand(normalization)
    invoker.excutecommand(asr)
    invoker.excutecommand(clear)
    # 接收者执行命令
    receive.getVideo()
    receive.video2Audio()
    receive.cutAudio()
    receive.normalizateAudio()
    receive.asrAudio()
    receive.clearTemp()

# /home/clhiker/resource/video/test_a.mkv
# /home/clhiker/resource/video/test_b.rmvb
# /home/clhiker/MEGA/Asr_Audio/resource/video