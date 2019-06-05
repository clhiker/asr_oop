#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
"""
设计模式——组合模式
组合模式(Composite Pattern):将对象组合成成树形结构以表示“部分-整体”的层次结构,
组合模式使得用户对单个对象和组合对象的使用具有一致性.
"""

class VideoList:
    def __init__(self):
        self.video_type = ['mp4', 'rmvb', 'mkv']
        self.videos_list = []
        self.subtitle_list = []

    def getVideoFile(self, video_path):
        suffix = os.path.splitext(video_path)[-1][1:]
        if suffix in self.video_type:
            self.videos_list.append(video_path)
            subtitle_path = video_path[: video_path.find('.')] + '.srt'
            self.subtitle_list.append([subtitle_path])
        else:
            pass

    def ergodicFiles(self, root):
        root_list = os.listdir(root)
        for item in root_list:
            path = root + os.sep + item
            if not os.path.isdir(path):
                self.getVideoFile(path)
            else:
                self.ergodicFiles(path)

    def readArgs(self, video_path, args):
        if args == '-f' or args == '-F':
            self.getVideoFile(video_path)

        elif args == '-od' or args == '-OD':
            root_list = os.listdir(name)
            for item in root_list:
                video_path = name + os.sep + item
                if not os.path.isdir(video_path):
                    self.getVideoFile(video_path)

        elif args == '-d' or args == '-D':
            self.ergodicFiles(video_path)

        else:
            assert 'error'

    def getVideoList(self):
        return self.videos_list

    def getSubtitleList(self):
        return self.subtitle_list






#
#
# # 抽象一个组织类
# class Component(object):
#
#     def __init__(self, name):
#         self.name = name
#
#     def add(self,comp):
#         pass
#
#     def remove(self,comp):
#         pass
#
#     def getPath(self):
#
#
# # 叶子节点
# class Leaf(Component):
#     def __init__(self, name):
#         super(Leaf, self).__init__(name)
#         print(name)
#
#     def add(self,comp):
#         suffix = os.path.splitext(self.name)[-1][1:]
#         if suffix in video_type:
#             pass
#
#         print ('不能添加下级节点')
#
#     # 音轨分离
#     def separateAudio(self, video_path):
#         audio_path = '../resource/audio/test_a.mp3'
#         subprocess.call('ffmpeg -i ' + video_path + ' -f mp3 -vn ' + audio_path, shell=True)
#
#     def remove(self,comp):
#         print ('不能删除下级节点')
#
#     def getPath(self):
#
#
#     def display(self, depth):
#         strtemp = ''
#         for i in range(depth):
#             strtemp += strtemp+'-'
#         print (strtemp+self.name)
#
#
# # 枝节点
# class Composite(Component):
#
#     def __init__(self, name):
#         self.name = name
#         self.children = []
#
#     def add(self,comp):
#         self.children.append(comp)
#
#     def remove(self,comp):
#         self.children.remove(comp)
#
#     def display(self, depth):
#         strtemp = ''
#         for i in range(depth):
#             strtemp += strtemp+'-'
#         print (strtemp+self.name)
#         for comp in self.children:
#             comp.display(depth+2)
#
#
# def createRoot(name):
#     root = Composite(name)
#     root_list = os.listdir(name)
#     for item in root_list:
#         path = name + os.sep + item
#         if not os.path.isdir(path):
#             root.add(Leaf(path))
#         else:
#             comp = Composite("Composite XY")
#
#
# if __name__ == "__main__":
#     name = input('input name')
#     args = input('input args')
#     if args == '-f' or args == '-F':
#         pass
#     elif args == '-od' or args == '-OD':
#         root = Composite(name)
#         root_list = os.listdir(name)
#         for item in root_list:
#             path = name + os.sep + item
#             if not os.path.isdir(path):
#                 root.add(Leaf(path))
#
#     elif args == '-d' or args == '-D':
#
#         root = Composite(name)
#         root_list = os.listdir(name)
#         for item in root_list:
#             path = name + os.sep + item
#             if not os.path.isdir(path):
#                 root.add(Leaf(path))
#             else:
#
#         pass
#     else:
#         assert 'error'
#
#
#     #生成树根
#     root = Composite("root")
#     #根上长出2个叶子
#     root.add(Leaf('leaf A'))
#     root.add(Leaf('leaf B'))
#
#     #根上长出树枝Composite X
#     comp = Composite("Composite X")
#     comp.add(Leaf('leaf XA'))
#     comp.add(Leaf('leaf XB'))
#     root.add(comp)
#
#     #根上长出树枝Composite X
#     comp2 = Composite("Composite XY")
#     #Composite X长出2个叶子
#     comp2.add(Leaf('leaf XYA'))
#     comp2.add(Leaf('leaf XYB'))
#     root.add(comp2)
#     # 根上又长出2个叶子,C和D,D没张昊,掉了
#     root.add(Leaf('Leaf C'))
#     leaf = Leaf("Leaf D")
#     root.add(leaf)
#     root.remove(leaf)
#     #展示组织
#     root.display(1)
#
# #
# # import filetype
# #
# #
# # def main():
# #     kind = filetype.guess('../resource/audio/test_a.mp3')
# #     if kind is None:
# #         print('Cannot guess file type!')
# #         return
# #
# #     print('File extension: %s' % kind.extension)
# #     print('File MIME type: %s' % kind.mime)
# #
# #
# # if __name__ == '__main__':
# #     main()