## Chuangsi LLM Safety Tools for Dify

**作者：** Chuangsi AI

**版本：** 0.0.4

**类型：** tool

### 概述

创思大模型安全工具是一款面向大语言模型的内容安全防护系统，旨在识别和拦截 LLM 输入与输出中的潜在安全风险，包括涉政敏感、色情、违法违规行为、负面价值导向、辱骂言论及隐私泄露等内容。针对存在风险的输入，该工具还支持安全可信代答，助力用户实现大模型系统的安全合规。

### 主要功能

**安全护栏**：识别并拦截大模型输入与输出中的内容安全风险，包括涉政、色情、违法违规、负面价值观、辱骂仇恨、恶意营销及隐私泄露等问题。

**安全代答**：针对存在潜在风险的输入，提供具备正向引导和内容安全的安全代答能力。

**灵活集成**：可无缝接入 Dify 架构，支持工作流、Agent 等多种对接方式。

**灵活配置**：支持自定义安全关键词、风险问答库与兜底回复，便于快速调整和管控安全策略。

### 基本使用示例

#### 安装及授权

1、登录 **创思大模型安全控制台**，https://console.chuangsiai.com/#/login?redirect=/dashboard/index

2、获取 **Access Key**和 **Secret Key**， https://console.chuangsiai.com/#/profile/accessKey

3、通过 **Marketplace**安装插件，安装完毕后点击“去授权”，并输入上述**Access Key**和 **Secret Key**，确保认证成功。
![image](https://github.com/user-attachments/assets/e47fa2dc-d12c-46cf-8e33-8cc56ea26200)

#### 创建安全策略

1、在**创思大模型安全控制台**，创建安全策略，获取**策略 ID**
![image](https://github.com/user-attachments/assets/7242c7c9-a0fc-4785-86cc-dad029d8da63)

2、点击上述创建的**安全策略**进入策略详情页，点击**配置**按钮，可以配置风险审查项的启用状态，配置用户自定义的安全审查词库、安全代答红线库等。
![image](https://github.com/user-attachments/assets/d6cf7f73-223b-4fa7-8239-ea1f352574f6)

#### 在 Chatflow 中调用

**Chatflow 简易示例**：分别调用插件对输入和输出进行内容安全审查，并搭配“条件分支”来进行判断。如果检测结果 suggestion 字段为"block"，则采用兜底的 Wording 进行作答，否则继续工作流或者输出 LLM 回答结果。
![image](https://github.com/user-attachments/assets/bce0edb5-3ec6-497e-8206-b95a385bd070)

**输入和输出工具调用示例如下**：
![image](https://github.com/user-attachments/assets/6954a8a6-7661-481a-9e0f-5ce66a8d8c9a)

具体参数说明如下：

- 待审查内容：大模型输入 or 大模型回答内容
- 策略 ID：上一部分介绍的在创思大模型安全控制台创建完安全策略后，获取的**策略 ID**

简易示例中，提取输入/回答安全审查处理建议节点代码如下：

```python
def main(arg1: str) -> dict:
    first_level_suggestion = arg1[0].get("suggestion")
    return {
        "result": first_level_suggestion,
    }
```

#### 在 Agent 中调用

以下是一个维基百科搜索安全审查智能体的示例，该智能体目标是对用户搜索词和搜索结果进行安全审查。

```
你是一个维基百科搜索大师，能够熟练调用 `wikipedia_search` 工具，为用户搜索维基百科的相关信息。

第一步：当用户提出具体的搜索需求时，先调用 `chuangsi_safe_guardrail` 工具，对用户的输入进行安全审查，工具的待监测文本内容字段输入就是用户搜索内容：
如果返回结果 `suggestion` 字段为 `block` 时，则直接返回“你的问题我无法为你提供检索服务，请尝试搜索其他话题。”
如果返回结果 `suggestion` 字段为 `pass` 或者 `review` 时，可以进入下一步。

第二步：调用 `wikipedia_search` 工具对用户搜索内容进行搜索，查询语句即为用户搜索内容，语言为中文。搜索完成后，返回搜索结果，并进入第三步。

第三步：调用 `chuangsi_safe_guardrail` 工具，对第二步返回的搜索结果进行安全审查，工具的待监测文本内容字段输入就是第二步返回的搜索结果：
如果返回结果 `suggestion` 字段为 `block` 时，则直接返回“维基百科检索的内容存在极端风险，将不予展示。”
如果返回结果 `suggestion` 字段为 `review` 时，则直接返回“维基百科检索的内容存在有潜在风险，请仔细甄别后采用。”+搜索返回结果。
如果返回结果 `suggestion` 字段为 `pass` 时，正常返回搜索结果即可。
```

![image](https://github.com/user-attachments/assets/d86383ee-83e5-41ae-9919-c48f55fea778)

### 功能演示

![image](https://github.com/user-attachments/assets/d1d2ee0e-71fa-44bd-8aab-50dab9db889d)

## Changelog

### v0.0.4

- 优化签名工具，使用 chuangsiai-sdk

### v0.0.3

- 修改调用说明文档

### v0.0.2

- 实现安全护栏插件

### v0.0.1

- 初始版本，实现基本调用鉴权逻辑
