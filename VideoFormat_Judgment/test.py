import subprocess  
import json  
  
def get_video_info(video_path):  
    # 构建ffprobe命令  
    command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_path]  
      
    # 运行ffprobe命令并捕获输出  
    try:  
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)  
        ffprobe_output = proc.stdout  

        # 直接将ffprobe的原始输出保存到文件（如果需要）  
        # 注意：这不会解析JSON，只是保存原始文本  
        with open('ffprobe_output.json', 'w') as f:  
            f.write(ffprobe_output)  
          
        # 解析JSON输出  
        video_info = json.loads(ffprobe_output)  
          
        # 提取一些基本信息（这里只是示例，具体信息取决于你的需求）  
        format_info = video_info['format']  
        streams = video_info['streams']  
          
        # 假设我们只关心第一个视频流  
        video_stream = next((s for s in streams if s['codec_type'] == 'video'), None)  
          
        if video_stream:  
            print(f"Duration: {format_info['duration']} seconds")  
            print(f"Resolution: {video_stream['width']}x{video_stream['height']}")  
            print(f"Framerate: {video_stream['avg_frame_rate']}")  
            print(f"Codec: {video_stream['codec_name']}")  
            print(f"Format Long Name: {format_info['format_long_name']}")    
            print(f"Bit Rate: {format_info['bit_rate']} bits/s")  
            # 可以根据需要添加更多信息  
        else:  
            print("No video stream found.")  
              
    except subprocess.CalledProcessError as e:  
        print(f"ffprobe failed with error: {e.stderr}")  
    except json.JSONDecodeError:  
        print("Error decoding JSON output from ffprobe.")  
  
# 使用示例  
video_path = 'example.mp4'  
get_video_info(video_path)