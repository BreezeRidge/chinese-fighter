"""
角色调色板工具 - 使用纯Python标准库为每个角色生成不同颜色的精灵图
读取PNG文件并应用HSV色调偏移
"""
import struct
import zlib
import sys
import os


def read_png(filepath):
    """读取PNG文件，返回(width, height, pixels)"""
    with open(filepath, 'rb') as f:
        # 验证PNG签名
        signature = f.read(8)
        if signature != b'\x89PNG\r\n\x1a\n':
            raise ValueError("不是有效的PNG文件")

        width = height = None
        pixels = []
        idat_data = b''

        # 读取所有chunk
        while True:
            chunk_length_bytes = f.read(4)
            if len(chunk_length_bytes) < 4:
                break

            chunk_length = struct.unpack('>I', chunk_length_bytes)[0]
            chunk_type = f.read(4)
            chunk_data = f.read(chunk_length)
            chunk_crc = f.read(4)

            if chunk_type == b'IHDR':
                width, height = struct.unpack('>II', chunk_data[:8])
            elif chunk_type == b'IDAT':
                idat_data += chunk_data
            elif chunk_type == b'IEND':
                break

        # 解压图像数据
        raw_data = zlib.decompress(idat_data)

        # 解析像素（假设RGBA格式，每行有1字节滤波类型）
        pixels = []
        bytes_per_pixel = 4  # RGBA
        stride = width * bytes_per_pixel + 1  # +1 for filter byte

        for y in range(height):
            row_start = y * stride
            filter_type = raw_data[row_start]
            row_data = raw_data[row_start + 1:row_start + stride]

            row_pixels = []
            for x in range(width):
                pixel_start = x * bytes_per_pixel
                r = row_data[pixel_start]
                g = row_data[pixel_start + 1]
                b = row_data[pixel_start + 2]
                a = row_data[pixel_start + 3]
                row_pixels.append((r, g, b, a))
            pixels.append(row_pixels)

        return width, height, pixels


def write_png(filepath, width, height, pixels):
    """写入PNG文件"""
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = zlib.crc32(chunk) & 0xffffffff
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', crc)

    with open(filepath, 'wb') as f:
        # PNG签名
        f.write(b'\x89PNG\r\n\x1a\n')

        # IHDR chunk
        ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)  # 6 = RGBA
        f.write(make_chunk(b'IHDR', ihdr_data))

        # IDAT chunk - 准备像素数据
        raw_data = b''
        for row in pixels:
            raw_data += b'\x00'  # 无滤波
            for r, g, b, a in row:
                raw_data += bytes([r, g, b, a])

        compressed = zlib.compress(raw_data, 9)
        f.write(make_chunk(b'IDAT', compressed))

        # IEND chunk
        f.write(make_chunk(b'IEND', b''))


def rgb_to_hsv(r, g, b):
    """RGB转HSV（输入0-255，输出H:0-1, S:0-1, V:0-1）"""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c

    if diff == 0:
        h = 0
    elif max_c == r:
        h = ((g - b) / diff) % 6
    elif max_c == g:
        h = ((b - r) / diff) + 2
    else:
        h = ((r - g) / diff) + 4

    h = h / 6.0
    s = 0 if max_c == 0 else diff / max_c
    v = max_c

    return h, s, v


def hsv_to_rgb(h, s, v):
    """HSV转RGB（输入H:0-1, S:0-1, V:0-1，输出0-255）"""
    c = v * s
    x = c * (1 - abs((h * 6) % 2 - 1))
    m = v - c

    if h < 1/6:
        r, g, b = c, x, 0
    elif h < 2/6:
        r, g, b = x, c, 0
    elif h < 3/6:
        r, g, b = 0, c, x
    elif h < 4/6:
        r, g, b = 0, x, c
    elif h < 5/6:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    r = int((r + m) * 255)
    g = int((g + m) * 255)
    b = int((b + m) * 255)

    return r, g, b


def apply_color_palette(pixels, hue_shift, saturation_factor, value_factor):
    """应用调色板到像素数据"""
    new_pixels = []

    for row in pixels:
        new_row = []
        for r, g, b, a in row:
            # 跳过完全透明的像素
            if a == 0:
                new_row.append((r, g, b, a))
                continue

            # 跳过黑色轮廓线
            if r < 30 and g < 30 and b < 30:
                new_row.append((r, g, b, a))
                continue

            # 跳过白色高光
            if r > 225 and g > 225 and b > 225:
                new_row.append((r, g, b, a))
                continue

            # 转换到HSV并应用变换
            h, s, v = rgb_to_hsv(r, g, b)
            h = (h + hue_shift) % 1.0
            s = min(1.0, s * saturation_factor)
            v = min(1.0, v * value_factor)

            # 转换回RGB
            r_new, g_new, b_new = hsv_to_rgb(h, s, v)
            new_row.append((r_new, g_new, b_new, a))

        new_pixels.append(new_row)

    return new_pixels


def generate_character_palettes():
    """为所有角色生成调色板精灵图"""

    # 加载原始精灵图
    source_path = "assets/sprites/chibi_fighter_original.png"
    if not os.path.exists(source_path):
        print(f"✗ 原始精灵图不存在: {source_path}")
        return False

    print(f"✓ 读取原始精灵图: {source_path}")
    try:
        width, height, source_pixels = read_png(source_path)
        print(f"  尺寸: {width}×{height}像素")
    except Exception as e:
        print(f"✗ 读取失败: {e}")
        return False

    # 定义角色调色板
    character_palettes = {
        "default": {
            "hue_shift": 0.0,
            "saturation": 1.0,
            "value": 1.0,
            "description": "默认角色（原色）"
        },
        "shaolin": {
            "hue_shift": 30 / 360,    # 30度 → 橙色
            "saturation": 1.2,
            "value": 1.05,
            "description": "少林僧（橙黄色-金刚之力）"
        },
        "emei": {
            "hue_shift": 200 / 360,   # 200度 → 青蓝色
            "saturation": 1.1,
            "value": 1.1,
            "description": "峨眉剑客（青蓝色-灵动之气）"
        },
        "wudang": {
            "hue_shift": 120 / 360,   # 120度 → 绿色
            "saturation": 0.9,
            "value": 1.05,
            "description": "武当道士（青绿色-道法自然）"
        }
    }

    # 生成每个角色的精灵图
    print("\n开始生成角色调色板精灵图...")
    print("=" * 60)

    for char_key, palette in character_palettes.items():
        print(f"\n[{char_key}] {palette['description']}")
        print(f"  色调偏移: {palette['hue_shift'] * 360:.0f}°")
        print(f"  饱和度因子: {palette['saturation']}")
        print(f"  明度因子: {palette['value']}")

        # 应用调色板
        if palette['hue_shift'] == 0.0 and palette['saturation'] == 1.0 and palette['value'] == 1.0:
            new_pixels = source_pixels
            print(f"  → 使用原始精灵图")
        else:
            new_pixels = apply_color_palette(
                source_pixels,
                palette['hue_shift'],
                palette['saturation'],
                palette['value']
            )
            print(f"  → 调色板应用完成")

        # 保存
        output_path = f"assets/sprites/{char_key}.png"
        try:
            write_png(output_path, width, height, new_pixels)
            file_size = os.path.getsize(output_path) / 1024
            print(f"  ✓ 保存: {output_path} ({file_size:.1f}KB)")
        except Exception as e:
            print(f"  ✗ 保存失败: {e}")
            return False

    print("\n" + "=" * 60)
    print("✓ 所有角色调色板精灵图生成完成！")
    print("\n颜色方案:")
    print("  • 默认角色: 原色（灰褐色基调）")
    print("  • 少林僧: 橙黄色（象征金刚之力）")
    print("  • 峨眉剑客: 青蓝色（象征灵动之气）")
    print("  • 武当道士: 青绿色（象征道法自然）")
    return True


if __name__ == "__main__":
    success = generate_character_palettes()
    sys.exit(0 if success else 1)
