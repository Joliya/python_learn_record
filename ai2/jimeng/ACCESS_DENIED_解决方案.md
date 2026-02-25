# Access Denied 错误解决方案

## 🔴 当前错误

```json
{
  "code": 50400,
  "data": null,
  "message": "Access Denied: Access Denied",
  "request_id": "20251022174600CA1242CEDD0FB314062A",
  "status": 50400
}
```

## ✅ 好消息

签名算法已经**完全正确**！错误从 `SignatureDoesNotMatch` 变成了 `Access Denied`，说明：
- ✅ 签名计算正确
- ✅ AK/SK 格式正确
- ❌ 权限不足

---

## 🔍 问题原因

`Access Denied` 通常由以下原因导致：

### 1. AK/SK 权限不足 ⭐ 最可能
你的 Access Key 可能没有访问**视觉智能服务（CV）**的权限。

### 2. 服务未开通
可能没有开通火山引擎的视觉智能服务。

### 3. 账户欠费
账户余额不足或已欠费。

### 4. IP 白名单限制
某些服务可能有 IP 白名单限制。

---

## 🛠️ 解决步骤

### 步骤1：检查 AK/SK 权限

1. **登录火山引擎控制台**
   - 访问：https://console.volcengine.com/iam/keymanage/

2. **查看 Access Key 权限**
   - 找到你正在使用的 AK
   - 点击"权限管理"或"详情"
   - 检查是否有以下权限：
     - `CVServiceFullAccess` - 视觉智能服务完全访问权限
     - 或 `CVServiceReadOnlyAccess` - 视觉智能服务只读权限

3. **如果没有权限，添加权限**
   - 点击"添加权限"
   - 搜索 "CV" 或 "视觉智能"
   - 勾选相应的权限策略
   - 保存

### 步骤2：检查服务开通状态

1. **访问视觉智能服务控制台**
   - https://console.volcengine.com/visual

2. **检查服务状态**
   - 查看服务是否已开通
   - 如果未开通，点击"开通服务"

3. **确认服务配额**
   - 检查是否有足够的配额
   - 查看是否有免费额度

### 步骤3：检查账户余额

1. **访问账户中心**
   - https://console.volcengine.com/finance/account/

2. **查看余额**
   - 确保账户余额充足
   - 如果欠费，请充值

### 步骤4：尝试使用子账号 AK/SK

如果你使用的是主账号 AK/SK，尝试：

1. **创建子账号**
   - 进入 IAM 控制台
   - 创建新的子用户

2. **授予特定权限**
   - 只授予 CV 服务的权限
   - 生成新的 AK/SK

3. **使用新的 AK/SK 测试**

---

## 🔧 临时测试方案

### 方案1：使用火山引擎 SDK

安装官方 SDK 测试权限：

```bash
pip install volcengine
```

测试代码：

```python
from volcengine.visual.VisualService import VisualService

# 使用你的 AK/SK
service = VisualService()
service.set_ak('your_ak')
service.set_sk('your_sk')

# 测试调用
try:
    resp = service.cv_process({
        'req_key': 'jimeng_realman_avatar_picture_create_role_omni',
        'image_url': 'https://example.com/test.jpg'
    })
    print("成功:", resp)
except Exception as e:
    print("失败:", e)
```

### 方案2：使用 API Explorer

1. **访问 API Explorer**
   - https://console.volcengine.com/api/explorer

2. **选择视觉智能服务**
   - 找到 CV 相关的 API
   - 尝试在线调用

3. **查看返回结果**
   - 如果在线调用成功，说明权限没问题
   - 如果失败，查看具体错误信息

---

## 📝 权限配置示例

### 最小权限策略（JSON）

如果你需要自定义权限策略，可以使用：

```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cv:CVProcess",
        "cv:CVSubmitTask",
        "cv:CVGetResult"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 🔍 调试建议

### 1. 确认 AK/SK 正确性

```python
import os

ak = os.getenv("HUOSHAN_API_KEY")
sk = os.getenv("HUOSHAN_API_SECRET")

print(f"AK 长度: {len(ak)}")
print(f"SK 长度: {len(sk)}")
print(f"AK 前缀: {ak[:10]}...")
print(f"SK 前缀: {sk[:10]}...")
```

### 2. 测试其他服务

尝试调用其他火山引擎服务，确认 AK/SK 本身是有效的：

```python
# 测试 IAM 服务（通常所有账号都有权限）
from jimeng_video import JimengVideoClient

client = JimengVideoClient(
    access_key=ak,
    secret_key=sk,
    base_url="https://iam.volcengineapi.com",
    service="iam"
)

# 如果这个调用成功，说明 AK/SK 本身没问题
```

### 3. 查看详细错误日志

在代码中添加更详细的日志：

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

---

## 📞 联系支持

如果以上方法都无法解决问题，建议：

### 1. 提交工单
- 访问：https://console.volcengine.com/workorder
- 选择"视觉智能"相关问题
- 提供错误信息和 request_id

### 2. 查看文档
- [视觉智能服务文档](https://www.volcengine.com/docs/6791)
- [IAM 权限管理](https://www.volcengine.com/docs/6257)

### 3. 社区求助
- 火山引擎开发者社区
- GitHub Issues

---

## ✅ 验证权限的快速方法

运行以下脚本验证权限：

```python
import os
import requests
import json
from jimeng_video import JimengVideoClient

ak = os.getenv("HUOSHAN_API_KEY")
sk = os.getenv("HUOSHAN_API_SECRET")

print("=" * 60)
print("火山引擎权限检查")
print("=" * 60)

# 1. 检查 AK/SK 格式
print(f"\n1. AK/SK 格式检查:")
print(f"   AK 长度: {len(ak)} (正常应该是 40-50 个字符)")
print(f"   SK 长度: {len(sk)} (正常应该是 40-50 个字符)")

# 2. 尝试调用 CV 服务
print(f"\n2. 尝试调用 CV 服务:")
try:
    client = JimengVideoClient(access_key=ak, secret_key=sk)
    result = client.submit_avatar_image_detection(
        "https://example.com/test.jpg"
    )
    print(f"   ✅ 成功! Task ID: {result}")
except Exception as e:
    error_msg = str(e)
    print(f"   ❌ 失败: {error_msg}")
    
    if "Access Denied" in error_msg:
        print("\n   原因: 权限不足")
        print("   解决: 请按照上述步骤检查并添加 CV 服务权限")
    elif "SignatureDoesNotMatch" in error_msg:
        print("\n   原因: 签名错误")
        print("   解决: 检查 AK/SK 是否正确")
    else:
        print(f"\n   原因: {error_msg}")

print("\n" + "=" * 60)
```

---

## 🎯 下一步

1. **立即检查权限** ⭐
   - 登录控制台
   - 检查 AK 权限
   - 添加 CV 服务权限

2. **确认服务开通**
   - 访问视觉智能控制台
   - 开通服务

3. **重新测试**
   - 运行代码
   - 查看结果

4. **如果仍然失败**
   - 提交工单
   - 联系技术支持

---

**更新时间**: 2025年10月22日  
**状态**: 签名算法已修复 ✅ | 等待权限配置 ⏳
