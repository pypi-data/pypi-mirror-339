from dotenv import load_dotenv

import argparse
import requests
import os

load_dotenv()

def get_weather(city: str, api_key: str = None):
    """
    获取指定城市的天气信息（模拟数据）
    
    Args:
        city: 城市名称
        api_key: 由于使用模拟数据，此参数将被忽略
    """
    print(f"正在查询城市 '{city}' 的天气信息...")
    if api_key:
        print(f"使用提供的API密钥: {api_key[:4]}...")
    else:
        print("未提供API密钥,使用模拟数据")
    # 使用模拟数据
    mock_data = {
        "location": {
            "name": city,
            "country": "模拟国家"
        },
        "current": {
            "temp_c": 23.5,
            "condition": {
                "text": "晴朗"
            },
            "wind_kph": 15.5,
            "humidity": 65
        }
    }
    
    try:
        data = mock_data
        print(f"城市: {data['location']['name']}, {data['location']['country']}")
        print(f"温度: {data['current']['temp_c']}°C")
        print(f"天气: {data['current']['condition']['text']}")
        print(f"风速: {data['current']['wind_kph']} km/h")
        print(f"湿度: {data['current']['humidity']}%")
    except KeyError as e:
        print(f"数据解析错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")

def main():
    parser = argparse.ArgumentParser(description="城市天气查询工具")
    parser.add_argument("city", help="要查询的城市名称")
    parser.add_argument("--api-key", help="WeatherAPI的API密钥，也可通过WEATHER_API_KEY环境变量设置")
    
    args = parser.parse_args()
    get_weather(args.city, args.api_key)

if __name__ == "__main__":
    main() 