
import os
import glob
import sys

def get_subdirs_with_mp3(root_dir):
    """获取所有包含mp3文件的子目录，并按创建时间排序"""
    subdirs = []
    for subdir in os.listdir(root_dir):
        full_path = os.path.join(root_dir, subdir)
        if os.path.isdir(full_path):
            # 不区分大小写匹配 .mp3/.MP3 等；排除隐藏文件和子目录；
            # 无法读取的系统目录（如 .Spotlight-V100）直接跳过。
            try:
                entries = os.listdir(full_path)
            except OSError:
                entries = []
            mp3_files = [
                os.path.join(full_path, f)
                for f in entries
                if not f.startswith('.')
                and os.path.isfile(os.path.join(full_path, f))
                and f.lower().endswith('.mp3')
            ]
            if mp3_files:
                # 获取子目录的创建时间
                creation_time = os.path.getctime(full_path)
                subdirs.append((full_path, subdir, creation_time, mp3_files))
    
    # 按创建时间排序
    subdirs.sort(key=lambda x: x[2])
    return subdirs

def main():
    # 使用脚本所在目录作为根目录
    root_directory = os.path.dirname(os.path.abspath(__file__))
    
    if not os.path.isdir(root_directory):
        print("脚本所在路径不是有效目录")
        return

    subdirs = get_subdirs_with_mp3(root_directory)
    
    # 准备写入文件的内容
    output_lines = []
    global_counter = 1
    
    for full_path, subdir_name, creation_time, mp3_files in subdirs:
        # 按文件创建时间排序
        mp3_files.sort(key=lambda x: os.path.getctime(x))
        
        # 记录子目录名、第一个文件的序号和文件数量
        file_count = len(mp3_files)
        line = f"{subdir_name} -> {global_counter} (文件数量: {file_count})"
        output_lines.append(line)
        
        # 更新全局计数器
        global_counter += len(mp3_files)
    
    # 将结果保存到index.txt文件
    output_file = os.path.join(root_directory, "index.txt")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in output_lines:
                f.write(line + '\n')
        print(f"索引已成功保存到: {output_file}")
        print("\n生成的索引内容:")
        for line in output_lines:
            print(line)
    except Exception as e:
        print(f"保存文件时出错: {e}")

if __name__ == "__main__":
    main()
