#!/usr/bin/env python3
"""
精灵图升级验证脚本
验证新的高质量chibi fighter精灵图是否正确加载
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pygame
from sprite_system import load_character_animations

def test_sprite_upgrade():
    """测试精灵图升级"""
    print("=" * 60)
    print("精灵图升级验证测试")
    print("=" * 60)

    # 初始化pygame
    pygame.init()

    test_results = []

    # 测试1: 检查精灵图文件大小（应该是19KB，而不是旧的7-8KB）
    print("\n[测试1] 检查精灵图文件大小...")
    characters = ["default", "shaolin", "emei", "wudang"]
    for char in characters:
        sprite_path = f"assets/sprites/{char}.png"
        if os.path.exists(sprite_path):
            size_kb = os.path.getsize(sprite_path) / 1024
            if size_kb > 15:  # 新精灵图应该约19KB
                print(f"  ✓ {char}.png: {size_kb:.1f}KB (高质量)")
                test_results.append(True)
            else:
                print(f"  ✗ {char}.png: {size_kb:.1f}KB (旧占位符)")
                test_results.append(False)
        else:
            print(f"  ✗ {char}.png: 文件不存在")
            test_results.append(False)

    # 测试2: 加载精灵图并检查帧数
    print("\n[测试2] 检查动画帧数...")
    try:
        sprite = load_character_animations("shaolin")

        # 检查每个动画的帧数（应该都是8帧）
        animations = ["idle", "walk", "jump", "attack_light", "attack_heavy", "hit"]
        for anim_name in animations:
            if anim_name in sprite.animations:
                frame_count = len(sprite.animations[anim_name].frames)
                if frame_count == 8:
                    print(f"  ✓ {anim_name}: {frame_count}帧 (流畅)")
                    test_results.append(True)
                else:
                    print(f"  ✗ {anim_name}: {frame_count}帧 (应为8帧)")
                    test_results.append(False)
            else:
                print(f"  ✗ {anim_name}: 动画不存在")
                test_results.append(False)

    except Exception as e:
        print(f"  ✗ 加载失败: {e}")
        test_results.append(False)

    # 测试3: 检查动画帧尺寸
    print("\n[测试3] 检查动画帧尺寸...")
    try:
        frame = sprite.get_current_frame()
        width, height = frame.get_size()
        if width == 64 and height == 64:
            print(f"  ✓ 帧尺寸: {width}x{height}像素")
            test_results.append(True)
        else:
            print(f"  ✗ 帧尺寸: {width}x{height}像素 (应为64x64)")
            test_results.append(False)
    except Exception as e:
        print(f"  ✗ 获取帧失败: {e}")
        test_results.append(False)

    # 测试4: 测试动画切换
    print("\n[测试4] 测试动画切换...")
    try:
        sprite.play("walk")
        sprite.update(0.1)
        sprite.play("attack_light")
        sprite.update(0.1)
        print(f"  ✓ 动画切换正常")
        test_results.append(True)
    except Exception as e:
        print(f"  ✗ 动画切换失败: {e}")
        test_results.append(False)

    # 总结
    print("\n" + "=" * 60)
    passed = sum(test_results)
    total = len(test_results)
    print(f"测试结果: {passed}/{total} 通过")

    if passed == total:
        print("✓ 精灵图升级成功！所有测试通过。")
        print("\n升级效果:")
        print("  • 文件大小: 7-8KB → 19KB (高质量)")
        print("  • 动画帧数: 3-6帧 → 8帧 (更流畅)")
        print("  • 动画种类: 6种完整动画")
        print("  • 许可证: CC0 (公共域)")
        return 0
    else:
        print("✗ 部分测试失败，请检查精灵图文件。")
        return 1

if __name__ == "__main__":
    exit_code = test_sprite_upgrade()
    sys.exit(exit_code)
