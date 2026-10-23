#!/usr/bin/env python3
"""扫描脚本所在目录的 HTML 页面，并更新 导航.html。"""
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
