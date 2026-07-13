#!/usr/bin/env python3
"""
音效资源搜索和下载工具
搜索开源CC0授权的格斗游戏音效
"""
import os

# Kenney.nl 是最可靠的CC0游戏资源来源
KENNEY_IMPACT_SOUNDS = "https://kenney.nl/assets/impact-sounds"
KENNEY_DIGITAL_AUDIO = "https://kenney.nl/assets/digital-audio"

# 我们需要的音效类型
SOUND_REQUIREMENTS = {
    "hit_light": "轻攻击音效 - 短促的打击声",
    "hit_heavy": "重攻击音效 - 沉重的撞击声",
    "hit_special": "特殊招式音效 - 特殊效果音",
    "block": "格挡音效 - 防御音",
    "jump": "跳跃音效 - 短促的起跳声",
    "buff": "增益音效 - 强化音效",
    "ko": "KO音效 - 击倒音效",
}

print("=" * 60)
print("音效资源搜索指南")
print("=" * 60)
print()
print("推荐音效资源来源:")
print()
print("1. Kenney.nl (CC0授权)")
print(f"   • Impact Sounds: {KENNEY_IMPACT_SOUNDS}")
print(f"   • Digital Audio: {KENNEY_DIGITAL_AUDIO}")
print(f"   • 授权: CC0 (公共域)")
print(f"   • 质量: 专业游戏音效")
print()
print("2. OpenGameArt.org")
print("   • 搜索: 'impact' 'hit' 'punch' 'kick'")
print("   • 筛选: CC0或CC-BY授权")
print()
print("3. Freesound.org")
print("   • 搜索: 'punch' 'hit' 'impact'")
print("   • 筛选: CC0授权")
print()
print("=" * 60)
print("需要的音效类型:")
print("=" * 60)
for sound_name, description in SOUND_REQUIREMENTS.items():
    print(f"  • {sound_name}: {description}")
print()
print("=" * 60)
print("下载步骤:")
print("=" * 60)
print("1. 访问 Kenney.nl Impact Sounds")
print("2. 点击 'Download' 下载音效包")
print("3. 解压缩到临时文件夹")
print("4. 选择合适的音效文件")
print("5. 重命名并复制到 assets/audio/ 目录")
print()
print("音效文件命名规范:")
print("  hit_light.wav  - 轻攻击")
print("  hit_heavy.wav  - 重攻击")
print("  hit_special.wav - 特殊招式")
print("  block.wav      - 格挡")
print("  jump.wav       - 跳跃")
print("  buff.wav       - 增益")
print("  ko.wav         - KO")
print()
print("=" * 60)
