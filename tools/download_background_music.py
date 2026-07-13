#!/usr/bin/env python3
"""
背景音乐资源搜索和下载工具
为格斗游戏寻找合适的CC0授权背景音乐
"""
import os

print("=" * 70)
print("背景音乐资源搜索指南")
print("=" * 70)
print()

# 推荐的音乐资源来源
MUSIC_SOURCES = {
    "Incompetech": {
        "url": "https://incompetech.com/music/royalty-free/",
        "license": "CC-BY 3.0（需署名）",
        "quality": "专业级",
        "genres": ["Action", "Aggressive", "Epic", "Rock"],
        "description": "Kevin MacLeod的免版税音乐库",
    },
    "FreePD": {
        "url": "https://freepd.com",
        "license": "CC0（公共域）",
        "quality": "高质量",
        "genres": ["Action", "Epic", "Cinematic"],
        "description": "完全免费的公共域音乐",
    },
    "OpenGameArt": {
        "url": "https://opengameart.org/art-search-advanced?keys=&field_art_type_tid=12",
        "license": "CC0 / CC-BY",
        "quality": "游戏专用",
        "genres": ["Chiptune", "Battle", "Menu"],
        "description": "游戏音乐社区资源",
    },
}

print("推荐音乐资源来源:")
print()
for name, info in MUSIC_SOURCES.items():
    print(f"{name}:")
    print(f"  URL: {info['url']}")
    print(f"  授权: {info['license']}")
    print(f"  质量: {info['quality']}")
    print(f"  风格: {', '.join(info['genres'])}")
    print(f"  说明: {info['description']}")
    print()

print("=" * 70)
print("需要的音乐类型:")
print("=" * 70)
print()

MUSIC_REQUIREMENTS = {
    "menu": {
        "description": "菜单背景音乐",
        "mood": "轻松、悠闲、神秘",
        "tempo": "中速（90-110 BPM）",
        "duration": "循环播放",
        "style": "电子、摇滚、中国风",
    },
    "battle": {
        "description": "战斗背景音乐",
        "mood": "紧张、激烈、动感",
        "tempo": "快速（120-140 BPM）",
        "duration": "循环播放",
        "style": "激进摇滚、电子、史诗",
    },
    "victory": {
        "description": "胜利音乐",
        "mood": "欢快、胜利、短促",
        "tempo": "任意",
        "duration": "5-10秒",
        "style": "凯旋音效、号角",
    },
}

for key, info in MUSIC_REQUIREMENTS.items():
    print(f"• {key}.ogg - {info['description']}")
    print(f"  氛围: {info['mood']}")
    print(f"  节奏: {info['tempo']}")
    print(f"  时长: {info['duration']}")
    print(f"  风格: {info['style']}")
    print()

print("=" * 70)
print("推荐曲目（Incompetech）:")
print("=" * 70)
print()

RECOMMENDED_TRACKS = [
    {
        "name": "Dances and Dames",
        "type": "battle",
        "style": "快节奏动作音乐",
        "url": "https://incompetech.com/music/royalty-free/music.html",
    },
    {
        "name": "Pepper Gun",
        "type": "battle",
        "style": "激进电子音乐",
        "url": "https://incompetech.com/music/royalty-free/music.html",
    },
    {
        "name": "Thatched Villagers",
        "type": "menu",
        "style": "悠闲背景音乐",
        "url": "https://incompetech.com/music/royalty-free/music.html",
    },
]

for track in RECOMMENDED_TRACKS:
    print(f"曲目: {track['name']}")
    print(f"  用途: {track['type']}")
    print(f"  风格: {track['style']}")
    print(f"  链接: {track['url']}")
    print()

print("=" * 70)
print("下载步骤:")
print("=" * 70)
print()
print("1. 访问音乐资源网站")
print("2. 使用搜索/筛选功能找合适音乐")
print("   - 关键词: action, battle, fight, epic, menu")
print("   - 授权: CC0 或 CC-BY")
print("3. 试听音乐（确认适合格斗游戏氛围）")
print("4. 下载MP3格式")
print("5. 转换为OGG格式（推荐）:")
print("   ffmpeg -i input.mp3 -c:a libvorbis -q:a 4 output.ogg")
print("6. 重命名并放入 assets/music/ 目录:")
print("   - menu.ogg")
print("   - battle.ogg")
print("   - victory.ogg")
print()

print("=" * 70)
print("文件命名规范:")
print("=" * 70)
print()
print("assets/music/")
print("  ├── menu.ogg      # 菜单背景音乐（循环）")
print("  ├── battle.ogg    # 战斗背景音乐（循环）")
print("  └── victory.ogg   # 胜利音乐（短促）")
print()

print("=" * 70)
print("授权注意事项:")
print("=" * 70)
print()
print("• CC0: 无需署名，完全自由使用")
print("• CC-BY: 需要署名作者，在游戏积分中添加:")
print("  \"Music by Kevin MacLeod (incompetech.com)\"")
print("  \"Licensed under Creative Commons: By Attribution 3.0\"")
print()

print("=" * 70)
