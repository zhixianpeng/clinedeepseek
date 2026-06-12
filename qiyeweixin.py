import requests
import json

WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0a615f47-a99f-47f7-ad22-583e23270044"

def send_markdown_message():
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": """
### 任务通知
**时间**：2025年6月5日
**状态**：✅ 执行成功aaaaaa
[点击查看详情](https://www.baidu.com)
            """
        }
    }
    response = requests.post(WEBHOOK_URL, json=data)
    print(response.json())

if __name__ == '__main__':
    send_markdown_message()