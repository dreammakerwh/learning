import os
import shutil
import re


def custom_sort_key(filename):
    try:
        # 按 - 分割文件名
        parts = filename.split('-', 1)
        if len(parts) == 2:
            prefix, suffix = parts
            # 提取 - 前面部分的数字
            prefix_num_match = re.search(r'\d+', prefix)
            if prefix_num_match:
                prefix_num = int(prefix_num_match.group())
            else:
                prefix_num = float('inf')

            # 提取 - 后面部分字符串开始的数字
            suffix_num_match = re.search(r'^\d+', suffix)
            if suffix_num_match:
                suffix_num = int(suffix_num_match.group())
            else:
                suffix_num = float('inf')
            return (prefix_num, suffix_num)
        else:
            # 若没有 -，尝试提取文件名中的数字
            num_match = re.search(r'\d+', filename)
            if num_match:
                num = int(num_match.group())
            else:
                num = float('inf')
            return (num, float('inf'))
    except Exception:
        return (float('inf'), float('inf'))


def main():
    source_dir = r'C:\Users\yyzhou\Downloads\CleoYCunquin_mp3'
    target_dir = r'D:\CleoYCunquin_1.3x'

    # 检查源目录是否存在
    if not os.path.exists(source_dir):
        print(f"错误: 未找到源目录 {source_dir}。")
        return

    # 若目标目录不存在则创建
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    try:
        # 获取源目录下所有文件
        files = os.listdir(source_dir)
        # 按自定义规则排序
        sorted_files = sorted(files, key=custom_sort_key)

        for file in sorted_files:
            source_file_path = os.path.join(source_dir, file)
            target_file_path = os.path.join(target_dir, file)
            # 拷贝文件
            shutil.copy2(source_file_path, target_file_path)
            print(f"已拷贝文件: {file}")

        print("所有文件拷贝完成。")
        import msvcrt
        msvcrt.getch()
    except Exception as e:
        print(f"发生未知错误: {e}")
        input()


if __name__ == "__main__":
    main()
    