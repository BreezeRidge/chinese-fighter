"""
角色调色板工具 - 为每个角色生成不同颜色的精灵图
使用HSV颜色空间进行色调偏移，保持亮度和饱和度
"""
import pygame
import sys
import os

def apply_color_palette(source_surface, hue_shift, saturation_factor=1.0, value_factor=1.0):
    """
    应用颜色调色板到精灵图

    Args:
        source_surface: 源精灵图Surface
        hue_shift: 色调偏移（0-360度）
        saturation_factor: 饱和度因子（0.5-1.5）
        value_factor: 明度因子（0.8-1.2）

    Returns:
        新的Surface
    """
    width, height = source_surface.get_size()
    new_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # 逐像素处理
    for x in range(width):
        for y in range(height):
            color = source_surface.get_at((x, y))
            r, g, b, a = color

            # 跳过完全透明的像素
            if a == 0:
                continue

            # 跳过黑色轮廓线（RGB都很低）
            if r < 30 and g < 30 and b < 30:
                new_surface.set_at((x, y), color)
                continue

            # 跳过白色高光（RGB都很高）
            if r > 225 and g > 225 and b > 225:
                new_surface.set_at((x, y), color)
                continue

            # 转换到HSV色彩空间
            r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
            max_c = max(r_norm, g_norm, b_norm)
            min_c = min(r_norm, g_norm, b_norm)
            diff = max_c - min_c

            # 计算色调H
            if diff == 0:
                h = 0
            elif max_c == r_norm:
                h = (60 * ((g_norm - b_norm) / diff) + 360) % 360
            elif max_c == g_norm:
                h = (60 * ((b_norm - r_norm) / diff) + 120) % 360
            else:
                h = (60 * ((r_norm - g_norm) / diff) + 240) % 360

            # 计算饱和度S
            s = 0 if max_c == 0 else (diff / max_c)

            # 计算明度V
            v = max_c

            # 应用调色板变换
            h = (h + hue_shift) % 360
            s = min(1.0, s * saturation_factor)
            v = min(1.0, v * value_factor)

            # 转换回RGB
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


def generate_character_palettes():
    """为所有角色生成调色板精灵图"""
    pygame.init()

    # 加载原始精灵图
    source_path = "assets/sprites/chibi_fighter_original.png"
    if not os.path.exists(source_path):
        print(f"✗ 原始精灵图不存在: {source_path}")
        return False

    source_sprite = pygame.image.load(source_path)
    print(f"✓ 加载原始精灵图: {source_sprite.get_size()}")

    # 定义角色调色板
    character_palettes = {
        "default": {
            "hue_shift": 0,
            "saturation": 1.0,
            "value": 1.0,
            "description": "默认角色（原色）"
        },
        "shaolin": {
            "hue_shift": 30,      # 偏橙色（力量感）
            "saturation": 1.2,    # 提高饱和度
            "value": 1.05,        # 稍微提亮
            "description": "少林僧（橙黄色-金刚之力）"
        },
        "emei": {
            "hue_shift": 200,     # 偏青蓝色（灵动感）
            "saturation": 1.1,    # 适度饱和
            "value": 1.1,         # 提亮（清爽）
            "description": "峨眉剑客（青蓝色-灵动之气）"
        },
        "wudang": {
            "hue_shift": 120,     # 偏绿色（道法自然）
            "saturation": 0.9,    # 降低饱和度（淡雅）
            "value": 1.05,        # 稍微提亮
            "description": "武当道士（青绿色-道法自然）"
        }
    }

    # 生成每个角色的精灵图
    print("\n开始生成角色调色板精灵图...")
    print("=" * 60)

    for char_key, palette in character_palettes.items():
        print(f"\n[{char_key}] {palette['description']}")
        print(f"  色调偏移: {palette['hue_shift']}°")
        print(f"  饱和度: {palette['saturation']}")
        print(f"  明度: {palette['value']}")

        # 应用调色板
        if palette['hue_shift'] == 0 and palette['saturation'] == 1.0 and palette['value'] == 1.0:
            # 默认角色直接复制
            new_sprite = source_sprite.copy()
            print(f"  → 使用原始精灵图")
        else:
            new_sprite = apply_color_palette(
                source_sprite,
                palette['hue_shift'],
                palette['saturation'],
                palette['value']
            )
            print(f"  → 调色板应用完成")

        # 保存
        output_path = f"assets/sprites/{char_key}.png"
        pygame.image.save(new_sprite, output_path)
        file_size = os.path.getsize(output_path) / 1024
        print(f"  ✓ 保存: {output_path} ({file_size:.1f}KB)")

    print("\n" + "=" * 60)
    print("✓ 所有角色调色板精灵图生成完成！")
    return True


if __name__ == "__main__":
    success = generate_character_palettes()
    sys.exit(0 if success else 1)
