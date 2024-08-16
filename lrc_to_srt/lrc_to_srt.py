import os  
import re  

def lrc_to_srt(lrc_path, srt_path, min_duration=1.0):  
    """  
    将单个LRC文件转换为SRT文件。  
  
    :param lrc_path: LRC文件的路径  
    :param srt_path: 要保存的SRT文件的路径  
    :param min_duration: 每段歌词的最小持续时间（秒），用于避免时间戳过近导致的重叠  
    """  
    with open(lrc_path, 'r', encoding='utf-8') as file:  
        lines = file.readlines() 
  
    srt_lines = []  
    index = 1  
    current_time = None  
    current_lyric = []  
  
    for line in lines:  
        line = line.strip()  
        if not line:  
            continue  # 跳过空行  
  
        # 尝试解析时间戳  
        time_match = re.match(r'\[(\d{2}:\d{2}(.\d+)?)\]', line) 
        if time_match:  
            if current_time is not None and current_lyric:  
                # 计算结束时间（这里简化为与下一句歌词开始时间相同，但添加最小持续时间检查）  
                end_time_str = time_match.group(1) 
                end_time = parse_time_str(end_time_str)  
                if end_time - parse_time_str(current_time) < min_duration:  
                    # 如果时间差小于最小持续时间，则调整结束时间为当前时间加上最小持续时间  
                    end_time_str = format_time_str(parse_time_str(current_time) + min_duration)  
  
                srt_line = f"{index}\n{format_time_str(parse_time_str(current_time))} --> {end_time_str}\n{''.join(current_lyric)}\n\n"  
                srt_lines.append(srt_line) 
                index += 1  
  
            current_time = time_match.group(1)  
            current_lyric = [line[time_match.end():].strip()]  # 去除时间戳后的歌词文本  
        else:  
            # 如果没有时间戳，则假设这是当前歌词的延续  
            current_lyric.append(line)  
  
    # 处理最后一行歌词（如果有的话）  
    if current_time is not None and current_lyric:  
        # 这里需要假设一个结束时间，因为没有下一句歌词的开始时间作为参考  
        # 可以是视频的总时长，或者是一个固定的结束时间  
        # 这里我们简单地使用当前时间加上一个默认持续时间  
        end_time = parse_time_str(current_time) + 3.0  # 假设默认持续时间为3秒  
        srt_line = f"{index}\n{format_time_str(parse_time_str(current_time))} --> {format_time_str(end_time)}\n{''.join(current_lyric)}\n\n"  
        srt_lines.append(srt_line)  
  
    with open(srt_path, 'w', encoding='utf-8') as file:  
        file.writelines(srt_lines)  
  
def parse_time_str(time_str):  
    """  
    将时间字符串（如"01:02.345"）解析为秒数。
    注意：此脚本无法解决大于一个小时的 lrc 文件转换问题  
    """  
    hours = 0
    minutes, seconds = map(float, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds

def format_time_str(seconds):
    """
    将秒数格式化为SRT时间字符串（如"00:01:02,345"）。
    注意：SRT文件使用逗号作为毫秒分隔符。
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = seconds % 60
    milliseconds = int((remaining_seconds - int(remaining_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(remaining_seconds):02d},{milliseconds:03d}"

def convert_lrc_folder_to_srt(folder_path, output_folder_path, min_duration=1.0):
    """
    将指定文件夹下的所有LRC文件转换为SRT文件。
    :param folder_path: 包含LRC文件的文件夹路径  
    :param output_folder_path: 存放生成的SRT文件的文件夹路径  
    :param min_duration: 每段歌词的最小持续时间（秒）  
    """  
    if not os.path.exists(output_folder_path):  
        os.makedirs(output_folder_path)  

    for filename in os.listdir(folder_path):  
        if filename.endswith('.lrc'):  
            lrc_path = os.path.join(folder_path, filename)  
            srt_filename = filename.replace('.lrc', '.srt')  
            srt_path = os.path.join(output_folder_path, srt_filename)  
            lrc_to_srt(lrc_path, srt_path, min_duration)  
            print(f"Converted {lrc_path} to {srt_path}")

# 使用示例
folder_path = input('请输入包含LRC文件的文件夹完整路径：')
output_folder_path = input('请输入存放生成的SRT文件的文件夹完整路径：')
convert_lrc_folder_to_srt(folder_path, output_folder_path, min_duration=2.0)