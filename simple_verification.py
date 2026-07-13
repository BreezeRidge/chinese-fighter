#!/usr/bin/env python3
"""v1.0.0 核心功能验证"""
import sys
sys.path.insert(0, 'src')

print("武林争霸 v1.0.0 - 核心功能验证\n")

# 测试1: 核心模块
print("[1/4] 核心模块...")
try:
    import pygame
    from fighter import Fighter, FighterState
    from ai_system import AIController, AIDifficulty, AIPersonality
    from config import GROUND_Y
    print("  ✅ 核心模块导入成功")
except Exception as e:
    print(f"  ❌ 失败: {e}")
    sys.exit(1)

# 测试2: 角色和精灵图
print("\n[2/4] 角色和精灵图...")
try:
    pygame.init()
    pygame.display.set_mode((100, 100))
    characters = ['default', 'shaolin', 'emei', 'wudang']
    for char in characters:
        Fighter(300, GROUND_Y, char, 1)
    print(f"  ✅ 4个角色精灵图加载成功")
except Exception as e:
    print(f"  ❌ 失败: {e}")
    sys.exit(1)

# 测试3: AI系统（战术增强验证）
print("\n[3/4] AI战术系统...")
try:
    f1 = Fighter(300, GROUND_Y, 'shaolin', 1)
    f2 = Fighter(370, GROUND_Y, 'emei', 2)
    
    # 测试难度分层
    difficulties = {
        AIDifficulty.EASY: 0.5,
        AIDifficulty.MEDIUM: 0.3,
        AIDifficulty.HARD: 0.15
    }
    for diff, expected_time in difficulties.items():
        ai = AIController(diff, AIPersonality.BALANCED)
        assert ai.reaction_time == expected_time, f"{diff.name}反应时间错误"
    
    # 测试连段系统
    ai = AIController(AIDifficulty.HARD, AIPersonality.AGGRESSIVE)
    ai._prev_opp_health = 100
    f1.health = 90  # 模拟掉血
    ai.action_cooldown = 0
    keys = ai.update(0.016, f2, f1)
    assert ai.combo_step > 0, "连段未触发"
    assert ai.combo_window > 0, "连段窗口未激活"
    
    print(f"  ✅ AI战术系统正常（难度分层+连段系统）")
except Exception as e:
    print(f"  ❌ 失败: {e}")
    sys.exit(1)

# 测试4: 战斗逻辑
print("\n[4/4] 战斗逻辑...")
try:
    f1 = Fighter(300, GROUND_Y, 'shaolin', 1)
    f2 = Fighter(400, GROUND_Y, 'emei', 2)
    
    initial_hp = f2.health
    f2.take_damage(10, 1.0)
    assert f2.health < initial_hp, "受伤逻辑失败"
    assert f2.state == FighterState.HIT, "受击状态未触发"
    
    print(f"  ✅ 战斗逻辑正常")
except Exception as e:
    print(f"  ❌ 失败: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✅ 所有核心功能验证通过")
print("✅ v1.0.0 生产就绪")
print("="*50)
pygame.quit()
