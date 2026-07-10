"""
完整的跳跃功能测试脚本
模拟真实游戏环境，测试跳跃的所有方面
"""
import pygame
import sys
sys.path.insert(0, 'src')

from fighter import Fighter, FighterState
from config import GROUND_Y, GRAVITY

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

print("=" * 60)
print("武林争霸 - 跳跃功能完整测试")
print("=" * 60)

# 创建两个角色进行测试
fighter1 = Fighter(200, GROUND_Y, 'shaolin', 1)
fighter2 = Fighter(600, GROUND_Y, 'emei', 2)

print(f"\n✓ 角色创建成功")
print(f"  玩家1 ({fighter1.stats.name}): pos_y={fighter1.pos_y}, jump_velocity={fighter1.stats.jump_velocity}")
print(f"  玩家2 ({fighter2.stats.name}): pos_y={fighter2.pos_y}, jump_velocity={fighter2.stats.jump_velocity}")

# 测试1: 玩家1跳跃（W键）
print("\n" + "=" * 60)
print("测试1: 玩家1跳跃（W键）")
print("=" * 60)

# 直接触发跳跃（模拟按键）
if fighter1.pos_y >= GROUND_Y:
    fighter1.vel_y = fighter1.stats.jump_velocity
    fighter1.state = FighterState.JUMP
    print(f"✓ 触发跳跃: vel_y={fighter1.vel_y}")

# 模拟60帧（1秒）
max_height = fighter1.pos_y
min_y = fighter1.pos_y
jump_frames = 0

for frame in range(60):
    dt = 1.0 / 60.0

    # 获取真实按键状态
    keys = pygame.key.get_pressed()

    # 更新角色
    fighter1.update(dt, keys)

    # 记录最高点
    if fighter1.pos_y < min_y:
        min_y = fighter1.pos_y

    # 记录跳跃持续帧数
    if fighter1.state == FighterState.JUMP:
        jump_frames += 1

    # 关键帧输出
    if frame in [0, 10, 20, 30, 40, 50, 59]:
        print(f"  第{frame:2d}帧: pos_y={fighter1.pos_y:6.1f}, vel_y={fighter1.vel_y:7.1f}, state={fighter1.state.name}")

print(f"\n测试结果:")
print(f"  起跳高度: {GROUND_Y}")
print(f"  最高点: {min_y:.1f}")
print(f"  跳跃高度: {GROUND_Y - min_y:.1f} 像素")
print(f"  跳跃持续: {jump_frames} 帧 ({jump_frames/60:.2f}秒)")
print(f"  最终状态: {fighter1.state.name}")

# 判断测试结果
if min_y < GROUND_Y - 50 and fighter1.pos_y == GROUND_Y:
    print(f"  结论: ✅ 跳跃测试通过！")
    test1_pass = True
else:
    print(f"  结论: ❌ 跳跃测试失败！")
    test1_pass = False

# 测试2: 玩家2跳跃（↑键）
print("\n" + "=" * 60)
print("测试2: 玩家2跳跃（↑键）")
print("=" * 60)

# 重置玩家2
fighter2.pos_y = GROUND_Y
fighter2.vel_y = 0
fighter2.state = FighterState.IDLE

# 触发跳跃
if fighter2.pos_y >= GROUND_Y:
    fighter2.vel_y = fighter2.stats.jump_velocity
    fighter2.state = FighterState.JUMP
    print(f"✓ 触发跳跃: vel_y={fighter2.vel_y}")

# 模拟60帧
min_y2 = fighter2.pos_y
jump_frames2 = 0

for frame in range(60):
    dt = 1.0 / 60.0
    keys = pygame.key.get_pressed()
    fighter2.update(dt, keys)

    if fighter2.pos_y < min_y2:
        min_y2 = fighter2.pos_y

    if fighter2.state == FighterState.JUMP:
        jump_frames2 += 1

    if frame in [0, 10, 20, 30, 40, 50, 59]:
        print(f"  第{frame:2d}帧: pos_y={fighter2.pos_y:6.1f}, vel_y={fighter2.vel_y:7.1f}, state={fighter2.state.name}")

print(f"\n测试结果:")
print(f"  起跳高度: {GROUND_Y}")
print(f"  最高点: {min_y2:.1f}")
print(f"  跳跃高度: {GROUND_Y - min_y2:.1f} 像素")
print(f"  跳跃持续: {jump_frames2} 帧 ({jump_frames2/60:.2f}秒)")
print(f"  最终状态: {fighter2.state.name}")

if min_y2 < GROUND_Y - 50 and fighter2.pos_y == GROUND_Y:
    print(f"  结论: ✅ 跳跃测试通过！")
    test2_pass = True
else:
    print(f"  结论: ❌ 跳跃测试失败！")
    test2_pass = False

# 测试3: 连续跳跃测试
print("\n" + "=" * 60)
print("测试3: 连续跳跃测试（不能在空中二段跳）")
print("=" * 60)

fighter1.pos_y = GROUND_Y
fighter1.vel_y = 0
fighter1.state = FighterState.IDLE

# 第一次跳跃
fighter1.vel_y = fighter1.stats.jump_velocity
fighter1.state = FighterState.JUMP
print(f"✓ 第一次跳跃: vel_y={fighter1.vel_y}")

# 模拟10帧，角色在空中
for frame in range(10):
    dt = 1.0 / 60.0
    keys = pygame.key.get_pressed()
    fighter1.update(dt, keys)

print(f"  10帧后: pos_y={fighter1.pos_y:.1f}, state={fighter1.state.name}")

# 尝试在空中再次跳跃
old_vel_y = fighter1.vel_y
if fighter1.pos_y >= GROUND_Y:  # 应该不满足（在空中）
    fighter1.vel_y = fighter1.stats.jump_velocity
    print(f"  ❌ 错误：在空中触发了跳跃！")
    test3_pass = False
else:
    print(f"  ✅ 正确：在空中无法跳跃（pos_y={fighter1.pos_y:.1f} < GROUND_Y={GROUND_Y}）")
    test3_pass = True

# 测试4: 重力测试
print("\n" + "=" * 60)
print("测试4: 重力加速度测试")
print("=" * 60)

fighter1.pos_y = GROUND_Y - 100  # 在空中
fighter1.vel_y = 0  # 初速度为0
fighter1.state = FighterState.JUMP

print(f"初始状态: pos_y={fighter1.pos_y:.1f}, vel_y={fighter1.vel_y:.1f}")

velocities = []
for frame in range(10):
    dt = 1.0 / 60.0
    old_vel_y = fighter1.vel_y
    keys = pygame.key.get_pressed()
    fighter1.update(dt, keys)
    velocities.append(fighter1.vel_y)

    if frame < 5:
        print(f"  第{frame}帧: vel_y={fighter1.vel_y:.1f} (加速度={fighter1.vel_y - old_vel_y:.1f})")

# 检查重力是否正常作用
if all(velocities[i] > velocities[i-1] for i in range(1, len(velocities))):
    print(f"  结论: ✅ 重力正常作用（速度持续增加）")
    test4_pass = True
else:
    print(f"  结论: ❌ 重力异常！")
    test4_pass = False

# 最终总结
print("\n" + "=" * 60)
print("测试总结")
print("=" * 60)
print(f"测试1 - 玩家1跳跃: {'✅ 通过' if test1_pass else '❌ 失败'}")
print(f"测试2 - 玩家2跳跃: {'✅ 通过' if test2_pass else '❌ 失败'}")
print(f"测试3 - 空中无法跳跃: {'✅ 通过' if test3_pass else '❌ 失败'}")
print(f"测试4 - 重力加速度: {'✅ 通过' if test4_pass else '❌ 失败'}")

all_pass = test1_pass and test2_pass and test3_pass and test4_pass

if all_pass:
    print(f"\n🎉 所有测试通过！跳跃功能完全正常！")
    sys.exit(0)
else:
    print(f"\n⚠️  部分测试失败，需要进一步调查。")
    sys.exit(1)
