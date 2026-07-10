"""
角色精灵图生成器
使用程序生成简单的像素风格角色（作为真实精灵图的替代）
"""
import pygame
import numpy as np
from pathlib import Path

pygame.init()

# 角色颜色方案
CHARACTER_COLORS = {
    "default": {
        "body": (150, 150, 150),
        "accent": (100, 100, 100),
        "highlight": (200, 200, 200)
    },
    "shaolin": {
        "body": (200, 100, 50),   # 橙红色（少林僧袍）
        "accent": (150, 50, 0),    # 深橙色
        "highlight": (255, 150, 100)  # 亮橙色
    },
    "emei": {
        "body": (100, 150, 200),   # 蓝色（峨眉剑客）
        "accent": (50, 100, 150),   # 深蓝色
        "highlight": (150, 200, 255)  # 亮蓝色
    },
    "wudang": {
        "body": (150, 200, 100),   # 绿色（武当道士）
        "accent": (100, 150, 50),   # 深绿色
        "highlight": (200, 255, 150)  # 亮绿色
    }
}

def create_character_sprite(char_name: str, size: int = 64):
    """
    创建简化的像素风格角色精灵图

    Args:
        char_name: 角色名称
        size: 精灵图大小
    """
    colors = CHARACTER_COLORS.get(char_name, CHARACTER_COLORS["default"])

    # 创建精灵图表面（8帧 x 6个动画）
    sprite_sheet = pygame.Surface((size * 8, size * 6), pygame.SRCALPHA)

    # 定义6种动画
    animations = [
        "idle",          # 行0
        "walk",          # 行1
        "jump",          # 行2
        "attack_light",  # 行3
        "attack_heavy",  # 行4
        "hit"           # 行5
    ]

    for row, anim_name in enumerate(animations):
        if anim_name == "idle":
            frames = 4
        elif anim_name == "walk":
            frames = 6
        elif anim_name == "jump":
            frames = 4
        elif anim_name == "attack_light":
            frames = 4
        elif anim_name == "attack_heavy":
            frames = 6
        else:  # hit
            frames = 3

        for col in range(frames):
            x = col * size
            y = row * size

            # 绘制角色主体（传入角色名称）
            draw_character_frame(
                sprite_sheet,
                x, y, size,
                colors,
                anim_name,
                col,
                frames,
                char_name  # 新增参数
            )

    return sprite_sheet

def draw_character_frame(surface, x, y, size, colors, anim_name, frame, total_frames, char_name):
    """绘制单个角色帧（真实版 - 包含服装、头饰、鞋子）"""
    body_color = colors["body"]
    accent_color = colors["accent"]
    highlight_color = colors["highlight"]

    center_x = x + size // 2
    center_y = y + size // 2

    # === 角色特定装备 ===

    # 1. 头部和头饰
    head_radius = size // 5
    head_y = center_y - size // 4

    # 皮肤颜色
    skin_color = (255, 220, 177)

    # 头部阴影
    pygame.draw.circle(surface, accent_color, (center_x + 2, head_y + 2), head_radius)
    # 头部主体
    pygame.draw.circle(surface, skin_color, (center_x, head_y), head_radius)

    # === 根据角色绘制头饰 ===
    if char_name == "shaolin":
        # 少林僧：僧帽（橙色）
        hat_points = [
            (center_x - head_radius - 3, head_y - head_radius),
            (center_x + head_radius + 3, head_y - head_radius),
            (center_x + head_radius, head_y - head_radius + 5),
            (center_x - head_radius, head_y - head_radius + 5)
        ]
        pygame.draw.polygon(surface, body_color, hat_points)
        pygame.draw.polygon(surface, accent_color, hat_points, 2)
        # 僧帽顶部圆点
        pygame.draw.circle(surface, accent_color, (center_x, head_y - head_radius - 2), 3)

    elif char_name == "emei":
        # 峨眉剑客：剑士头巾（蓝色）
        headband_rect = pygame.Rect(center_x - head_radius - 2, head_y - head_radius + 2,
                                    head_radius * 2 + 4, 6)
        pygame.draw.rect(surface, body_color, headband_rect)
        pygame.draw.rect(surface, highlight_color, headband_rect, 1)
        # 头巾结（右侧飘带）
        ribbon_points = [
            (center_x + head_radius + 2, head_y - head_radius + 4),
            (center_x + head_radius + 8, head_y - head_radius),
            (center_x + head_radius + 8, head_y - head_radius + 8)
        ]
        pygame.draw.polygon(surface, body_color, ribbon_points)

    elif char_name == "wudang":
        # 武当道士：道冠（绿色）
        crown_width = head_radius * 1.5
        crown_height = 8
        crown_rect = pygame.Rect(center_x - crown_width // 2, head_y - head_radius - 2,
                                 crown_width, crown_height)
        pygame.draw.rect(surface, body_color, crown_rect)
        pygame.draw.rect(surface, accent_color, crown_rect, 1)
        # 道冠顶部装饰
        pygame.draw.circle(surface, highlight_color, (center_x, head_y - head_radius - 3), 2)

    else:
        # 默认：简单发型
        pygame.draw.circle(surface, (50, 50, 50), (center_x, head_y - head_radius + 2), head_radius - 2)

    # 眼睛
    eye_y = head_y
    pygame.draw.circle(surface, (0, 0, 0), (center_x - 4, eye_y), 2)
    pygame.draw.circle(surface, (0, 0, 0), (center_x + 4, eye_y), 2)
    pygame.draw.circle(surface, (255, 255, 255), (center_x - 3, eye_y - 1), 1)
    pygame.draw.circle(surface, (255, 255, 255), (center_x + 5, eye_y - 1), 1)

    # 嘴巴
    mouth_y = head_y + 5
    pygame.draw.arc(surface, (0, 0, 0), (center_x - 4, mouth_y - 2, 8, 6), 3.14, 6.28, 2)

    # 2. 身体和服装
    body_width = size // 2.5
    body_height = size // 2.5
    body_y = head_y + head_radius + 2

    # === 根据角色绘制服装 ===
    # 服装阴影
    body_rect_shadow = pygame.Rect(center_x - body_width // 2 + 2, body_y + 2, body_width, body_height)
    pygame.draw.ellipse(surface, accent_color, body_rect_shadow)

    # 服装主体
    body_rect = pygame.Rect(center_x - body_width // 2, body_y, body_width, body_height)
    pygame.draw.ellipse(surface, body_color, body_rect)

    # 服装装饰
    if char_name == "shaolin":
        # 少林僧袍：中间系带
        belt_rect = pygame.Rect(center_x - body_width // 2 + 2, body_y + body_height // 2 - 2,
                               body_width - 4, 4)
        pygame.draw.rect(surface, accent_color, belt_rect)
        # 僧袍纹路
        for i in range(3):
            line_y = body_y + 5 + i * 5
            pygame.draw.line(surface, accent_color,
                           (center_x - 5, line_y), (center_x + 5, line_y), 1)

    elif char_name == "emei":
        # 峨眉剑装：交叉襟
        pygame.draw.line(surface, accent_color,
                        (center_x - body_width // 2 + 3, body_y + 2),
                        (center_x + body_width // 2 - 3, body_y + body_height - 2), 2)
        pygame.draw.line(surface, accent_color,
                        (center_x + body_width // 2 - 3, body_y + 2),
                        (center_x - body_width // 2 + 3, body_y + body_height - 2), 2)
        # 剑带
        pygame.draw.line(surface, highlight_color,
                        (center_x - body_width // 2, body_y + body_height // 2),
                        (center_x + body_width // 2, body_y + body_height // 2), 2)

    elif char_name == "wudang":
        # 武当道袍：太极图案
        tai_chi_center = (center_x, body_y + body_height // 2)
        pygame.draw.circle(surface, (255, 255, 255), tai_chi_center, 5)
        pygame.draw.circle(surface, (0, 0, 0), tai_chi_center, 5, 1)
        pygame.draw.circle(surface, (0, 0, 0), (center_x, tai_chi_center[1] - 2), 2)
        pygame.draw.circle(surface, (255, 255, 255), (center_x, tai_chi_center[1] + 2), 2)

    # 服装高光
    highlight_rect = pygame.Rect(center_x - body_width // 4, body_y + 2, body_width // 3, body_height // 4)
    pygame.draw.ellipse(surface, highlight_color, highlight_rect)

    # 3. 手臂（根据动画调整）
    shoulder_y = body_y + 3
    arm_length = size // 3

    # 袖子颜色（与服装一致）
    sleeve_color = body_color
    hand_color = skin_color

    if anim_name == "attack_light":
        progress = frame / total_frames
        arm_extend = int(15 * progress)
        # 左手臂
        pygame.draw.line(surface, sleeve_color, (center_x - body_width // 2, shoulder_y),
                        (center_x - body_width // 2 - 10, shoulder_y + 5), 6)
        pygame.draw.circle(surface, hand_color, (center_x - body_width // 2 - 10, shoulder_y + 5), 5)
        # 右手臂（出拳）
        pygame.draw.line(surface, sleeve_color, (center_x + body_width // 2, shoulder_y),
                        (center_x + body_width // 2 + arm_extend, shoulder_y), 7)
        pygame.draw.circle(surface, highlight_color, (center_x + body_width // 2 + arm_extend, shoulder_y), 6)
    else:
        offset = int(3 * np.sin(frame / total_frames * np.pi * 2)) if anim_name == "idle" else 0
        # 左手臂
        pygame.draw.line(surface, sleeve_color, (center_x - body_width // 2, shoulder_y),
                        (center_x - body_width // 2, shoulder_y + arm_length + offset), 6)
        pygame.draw.circle(surface, hand_color, (center_x - body_width // 2, shoulder_y + arm_length + offset), 5)
        # 右手臂
        pygame.draw.line(surface, sleeve_color, (center_x + body_width // 2, shoulder_y),
                        (center_x + body_width // 2, shoulder_y + arm_length - offset), 6)
        pygame.draw.circle(surface, hand_color, (center_x + body_width // 2, shoulder_y + arm_length - offset), 5)

    # === 特殊武器 ===
    if char_name == "emei" and anim_name in ["attack_light", "attack_heavy"]:
        # 峨眉剑客：持剑
        sword_x = center_x + body_width // 2 + (15 if anim_name == "attack_light" else 10)
        sword_y = shoulder_y - 5
        # 剑柄
        pygame.draw.rect(surface, accent_color, (sword_x - 2, sword_y, 4, 8))
        # 剑刃
        sword_blade = [
            (sword_x, sword_y - 15),
            (sword_x - 2, sword_y),
            (sword_x + 2, sword_y)
        ]
        pygame.draw.polygon(surface, (200, 200, 200), sword_blade)
        pygame.draw.polygon(surface, (255, 255, 255), sword_blade, 1)

    # 4. 腿部和鞋子
    leg_start_y = body_y + body_height
    leg_length = size // 3.5

    # 裤子颜色
    pants_color = accent_color
    shoe_color = (50, 50, 50)  # 黑色鞋子

    if anim_name == "walk":
        leg_offset = int(8 * np.sin(frame / total_frames * np.pi * 2))
        # 左腿
        pygame.draw.line(surface, pants_color, (center_x - 5, leg_start_y),
                        (center_x - 5 + leg_offset, leg_start_y + leg_length), 7)
        # 左鞋
        shoe_rect = pygame.Rect(center_x - 5 + leg_offset - 6, leg_start_y + leg_length - 3, 12, 6)
        pygame.draw.ellipse(surface, shoe_color, shoe_rect)
        pygame.draw.ellipse(surface, (100, 100, 100), shoe_rect, 1)

        # 右腿
        pygame.draw.line(surface, pants_color, (center_x + 5, leg_start_y),
                        (center_x + 5 - leg_offset, leg_start_y + leg_length), 7)
        # 右鞋
        shoe_rect = pygame.Rect(center_x + 5 - leg_offset - 6, leg_start_y + leg_length - 3, 12, 6)
        pygame.draw.ellipse(surface, shoe_color, shoe_rect)
        pygame.draw.ellipse(surface, (100, 100, 100), shoe_rect, 1)
    else:
        # 左腿
        pygame.draw.line(surface, pants_color, (center_x - 5, leg_start_y),
                        (center_x - 5, leg_start_y + leg_length), 7)
        shoe_rect = pygame.Rect(center_x - 5 - 6, leg_start_y + leg_length - 3, 12, 6)
        pygame.draw.ellipse(surface, shoe_color, shoe_rect)
        pygame.draw.ellipse(surface, (100, 100, 100), shoe_rect, 1)

        # 右腿
        pygame.draw.line(surface, pants_color, (center_x + 5, leg_start_y),
                        (center_x + 5, leg_start_y + leg_length), 7)
        shoe_rect = pygame.Rect(center_x + 5 - 6, leg_start_y + leg_length - 3, 12, 6)
        pygame.draw.ellipse(surface, shoe_color, shoe_rect)
        pygame.draw.ellipse(surface, (100, 100, 100), shoe_rect, 1)

    # === 特殊鞋子 ===
    if char_name == "shaolin":
        # 少林僧：布鞋（添加鞋带）
        pygame.draw.line(surface, accent_color,
                        (center_x - 5 - 3, leg_start_y + leg_length - 1),
                        (center_x - 5 + 3, leg_start_y + leg_length - 1), 1)
        pygame.draw.line(surface, accent_color,
                        (center_x + 5 - 3, leg_start_y + leg_length - 1),
                        (center_x + 5 + 3, leg_start_y + leg_length - 1), 1)

    # 边框
    pygame.draw.rect(surface, (200, 200, 200), pygame.Rect(x, y, size, size), 1)

def generate_all_sprites():
    """生成所有角色的精灵图"""
    output_dir = Path("assets/sprites")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("生成角色精灵图...")

    for char_name in CHARACTER_COLORS.keys():
        print(f"  生成 {char_name}.png...")

        sprite_sheet = create_character_sprite(char_name, size=64)

        # 保存
        output_path = output_dir / f"{char_name}.png"
        pygame.image.save(sprite_sheet, str(output_path))

        print(f"  ✓ 保存到 {output_path}")

    print("\n所有精灵图生成完成！")
    print(f"输出目录: {output_dir.absolute()}")

if __name__ == "__main__":
    generate_all_sprites()
    pygame.quit()
