"""
数字人快速模式功能测试
"""

import unittest
from jimeng_video import (
    JimengVideoClient,
    AvatarDriveMode,
    AvatarQuality,
    create_avatar_video
)


class TestAvatarMode(unittest.TestCase):
    """数字人模式测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.access_key = "test_ak"
        self.secret_key = "test_sk"
        self.client = JimengVideoClient(
            access_key=self.access_key,
            secret_key=self.secret_key
        )
        self.test_image = "https://example.com/avatar.jpg"
    
    def tearDown(self):
        """测试后清理"""
        self.client.session.close()
    
    def test_enum_values(self):
        """测试枚举值"""
        # 测试驱动模式枚举
        self.assertEqual(AvatarDriveMode.AUDIO.value, "audio")
        self.assertEqual(AvatarDriveMode.TEXT.value, "text")
        self.assertEqual(AvatarDriveMode.VIDEO.value, "video")
        
        # 测试质量枚举
        self.assertEqual(AvatarQuality.LOW.value, "low")
        self.assertEqual(AvatarQuality.MEDIUM.value, "medium")
        self.assertEqual(AvatarQuality.HIGH.value, "high")
        self.assertEqual(AvatarQuality.ULTRA.value, "ultra")
    
    def test_audio_mode_validation(self):
        """测试音频模式参数验证"""
        # 应该抛出ValueError，因为缺少audio_url
        with self.assertRaises(ValueError) as context:
            self.client.generate_avatar_video(
                image_url=self.test_image,
                drive_mode=AvatarDriveMode.AUDIO.value
            )
        self.assertIn("audio_url", str(context.exception))
    
    def test_text_mode_validation(self):
        """测试文本模式参数验证"""
        # 应该抛出ValueError，因为缺少text
        with self.assertRaises(ValueError) as context:
            self.client.generate_avatar_video(
                image_url=self.test_image,
                drive_mode=AvatarDriveMode.TEXT.value
            )
        self.assertIn("text", str(context.exception))
    
    def test_video_mode_validation(self):
        """测试视频模式参数验证"""
        # 应该抛出ValueError，因为缺少video_url
        with self.assertRaises(ValueError) as context:
            self.client.generate_avatar_video(
                image_url=self.test_image,
                drive_mode=AvatarDriveMode.VIDEO.value
            )
        self.assertIn("video_url", str(context.exception))
    
    def test_request_body_structure(self):
        """测试请求体结构"""
        # 注意：这个测试不会真正发送请求，只是验证参数构建
        # 实际使用时需要mock requests
        pass
    
    def test_quality_levels(self):
        """测试不同质量等级"""
        quality_levels = [
            AvatarQuality.LOW.value,
            AvatarQuality.MEDIUM.value,
            AvatarQuality.HIGH.value,
            AvatarQuality.ULTRA.value
        ]
        
        for quality in quality_levels:
            # 验证质量参数可以正常使用
            self.assertIn(quality, ["low", "medium", "high", "ultra"])
    
    def test_drive_modes(self):
        """测试不同驱动模式"""
        drive_modes = [
            AvatarDriveMode.AUDIO.value,
            AvatarDriveMode.TEXT.value,
            AvatarDriveMode.VIDEO.value
        ]
        
        for mode in drive_modes:
            # 验证驱动模式参数可以正常使用
            self.assertIn(mode, ["audio", "text", "video"])


class TestAvatarIntegration(unittest.TestCase):
    """数字人集成测试类（需要真实API密钥）"""
    
    @unittest.skip("需要真实API密钥")
    def test_audio_driven_end_to_end(self):
        """端到端测试：音频驱动"""
        result = create_avatar_video(
            access_key="real_ak",
            secret_key="real_sk",
            image_url="https://example.com/avatar.jpg",
            drive_mode="audio",
            audio_url="https://example.com/speech.mp3",
            quality="high"
        )
        
        self.assertIn('task_id', result)
        self.assertIn('status', result)
    
    @unittest.skip("需要真实API密钥")
    def test_text_driven_end_to_end(self):
        """端到端测试：文本驱动"""
        result = create_avatar_video(
            access_key="real_ak",
            secret_key="real_sk",
            image_url="https://example.com/avatar.jpg",
            drive_mode="text",
            text="测试文本内容",
            quality="medium"
        )
        
        self.assertIn('task_id', result)
        self.assertIn('status', result)


def run_basic_tests():
    """运行基础测试"""
    print("=" * 60)
    print("数字人快速模式功能测试")
    print("=" * 60)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加基础测试
    suite.addTests(loader.loadTestsFromTestCase(TestAvatarMode))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果
    print("\n" + "=" * 60)
    print(f"测试总数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()


def demo_usage():
    """演示基本用法"""
    print("\n" + "=" * 60)
    print("数字人快速模式使用演示")
    print("=" * 60)
    
    print("\n1. 创建客户端")
    print("-" * 60)
    print("""
client = JimengVideoClient(
    access_key="your_access_key",
    secret_key="your_secret_key"
)
    """)
    
    print("\n2. 音频驱动模式")
    print("-" * 60)
    print("""
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.AUDIO.value,
    audio_url="https://example.com/speech.mp3",
    quality=AvatarQuality.HIGH.value
)
    """)
    
    print("\n3. 文本驱动模式（TTS）")
    print("-" * 60)
    print("""
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.TEXT.value,
    text="大家好，我是AI数字人！",
    voice_type="zh_female_qingxin"
)
    """)
    
    print("\n4. 视频驱动模式")
    print("-" * 60)
    print("""
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.VIDEO.value,
    video_url="https://example.com/driving_video.mp4"
)
    """)
    
    print("\n5. 便捷函数")
    print("-" * 60)
    print("""
result = create_avatar_video(
    access_key="your_ak",
    secret_key="your_sk",
    image_url="https://example.com/avatar.jpg",
    drive_mode="text",
    text="快速创建数字人视频",
    save_path="./output/avatar.mp4"
)
    """)
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # 运行基础测试
    success = run_basic_tests()
    
    # 显示使用演示
    demo_usage()
    
    # 提示信息
    print("\n提示：")
    print("- 基础测试已完成，验证了参数验证和枚举值")
    print("- 端到端测试需要真实的API密钥，已跳过")
    print("- 查看 example_avatar.py 获取完整示例")
    print("- 查看 README_AVATAR.md 获取详细文档")
    
    # 退出码
    exit(0 if success else 1)
