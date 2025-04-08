import json
import subprocess
import sys

def test_mcp_server(command):
    tests = [
        {
            "name": "测试echo工具",
            "input": {"name": "echo_tool", "arguments": {"text": "你好，世界！"}},
            "expected": "你好，世界！"
        },
        {
            "name": "测试静态资源",
            "input": {"type": "resource", "name": "echo://static"},
            "expected": "Echo!"
        },
        {
            "name": "测试动态资源",
            "input": {"type": "resource", "name": "echo://测试文本"},
            "expected": "Echo: 测试文本"
        },
        {
            "name": "测试提示词",
            "input": {"type": "prompt", "name": "echo", "arguments": {"text": "这是一个提示词"}},
            "expected": "这是一个提示词"
        }
    ]

    for test in tests:
        print(f"\n执行测试: {test['name']}")
        input_json = json.dumps(test['input'], ensure_ascii=False)
        
        try:
            # 启动服务器进程
            process = subprocess.Popen(
                command.split(),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 等待服务器启动
            while True:
                line = process.stderr.readline()
                if not line or "Server is ready" in line:
                    break
            
            # 发送测试输入
            print(f"发送: {input_json}")
            process.stdin.write(input_json + "\n")
            process.stdin.flush()
            
            # 读取响应
            response = process.stdout.readline().strip()
            print(f"收到: {response}")
            
            # 验证响应
            try:
                response_json = json.loads(response)
                if response_json.get("result") == test["expected"]:
                    print("✅ 测试通过")
                else:
                    print("❌ 测试失败")
                    print(f"预期: {test['expected']}")
                    print(f"实际: {response_json.get('result')}")
            except json.JSONDecodeError:
                print("❌ 测试失败：响应不是有效的JSON")
                print(f"收到的响应: {response}")
        
        finally:
            # 确保进程被终止
            process.terminate()
            process.wait()

if __name__ == "__main__":
    command = "uvx baiyx-mcp-server-echo"
    test_mcp_server(command) 