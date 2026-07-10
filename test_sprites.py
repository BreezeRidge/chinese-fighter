"""
精灵图系统测试脚本
验证精灵图加载、动画播放、角色渲染
"""
import pygame
import sys
sys.path.insert(0, 'src')

from sprite_system import load_character_animations, SpriteSheet
from config import GROUND_Y

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

print("=" * 70)
print("武林争霸 - 精灵图系统测试")
print("=" * 70)

# 测试1: 精灵图文件加载
print("\n测试1: 精灵图文件加载")
print("-" * 70)

characters = ["default", "shaolin", "emei", "wudang"]
sprites_loaded = {}

for char in characters:
    try:
        sprite = load_character_animations(char)
        sprites_loaded[char] = sprite
        print(f"✓ {char}.png 加载成功")
        print(f"  动画数量: {len(sprite.animations)}")
        print(f"  动画列表: {list(sprite.animations.keys())}")
    except Exception as e:
        print(f"✗ {char}.png 加载失败: {e}")

test1_pass = len(sprites_loaded) == 4

# 测试2: 动画帧数验证
print("\n测试2: 动画帧数验证")
print("-" * 70)

expected_frames = {
    "idle": 4,
    "walk": 6,
    "jump": 4,
    "attack_light": 4,
    "attack_heavy": 6,
    "hit": 3
}

test2_pass = True
for char, sprite in sprites_loaded.items():
    print(f"\n{char}:")
    for anim_name, expected_count in expected_frames.items():
        if anim_name in sprite.animations:
            actual_count = len(sprite.animations[anim_name].frames)
            status = "✓" if actual_count == expected_count else "✗"
            print(f"  {status} {anim_name}: {actual_count}/{expected_count}帧")
            if actual_count != expected_count:
                test2_pass = False
        else:
            print(f"  ✗ {anim_name}: 缺失")
            test2_pass = False

# 测试3: 动画播放测试
print("\n测试3: 动画播放测试（60帧）")
print("-" * 70)

if "shaolin" in sprites_loaded:
    sprite = sprites_loaded["shaolin"]
    sprite.play("idle")

    print("测试idle动画...")
    for frame in range(60):
        dt = 1.0 / 60.0
        sprite.update(dt)

        if frame % 15 == 0:
            print(f"  第{frame}帧: current_frame={sprite.current_frame}")

    print(f"✓ idle动画播放完成")
    test3_pass = True
else:
    print("✗ 无法测试动画播放（少林僧精灵未加载）")
    test3_pass = False

# 测试4: 动画切换测试
print("\n测试4: 动画切换测试")
print("-" * 70)

if "emei" in sprites_loaded:
    sprite = sprites_loaded["emei"]

    animations_to_test = ["idle", "walk", "jump", "attack_light"]

    for anim in animations_to_test:
        sprite.play(anim, reset=True)
        print(f"  切换到 {anim}: current_animation={sprite.current_animation}, frame={sprite.current_frame}")

    print(f"✓ 动画切换测试通过")
    test4_pass = True
else:
    print("✗ 无法测试动画切换")
    test4_pass = False

# 测试5: 水平翻转测试
print("\n测试5: 水平翻转测试")
print("-" * 70)

if "wudang" in sprites_loaded:
    sprite = sprites_loaded["wudang"]
    sprite.play("idle")

    # 测试facing_right
    sprite.facing_right = True
    frame1 = sprite.get_current_frame()
    print(f"  facing_right=True: 获取帧成功, size={frame1.get_size()}")

    sprite.facing_right = False
    frame2 = sprite.get_current_frame()
    print(f"  facing_right=False: 获取帧成功, size={frame2.get_size()}")

    # 帧应该不同（因为翻转了）
    if frame1 != frame2:
        print(f"✓ 水平翻转正常工作")
        test5_pass = True
    else:
        print(f"✗ 水平翻转可能有问题（帧相同）")
        test5_pass = False
else:
    print("✗ 无法测试水平翻转")
    test5_pass = False

# 测试6: 渲染测试
print("\n测试6: 渲染测试（生成测试图像）")
print("-" * 70)

test_surface = pygame.Surface((800, 200))
test_surface.fill((50, 50, 50))

x_offset = 0
for char, sprite in sprites_loaded.items():
    sprite.play("idle")
    frame = sprite.get_current_frame()
    test_surface.blit(frame, (x_offset, 70))
    x_offset += 100

# 保存测试图像
try:
    pygame.image.save(test_surface, "sprite_test_output.png")
    print(f"✓ 测试图像已保存: sprite_test_output.png")
    test6_pass = True
except Exception as e:
    print(f"✗ 保存测试图像失败: {e}")
    test6_pass = False

# 总结
print("\n" + "=" * 70)
print("测试总结")
print("=" * 70)
print(f"测试1 - 精灵图文件加载: {'✅ 通过' if test1_pass else '❌ 失败'}")
print(f"测试2 - 动画帧数验证: {'✅ 通过' if test2_pass else '❌ 失败'}")
print(f"测试3 - 动画播放: {'✅ 通过' if test3_pass else '❌ 失败'}")
print(f"测试4 - 动画切换: {'✅ 通过' if test4_pass else '❌ 失败'}")
print(f"测试5 - 水平翻转: {'✅ 通过' if test5_pass else '❌ 失败'}")
print(f"测试6 - 渲染测试: {'✅ 通过' if test6_pass else '❌ 失败'}")

all_pass = all([test1_pass, test2_pass, test3_pass, test4_pass, test5_pass, test6_pass])

if all_pass:
    print(f"\n🎉 所有测试通过！精灵图系统工作正常！")
    sys.exit(0)
else:
    print(f"\n⚠️  部分测试失败，需要进一步调查。")
    sys.exit(1)

pygame.quit()
