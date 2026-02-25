import os
import requests
import alibabacloud_oss_v2 as oss  # 导入阿里云OSS V2 SDK
from dotenv import load_dotenv

load_dotenv()


os.environ['OSS_ACCESS_KEY_ID'] = os.getenv("OSS_ACCESS_KEY_ID")
os.environ['OSS_ACCESS_KEY_SECRET'] = os.getenv("OSS_ACCESS_KEY_SECRET")


class AliyunOSS:
    """
    阿里云OSS工具类，用于上传图片到OSS存储
    """
    def __init__(self):
        """
        初始化OSS客户端
        """
        try:
            credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
            # 加载SDK的默认配置，并设置凭证提供者
            cfg = oss.config.load_default()
            cfg.credentials_provider = credentials_provider

            cfg.region = "cn-beijing"
            cfg.endpoint = "https://oss-cn-beijing.aliyuncs.com"

            # 使用配置好的信息创建OSS客户端
            self.oss_domain = ""
            self.client = oss.Client(cfg)
            self.bucket = ""
            self.endpoint = ""
            self.bucket_url = f"https://{self.bucket}.{self.endpoint}"
        except AttributeError as e:
            raise Exception("阿里云OSS配置缺失，请检查settings配置")
        except Exception as e:
            raise
    
    def upload_image(self, image_data, key, bucket="picaso-static"):
        """
        上传图片到OSS
        
        Args:
            image_data: 图片数据，可以是文件对象或二进制数据
            bucket: 存储空间名称，默认为picaso-ai-images
            key: 存储的文件夹路径
            
        Returns:
            str: 上传成功后的图片URL
        """
        try:
            # 执行上传对象的请求，指定存储空间名称、对象名称和数据内容
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=bucket,
                key=key,
                body=image_data,
            ))

            # 输出请求的结果状态码、请求ID、内容MD5、ETag、CRC64校验码和版本ID，用于检查请求是否成功
            print(f'status code: {result.status_code},'
                f' request id: {result.request_id},'
                f' content md5: {result.content_md5},'
                f' etag: {result.etag},'
                f' hash crc64: {result.hash_crc64},'
                f' version id: {result.version_id},'
            )
            return self.get_bucket_url(key)
                
        except Exception as e:
            raise Exception(f"上传图片到OSS时出错: {str(e)}")
    
    def upload_network_file(self, url, key, bucket="picaso-static"):
        """
        上传网络文件到OSS
        """
        try:
            # 从网络下载文件
            response = requests.get(url)
            if response.status_code == 200:
                # 上传文件到OSS
                return self.upload_image(response.content, key, bucket)
            else:   
                raise Exception(f"下载网络文件失败: {url}")
        except Exception as e:
            raise Exception(f"上传网络文件到OSS时出错: {str(e)}")
    
    def upload_local_file(self, file_path, bucket="picaso-static", key=None):
        """
        上传本地文件到OSS
        
        Args:
            file_path: 本地文件路径
            
        Returns:
            str: 上传成功后的文件URL
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise Exception(f"文件不存在: {file_path}")
            if not key:
                # 获取文件名
                filename = os.path.basename(file_path)
                key = f"cases/images/{filename}"
            
            # 打开文件并上传
            with open(file_path, 'rb') as file_obj:
                return self.upload_image(file_obj, key, bucket)
                
        except Exception as e:
            raise Exception(f"上传本地文件到OSS时出错: {str(e)}")
    
    def delete_file(self, key, bucket="picaso-static"):
        """
        从OSS删除文件
        
        Args:
            oss_path: OSS中的文件路径
            
        Returns:
            bool: 删除是否成功
        """
        try:
            # 如果传入的是完整URL，提取路径部分
            if key.startswith(self.bucket_url):
                key = key[len(self.bucket_url):].lstrip('/')
                
            result = self.client.delete_object(oss.DeleteObjectRequest(
                bucket=bucket,
                key=key,
            ))
            return result.status_code == 204
            
        except Exception as e:
            raise Exception(f"从OSS删除文件时出错: {str(e)}")
            return False

    def get_file_url(self, key):
        """
        获取OSS文件的URL
        
        Args:
            key: OSS中的文件路径
            bucket: 存储空间名称，默认为picaso-static
            
        Returns:
            str: 文件的URL
        """
        return f"{self.oss_domain}/{key}"
    
    def get_bucket_url(self, key):
        """
        获取OSS桶的URL
        """
        return f"{self.bucket_url}/{key}"


oss_client = AliyunOSS()



print(oss_client.upload_local_file('/Users/buzhimingrenshilaonianji/Downloads/20251117-150936.jpeg'))