from typing import Any
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from utils.api_request_builder import ApiRequestBuilder 
import requests

class ChuangsiaiProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证提供的 创思 AccessKey 是否有效。
        尝试使用该 token 创建一个测试页面。
        如果验证失败，应抛出 ToolProviderCredentialValidationError 异常。
        """
        access_key = credentials.get("chuangsi_access_key")
        secret_key = credentials.get("chuangsi_secret_key")
        if not access_key:
            raise ToolProviderCredentialValidationError("创思 AccessKey 不能为空。")
        if not secret_key:
            raise ToolProviderCredentialValidationError("创思 SecretKey 不能为空。")

        try:
            # 尝试执行一个凭证验证
            # 1. 初始化签名工具
            builder = ApiRequestBuilder(access_key, secret_key)
            URL = "/api/verify/signature"          # 接口路径 
            BASE_URL = "https://api.chuangsiai.com"
            BODY = { "content": "verify" }  # 请求体内容
            # 2. 生成请求头（自动包含签名和时间戳）
            headers = builder.build_headers('POST', URL, BODY)
            # 3. 发送请求（发送请求的body参数必须和参加签名的body一致）
            response = requests.post(
                f"{BASE_URL}{URL}",
                json=BODY,
                headers=headers
            )
            response_data = response.json()
            # print("验证:", response_data)
            if response_data.get("code") == 200:
                print("✅ 验证成功:", response_data)
                return
            else:
                print("❌ 验证错误:", response_data)
                raise Exception(response_data.get("message", "创思凭证验证失败，未知错误。"))
        except Exception as e:
            print("❌ 验证请求错误:", e)
            # 如果 API 调用失败，说明凭证很可能无效
            raise ToolProviderCredentialValidationError(f"创思 凭证验证失败: {e}")