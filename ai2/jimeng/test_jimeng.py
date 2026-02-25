"""
即梦AI视频生成测试文件
"""

import os
from jimeng_video import JimengVideoClient, VideoStyle, VideoResolution, create_video


def test_client_initialization():
    """测试客户端初始化"""
    access_key = os.getenv("JIMENG_ACCESS_KEY", "test_access_key")
    secret_key = os.getenv("JIMENG_SECRET_KEY", "test_secret_key")
    
    client = JimengVideoClient(
        access_key=access_key,
        secret_key=secret_key
    )
    assert client.access_key == access_key
    assert client.secret_key == secret_key
    assert client.base_url == "https://visual.volcengineapi.com"
    assert client.service == "cv"
    assert client.region == "cn-north-1"
    assert client.timeout == 30
    print("✓ 客户端初始化测试通过")


def test_headers():
    """测试请求头生成"""
    client = JimengVideoClient(
        access_key="test_access_key",
        secret_key="test_secret_key"
    )
    
    headers = client._get_headers('{"test": "data"}')
    assert 'Content-Type' in headers
    assert headers['Content-Type'] == "application/json"
    assert 'X-Date' in headers
    # 签名相关的头部会自动生成
    print("✓ 请求头生成测试通过")


def test_context_manager():
    """测试上下文管理器"""
    with JimengVideoClient(
        access_key="test_access_key",
        secret_key="test_secret_key"
    ) as client:
        assert client is not None
        assert client.access_key == "test_access_key"
        assert client.secret_key == "test_secret_key"
    print("✓ 上下文管理器测试通过")


def test_enums():
    """测试枚举类型"""
    # 测试VideoStyle
    assert VideoStyle.DEFAULT.value == "default"
    assert VideoStyle.CINEMATIC.value == "cinematic"
    assert VideoStyle.ANIME.value == "anime"
    
    # 测试VideoResolution
    assert VideoResolution.SD_480P.value == "480p"
    assert VideoResolution.HD_720P.value == "720p"
    assert VideoResolution.FHD_1080P.value == "1080p"
    assert VideoResolution.UHD_4K.value == "4k"
    print("✓ 枚举类型测试通过")


def test_batch_generate_structure():
    """测试批量生成函数结构(不实际调用API)"""
    client = JimengVideoClient(
        access_key="test_access_key",
        secret_key="test_secret_key"
    )
    
    prompts = [
        "测试提示词1",
        "测试提示词2",
        "测试提示词3"
    ]
    
    # 这里只测试函数结构,不实际调用
    assert hasattr(client, 'batch_generate')
    print("✓ 批量生成函数结构测试通过")


def run_all_tests():
    """运行所有测试"""
    print("开始运行测试...\n")
    
    test_client_initialization()
    test_headers()
    test_context_manager()
    test_enums()
    test_batch_generate_structure()
    
    print("\n所有测试通过! ✓✓✓")


if __name__ == "__main__":
    run_all_tests()
    
    print("\n" + "="*50)
    print("注意: 以上是基础功能测试")
    print("如需测试实际API调用,请设置环境变量:")
    print("  - JIMENG_ACCESS_KEY: 火山引擎Access Key")
    print("  - JIMENG_SECRET_KEY: 火山引擎Secret Key")
    print("然后参考 example.py 中的示例代码")
    print("密钥获取: https://console.volcengine.com/iam/keymanage/")
    print("="*50)

