# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_random_reply']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.2.1,<3.0.0',
 'nonebot-plugin-send-anything-anywhere>=0.7.1,<0.8.0',
 'nonebot2>=2.2.0,<3.0.0',
 'nonebot_plugin_userinfo>=0.2.6,<0.3.0',
 'openai>=1.55.3,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-random-reply',
    'version': '0.4.0',
    'description': '随机攻击群友插件',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-random-reply\n</div>\n\n# 介绍\n- 根据当前语境在群聊内随机攻击群友\n- 可以更换回复风格prompt自定义bot的说话风格随机拟人回复\n- 基于ChatGLM大模型智能体选择表情包拟人回复，功能实现使用了[该博客](https://www.vinlic.com/p/47461/#%E5%88%9B%E5%BB%BA%E6%99%BA%E8%83%BD%E4%BD%93)的思路和[该项目](https://github.com/LLM-Red-Team/emo-visual-data)的表情包视觉标注。使用[glm-free-api](https://github.com/LLM-Red-Team/glm-free-api)进行api轻量化调用。\n- 支持Gemini和oneapi格式的LLM\n\n> "有什么让LLM更拟人的方案？\n>\n>哎！我发现原来缺了点表情包！假如模型会发表情包岂不是很好玩？\n>\n>表情包是一种模因，模因就是可以被人模仿并传递给其他人的信息，比如一段音乐、一个观念、一个时尚趋势、一句流行语、一个动作等等，但不是所有模因都像表情包这样能够简洁表达一种心境，还具有高度的传染性和多样性，每次发送和接收表情包都会让我们大脑产生多巴胺。\n>\n>借助多模态大模型的视觉推理对表情包图像进行数据标注，再将这批数据作为知识库内容，智谱清言是否有能力通过用户输入的query来RAG（检索增强）检索到语义最接近的表情包数据，然后将相应的表情包图像文件名输出？"  \n> —— 表情包智能体诞生记\n\n\n- bot的回复效果与选用的llm模型有关，经过半个多月的测试，中文语境下使用deepseek-r1的回复效果最佳，但是成本较高。推荐使用deepseek-v3模型，在保证回复质量的情况下减少使用成本。免费方案可以使用硅基流动的THUDM/glm-4-9b-chat模型进行下位替代，但是效果欠佳。\n- bot的回复效果也与调教prompt有关，通过修改prompt也可以达到模拟真人在群聊内回复的效果，欢迎prompt工程师们优化当前的prompt。\n\n# 效果\n<img src="demo2.jpg" width="40%">\n<img src="demo5.png" width="40%">\n<img src="demo4.jpg" width="40%">\n<img src="demo6.png" width="40%">\n<img src="demo1.jpg" width="40%">\n<img src="demo3.jpg" width="40%">\n\n\n# 安装\n\n* 手动安装\n  ```\n  git clone https://github.com/Alpaca4610/nonebot_plugin_random_reply.git\n  ```\n\n  下载完成后在bot项目的pyproject.toml文件手动添加插件：\n\n  ```\n  plugin_dirs = ["xxxxxx","xxxxxx",......,"下载完成的插件路径/nonebot-plugin-random-reply]\n  ```\n* 使用 pip\n  ```\n  pip install nonebot-plugin-random-reply\n  ```\n\n# 配置文件\n\n在Bot根目录下的.env文件中追加如下内容：\n## 必填内容：\n#### 回复模型支持oneapi格式的模型和Gemini，只填oneapi_key则使用指定的oneapi格式的模型，只填gemini_key则使用对应的gemini模型，两者都填则默认使用oneapi格式的模型，二选一填即可\n```\noneapi_key = ""  # OneAPI KEY\noneapi_url = ""  # llm提供商地址，使用deepseek请填写"https://api.deepseek.com"，使用硅基流动请填写"https://api.siliconflow.cn/v1"，使用OpenAI官方服务不需要填写\noneapi_model = "deepseek-chat" # 使用的语言大模型，建议使用ds-v3模型兼顾质量和成本\n\ngemini_model = "gemini-2.0-flash" # Gemini模型，不填默认使用gemini-2.0-flash达到较好的效果\ngemini_key = ""  # Gemini KEY\n\nrandom_re_g = ["123456789","987654321"]  # 启用随机回复的群聊白名单\n```\n\n## 可选内容（嫌麻烦可以不看）：\n```\nreply_lens = 30 # 参考的聊天记录长度\nreply_pro = 0.08   # 随机回复概率，取值范围0~1，越大回复概率越高\nreply_prompt_url = ""  # 自定义bot的回复风格prompt的txt文件的**绝对路径**\n```\n## 表情包配置（可以不配置，不影响文字回复）：\n根据[此处](https://github.com/LLM-Red-Team/glm-free-api?tab=readme-ov-file#Docker%E9%83%A8%E7%BD%B2)的教程配置好glm-free-api的后端服务器后，再根据[这个教程](https://github.com/LLM-Red-Team/glm-free-api?tab=readme-ov-file#%E6%8E%A5%E5%85%A5%E5%87%86%E5%A4%87)获取chatglm的token。得到后端服务器地址和chatglm的token后，在bot配置文件中追加：\n```\nrandom_meme_url = "http://xxx.xxx.xxx.xxx:xxxx/v1/images/generations"    # 用于llm选择表情包的glm-free-api地址\nrandom_meme_token = ""     # glm-free-api的token\n```\n\n# 使用方法\n- 填好配置文件和群聊白名单后，bot就会根据当前话题随机攻击群友\n- 不填写表情包发送相关配置不会发送表情包\n- @机器人会根据本条信息回复\n\n# 自定义prompt范例\n\n```\n【任务规则】\n1. 根据当前聊天记录的语境，回复最后1条内容进行回应，聊天记录中可能有多个话题，注意分辨最后一条信息的话题，禁止跨话题联想其他历史信息\n2. 用中文互联网常见的口语化短句回复，禁止使用超过30个字的长句\n3. 模仿真实网友的交流特点：适当使用缩写、流行梗、表情符号（但每条最多1个）,精准犀利地进行吐槽\n4. 输出必须为纯文本，禁止任何格式标记或前缀\n5. 使用00后常用网络语态（如：草/绝了/好耶）\n6. 核心萌点：偶尔暴露二次元知识\n7. 当出现多个话题时，优先回应最新的发言内容\n\n【回复特征】\n- 句子碎片化（如：笑死 / 确实 / 绷不住了）\n- 高频使用语气词（如：捏/啊/呢/吧）\n- 有概率根据回复的语境加入合适emoji帮助表达\n- 有概率使用某些流行的拼音缩写\n- 有概率玩谐音梗\n\n【应答策略】\n遇到ACG话题时：\n有概率接经典梗（如：团长你在干什么啊团长）\n禁用颜文字时改用括号吐槽（但每3条限1次）\n克制使用表情包替代词（每5条发言限用1个→）\n```\n',
    'author': 'Alpaca',
    'author_email': '202396298@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
