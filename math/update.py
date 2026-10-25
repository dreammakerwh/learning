#!/usr/bin/env python3
"""生成数学学习导航和音频 TXT 索引。"""
from html import escape
from pathlib import Path

folder = Path(__file__).resolve().parent
navigation = folder / "index.html"
pages = sorted(
    (p for p in folder.iterdir()
     if p.is_file() and p.suffix.lower() in {".html", ".htm"}
     and p.resolve() != navigation.resolve()),
    key=lambda p: p.name.casefold(),
)
links = "\n".join(
    f'      <li><a href="{escape(p.name, quote=True)}">{escape(p.stem)}</a></li>'
    for p in pages
)
content = f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>数学学习导航</title>
  <style>
    :root {{ color-scheme: light; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; padding: 48px 20px; color: #233044; background: linear-gradient(145deg, #f0f7ff, #f9f5ff); }}
    main {{ width: min(680px, 100%); margin: 0 auto; }}
    h1 {{ margin: 0 0 8px; font-size: clamp(28px, 6vw, 40px); }}
    p {{ margin: 0 0 24px; color: #64748b; }}
    ul {{ display: grid; gap: 12px; margin: 0; padding: 0; list-style: none; }}
    a {{ display: block; padding: 17px 20px; border: 1px solid #e2e8f0; border-radius: 14px; color: #2457a6; background: #fff; text-decoration: none; box-shadow: 0 4px 14px #1e3a5f0a; transition: transform .15s, box-shadow .15s; }}
    a:hover, a:focus-visible {{ transform: translateY(-2px); box-shadow: 0 8px 22px #1e3a5f18; outline: none; }}
  </style>
</head>
<body>
  <main>
    <h1>数学学习导航</h1>
    <p>选择一个页面开始学习</p>
    <ul>
{links if links else '      <li>当前目录没有其他 HTML 页面</li>'}
    </ul>
  </main>
</body>
</html>
'''
navigation.write_text(content, encoding="utf-8")
print(f"已更新 {navigation.name}，共添加 {len(pages)} 个页面链接。")

# 音频索引只提供 TXT 文件导航，不读取或展示 TXT 文件内容。
text_files = sorted(
    (p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ".txt"),
    key=lambda p: p.name.casefold(),
)

# 带数字前缀（如 2_details.txt）的文件归入卡1；无数字前缀的文件归入卡2。
cards = [
    ("卡1", [p for p in text_files if p.stem.split("_", 1)[0].isdigit()]),
    ("卡2", [p for p in text_files if not p.stem.split("_", 1)[0].isdigit()]),
]
card_html = "\n".join(
    f'''    <section class="card">
      <h2>{escape(title)}</h2>
      <ul>
{chr(10).join(f'        <li><a href="{escape(p.name, quote=True)}">{escape(p.name)}</a></li>' for p in files) if files else '        <li class="empty">没有 TXT 文件</li>'}
      </ul>
    </section>'''
    for title, files in cards
)
audio_index = folder / "00-收音机音频索引.html"
audio_content = f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>音频索引</title>
  <style>
    :root {{ color-scheme: light; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; padding: 40px 20px; color: #233044; background: linear-gradient(145deg, #f0f7ff, #f9f5ff); }}
    main {{ width: min(760px, 100%); margin: 0 auto; }}
    h1 {{ margin: 0 0 24px; font-size: clamp(28px, 6vw, 40px); }}
    .cards {{ display: grid; gap: 18px; }}
    .card {{ padding: 20px; border: 1px solid #e2e8f0; border-radius: 16px; background: #fff; box-shadow: 0 4px 14px #1e3a5f0a; }}
    h2 {{ margin: 0 0 12px; font-size: 20px; }}
    ul {{ display: grid; gap: 8px; margin: 0; padding: 0; list-style: none; }}
    a {{ display: block; padding: 11px 14px; border-radius: 10px; color: #2457a6; background: #f4f7fb; text-decoration: none; overflow-wrap: anywhere; }}
    a:hover, a:focus-visible {{ background: #eaf1fb; outline: none; }}
    .empty {{ color: #64748b; }}
  </style>
</head>
<body>
  <main>
    <h1>西班牙语音频:优先听 CleoYCunquin_mp3（1406开始的），Sarah y Pato 和BenHolly西 </h1>
    <div class="cards">
{card_html}
    </div>
  </main>
</body>
</html>
'''
audio_index.write_text(audio_content, encoding="utf-8")
print(f"已生成 {audio_index.name}，共添加 {len(text_files)} 个 TXT 链接。")
