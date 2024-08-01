import os  
import json  
  
def modify_json_files(directory, parameter: str, new_value):  
    """  
    遍历指定目录中的所有.exp3.json文件, 将文件中的"Value"修改为新的值。  
  
    :param directory: 包含.exp3.json文件的目录路径  
    :param new_value: 新的Value值  
    """  
    # 遍历目录  
    for filename in os.listdir(directory):  
        if filename.endswith('.exp3.json'):  
            print(filename)
            # 完整文件路径  
            file_path = os.path.join(directory, filename)  
              
            # 读取JSON文件  
            with open(file_path, 'r', encoding='utf-8') as file:  
                data = json.load(file)  
              
            # 假设我们总是修改第一个Parameters中的Value（如果有多个可能需要更复杂的逻辑）  
            if 'Parameters' in data and data['Parameters']:  
                for param in data['Parameters']:  
                    if param['Id'] == parameter:  
                        param['Value'] = new_value  
              
            # 将修改后的数据写回文件  
            with open(file_path, 'w', encoding='utf-8') as file:  
                json.dump(data, file, ensure_ascii=False, indent=4)  
  
# 使用示例  
directory_path = input('请输入包含.exp3.json文件的目录路径(请不要带引号):')  # 修改为你的目录路径  
parameterId = input('请输入要修改的参数ID(全名):')  # 修改为你要修改的参数ID
new_value = input('请输入新的Value值(整数或小数):')  # 修改为你要设置的新Value值 

# 尝试将用户输入转换为浮点数  
try:  
    new_value = float(new_value)  
    print("你输入的数字是:", new_value)  
except ValueError:  
    # 如果转换失败（比如用户输入的不是数字），则捕获异常并打印错误消息  
    print("错误：请输入一个有效的数字")

modify_json_files(directory_path, parameterId, new_value)