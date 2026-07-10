"""
音效系统
职责：管理游戏音效和背景音乐
"""
import pygame
import os
from typing import Dict, Optional


class SoundManager:
    """
    音效管理器
    职责：加载、播放、控制音效和音乐
    """

    def __init__(self):
        """初始化音效系统"""
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # 音量控制
        self.sfx_volume = 0.7
        self.music_volume = 0.5

        # 音效字典
        self.sounds: Dict[str, pygame.mixer.Sound] = {}

        # 音乐状态
        self.current_music: Optional[str] = None
        self.music_playing = False

        # 加载音效（如果存在）
        self._load_sounds()

    def _load_sounds(self):
        """
        加载音效文件（如果存在）
        如果音效文件不存在，使用程序生成的简单音效
        """
        from config import Paths

        # 定义音效文件映射
        sound_files = {
            "hit_light": f"{Paths.AUDIO}/hit_light.wav",
            "hit_heavy": f"{Paths.AUDIO}/hit_heavy.wav",
            "hit_special": f"{Paths.AUDIO}/hit_special.wav",
            "block": f"{Paths.AUDIO}/block.wav",
            "jump": f"{Paths.AUDIO}/jump.wav",
            "buff": f"{Paths.AUDIO}/buff.wav",
            "ko": f"{Paths.AUDIO}/ko.wav",
        }

        # 尝试加载音效文件
        for sound_name, file_path in sound_files.items():
            if os.path.exists(file_path):
                try:
                    sound = pygame.mixer.Sound(file_path)
                    sound.set_volume(self.sfx_volume)
                    self.sounds[sound_name] = sound
                    print(f"✓ 加载音效: {sound_name}")
                except:
                    print(f"✗ 无法加载音效: {sound_name}")
            else:
                # 文件不存在，使用程序生成音效
                self.sounds[sound_name] = self._generate_simple_sound(sound_name)

    def _generate_simple_sound(self, sound_type: str) -> pygame.mixer.Sound:
        """
        程序生成简单音效（当音效文件不存在时）

        Args:
            sound_type: 音效类型

        Returns:
            pygame.mixer.Sound 对象
        """
        import numpy as np

        sample_rate = 22050

        if sound_type == "hit_light":
            # 轻攻击：短促的高频音
            duration = 0.1
            frequency = 800
        elif sound_type == "hit_heavy":
            # 重攻击：低沉的冲击音
            duration = 0.2
            frequency = 200
        elif sound_type == "hit_special":
            # 特殊招式：华丽的和弦
            duration = 0.3
            frequency = 600
        elif sound_type == "block":
            # 格挡：金属碰撞音
            duration = 0.15
            frequency = 1200
        elif sound_type == "jump":
            # 跳跃：上升音调
            duration = 0.2
            frequency = 400
        elif sound_type == "buff":
            # 增益：魔法音效
            duration = 0.4
            frequency = 1000
        elif sound_type == "ko":
            # KO：下降音调
            duration = 0.5
            frequency = 300
        else:
            duration = 0.1
            frequency = 440

        # 生成正弦波
        samples = int(duration * sample_rate)
        wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, samples))

        # 添加包络（淡入淡出）
        envelope = np.linspace(1.0, 0.0, samples)
        wave = wave * envelope

        # 转换为pygame音效
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))

        sound = pygame.mixer.Sound(stereo_wave)
        sound.set_volume(self.sfx_volume)

        return sound

    def play_sound(self, sound_name: str, force: bool = False):
        """
        播放音效

        Args:
            sound_name: 音效名称
            force: 是否强制播放（即使正在播放）
        """
        if sound_name in self.sounds:
            if force:
                self.sounds[sound_name].stop()
            self.sounds[sound_name].play()

    def play_hit_sound(self, attack_type: str):
        """
        播放击中音效

        Args:
            attack_type: 攻击类型 ("light", "heavy", "special")
        """
        sound_map = {
            "light": "hit_light",
            "heavy": "hit_heavy",
            "special": "hit_special",
        }

        sound_name = sound_map.get(attack_type, "hit_light")
        self.play_sound(sound_name)

    def play_block_sound(self):
        """播放格挡音效"""
        self.play_sound("block")

    def play_jump_sound(self):
        """播放跳跃音效"""
        self.play_sound("jump")

    def play_buff_sound(self):
        """播放增益激活音效"""
        self.play_sound("buff")

    def play_ko_sound(self):
        """播放KO音效"""
        self.play_sound("ko", force=True)

    def play_music(self, music_name: str, loop: bool = True):
        """
        播放背景音乐

        Args:
            music_name: 音乐名称
            loop: 是否循环播放
        """
        from config import Paths

        music_file = f"{Paths.AUDIO}/{music_name}.mp3"

        if os.path.exists(music_file):
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1 if loop else 0)
                self.current_music = music_name
                self.music_playing = True
                print(f"♪ 播放音乐: {music_name}")
            except Exception as e:
                print(f"✗ 无法播放音乐: {e}")
        else:
            print(f"✗ 音乐文件不存在: {music_file}")

    def stop_music(self):
        """停止背景音乐"""
        pygame.mixer.music.stop()
        self.music_playing = False

    def pause_music(self):
        """暂停背景音乐"""
        pygame.mixer.music.pause()

    def resume_music(self):
        """恢复背景音乐"""
        pygame.mixer.music.unpause()

    def set_sfx_volume(self, volume: float):
        """
        设置音效音量

        Args:
            volume: 音量 (0.0-1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    def set_music_volume(self, volume: float):
        """
        设置音乐音量

        Args:
            volume: 音量 (0.0-1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def cleanup(self):
        """清理音效系统"""
        pygame.mixer.quit()


# 全局音效管理器单例
_sound_manager: Optional[SoundManager] = None


def get_sound_manager() -> SoundManager:
    """获取全局音效管理器"""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
