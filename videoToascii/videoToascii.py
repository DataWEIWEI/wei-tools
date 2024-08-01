from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import shutil
import sys


class videoToascii:

    def __init__(self, filename: str,):
        # 执行前的一些判断
        if not os.path.isfile(filename):
            print("源文件找不到，或者不存在！")
            exit()

        temp_arr = filename.split('.')

        # 字符列表，从左至右逐渐变得稀疏，对应着颜色由深到浅
        self.ascii_char = list("$@B%8&WM#*oahkbdpqwO0QLCJYXzcvunxrjft/\|()1[]?-_+~<>i!......... ")

        # 传入视频文件名
        self.filename = filename
        # 输出视频文件名
        self.outname = temp_arr[0] + "_out." + temp_arr[1]

        # 存储图片的临时路径、输出路径
        self.pic_path = 'temp_pic'
        self.ascii_path = 'temp_ascii'
        self.outpath = 'temp_out'

        # 设置图片缩小的倍数
        self.resize_times = 6   # 涉及到转换时间，倍数越小，时间指数上升

        # 设置输出文件的名字,声音文件以及带声音的输出文件
        self.mp3ilename = os.path.join(self.outpath, temp_arr[0] + '.mp3')
        self.mp4filename = os.path.join(self.outpath, self.outname)

        # 合并输出的视频文件
        self.mergefilename = os.path.join(self.outpath, temp_arr[0] + '_voice.' + temp_arr[1])

    def createpath(self):
        # 源视频文件的图片路径
        if not os.path.exists(self.pic_path):
            os.makedirs(self.pic_path)
        else:
            # 清空在创建
            shutil.rmtree(self.pic_path)
            os.makedirs(self.pic_path)

        # 转换之后的图片路径
        if not os.path.exists(self.ascii_path):
            os.makedirs(self.ascii_path)
        else:
            # 清空再创建
            shutil.rmtree(self.ascii_path)
            os.makedirs(self.ascii_path)

        # 存储输出文件的目录
        if not os.path.exists(self.outpath):
            os.makedirs(self.outpath)

    def video2pic(self):
        # 使用ffmpeg切割图片，命令行如下
        cmd = 'ffmpeg -i {0} -r 24 {1}/%06d.jpeg'.format(self.filename, self.pic_path)
        os.system(cmd)

    def pic2ascii(self):
        # 读取原始图片目录
        pic_list = sorted(os.listdir(self.pic_path))

        total_len = len(pic_list)
        count = 1
        # 遍历每张图片
        for pic in pic_list:
            # 图片完整路径
            imgpath = os.path.join(self.pic_path, pic)

            # 1、缩小图片，转成灰度模式，存入数组
            origin_img = Image.open(imgpath)
            # 缩小之后宽高
            resize_width = int(origin_img.size[0] / self.resize_times)
            resize_height = int(origin_img.size[1] / self.resize_times)
            resize_img = origin_img.resize((resize_width, resize_height), Image.ANTIALIAS).convert("L")
            img_arr = np.array(resize_img)

            # 2、新建空白图片（灰度模式、与原始图片等宽高）
            new_img = Image.new("L", origin_img.size, 255)
            draw_obj = ImageDraw.Draw(new_img)
            font = ImageFont.truetype("arial.ttf", 8)

            # 3、将每个字符绘制在 8*8 的区域内
            for i in range(resize_height):
                for j in range(resize_width):
                    x, y = j * self.resize_times, i * self.resize_times
                    index = int(img_arr[i][j] / 4)
                    draw_obj.text((x, y), self.ascii_char[index], font=font, fill=0)

            # 4、保存字符图片
            new_img.save(os.path.join('temp_ascii', pic), "JPEG")
            print("已生成ascii图（%d/%d）" % (count, total_len))
            count += 1

    def ascii2video(self):
        # 输出视频保存路径
        savepath = os.path.join(self.outpath, self.outname)
        self.mp4filename = savepath
        cmd = 'ffmpeg -threads 2 -start_number 000001 -r 24 -i {0}/%06d.jpeg -vcodec mpeg4 {1}'.format(
            self.ascii_path, savepath)
        os.system(cmd)

    def video2mp3(self):
        # mp3名字和保存路径
        name = self.filename.split('.')[0] + '.mp3'
        savepath = os.path.join(self.outpath, name)
        self.mp3filename = savepath
        cmd = 'ffmpeg -i {0} -f mp3 {1}'.format(self.filename, savepath)
        os.system(cmd)

    def mp4andmp3(self):
        cmd = 'ffmpeg -i {0} -i {1} -strict -2 -f mp4 {2}'.format(self.mp4filename, self.mp3ilename,
                                                                  self.mergefilename)
        os.system(cmd)

    def start(self):
        """
            > 程序流程：
                1、创建路径
                2、将原始视频分割成图片
                3、将图片缩放、转成ascii形式
                4、将ascii形式的图片合成视频
                5、获取音频mp3文件
                6、合并视频和音频文件
        :return:
        """
        self.createpath()
        self.video2pic()
        self.pic2ascii()
        self.ascii2video()

        self.video2mp3()
        self.mp4andmp3()

        print("程序执行完成")


if __name__== "__main__":
    luoli = videoToascii(filename="luoli.mp4")
    luoli.start()



