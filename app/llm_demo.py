import os
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, OpenAI


def main() -> None:
    # 1. 从项目根目录读取 .env。
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(project_root / ".env")

    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()

    if not api_key:
        raise SystemExit("没有读取到 DEEPSEEK_API_KEY，请检查项目根目录的 .env。")

    # 2. 使用 DeepSeek 的地址和密钥创建客户端。
    try:
        with OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
            timeout=30.0,
            max_retries=0,
        ) as client:
            # 3. 提交一次模型请求。
            response = client.chat.completions.create(
                model="deepseek-flash",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "你是售后助手，请简洁回答。"
                            "没有订单查询工具提供的数据时，不得编造订单状态。"
                        ),
                    },
                    {
                        "role": "user",
                        "content": "请帮我查询订单 A1001 是否已经发货。",
                    },
                ],
                max_tokens=300,
                stream=False,
                extra_body={"thinking": {"type": "disabled"}},
            )

    except APIStatusError as error:
        raise SystemExit(
            f"API 请求失败，HTTP 状态码：{error.status_code}。"
            "请根据状态码检查请求或账户配置。"
        ) from None

    except APIConnectionError:
        raise SystemExit(
            "连接失败或请求超时，请检查网络及 API 地址，不要连续反复运行。"
        ) from None

    # 4. 读取模型回复。
    if not response.choices:
        raise SystemExit("API 没有返回可读取的回答。")

    message = response.choices[0].message

    print("模型：", response.model)
    print("回复：", message.content)
    print("结束原因：", response.choices[0].finish_reason)

    # 5. 查看本次调用的 Token 用量。
    if response.usage is not None:
        print("输入 Token：", response.usage.prompt_tokens)
        print("输出 Token：", response.usage.completion_tokens)


if __name__ == "__main__":
    main()