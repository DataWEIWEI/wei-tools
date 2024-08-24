import os
import sys  
import glob  
  
# 获取用户输入  
file_path = input('请输入您要重命名文件的文件夹路径（绝对路径）：')  
file_type_input = input('请输入您要设置的文件类型（例：*.jpg | 如果您需要重命名所有类型文件请直接回车）：')  
postfix = input('请输入您要设置的文件名后缀（注意：这将是新的扩展名，如果需要保留原扩展名请直接回车）：')  
prefix = input('请输入您要设置的文件名前缀（如果需要直接回车）：')  
mark = input('请输入您要设置的文件名间隔符（如果不需要直接回车）：')  
number_digits = int(input('请输入您所要设置编号的位数：'))  
  
# 如果用户想要重命名所有文件，则设置 file_type 为匹配所有文件的通配符  
if file_type_input == '':  
    file_type = os.path.join(file_path, '*')  
else:  
    # 确保 file_type 是以目录路径开头，并包含通配符  
    file_type = os.path.join(file_path, file_type_input)  
  
# 使用 glob 在指定路径下搜索文件  
files = glob.glob(file_type)  

print(file_path)

while True:  
    # 询问用户是否继续  
    user_input = input("请再次确认文件夹路径，输入1继续运行，输入0终止脚本运行: ")  
      
    # 根据用户的输入做出决定  
    if user_input == '1':  
        # 用户选择继续  
        print("脚本继续运行...")  
        # 在这里添加你的代码逻辑  
        break
    elif user_input == '0':  
        # 用户选择终止脚本  
        print("脚本即将终止...")  
        break  # 退出循环，即退出脚本（因为后面没有其他代码）  
    else:  
        # 如果用户输入了除1或0以外的值，打印错误信息并继续循环  
        print("无效的输入，请输入1或0！")  

  
# ...（接下来是重命名文件的逻辑）  
  
# 示例：重命名文件的逻辑  
count = 1  
for file in files:  
    # 检查当前项是否真的是一个文件（而不是文件夹） 
    if not os.path.isdir(file):     
        # 获取文件的原始名称（不包括目录路径）和扩展名  
        filename, ext = os.path.splitext(os.path.basename(file))  
        
        # 如果 postfix 为空，则保留原扩展名；否则，使用新的 postfix  
        if postfix:  
            new_ext = postfix  
        else:  
            new_ext = ext  
        
        # 构建新文件名  
        new_filename = f"{prefix}{mark}{count:0{number_digits}d}{new_ext}"  
        
        # 构建新文件的完整路径  
        new_file_path = os.path.join(file_path, new_filename)  
        
        # 重命名文件  
        os.rename(file, new_file_path)  
        print(f"Renamed {file} to {new_file_path}")  
        
        count += 1
    else:  
        # 如果它是一个文件夹，则打印一条消息（可选）  
        print(f"Skipping directory: {file}")  