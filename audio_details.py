
import os
import glob
import sys
import re

# 配置需要跳过详细信息输出的子目录名称列表
SKIP_DIRECTORIES = {
    "daoqi1",
    "daoqi2", 
    "daoqi3",
    "daoqi4",
    "daoqi5","Rocket Girls Journey to the West音频","SarahDuck1","SarahDuck2","SarahDuck3","汪汪队rubble",
    "佩奇第一季音频","Bluey1","Bluey 2","Bluey 3","01.喵喵成长记 22集","03.喵喵好伙伴 22集 英语中字",
    "67","89","67D","991","Bluey3_1.38x","Bluey1_1.38x","Bluey2_1.38x","daoqi2_1.38x","daoqi4_1.38x","daoqi3_1.38x","daoqi1_1.38x","BenHolly1_1.35",
	"BenHolly2_1.35","peiqi3_1.38x","peiqi4_1.38x","SarahDuck1_1.38x","peixi1_1.38x","GirlToWest_1.38x","01.喵喵成长记 22集 英语中字",
	"03.Rocket Girl  火箭女孩音频252集","西游记","J级-音频","H级-音频","World80days","Pinocchio","RobinHood","Alices","Aladdin","Duggee粤语mp3",
	"粤语学习合并","peixi2_1.38x","WolfooLucy_mp3","WolfooLucy_1.3x","WolfooLucy_1.8x"
}

def natural_sort_key(filename):
    """
    生成自然排序键，优先按数字编号排序
    """
    # 将文件名分割为数字和非数字部分
    parts = re.split(r'(\d+)', filename)
    # 将数字部分转换为整数，非数字部分保持字符串
    return [int(part) if part.isdigit() else part.lower() for part in parts]

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
    summary_lines = []
    detail_lines = []
    global_counter = 1
    
    skipped_count = 0
    processed_count = 0
    
    for full_path, subdir_name, creation_time, mp3_files in subdirs:
        # 按文件名排序，优先按数字编号排序
        mp3_files.sort(key=lambda x: natural_sort_key(os.path.basename(x)))
        
        # 获取文件数量
        file_count = len(mp3_files)
        
        # 记录子目录名和第一个文件的序号（始终记录）
        summary_line = f"{subdir_name} -> {global_counter} (文件数量: {file_count})"
        summary_lines.append(summary_line)
        
        # 检查是否需要跳过详细信息输出
        if subdir_name in SKIP_DIRECTORIES:
            # 将跳过信息也写入details.txt
            detail_lines.append(f"{subdir_name} (起始索引: {global_counter}, 文件数量: {file_count})")
            detail_lines.append("")  # 添加空行分隔
            skipped_count += 1
        else:
            # 在详细文件中添加子目录信息
            detail_lines.append(f"{subdir_name} (起始索引: {global_counter}, 文件数量: {file_count})")
            
            # 为每个文件添加全局编号信息
            for i, mp3_file in enumerate(mp3_files, 1):
                file_name = os.path.basename(mp3_file)
                global_index = global_counter + i - 1  # 全局索引 = 子目录起始索引 + 文件在子目录中的位置 - 1
                detail_lines.append(f"  {global_index}. {file_name}")
            
            detail_lines.append("")  # 添加空行分隔
            processed_count += 1
        
        # 更新全局计数器（始终更新）
        global_counter += len(mp3_files)
    
    # 将结果保存到details.txt文件
    output_file = os.path.join(root_directory, "details.txt")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in detail_lines:
                f.write(line + '\n')
        print(f"详细信息已成功保存到: {output_file}")
        
        # 输出摘要信息到控制台
        print(f"\n处理完成！共处理 {processed_count} 个子目录的详细信息，跳过 {skipped_count} 个子目录的详细信息输出")
        print("\n子目录索引摘要:")
        for line in summary_lines:
            print(line)
            
    except Exception as e:
        print(f"保存文件时出错: {e}")
    
    # 防止Windows命令行窗口自动关闭
    print("\n按任意键退出...")
    try:
        # Windows系统使用msvcrt.getch()
        import msvcrt
        msvcrt.getch()
    except ImportError:
        # 非Windows系统使用input()
        input()

if __name__ == "__main__":
    main()
