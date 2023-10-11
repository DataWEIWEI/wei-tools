import os
import cv2
import sys
import time
import magic
import threading


# 加载动画
def animated_loading():
    chars = "/—\|"
    for char in chars:
        sys.stdout.write('\r' + 'loading...' + char)
        time.sleep(.1)
        sys.stdout.flush()


# 检查是否为视频文件
def is_video_file(file_path):
    mime = magic.Magic(mime=True)
    filename = mime.from_file(file_path)
    return filename.find('video') != -1


    # 提取所有视频文件的路径
def file_path_extract(all_files):
    root_dir = './'  # 当前文件夹路径

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:  # 判断文件后缀名
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(
                file_path, root_dir)  # 文件的相对路径
            if is_video_file(relative_path):
                all_files.update({f'{relative_path}': f'{filename}'})


def is_video_corrupted(video_path: dict):
    try:
        # 尝试打开视频文件
        cap = cv2.VideoCapture(video_path)

        # 检查是否成功打开视频文件
        if not cap.isOpened():
            return True

        # 读取一帧并检查是否成功
        ret, _ = cap.read()
        if not ret:
            return True

        # 关闭视频文件
        cap.release()

        return False  # 视频文件未损坏
    except Exception as e:
        print("Error:", e)
        return True  # 发生异常，视频文件可能损坏


# 删除文件
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted successfully.")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")


# 指定要检查的视频文件路径
video_path = {}
# 定义线程的名称和目标
# 启动线程
# 当进程还活着时，调用animated_loading()函数
the_process = threading.Thread(name='process', target=file_path_extract, kwargs={'all_files': video_path})
the_process.start()
while the_process.is_alive():
    animated_loading()

num = 0
for video in video_path:
    # 调用函数检查视频文件是否损坏
    if is_video_corrupted(video):
        # 已经损坏
        print(f"{video} is corrupted.")
        print('delete this video file')
        delete_file(video)
    else:
        # 没有损坏
        print(f"{video} is not corrupted.")

    num += 1
    print(f'detected {num} video')

print('detection complete!!!')
