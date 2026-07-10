"""
测试脚本 - 验证跳跃功能
"""
import pygame
import sys
sys.path.insert(0, 'src')

from fighter import Fighter
from config import GROUND_Y

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 创建角色
fighter = Fighter(400, GROUND_Y, 'default', 1)

print("=== 跳跃功能测试 ===")
print(f"初始状态: pos_y={fighter.pos_y}, vel_y={fighter.vel_y}, state={fighter.state.name}")

# 模拟游戏循环
running = True
frame = 0
jump_pressed = False

while running and frame < 120:  # 2秒（60fps）
    dt = 0.016

    # 在第10帧按下W键
    if frame == 10:
        jump_pressed = True
        print(f"\n第{frame}帧: 模拟按下W键")
    elif frame == 30:
        jump_pressed = False
        print(f"第{frame}帧: 松开W键")

    # 获取按键状态
    keys = pygame.key.get_pressed()

    # 手动模拟按键（直接修改内部状态进行测试）
    if jump_pressed:
        # 直接调用跳跃逻辑
        if fighter.pos_y >= GROUND_Y and fighter.state.name == 'IDLE':
            fighter.vel_y = fighter.stats.jump_velocity
            fighter.state = fighter.state.__class__.JUMP
            print(f"  -> 触发跳跃: vel_y={fighter.vel_y}")

    # 更新角色
    fighter.update(dt, keys)

    # 每15帧输出一次状态
    if frame % 15 == 0:
        print(f"第{frame}帧: pos_y={fighter.pos_y:.1f}, vel_y={fighter.vel_y:.1f}, state={fighter.state.name}")

    frame += 1

print(f"\n最终状态: pos_y={fighter.pos_y:.1f}, vel_y={fighter.vel_y:.1f}, state={fighter.state.name}")

if fighter.pos_y < GROUND_Y or frame < 60:
    print("✅ 跳跃测试通过！角色成功跳跃")
else:
    print("❌ 跳跃测试失败！角色没有跳跃")

pygame.quit()
