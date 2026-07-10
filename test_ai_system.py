"""
AI对战系统测试脚本
测试AI的决策、难度、性格
"""
import pygame
import sys
sys.path.insert(0, 'src')

from fighter import Fighter
from ai_system import AIController, AIKeyWrapper, AIDifficulty, AIPersonality
from config import GROUND_Y

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

print("=" * 70)
print("武林争霸 - AI对战系统测试")
print("=" * 70)

# 测试1: AI控制器创建
print("\n测试1: AI控制器创建")
print("-" * 70)

try:
    ai_easy = AIController(AIDifficulty.EASY, AIPersonality.BALANCED)
    print(f"✓ EASY难度AI创建成功")
    print(f"  反应时间: {ai_easy.reaction_time}s")
    print(f"  攻击频率: {ai_easy.attack_frequency}")
    print(f"  格挡概率: {ai_easy.block_chance}")

    ai_medium = AIController(AIDifficulty.MEDIUM, AIPersonality.AGGRESSIVE)
    print(f"✓ MEDIUM难度AI创建成功")

    ai_hard = AIController(AIDifficulty.HARD, AIPersonality.DEFENSIVE)
    print(f"✓ HARD难度AI创建成功")

    test1_pass = True
except Exception as e:
    print(f"✗ AI控制器创建失败: {e}")
    test1_pass = False

# 测试2: AI决策测试
print("\n测试2: AI决策测试")
print("-" * 70)

try:
    # 创建测试角色
    player = Fighter(300, GROUND_Y, 'shaolin', 1)
    ai_fighter = Fighter(900, GROUND_Y, 'emei', 2)

    # 创建AI控制器
    ai = AIController(AIDifficulty.MEDIUM, AIPersonality.BALANCED)

    print(f"✓ 角色创建成功")
    print(f"  玩家: {player.stats.name} at x={player.pos_x}")
    print(f"  AI: {ai_fighter.stats.name} at x={ai_fighter.pos_x}")

    # 测试不同距离的决策
    distances = [250, 150, 80]
    for distance in distances:
        # 设置距离
        ai_fighter.pos_x = player.pos_x + distance

        # 获取AI决策
        decision = ai.update(0.016, ai_fighter, player)

        actions = [k for k, v in decision.items() if v]
        print(f"  距离{distance}px: {', '.join(actions) if actions else '无动作'}")

    test2_pass = True
except Exception as e:
    print(f"✗ AI决策测试失败: {e}")
    import traceback
    traceback.print_exc()
    test2_pass = False

# 测试3: AIKeyWrapper测试
print("\n测试3: AIKeyWrapper测试")
print("-" * 70)

try:
    player = Fighter(300, GROUND_Y, 'shaolin', 1)
    ai_fighter = Fighter(900, GROUND_Y, 'emei', 2)
    ai = AIController(AIDifficulty.MEDIUM, AIPersonality.BALANCED)

    # 创建AIKeyWrapper
    ai_keys = AIKeyWrapper(ai, ai_fighter, player)
    ai_keys.update(0.016)

    print(f"✓ AIKeyWrapper创建成功")

    # 测试按键接口
    test_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_j, pygame.K_k]
    key_names = ["LEFT", "RIGHT", "UP", "J(轻攻)", "K(重攻)"]

    pressed = []
    for key, name in zip(test_keys, key_names):
        if ai_keys[key]:
            pressed.append(name)

    print(f"  当前按键: {', '.join(pressed) if pressed else '无'}")

    test3_pass = True
except Exception as e:
    print(f"✗ AIKeyWrapper测试失败: {e}")
    import traceback
    traceback.print_exc()
    test3_pass = False

# 测试4: 性格差异测试
print("\n测试4: AI性格差异测试")
print("-" * 70)

try:
    player = Fighter(300, GROUND_Y, 'shaolin', 1)
    ai_fighter = Fighter(400, GROUND_Y, 'emei', 2)  # 近距离

    personalities = [
        (AIPersonality.AGGRESSIVE, "进攻型"),
        (AIPersonality.DEFENSIVE, "防守型"),
        (AIPersonality.BALANCED, "平衡型")
    ]

    for personality, name in personalities:
        ai = AIController(AIDifficulty.MEDIUM, personality)

        # 收集10次决策统计
        attack_count = 0
        block_count = 0

        for i in range(10):
            decision = ai.update(0.016, ai_fighter, player)
            if decision.get('attack_light') or decision.get('attack_heavy'):
                attack_count += 1
            if decision.get('block'):
                block_count += 1

        print(f"  {name}: 攻击{attack_count}次, 格挡{block_count}次")

    test4_pass = True
except Exception as e:
    print(f"✗ AI性格测试失败: {e}")
    test4_pass = False

# 测试5: 模拟实战
print("\n测试5: AI实战模拟（30帧）")
print("-" * 70)

try:
    player = Fighter(300, GROUND_Y, 'shaolin', 1)
    ai_fighter = Fighter(900, GROUND_Y, 'emei', 2)
    ai = AIController(AIDifficulty.MEDIUM, AIPersonality.BALANCED)

    # 模拟30帧
    for frame in range(30):
        dt = 0.016

        # AI决策
        ai.update(dt, ai_fighter, player)
        ai_keys = AIKeyWrapper(ai, ai_fighter, player)
        ai_keys.update(dt)

        # 更新AI角色
        keys = pygame.key.get_pressed()
        ai_fighter.update(dt, ai_keys)

        # 关键帧输出
        if frame % 10 == 0:
            distance = abs(ai_fighter.pos_x - player.pos_x)
            print(f"  第{frame}帧: AI位置={ai_fighter.pos_x:.0f}, 距离={distance:.0f}, 状态={ai_fighter.state.name}")

    print(f"✓ AI实战模拟完成")
    test5_pass = True
except Exception as e:
    print(f"✗ AI实战模拟失败: {e}")
    import traceback
    traceback.print_exc()
    test5_pass = False

# 总结
print("\n" + "=" * 70)
print("测试总结")
print("=" * 70)
print(f"测试1 - AI控制器创建: {'✅ 通过' if test1_pass else '❌ 失败'}")
print(f"测试2 - AI决策: {'✅ 通过' if test2_pass else '❌ 失败'}")
print(f"测试3 - AIKeyWrapper: {'✅ 通过' if test3_pass else '❌ 失败'}")
print(f"测试4 - AI性格差异: {'✅ 通过' if test4_pass else '❌ 失败'}")
print(f"测试5 - AI实战模拟: {'✅ 通过' if test5_pass else '❌ 失败'}")

all_pass = all([test1_pass, test2_pass, test3_pass, test4_pass, test5_pass])

if all_pass:
    print(f"\n🎉 所有测试通过！AI对战系统工作正常！")
    sys.exit(0)
else:
    print(f"\n⚠️  部分测试失败，需要进一步调查。")
    sys.exit(1)

pygame.quit()
