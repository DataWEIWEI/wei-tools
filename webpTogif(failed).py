import imageio

# 输入WebP文件路径
webp_file_path = input('请确认输入文件路径：')

# 输出GIF文件路径
gif_file_path = input('请确认输出文件路径：')

# 使用imageio将WebP文件转换为GIF
with imageio.get_reader(webp_file_path) as reader:
    # 获取帧的延迟时间
    delay_times = [delay / 1000 for delay in reader.get_meta_data().get('duration', [100])]

    # 读取所有帧并保存为GIF
    with imageio.get_writer(gif_file_path, mode='I', duration=delay_times) as writer:
        for frame in reader:
            writer.append_data(frame)

print(f'WebP文件已转换为GIF并保存为 {gif_file_path}')






