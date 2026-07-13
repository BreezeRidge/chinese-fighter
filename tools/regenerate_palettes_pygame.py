#!/usr/bin/env python3
"""
使用Pygame重新生成角色调色板精灵图
确保100%兼容Pygame加载
"""
import sys
import os

# 需要pygame
try:
    import pygame
    pygame.init()
except ImportError:
    print("错误: 需要安装pygame")
    print("运行: pip install pygame")
    sys.exit(1)

def apply_color_palette_pygame(source_surface, hue_shift, saturation_factor, value_factor):
    """使用Pygame应用调色板"""
    width, height = source_surface.get_size()
    new_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # 逐像素处理
    for y in range(height):
        for x in range(width):
            color = source_surface.get_at((x, y))
            r, g, b, a = color

            # 跳过透明像素
            if a == 0:
                new_surface.set_at((x, y), color)
                continue

            # 跳过黑色轮廓
            if r < 30 and g < 30 and b < 30:
                new_surface.set_at((x, y), color)
                continue

            # 跳过白色高光
            if r > 225 and g > 225 and b > 225:
                new_surface.set_at((x, y), color)
                continue

            # RGB to HSV
            r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
            max_c = max(r_norm, g_norm, b_norm)
            min_c = min(r_norm, g_norm, b_norm)
            diff = max_c - min_c

            # 计算H
            if diff == 0:
                h = 0
            elif max_c == r_norm:
                h = (60 * ((g_norm - b_norm) / diff) + 360) % 360
            elif max_c == g_norm:
                h = (60 * ((b_norm - r_norm) / diff) + 120) % 360
            else:
                h = (60 * ((r_norm - g_norm) / diff) + 240) % 360

            s = 0 if max_c == 0 else (diff / max_c)
            v = max_c

            # 应用变换
            h = (h + hue_shift) % 360
            s = min(1.0, s * saturation_factor)
            v = min(1.0, v * value_factor)

            # HSV to RGB
            c = v * s
            x_val = c * (1 - abs((h / 60) % 2 - 1))
            m = v - c

            if 0 <= h < 60:
                r_new, g_new, b_new = c, x_val, 0
            elif 60 <= h < 120:
                r_new, g_new, b_new = x_val, c, 0
            elif 120 <= h < 180:
                r_new, g_new, b_new = 0, c, x_val
            elif 180 <= h < 240:
                r_new, g_new, b_new = 0, x_val, c
            elif 240 <= h < 300:
                r_new, g_new, b_new = x_val, 0, c
            else:
                r_new, g_new, b_new = c, 0, x_val

            r_new = int((r_new + m) * 255)
            g_new = int((g_new + m) * 255)
            b_new = int((b_new + m) * 255)

            new_surface.set_at((x, y), (r_new, g_new, b_new, a))

    return new_surface

def regenerate_palettes():
    """使用Pygame重新生成调色板精灵图"""
    print("=" * 60)
    print("使用Pygame重新生成角色调色板精灵图")
    print("=" * 60)

    # 加载原始精灵图
    source_path = "assets/sprites/chibi_fighter_original.png"
    if not os.path.exists(source_path):
        print(f"✗ 原始精灵图不存在: {source_path}")
        return False

    source_sprite = pygame.image.load(source_path)
    print(f"✓ 加载原始精灵图: {source_sprite.get_size()}")

    # 定义调色板
    palettes = {
        "default": (0, 1.0, 1.0, "默认角色（原色）"),
        "shaolin": (30, 1.2, 1.05, "少林僧（橙黄色）"),
        "emei": (200, 1.1, 1.1, "峨眉剑客（青蓝色）"),
        "wudang": (120, 0.9, 1.05, "武当道士（青绿色）"),
    }

    print("\n开始生成...")
    for char_key, (hue, sat, val, desc) in palettes.items():
        print(f"\n[{char_key}] {desc}")
        print(f"  色调偏移: {hue}°, 饱和度: {sat}, 明度: {val}")

        if hue == 0 and sat == 1.0 and val == 1.0:
            # 默认角色直接复制
            new_sprite = source_sprite.copy()
            print(f"  → 使用原始精灵图")
        else:
            new_sprite = apply_color_palette_pygame(source_sprite, hue, sat, val)
            print(f"  → 调色板处理完成")

        # 保存（Pygame保存的PNG格式100%兼容）
        output_path = f"assets/sprites/{char_key}.png"
        pygame.image.save(new_sprite, output_path)

        file_size = os.path.getsize(output_path) / 1024
        print(f"  ✓ 保存: {output_path} ({file_size:.1f}KB)")

        # 验证可以重新加载
        test_load = pygame.image.load(output_path)
        print(f"  ✓ 验证加载: {test_load.get_size()}")

    print("\n" + "=" * 60)
    print("✓ 所有角色精灵图使用Pygame重新生成完成！")
    print("  这些PNG文件保证100%兼容Pygame加载")
    return True

if __name__ == "__main__":
    success = regenerate_palettes()
    sys.exit(0 if success else 1)
