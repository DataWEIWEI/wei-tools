import os
import sys
import time
import shutil
import threading
from tqdm import tqdm

# 加载动画
def animated_loading():
    chars = "/—\|"
    for char in chars:
        sys.stdout.write('\r' + 'loading...' + char)
        time.sleep(.1)
        sys.stdout.flush()


def file_path_extract(all_files):
    root_dir = './'  # 当前文件夹路径

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(extension):    # 判断文件后缀名
                file_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(
                    file_path, root_dir)  # 文件的相对路径
                all_files.update({f'{relative_path}': f'{filename}'})



def file_copy(folder_path, all_files):
        for dirpath, filename in tqdm(all_files.items()):
            shutil.copy2(dirpath, folder_path + r'\\' + filename)

# 定义文件夹路径
folder_path = './extractAll'  # 文件夹的相对路径或绝对路径
extension = input('\n请希望提取的文件的输入后缀名：')

# 检查文件夹是否存在
if not os.path.exists(folder_path):
    # 创建文件夹
    os.mkdir(folder_path)
else:
    print(f"文件夹 '{folder_path}' 已经存在。")

all_files = {}

# 定义线程的名称和目标
# 启动线程
# 当进程还活着时，调用animated_loading()函数
the_process = threading.Thread(name='process', target=file_path_extract, kwargs={'all_files': all_files})
the_process.start()
while the_process.is_alive():
    animated_loading()

print('文件开始复制清等待…………')
file_copy(folder_path, all_files)
print('文件复制结束，十秒后自动关闭')
time.sleep(10)

