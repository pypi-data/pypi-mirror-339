from mcp_server_time.server import TimeServer

def test_server():
    server = TimeServer()
    
    # 1. 测试获取不同地区的当前时间
    print("\n1. 测试获取不同地区的当前时间:")
    cities = {
        "上海": "Asia/Shanghai",
        "纽约": "America/New_York",
        "伦敦": "Europe/London",
        "东京": "Asia/Tokyo",
        "悉尼": "Australia/Sydney",
        "巴黎": "Europe/Paris"
    }
    
    for city, timezone in cities.items():
        result = server.get_current_time(timezone)
        print(f"{city}时间: {result.datetime} (夏令时: {'是' if result.is_dst else '否'})")
    
    # 2. 测试时区转换（多个时区）
    print("\n2. 测试时区转换:")
    test_time = "14:30"
    source_tz = "Asia/Shanghai"
    
    print(f"\n当{test_time}（上海时间）时，世界各地时间：")
    for city, target_tz in cities.items():
        if target_tz != source_tz:
            result = server.convert_time(
                source_tz=source_tz,
                time_str=test_time,
                target_tz=target_tz
            )
            print(f"{city}: {result.target.datetime} (时差: {result.time_difference})")
    
    # 3. 测试特殊时区
    print("\n3. 测试特殊时区:")
    special_zones = {
        "印度(非整点时区)": "Asia/Kolkata",        # UTC+5:30
        "尼泊尔(特殊时区)": "Asia/Kathmandu",      # UTC+5:45
        "澳大利亚中部": "Australia/Adelaide",      # UTC+9:30
    }
    
    print("\n特殊时区当前时间：")
    for name, timezone in special_zones.items():
        result = server.get_current_time(timezone)
        print(f"{name}: {result.datetime}")
    
    # 4. 测试时区转换（特殊时区）
    print("\n从上海时间14:30转换到特殊时区：")
    for name, target_tz in special_zones.items():
        result = server.convert_time(
            source_tz="Asia/Shanghai",
            time_str="14:30",
            target_tz=target_tz
        )
        print(f"{name}: {result.target.datetime} (时差: {result.time_difference})")

if __name__ == "__main__":
    test_server() 