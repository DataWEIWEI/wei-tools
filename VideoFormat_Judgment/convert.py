import subprocess  
  
def convert_mov_to_mp4(input_file, output_file):  
    # 构造FFmpeg命令  
    # 这里使用`-c:v copy -c:a copy`来复制视频和音频流，而不是重新编码它们  
    # 这样可以避免质量损失  
    cmd = [  
        'ffmpeg',  
        '-i', input_file,  # 输入文件  
        '-c:v', 'copy',    # 视频编解码器设置为复制（不重新编码）  
        '-c:a', 'copy',    # 音频编解码器设置为复制（不重新编码）  
        '-movflags', '+faststart',  # 优化MP4文件以便更快地从网络加载  
        output_file        # 输出文件  
    ]  
  
    # 执行FFmpeg命令  
    try:  
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)  
        print(f"Conversion successful: {input_file} -> {output_file}")  
    except subprocess.CalledProcessError as e:  
        # 如果FFmpeg返回错误，打印错误信息  
        print(f"Conversion failed: {e.stderr.decode()}")  
  
# 示例用法  
input_file = 'example.mov'  
output_file = 'output.mp4'  
convert_mov_to_mp4(input_file, output_file)