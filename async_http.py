import asyncio
import json
import time
import uuid
from collections import deque

import aiohttp
from rich.live import Live
from rich.panel import Panel

url = "http://localhost:8080/hello"

headers = {
    "Content-Type": "application/json",
}


def create_payload(fill_str: str) -> dict:
    return {
        "serviceId": "passthrough",
        "inputParams": {
            "requestData": {
                "method": "multipleRequest",
                "params": {
                    "requests": [
                        {
                            "method": "relativeMove",
                            "params": {
                                "motor": fill_str
                            }
                        }
                    ]
                }
            }
        }
    }


async def main():
    # 步骤1: 配置参数
    target_url = url
    total_ops = 800 * 10  # 总请求量
    concurrency = 100  # 并发连接数
    ops_per_second = 800  # 目标OPS
    timeout_seconds = 5  # 单请求超时

    # 步骤2: 创建共享数据结构
    rate_limiter = deque(maxlen=ops_per_second)
    stats = {
        'success': 0,
        'failures': 0,
        'latencies': []
    }

    # 步骤3: 创建异步会话
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=concurrency),
            timeout=aiohttp.ClientTimeout(total=timeout_seconds)
    ) as session:
        tasks = []
        start_time = time.monotonic()

        # 创建生产者和消费者
        async def producer():
            interval = 1.0 / ops_per_second
            next_time = start_time
            while len(tasks) < total_ops:
                if time.monotonic() >= next_time:
                    rate_limiter.append(time.monotonic())
                    next_time += interval
                await asyncio.sleep(0.001)

        async def consumer():
            while len(stats['latencies']) < total_ops:
                if rate_limiter:
                    rate_limiter.popleft()
                    req_start = time.monotonic()
                    try:
                        random_str = str(uuid.uuid4())
                        async with session.post(url=target_url, headers=headers,
                                                data=json.dumps(create_payload(
                                                    random_str))) as resp:
                            if resp.status == 200:
                                stats['success'] += 1
                            else:
                                stats['failures'] += 1
                    except Exception:
                        stats['failures'] += 1
                    finally:
                        stats['latencies'].append(time.monotonic() - req_start)
                await asyncio.sleep(0.001)

        # 启动并发任务
        tasks = [asyncio.create_task(consumer()) for _ in range(concurrency)]
        tasks.append(asyncio.create_task(producer()))

        # 等待完成
        with Live(auto_refresh=False) as live:
            while len(stats['latencies']) < total_ops:
                current = len(stats['latencies'])
                total = total_ops
                # print(f"{len(stats['latencies'])} - {total_ops}")
                # 构建显示内容
                current_int = int(current / total * 100)
                total_int = 100
                content = f"[bold green]Progress:[/] {current}/{total}\n"
                content += "▰" * current_int + "▱" * (total_int - current_int)

                # 更新Live显示
                live.update(Panel(content, title="Processing"))
                live.refresh()

                await asyncio.sleep(0.1)

        # 计算统计数据
        duration = time.monotonic() - start_time
        actual_ops = len(stats['latencies']) / duration
        avg_latency = sum(stats['latencies']) * 1000 / len(stats['latencies'])

        print(f"\nResults:")
        print(f"Target OPS: {ops_per_second}/s")
        print(f"Actual OPS: {actual_ops:.2f}/s")
        print(f"Success Rate: {(stats['success'] / total_ops) * 100:.2f}%")
        print(f"Average Latency: {avg_latency:.2f}ms")
        print(f"Total Duration: {duration:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
