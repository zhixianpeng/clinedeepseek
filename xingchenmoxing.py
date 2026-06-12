import requests
import json


# -------------------------- 替换这里的信息 --------------------------
API_KEY = "app-XgDeAJDuUR1qcHD49FJDtD92"
API_URL = "https://agent.teleai.com.cn/v1/chat-messages"
USER_QUERY = ""
# ----------------------------------------------------------------

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "input_data": {},
    "query": USER_QUERY,
    "conversation_id": "",
    "mode": "streaming",
    "user": "admin",
    "files": []
}

response = requests.post(API_URL, headers=headers, json=payload)
print("状态码：", response.status_code)




full_content = ""
for line in response.iter_lines(decode_unicode=True):
    if line.startswith("data: "):
        # 去掉前缀解析json
        json_str = line[6:]
        try:
            data = json.loads(json_str)
            # 根据你返回的结构提取回答内容，适配不同格式
            if "answer" in data:
                full_content += data["answer"]
            elif "choices" in data and len(data["choices"])>0:
                # 兼容OpenAI格式的流式返回（比如DeepSeek、火山引擎都用这个结构）
                delta = data["choices"][0].get("delta", {})
                if "content" in delta:
                    full_content += delta["content"]
        except json.JSONDecodeError:
            continue

# 最终输出完整的回答
print("完整回答：\n", full_content)
