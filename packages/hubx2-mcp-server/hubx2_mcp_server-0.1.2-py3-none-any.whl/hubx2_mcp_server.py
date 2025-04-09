import os
import webbrowser
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("hubx2-mcp-server")


import requests
import json



def call_jsonrpc(method, params=None):
    """
    调用JSON-RPC方法
    
    Args:
        method: 方法名称
        params: 方法参数
    
    Returns:
        响应结果
    """
    # 构建JSON-RPC请求数据
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }

    # 参数需要作为一个数组或对象传递
    if params is not None:
        # 如果参数是单一值，将其包装在列表中
        if not isinstance(params, (dict, list)):
            params = [params]
        payload["params"] = params

    # 发送请求到服务器
    exec_host = os.getenv('HUBX_EXEC_HOST') if os.getenv('HUBX_EXEC_HOST') else '127.0.0.1'
    response = requests.post(
        f"http://{exec_host}:8061/jsonrpc",  # 替换为实际服务器IP
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )

    # 解析响应
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容类型: {response.headers.get('Content-Type', '未知')}")

    try:
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '').lower()

            # 检查是否为二进制数据
            if 'application/octet-stream' in content_type or 'application/binary' in content_type:
                return {"result": f"[二进制数据，长度: {len(response.content)}字节]"}

            # 检查是否为XML
            elif 'application/xml' in content_type or 'text/xml' in content_type:
                return {"result": response.text}

            # 默认尝试解析为JSON
            else:
                return response.json()
        else:
            return {"error": f"HTTP错误: {response.status_code}"}
    except json.JSONDecodeError:
        # 如果JSON解析失败，返回原始文本
        return {"result": response.text}
    finally:
        response.close()



@mcp.tool()
async def start_performance_test() -> str:
    """在设备上开启性能测试（包含内存和cpu测试）"""
    result = call_jsonrpc('start_performance_test')
    return result



@mcp.tool()
async def stop_performance_test() -> str:
    """停止进行中的性能测试（包含内存和cpu测试）"""
    result = call_jsonrpc('stop_performance_test')
    return result


@mcp.tool()
async def change_hubx_theme(theme_name:str) -> str:
    """切换HubX的主题
    Args:
        theme: 主题名称，仅支持"dark"或"light"
    """
    result = call_jsonrpc('change_hubx_theme', theme_name)
    return result

@mcp.tool()
async def run_recent_autotest_task() -> str:
    """运行最近一次的自动化测试任务"""
    result = call_jsonrpc('run_recent_autotest_task')
    return result

@mcp.tool()
async def stop_autotest_task() -> str:
    """停止所有的的自动化测试任务"""
    result = call_jsonrpc('stop_autotest_task')
    return result


@mcp.tool()
async def execute_autotest_script(text:str) -> str:
    """在hubx上执行自动化测试脚本"""
    if 'ui = Device()' not in text:
        text = 'ui = Device()\n' + text

    result = call_jsonrpc('execute_autotest_script', text)
    return result

@mcp.tool()
async def edit_autotest_script(text:str) -> str:
    """在hubx上插入自动化测试脚本"""
    result = call_jsonrpc('edit_autotest_script', text)
    return result

@mcp.tool()
async def stop_autotest_script() -> str:
    """停止正在执行的自动化测试脚本"""
    result = call_jsonrpc('stop_execute_autotest_script')
    return result

@mcp.tool()
async def get_tool_use_chart() -> str:
    """获取hubx工具使用情况图表"""
    chart_url = 'http://10.10.96.223:8023/user/chart'
    webbrowser.open(chart_url)
    return {"tool_use_chart": chart_url}


@mcp.tool()
async def porsche_upgrade_car_version(version_num=None, upgrade_type='all') -> str:
    """
    保时捷项目车机升级版本
    Args:
        version_num(int): 版本号，默认为None，如果为None，则使用最新版本，否则选择升级到指定版本
        upgrade_type(str): 升级类型，默认为'all'，可选值为'all'、'mpu'、'mcu',分别对应升级整机，仅升级mpu版本和mcu版本
    """
    result = call_jsonrpc('porsche_upgrade_car_version', [version_num, upgrade_type])
    return result
    
@mcp.tool()
async def get_resource_image_data() -> str:
    """获取资源图片数据"""
    result = call_jsonrpc('get_resource_image_data')
    return result


@mcp.tool()
async def get_xml_hierarchy_data() -> str:
    """获取页面XML层级数据"""
    result = call_jsonrpc('get_xml_hierarchy_data')

    # 检查结果是否包含二进制数据并进行适当处理
    if isinstance(result, dict) and 'result' in result:
        # 如果结果是二进制数据，可能需要进行适当的编码转换
        if isinstance(result['result'], str):
            try:
                # 尝试解析为JSON字符串
                return result['result']
            except Exception as e:
                return f"处理XML数据时出错：{str(e)}"
        elif isinstance(result['result'], (dict, list)):
            # 如果是复杂的数据结构，转换为JSON字符串
            return json.dumps(result['result'], ensure_ascii=False)
        else:
            # 其他情况
            return str(result['result'])

    # 返回原始结果的字符串表示
    return str(result)

def main():
    """主函数"""
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()