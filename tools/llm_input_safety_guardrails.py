from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.api_request_builder import ApiRequestBuilder 
import requests


class SafeGuardTool(Tool):
    """
    安全护栏工具类
    """

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        根据输入的监测内容和策略KEY，调用创思安全护栏接口进行内容安全检测。
        该工具将内容和策略KEY作为输入参数，返回安全护栏检测结果。

        Args:
            tool_parameters: 一个包含工具输入参数的字典:
                - c_content (str):  需要检测的内容。
                - strategy_key (str):  安全护栏策略KEY。

        Yields:
            ToolInvokeMessage: 包含安全护栏检测结果的消息。

        Raises:
            Exception: 如果凭证无效或请求失败，将抛出异常。
        """
        # 1. 从运行时获取凭证
        try:
            access_key = self.runtime.credentials["chuangsi_access_key"]
            secret_key = self.runtime.credentials["chuangsi_secret_key"]
        except KeyError:
            raise Exception("AccessKey 或 SecretKey 未配置或无效。请在插件设置中提供。")

        # 2. 获取工具输入参数
        c_content = tool_parameters.get("c_content", "") # 使用 .get 提供默认值
        strategy_key = tool_parameters.get("strategy_key", "")

        if not strategy_key:
            raise Exception("策略KEY不能为空。请提供有效的策略KEY。")

        # 1. 初始化签名工具
        builder = ApiRequestBuilder(access_key, secret_key)
        URL = "/api/content/safety"          # 接口路径
        BASE_URL = "https://api.chuangsiai.com"
        BODY = { "content": c_content , "strategyKey": strategy_key }  # 请求体内容
        # 2. 生成请求头（自动包含签名和时间戳）
        headers = builder.build_headers('POST', URL, BODY)
        # 3. 发送请求（发送请求的body参数必须和参加签名的body一致）
        try:
            response = requests.post(
                f"{BASE_URL}{URL}",
                json=BODY,
                headers=headers
            )
            response_data = response.json()
            # raise Exception(f"模拟调用安全护栏失败")
        except Exception as e:
            # 如果库调用失败，抛出异常
            raise Exception(f"调用安全护栏失败: {e}")

        # print("请求结果:", response_data)
        # if response_data.get("code") == 0:
        #     print("✅ 请求成功:", response_data)
        # else:
        #     print("❌ 请求错误:", response_data)

  
        # # 文本输出
        # yield self.create_text_message("这是文本消息")
        # # JSON输出
        # yield self.create_json_message({"key": "value"})
        # # 链接输出
        # yield self.create_link_message("https://example.com")
        # # 变量输出 (用于工作流)
        # yield self.create_variable_message("variable_name", "variable_value")
        # 4. 返回结果
        yield self.create_json_message(response_data)