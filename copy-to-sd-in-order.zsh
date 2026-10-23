#!/bin/zsh -f
# Copy non-hidden regular files one at a time in filename order.
# Usage: ./copy-to-sd-in-order.zsh SOURCE_DIRECTORY [DESTINATION_DIRECTORY]

export LC_ALL=C

# 防止 cp 把源文件的扩展属性/资源叉一并带过去（FAT 上会额外写进 ._ 侧文件）。
# 注意：macOS 26 的 FAT 驱动会给每个新文件加上 com.apple.provenance 并生成 ._ 侧文件，
# 这是系统级行为，任何拷贝命令都拦不住；真正清除靠脚本末尾的清理步骤。
export COPYFILE_DISABLE=1

if (( $# < 1 || $# > 2 )); then
  printf '用法：%s 源目录 [目标目录]\n' "$0" >&2
  exit 2
fi

source_input=$1
target_input=${2-}

if [[ -z $target_input ]]; then
  printf '目标目录（例如 /Volumes/SDCARD/MUSIC）：'
  IFS= read -r target_input
fi

if [[ ! -d $source_input ]]; then
  printf '错误：源目录不存在：%s\n' "$source_input" >&2
  exit 1
fi

mkdir -p $target_input
if [[ ! -d $target_input ]]; then
  printf '错误：目标目录不存在：%s\n' "$target_input" >&2
  exit 1
fi

source_dir=$(cd "$source_input" && pwd -P) || exit 1
target_dir=$(cd "$target_input" && pwd -P) || exit 1

if [[ $source_dir == $target_dir ]]; then
  printf '错误：源目录和目标目录不能相同。\n' >&2
  exit 1
fi

# zsh expands this glob in filename order. (N.) means: allow no matches,
# and select regular files only. A leading dot is excluded by the glob.
files=( "$source_dir"/*(N.) )

if (( ${#files} == 0 )); then
  printf '源目录中没有可复制的非隐藏普通文件。\n'
  exit 0
fi

total=${#files}
copied=0
skipped=0
overall_start=$SECONDS

for (( i = 1; i <= total; i++ )); do
  file=${files[i]}
  name=${file:t}
  destination="$target_dir/$name"

  if [[ -e $destination || -L $destination ]]; then
    printf '[%d/%d] 跳过（已存在）：%s\n' "$i" "$total" "$name"
    skipped=$((skipped + 1))
    continue
  fi

  size=$(stat -f %z "$file" 2>/dev/null || print 0)
  printf '[%d/%d] 正在复制：%s（%.1f MB）\n' "$i" "$total" "$name" "$(( size / 1048576.0 ))"
  start=$SECONDS
  # -X 不复制扩展属性/资源叉，避免把源文件元数据写进 ._；-n 再增加一层防覆盖。
  if cp -X -n "$file" "$destination"; then
    printf '      完成：%s（%.1f 秒）\n' "$name" "$(( SECONDS - start ))"
    copied=$((copied + 1))
  else
    printf '复制失败：%s\n' "$name" >&2
    exit 1
  fi
done

# 关键步骤：删除目标目录里系统自动生成的 ._ AppleDouble 与 .DS_Store。
# macOS 26 写 FAT 卷时，每个新文件都会被系统生成 ._ 侧文件，拷贝完统一删除即可。
cleaned=$(find "$target_dir" \( -name '._*' -o -name '.DS_Store' \) -type f -delete -print | wc -l | tr -d ' ')
if (( cleaned > 0 )); then
  printf '清理元数据文件：%s 个\n' "$cleaned"
fi

printf '完成：复制 %d 个，跳过 %d 个，总用时 %.1f 秒。请安全弹出 SD 卡。\n' "$copied" "$skipped" "$(( SECONDS - overall_start ))"
