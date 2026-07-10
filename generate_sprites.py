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

            # 绘制角色主体
            draw_character_frame(
                sprite_sheet,
                x, y, size,
                colors,
                anim_name,
                col,
                frames
            )

    return sprite_sheet

def draw_character_frame(surface, x, y, size, colors, anim_name, frame, total_frames):
    """绘制单个角色帧"""
    body_color = colors["body"]
    accent_color = colors["accent"]
    highlight_color = colors["highlight"]

    # 基础人形轮廓
    center_x = x + size // 2
    center_y = y + size // 2

    # 头部（圆形）
    head_radius = size // 6
    head_y = center_y - size // 4
    pygame.draw.circle(surface, body_color, (center_x, head_y), head_radius)
    pygame.draw.circle(surface, highlight_color, (center_x - 2, head_y - 2), 2)  # 眼睛

    # 身体（矩形）
    body_width = size // 3
    body_height = size // 3
    body_rect = pygame.Rect(
        center_x - body_width // 2,
        head_y + head_radius,
        body_width,
        body_height
    )
    pygame.draw.rect(surface, body_color, body_rect)

    # 根据动画类型调整姿势
    if anim_name == "idle":
        # 站立姿势 - 轻微呼吸动画
        offset = int(2 * np.sin(frame / total_frames * np.pi * 2))
        body_rect.y += offset

    elif anim_name == "walk":
        # 行走动画 - 腿部摆动
        leg_offset = int(5 * np.sin(frame / total_frames * np.pi * 2))
        # 左腿
        pygame.draw.line(surface, accent_color,
                        (center_x - 5, body_rect.bottom),
                        (center_x - 5 + leg_offset, body_rect.bottom + size // 4), 3)
        # 右腿
        pygame.draw.line(surface, accent_color,
                        (center_x + 5, body_rect.bottom),
                        (center_x + 5 - leg_offset, body_rect.bottom + size // 4), 3)
        return

    elif anim_name == "jump":
        # 跳跃动画 - 向上姿势
        body_rect.y -= 5
        # 双腿弯曲
        pygame.draw.line(surface, accent_color,
                        (center_x - 5, body_rect.bottom),
                        (center_x - 8, body_rect.bottom + 8), 3)
        pygame.draw.line(surface, accent_color,
                        (center_x + 5, body_rect.bottom),
                        (center_x + 8, body_rect.bottom + 8), 3)
        return

    elif anim_name == "attack_light":
        # 轻攻击 - 手臂前伸
        arm_extend = int(10 * (frame / total_frames))
        pygame.draw.line(surface, highlight_color,
                        (body_rect.right, center_y),
                        (body_rect.right + arm_extend, center_y), 4)

    elif anim_name == "attack_heavy":
        # 重攻击 - 大幅度挥拳
        if frame < total_frames // 2:
            # 蓄力
            pygame.draw.line(surface, accent_color,
                            (body_rect.left, center_y),
                            (body_rect.left - 10, center_y - 5), 4)
        else:
            # 出拳
            pygame.draw.line(surface, highlight_color,
                            (body_rect.right, center_y),
                            (body_rect.right + 15, center_y), 5)

    elif anim_name == "hit":
        # 受击动画 - 后仰
        body_rect.x -= 3
        head_y -= 2

    # 绘制腿部（默认）
    if anim_name not in ["walk", "jump"]:
        pygame.draw.line(surface, accent_color,
                        (center_x - 5, body_rect.bottom),
                        (center_x - 5, body_rect.bottom + size // 4), 3)
        pygame.draw.line(surface, accent_color,
                        (center_x + 5, body_rect.bottom),
                        (center_x + 5, body_rect.bottom + size // 4), 3)

    # 绘制边框
    pygame.draw.rect(surface, (255, 255, 255),
                    pygame.Rect(x, y, size, size), 1)

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
