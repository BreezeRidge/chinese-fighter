#!/usr/bin/env python3
"""
项目验证工具
验证所有文件、资源和配置的完整性
"""
import os
import sys

def check_file_exists(path, description):
    """检查文件是否存在"""
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    size = ""
    if exists and os.path.isfile(path):
        size_kb = os.path.getsize(path) / 1024
        size = f" ({size_kb:.1f}KB)"
    print(f"  {status} {description}: {path}{size}")
    return exists

def verify_project():
    """验证项目完整性"""
    print("=" * 70)
    print("武林争霸 - 项目完整性验证")
    print("=" * 70)

    results = []

    # 1. 核心代码文件
    print("\n[1] 核心代码文件:")
    core_files = [
        ("src/main.py", "游戏主程序"),
        ("src/fighter.py", "角色系统"),
        ("src/sprite_system.py", "精灵图系统"),
        ("src/special_moves.py", "特殊招式"),
        ("src/sound.py", "音效系统"),
        ("src/ai_system.py", "AI系统"),
        ("src/ui.py", "UI系统"),
        ("src/config.py", "配置文件"),
    ]
    for path, desc in core_files:
        results.append(check_file_exists(path, desc))

    # 2. 精灵图资源
    print("\n[2] 精灵图资源:")
    sprite_files = [
        ("assets/sprites/chibi_fighter_original.png", "原始精灵图"),
        ("assets/sprites/default.png", "默认角色"),
        ("assets/sprites/shaolin.png", "少林僧"),
        ("assets/sprites/emei.png", "峨眉剑客"),
        ("assets/sprites/wudang.png", "武当道士"),
    ]
    for path, desc in sprite_files:
        results.append(check_file_exists(path, desc))

    # 3. 音效资源
    print("\n[3] 音效资源:")
    audio_files = [
        ("assets/audio/hit_light.ogg", "轻攻击音效"),
        ("assets/audio/hit_heavy.ogg", "重攻击音效"),
        ("assets/audio/hit_special.ogg", "特殊招式音效"),
        ("assets/audio/block.ogg", "格挡音效"),
        ("assets/audio/jump.ogg", "跳跃音效"),
        ("assets/audio/buff.ogg", "增益音效"),
        ("assets/audio/ko.ogg", "KO音效"),
    ]
    for path, desc in audio_files:
        results.append(check_file_exists(path, desc))

    # 4. 工具脚本
    print("\n[4] 工具脚本:")
    tool_files = [
        ("tools/generate_character_palettes_pure.py", "纯Python调色板工具"),
        ("tools/regenerate_palettes_pygame.py", "Pygame调色板工具"),
        ("tools/download_sound_effects.py", "音效下载指南"),
        ("tools/fix_character_loading.sh", "角色加载修复脚本"),
    ]
    for path, desc in tool_files:
        results.append(check_file_exists(path, desc))

    # 5. 文档文件
    print("\n[5] 文档文件:")
    doc_files = [
        ("README.md", "项目README"),
        ("CHANGELOG.md", "变更日志"),
        ("docs/角色加载问题诊断报告.md", "加载问题诊断"),
        ("docs/角色加载问题-根本原因和修复.md", "加载问题修复"),
        ("docs/永久修复执行指南.md", "永久修复指南"),
        ("docs/会话工作总结报告.md", "会话总结"),
        ("assets/audio/README.md", "音效资源说明"),
    ]
    for path, desc in doc_files:
        results.append(check_file_exists(path, desc))

    # 6. 配置和启动脚本
    print("\n[6] 配置和脚本:")
    config_files = [
        ("run.sh", "游戏启动脚本"),
    ]
    for path, desc in config_files:
        results.append(check_file_exists(path, desc))

    # 统计结果
    total = len(results)
    passed = sum(results)
    failed = total - passed

    print("\n" + "=" * 70)
    print(f"验证结果: {passed}/{total} 通过")

    if failed > 0:
        print(f"⚠️  {failed} 个文件缺失")
    else:
        print("✅ 所有文件完整")

    # 额外检查
    print("\n[额外检查]")

    # 检查Git状态
    import subprocess
    try:
        result = subprocess.run(['git', 'status', '--porcelain'],
                               capture_output=True, text=True)
        if result.stdout.strip():
            print("  ⚠️  工作区有未提交的更改")
        else:
            print("  ✓ Git工作区干净")
    except:
        print("  - Git状态检查失败")

    # 检查版本标签
    try:
        result = subprocess.run(['git', 'tag'],
                               capture_output=True, text=True)
        tags = result.stdout.strip().split('\n')
        print(f"  ✓ Git标签数量: {len(tags)}")
        if tags:
            print(f"    最新标签: {tags[-1]}")
    except:
        print("  - Git标签检查失败")

    print("\n" + "=" * 70)

    return passed == total

if __name__ == "__main__":
    success = verify_project()
    sys.exit(0 if success else 1)
