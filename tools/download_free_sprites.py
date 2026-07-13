#!/usr/bin/env python3
"""
免费精灵图资源下载和集成工具
自动下载Kenney资源并集成到游戏
"""
import os
import sys
import urllib.request
import zipfile
import shutil

print("=" * 70)
print("免费精灵图资源下载和集成工具")
print("=" * 70)
print()

# Kenney资源直接下载链接
KENNEY_URLS = {
    "platformer": "https://kenney.nl/content/3-assets/508-platformer-pack-redux-360-assets/kenney_platformer-pack-redux.zip",
    "topdown": "https://kenney.nl/content/3-assets/137-top-down-shooter/topdown-shooter.zip",
}

def download_file(url, output_path):
    """下载文件"""
    print(f"下载: {url}")
    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"✓ 下载完成: {output_path}")
        return True
    except Exception as e:
        print(f"✗ 下载失败: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """解压ZIP文件"""
    print(f"解压: {zip_path}")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✓ 解压完成: {extract_to}")
        return True
    except Exception as e:
        print(f"✗ 解压失败: {e}")
        return False

def find_character_sprites(extract_dir):
    """查找角色精灵图"""
    print("查找角色精灵图...")
    sprites = []

    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith('.png'):
                # 查找包含 "player" 或 "character" 的文件
                if 'player' in file.lower() or 'character' in file.lower():
                    sprites.append(os.path.join(root, file))

    return sprites

def main():
    """主函数"""

    # 1. 选择资源包
    print("可用资源包:")
    print("  1. Platformer Pack Redux")
    print("  2. Top Down Shooter")
    print()

    choice = input("选择资源包 (1/2) [1]: ").strip() or "1"

    if choice == "1":
        url = KENNEY_URLS["platformer"]
        pack_name = "platformer"
    else:
        url = KENNEY_URLS["topdown"]
        pack_name = "topdown"

    # 2. 下载
    temp_dir = "/tmp/kenney_download"
    os.makedirs(temp_dir, exist_ok=True)

    zip_path = os.path.join(temp_dir, f"{pack_name}.zip")

    if not download_file(url, zip_path):
        print("\n提示: 自动下载失败，请手动下载:")
        print(f"  1. 访问: https://kenney.nl/assets")
        print(f"  2. 搜索: {pack_name}")
        print(f"  3. 点击Download下载ZIP")
        print(f"  4. 解压后查看 PNG 文件")
        sys.exit(1)

    # 3. 解压
    extract_dir = os.path.join(temp_dir, pack_name)
    if not extract_zip(zip_path, extract_dir):
        sys.exit(1)

    # 4. 查找精灵图
    sprites = find_character_sprites(extract_dir)

    if not sprites:
        print("\n✗ 未找到角色精灵图")
        print(f"请手动查看: {extract_dir}")
        sys.exit(1)

    print(f"\n✓ 找到 {len(sprites)} 个精灵图:")
    for i, sprite in enumerate(sprites[:10], 1):  # 只显示前10个
        print(f"  {i}. {os.path.basename(sprite)}")

    # 5. 选择并复制
    print("\n" + "=" * 70)
    print("集成到游戏")
    print("=" * 70)

    if len(sprites) >= 4:
        print("\n将自动选择前4个精灵图作为4个角色")
        confirm = input("继续? (y/n) [y]: ").strip().lower() or "y"

        if confirm == "y":
            # 备份现有精灵图
            backup_dir = "assets/sprites_backup_kenney"
            if os.path.exists("assets/sprites"):
                os.makedirs(backup_dir, exist_ok=True)
                for f in os.listdir("assets/sprites"):
                    if f.endswith('.png'):
                        shutil.copy(
                            os.path.join("assets/sprites", f),
                            os.path.join(backup_dir, f)
                        )
                print(f"✓ 备份完成: {backup_dir}")

            # 复制新精灵图
            characters = ["default", "shaolin", "emei", "wudang"]
            for i, char in enumerate(characters):
                if i < len(sprites):
                    dest = f"assets/sprites/{char}.png"
                    shutil.copy(sprites[i], dest)
                    print(f"✓ 复制: {os.path.basename(sprites[i])} -> {char}.png")

            print("\n" + "=" * 70)
            print("✓ 集成完成!")
            print("=" * 70)
            print("\n下一步:")
            print("  1. 运行游戏测试: python3 src/main.py")
            print("  2. 如果需要，应用调色板差异化:")
            print("     python3 tools/regenerate_palettes_pygame.py")
    else:
        print(f"\n✗ 精灵图数量不足 (需要4个，找到{len(sprites)}个)")
        print(f"请手动选择: {extract_dir}")

if __name__ == "__main__":
    main()
