"""
即梦AI视频生成3.0 Pro接入封装
火山引擎视频生成API接入

功能：
1. 视频生成（文生视频）
2. 数字人快速模式（图片+音频/文本/视频驱动）
"""

import os
import time
import json
import hashlib
import hmac
from datetime import datetime
from urllib.parse import quote
from dotenv import load_dotenv
import requests
from typing import Optional, Dict, Any, List
from enum import Enum


load_dotenv()


class VideoStatus(Enum):
    """视频生成状态枚举"""
    PENDING = "pending"  # 等待中
    PROCESSING = "processing"  # 处理中
    SUCCESS = "success"  # 成功
    FAILED = "failed"  # 失败


class VideoStyle(Enum):
    """视频风格枚举"""
    DEFAULT = "default"  # 默认
    CINEMATIC = "cinematic"  # 电影风格
    ANIME = "anime"  # 动漫风格
    REALISTIC = "realistic"  # 写实风格
    ARTISTIC = "artistic"  # 艺术风格


class VideoResolution(Enum):
    """视频分辨率枚举"""
    SD_480P = "480p"  # 标清
    HD_720P = "720p"  # 高清
    FHD_1080P = "1080p"  # 全高清
    UHD_4K = "4k"  # 超高清


class AvatarDriveMode(Enum):
    """数字人驱动模式枚举"""
    AUDIO = "audio"  # 音频驱动
    VIDEO = "video"  # 视频驱动
    TEXT = "text"  # 文本驱动（TTS）


class AvatarQuality(Enum):
    """数字人视频质量枚举"""
    LOW = "low"  # 低质量，快速生成
    MEDIUM = "medium"  # 中等质量
    HIGH = "high"  # 高质量
    ULTRA = "ultra"  # 超高质量


class JimengVideoClient:
    """
    即梦AI视频生成客户端
    
    提供简单易用的视频生成接口
    """
    
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        base_url: str = "https://visual.volcengineapi.com",
        service: str = "cv",
        region: str = "cn-north-1",
        timeout: int = 30
    ):
        """
        初始化即梦AI视频生成客户端
        
        Args:
            access_key: 火山引擎Access Key (AK)
            secret_key: 火山引擎Secret Key (SK)
            base_url: API基础URL
            service: 服务名称，默认为cv
            region: 区域，默认为cn-north-1
            timeout: 请求超时时间(秒)
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.service = service
        self.region = region
        self.timeout = timeout
        self.session = requests.Session()
        
    def _sign_request(self, method: str, path: str, params: Dict[str, Any], body: str = "") -> Dict[str, str]:
        """
        对请求进行签名(火山引擎签名v4算法)
        
        Args:
            method: HTTP方法
            path: 请求路径
            params: 查询参数
            body: 请求体
            
        Returns:
            包含签名的请求头
        """
        # 获取当前时间
        now = datetime.utcnow()
        timestamp = now.strftime('%Y%m%dT%H%M%SZ')
        date = now.strftime('%Y%m%d')
        
        # 计算请求体hash
        payload_hash = hashlib.sha256(body.encode('utf-8')).hexdigest()
        
        # 构建请求头（按照官方SDK的顺序）
        host = self.base_url.replace('https://', '').replace('http://', '')
        headers = {
            'Host': host,
            'Content-Type': 'application/json',
            'X-Content-Sha256': payload_hash,
            'X-Date': timestamp,
        }
        
        # 如果不需要签名，直接返回基本headers
        if not self.secret_key:
            return headers
        
        # 构建规范化查询字符串（需要URL编码和排序）
        if params:
            # 对参数进行排序和URL编码（使用官方SDK的safe参数）
            sorted_params = sorted(params.items())
            query_parts = []
            for key, value in sorted_params:
                encoded_key = quote(str(key), safe="-_.~")
                encoded_value = quote(str(value), safe="-_.~")
                query_parts.append(f"{encoded_key}={encoded_value}")
            canonical_query_string = "&".join(query_parts)
        else:
            canonical_query_string = ""
        
        # 构建规范化请求头（按照官方SDK的顺序：content-type, host, x-content-sha256, x-date）
        canonical_headers = f"content-type:{headers['Content-Type']}\nhost:{host}\nx-content-sha256:{payload_hash}\nx-date:{timestamp}\n"
        signed_headers = "content-type;host;x-content-sha256;x-date"
        
        # 构建规范化请求字符串
        canonical_request = f"{method}\n{path}\n{canonical_query_string}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
        print("canonical_request:", canonical_request)
        
        # 计算规范化请求的hash
        hashed_canonical_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        print("hashed_canonical_request:", hashed_canonical_request)
        
        # 构建签名字符串
        credential_scope = f"{date}/{self.region}/{self.service}/request"
        print("credential_scope:", credential_scope)
        string_to_sign = f"HMAC-SHA256\n{timestamp}\n{credential_scope}\n{hashed_canonical_request}"
        print("string_to_sign:", string_to_sign)
        
        # 计算签名（注意：不加VOLC前缀，直接使用SK）
        k_date = hmac.new(self.secret_key.encode('utf-8'), date.encode('utf-8'), hashlib.sha256).digest()
        k_region = hmac.new(k_date, self.region.encode('utf-8'), hashlib.sha256).digest()
        k_service = hmac.new(k_region, self.service.encode('utf-8'), hashlib.sha256).digest()
        k_signing = hmac.new(k_service, b"request", hashlib.sha256).digest()
        signature = hmac.new(k_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        
        # 构建Authorization header
        authorization = f"HMAC-SHA256 Credential={self.access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
        headers['Authorization'] = authorization
        
        return headers
    
    def _get_headers(self, body: str = "", params: Dict[str, Any] = None) -> Dict[str, str]:
        """
        获取请求头（包含签名）
        
        Args:
            body: 请求体
            
        Returns:
            请求头字典
        """
        return self._sign_request("POST", "/", params, body)
    
    def generate_video(
        self,
        prompt: str,
        style: str = VideoStyle.DEFAULT.value,
        resolution: str = VideoResolution.FHD_1080P.value,
        duration: int = 5,
        fps: int = 30,
        negative_prompt: Optional[str] = None,
        reference_image: Optional[str] = None,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        提交视频生成任务
        
        Args:
            prompt: 视频描述文本提示词
            style: 视频风格,可选值见VideoStyle枚举
            resolution: 视频分辨率,可选值见VideoResolution枚举
            duration: 视频时长(秒),默认5秒
            fps: 视频帧率,默认30fps
            negative_prompt: 负面提示词,描述不希望出现的内容
            reference_image: 参考图片URL或base64编码
            custom_params: 自定义参数字典
            
        Returns:
            包含task_id的响应字典
            
        Raises:
            requests.RequestException: 请求失败时抛出
        """
        # 火山引擎使用统一endpoint，通过action参数区分操作
        url = f"{self.base_url}"
        
        # 构建请求参数，使用火山引擎标准格式
        req_data: Dict[str, Any] = {
            'req_key': 'jimeng_ti2v_v30_pro',  # 主要输入参数
            'prompt': prompt,
        }
        
        # 添加可选参数
        if negative_prompt:
            req_data['negative_prompt'] = negative_prompt
        if reference_image:
            req_data['image_urls'] = [reference_image]
        if custom_params:
            req_data.update(custom_params)
        
        data: Dict[str, Any] = {
            'Action': 'SubmitTask',  # 提交任务的action
            'Version': '2022-08-31',  # API版本
            'req_key': json.dumps(req_data),  # 实际请求参数
        }
        
        body = json.dumps(data)
        
        try:
            response = self.session.post(
                url,
                headers=self._get_headers(body),
                data=body,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            # 检查返回的ResponseMetadata
            if 'ResponseMetadata' in result:
                if result['ResponseMetadata'].get('Error'):
                    error_info = result['ResponseMetadata']['Error']
                    raise Exception(f"API错误: {error_info.get('Message', '未知错误')}")
            
            return result
        except requests.RequestException as e:
            raise Exception(f"视频生成任务提交失败: {str(e)}") from e
    
    def query_task(self, task_id: str) -> Dict[str, Any]:
        """
        查询视频生成任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态信息字典,包含status、progress、result等字段
            
        Raises:
            requests.RequestException: 请求失败时抛出
        """
        # 火山引擎使用统一endpoint，通过action参数区分操作
        url = f"{self.base_url}"
        
        data = {
            'Action': 'GetVideoResult',  # 查询结果的action
            'Version': '2022-08-31',  # API版本
            'task_id': task_id
        }
        
        body = json.dumps(data)
        
        try:
            response = self.session.post(
                url,
                headers=self._get_headers(body),
                data=body,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            # 检查返回的ResponseMetadata
            if 'ResponseMetadata' in result:
                if result['ResponseMetadata'].get('Error'):
                    error_info = result['ResponseMetadata']['Error']
                    raise Exception(f"API错误: {error_info.get('Message', '未知错误')}")
            
            return result
        except requests.RequestException as e:
            raise Exception(f"查询任务状态失败: {str(e)}") from e
    
    def wait_for_completion(
        self,
        task_id: str,
        max_wait_time: int = 600,
        poll_interval: int = 5,
        callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        等待视频生成任务完成
        
        Args:
            task_id: 任务ID
            max_wait_time: 最大等待时间(秒),默认600秒
            poll_interval: 轮询间隔(秒),默认5秒
            callback: 进度回调函数,接收(task_id, progress, status)参数
            
        Returns:
            完成后的任务结果字典
            
        Raises:
            TimeoutError: 超时时抛出
            Exception: 任务失败时抛出
        """
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > max_wait_time:
                raise TimeoutError(f"任务{task_id}等待超时,已等待{elapsed:.0f}秒")
            
            result = self.query_task(task_id)
            status = result.get('status', '')
            progress = result.get('progress', 0)
            
            # 执行回调
            if callback:
                callback(task_id, progress, status)
            
            # 检查任务状态
            if status == VideoStatus.SUCCESS.value:
                return result
            elif status == VideoStatus.FAILED.value:
                error_msg = result.get('error_message', '未知错误')
                raise Exception(f"任务{task_id}生成失败: {error_msg}")
            
            # 等待后继续轮询
            time.sleep(poll_interval)
    
    def generate_and_wait(
        self,
        prompt: str,
        style: str = VideoStyle.DEFAULT.value,
        resolution: str = VideoResolution.FHD_1080P.value,
        duration: int = 5,
        fps: int = 30,
        negative_prompt: Optional[str] = None,
        reference_image: Optional[str] = None,
        max_wait_time: int = 600,
        poll_interval: int = 5,
        progress_callback: Optional[callable] = None,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        一键生成视频并等待完成(推荐使用)
        
        这是最简单的调用方式,提交任务后自动等待完成并返回结果
        
        Args:
            prompt: 视频描述文本提示词
            style: 视频风格
            resolution: 视频分辨率
            duration: 视频时长(秒)
            fps: 视频帧率
            negative_prompt: 负面提示词
            reference_image: 参考图片
            max_wait_time: 最大等待时间(秒)
            poll_interval: 轮询间隔(秒)
            progress_callback: 进度回调函数
            custom_params: 自定义参数
            
        Returns:
            包含视频URL和相关信息的结果字典
            
        Raises:
            Exception: 生成失败时抛出
        """
        # 提交任务
        submit_result = self.generate_video(
            prompt=prompt,
            style=style,
            resolution=resolution,
            duration=duration,
            fps=fps,
            negative_prompt=negative_prompt,
            reference_image=reference_image,
            custom_params=custom_params
        )
        
        task_id = submit_result.get('task_id')
        if not task_id:
            raise Exception("任务提交失败,未获取到task_id")
        
        # 等待完成
        result = self.wait_for_completion(
            task_id=task_id,
            max_wait_time=max_wait_time,
            poll_interval=poll_interval,
            callback=progress_callback
        )
        
        return result
    
    def download_video(
        self,
        video_url: str,
        save_path: str,
        chunk_size: int = 8192
    ) -> str:
        """
        下载生成的视频
        
        Args:
            video_url: 视频URL
            save_path: 保存路径
            chunk_size: 下载块大小(字节)
            
        Returns:
            保存的文件路径
            
        Raises:
            requests.RequestException: 下载失败时抛出
        """
        try:
            response = self.session.get(video_url, stream=True, timeout=300)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
            
            return save_path
        except Exception as e:
            raise Exception(f"视频下载失败: {str(e)}") from e
    
    def batch_generate(
        self,
        prompts: List[str],
        style: str = VideoStyle.DEFAULT.value,
        resolution: str = VideoResolution.FHD_1080P.value,
        **kwargs
    ) -> List[str]:
        """
        批量生成视频任务
        
        Args:
            prompts: 提示词列表
            style: 视频风格
            resolution: 视频分辨率
            **kwargs: 其他参数
            
        Returns:
            任务ID列表
        """
        task_ids = []
        for prompt in prompts:
            result = self.generate_video(
                prompt=prompt,
                style=style,
                resolution=resolution,
                **kwargs
            )
            task_id = result.get('task_id')
            if task_id:
                task_ids.append(task_id)
        
        return task_ids
    
    def submit_avatar_image_detection(self, image_url: str) -> str:
        """
        步骤1：提交图片主体识别任务
        
        Args:
            image_url: 数字人图片URL或base64编码
            
        Returns:
            包含task_id的响应字典
            
        Raises:
            requests.RequestException: 请求失败时抛出
        """
        url = f"{self.base_url}?Action=CVSubmitTask&Version=2022-08-31"

        print(url)
        
        req_data = {
            'req_key': 'jimeng_realman_avatar_picture_create_role_omni',  # 图片主体识别
            'image_url': image_url,
        }
        
        body = json.dumps(req_data)
        params = {
            'Action': 'CVSubmitTask',
            'Version': '2022-08-31',
        }
        header = self._get_headers(body, params)
        print(header)
        try:
            response = self.session.post(
                url,
                headers=header,
                data=body,
                timeout=self.timeout
            )
            print(response.text)
            result = response.json()
            print(result)
            
            # 检查是否有错误
            if 'code' in result and result['code'] != 0:
                error_msg = result.get('message', '未知错误')
                raise Exception(f"API错误 (code={result['code']}): {error_msg}")
            
            # 检查data字段
            if 'data' not in result or result['data'] is None:
                raise Exception(f"API返回数据异常: {result}")
            
            task_id = result['data'].get('task_id')
            if not task_id:
                raise Exception(f"未获取到task_id: {result}")
            
            print(f"图片识别任务ID: {task_id}")
            return task_id
        except requests.RequestException as e:
            raise Exception(f"图片主体识别任务提交失败: {str(e)}") from e
    
    def submit_avatar_video_generation(
        self,
        image_url: str,
        drive_mode: str = AvatarDriveMode.AUDIO.value,
        audio_url: Optional[str] = None,
        text: Optional[str] = None,
        video_url: Optional[str] = None,
        voice_type: Optional[str] = None,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        步骤2：提交数字人视频生成任务
        
        Args:
            image_url: 数字人图片URL（使用步骤1识别后的图片）
            drive_mode: 驱动模式，可选值见AvatarDriveMode枚举
            audio_url: 音频驱动URL（drive_mode=audio时必填）
            text: 文本内容（drive_mode=text时必填，用于TTS）
            video_url: 视频驱动URL（drive_mode=video时必填）
            voice_type: 声音类型（drive_mode=text时可用）
            custom_params: 自定义参数字典
            
        Returns:
            包含task_id的响应字典
            
        Raises:
            ValueError: 参数错误时抛出
            requests.RequestException: 请求失败时抛出
        """
        
        url = f"{self.base_url}?Action=CVSubmitTask&Version=2022-08-31"
        
        # 构建请求参数
        req_data: Dict[str, Any] = {
            'req_key': 'jimeng_realman_avatar_picture_omni_v2',  # 数字人视频生成
            'image_url': image_url,
            'audio_url': audio_url,
        }
        
        body = json.dumps(req_data)
        
        try:
            response = self.session.post(
                url,
                headers=self._get_headers(body),
                data=body,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            print(result)
            print(result['data']['task_id'])
            
            return result
        except requests.RequestException as e:
            raise Exception(f"数字人视频生成任务提交失败: {str(e)}") from e
    
    def query_avatar_task(self, task_id: str) -> Dict[str, Any]:
        """
        查询图片识别任务状态
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态信息字典
            
        Raises:
            requests.RequestException: 请求失败时抛出
        """
        url = f"{self.base_url}?Action=CVGetResult&Version=2022-08-31"
        
        data = {
            'task_id': task_id,
            'req_key': 'jimeng_realman_avatar_picture_create_role_omni',
        }
        
        body = json.dumps(data)
        
        try:
            response = self.session.post(
                url,
                headers=self._get_headers(body),
                data=body,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            print(result)
            print(json.loads(result['data']['resp_data']))
            print(result['data']['status'])
            return result
        except requests.RequestException as e:
            raise Exception(f"查询任务状态失败: {str(e)}") from e

    def query_avatar_video_task(self, task_id: str) -> Dict[str, Any]:
        """
        查询数字人视频生成任务状态
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态信息字典
            
        Raises:
            requests.RequestException: 请求失败时抛出
        """
        url = f"{self.base_url}?Action=CVGetResult&Version=2022-08-31"
        
        data = {
            'task_id': task_id,
            'req_key': 'jimeng_realman_avatar_picture_omni_v2',
        }
        
        body = json.dumps(data)
        
        try:
            response = self.session.post(
                url,
                headers=self._get_headers(body),
                data=body,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            print(result)
            print(result['data'])
            return result
        except requests.RequestException as e:
            raise Exception(f"查询任务状态失败: {str(e)}") from e
    
    def generate_avatar_video(
        self,
        image_url: str,
        drive_mode: str = AvatarDriveMode.AUDIO.value,
        audio_url: Optional[str] = None,
        text: Optional[str] = None,
        video_url: Optional[str] = None,
        quality: str = AvatarQuality.HIGH.value,
        resolution: str = "1080p",
        voice_type: Optional[str] = None,
        background_music: Optional[str] = None,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        生成数字人视频（快速模式 - 完整流程）
        
        执行完整的两步骤流程：
        1. 提交图片主体识别任务并等待完成
        2. 使用识别结果提交视频生成任务
        
        Args:
            image_url: 数字人图片URL或base64编码
            drive_mode: 驱动模式，可选值见AvatarDriveMode枚举
            audio_url: 音频驱动URL（drive_mode=audio时必填）
            text: 文本内容（drive_mode=text时必填，用于TTS）
            video_url: 视频驱动URL（drive_mode=video时必填）
            quality: 视频质量，可选值见AvatarQuality枚举
            resolution: 视频分辨率，默认1080p
            voice_type: 声音类型（drive_mode=text时可用）
            background_music: 背景音乐URL
            custom_params: 自定义参数字典
            
        Returns:
            包含video_task_id的响应字典
            
        Raises:
            ValueError: 参数错误时抛出
            Exception: 任务失败时抛出
        """
        print("步骤1/2: 提交图片主体识别任务...")
        # 步骤1：图片主体识别
        detection_task_id = self.submit_avatar_image_detection(image_url)
        
        if not detection_task_id:
            # 如果是同步返回结果，直接使用
            processed_image_url = detection_result.get('data', {}).get('image_url', image_url)
        else:
            # 异步任务，需要轮询等待
            print(f"图片识别任务ID: {detection_task_id}，等待完成...")
            max_wait = 60  # 最多等待60秒
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                status_result = self.query_avatar_task(detection_task_id)
                status = status_result.get('status')
                
                if status == 'success':
                    processed_image_url = status_result.get('data', {}).get('image_url', image_url)
                    print("图片识别完成！")
                    break
                elif status == 'failed':
                    raise Exception(f"图片识别失败: {status_result.get('message')}")
                
                time.sleep(2)
            else:
                raise TimeoutError("图片识别任务超时")
        
        print("步骤2/2: 提交数字人视频生成任务...")
        # 步骤2：视频生成
        video_result = self.submit_avatar_video_generation(
            image_url=processed_image_url,
            drive_mode=drive_mode,
            audio_url=audio_url,
            text=text,
            video_url=video_url,
            voice_type=voice_type,
            custom_params=custom_params
        )
        
        print(f"视频生成任务已提交，任务ID: {video_result.get('task_id')}")
        return video_result
    
    def generate_avatar_and_wait(
        self,
        image_url: str,
        drive_mode: str = AvatarDriveMode.AUDIO.value,
        audio_url: Optional[str] = None,
        text: Optional[str] = None,
        video_url: Optional[str] = None,
        quality: str = AvatarQuality.HIGH.value,
        resolution: str = "1080p",
        voice_type: Optional[str] = None,
        background_music: Optional[str] = None,
        max_wait_time: int = 600,
        poll_interval: int = 5,
        progress_callback: Optional[callable] = None,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        一键生成数字人视频并等待完成（推荐使用）
        
        这是最简单的调用方式，提交任务后自动等待完成并返回结果
        
        Args:
            image_url: 数字人图片URL或base64编码
            drive_mode: 驱动模式
            audio_url: 音频驱动URL
            text: 文本内容（TTS）
            video_url: 视频驱动URL
            quality: 视频质量
            resolution: 视频分辨率
            voice_type: 声音类型
            background_music: 背景音乐
            max_wait_time: 最大等待时间(秒)
            poll_interval: 轮询间隔(秒)
            progress_callback: 进度回调函数
            custom_params: 自定义参数
            
        Returns:
            包含视频URL和相关信息的结果字典
            
        Raises:
            Exception: 生成失败时抛出
        """
        # 提交任务（包含图片识别和视频生成两步骤）
        submit_result = self.generate_avatar_video(
            image_url=image_url,
            drive_mode=drive_mode,
            audio_url=audio_url,
            text=text,
            video_url=video_url,
            quality=quality,
            resolution=resolution,
            voice_type=voice_type,
            background_music=background_music,
            custom_params=custom_params
        )
        
        video_task_id = submit_result.get('task_id')
        if not video_task_id:
            raise Exception("视频生成任务提交失败,未获取到task_id")
        
        # 等待视频生成完成
        print(f"等待视频生成完成，任务ID: {video_task_id}")
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > max_wait_time:
                raise TimeoutError(f"视频生成任务{video_task_id}等待超时,已等待{elapsed:.0f}秒")
            
            result = self.query_avatar_task(video_task_id)
            status = result.get('status', '')
            progress = result.get('progress', 0)
            
            # 执行回调
            if progress_callback:
                progress_callback(video_task_id, progress, status)
            
            # 检查任务状态
            if status == 'success':
                print("视频生成完成！")
                return result
            elif status == 'failed':
                error_msg = result.get('message', '未知错误')
                raise Exception(f"视频生成任务{video_task_id}失败: {error_msg}")
            
            # 等待后继续轮询
            time.sleep(poll_interval)
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.session.close()


# 便捷函数
def create_video(
    access_key: str,
    secret_key: str,
    prompt: str,
    style: str = "default",
    resolution: str = "1080p",
    duration: int = 5,
    save_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    快速创建视频的便捷函数
    
    Args:
        access_key: 火山引擎Access Key
        secret_key: 火山引擎Secret Key
        prompt: 视频描述
        style: 视频风格
        resolution: 分辨率
        duration: 时长(秒)
        save_path: 视频保存路径(可选)
        
    Returns:
        生成结果字典
    """
    with JimengVideoClient(access_key=access_key, secret_key=secret_key) as client:
        result = client.generate_and_wait(
            prompt=prompt,
            style=style,
            resolution=resolution,
            duration=duration
        )
        
        # 如果指定了保存路径,则下载视频
        if save_path and result.get('video_url'):
            client.download_video(result['video_url'], save_path)
            result['local_path'] = save_path
        
        return result


def create_avatar_video(
    access_key: str,
    secret_key: str,
    image_url: str,
    drive_mode: str = "audio",
    audio_url: Optional[str] = None,
    text: Optional[str] = None,
    video_url: Optional[str] = None,
    quality: str = "high",
    save_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    快速创建数字人视频的便捷函数
    
    Args:
        access_key: 火山引擎Access Key
        secret_key: 火山引擎Secret Key
        image_url: 数字人图片URL
        drive_mode: 驱动模式 (audio/text/video)
        audio_url: 音频URL
        text: 文本内容
        video_url: 视频URL
        quality: 质量 (low/medium/high/ultra)
        save_path: 视频保存路径(可选)
        
    Returns:
        生成结果字典
    """
    with JimengVideoClient(access_key=access_key, secret_key=secret_key) as client:
        result = client.generate_avatar_and_wait(
            image_url=image_url,
            drive_mode=drive_mode,
            audio_url=audio_url,
            text=text,
            video_url=video_url,
            quality=quality
        )
        
        # 如果指定了保存路径,则下载视频
        if save_path and result.get('video_url'):
            client.download_video(result['video_url'], save_path)
            result['local_path'] = save_path
        
        return result



img_url = 'https://picaso-static.oss-cn-beijing.aliyuncs.com/cases/images/c578b3a4-b352-459f-b071-27a7aec9951e.png'


access_key = os.getenv("HUOSHAN_API_KEY")
secret_key = os.getenv("HUOSHAN_API_SECRET")



with JimengVideoClient(access_key=access_key, secret_key=secret_key) as client:
    response = client.submit_avatar_image_detection(img_url)
    print(response)
