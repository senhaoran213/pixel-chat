#!/usr/bin/env python3
"""
简单的API测试脚本
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("🚀 开始测试 Pixel Chat API...")
    
    # 测试根路径
    print("\n1. 测试根路径...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 根路径访问成功")
        else:
            print("❌ 根路径访问失败")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return
    
    # 测试创建用户
    print("\n2. 测试创建用户...")
    try:
        response = requests.post(f"{BASE_URL}/users", data={"username": "测试用户"})
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ 用户创建成功: {user_data}")
            user_id = user_data.get("user_id")
        else:
            print("❌ 用户创建失败")
            return
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        return
    
    # 测试获取用户列表
    print("\n3. 测试获取用户列表...")
    try:
        response = requests.get(f"{BASE_URL}/users")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ 获取用户列表成功: {len(users)} 个用户")
        else:
            print("❌ 获取用户列表失败")
    except Exception as e:
        print(f"❌ 获取用户列表失败: {e}")
    
    # 测试获取聊天室列表
    print("\n4. 测试获取聊天室列表...")
    try:
        response = requests.get(f"{BASE_URL}/rooms")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            rooms = response.json()
            print(f"✅ 获取聊天室列表成功: {len(rooms)} 个聊天室")
            if rooms:
                room_id = rooms[0].get("id")
                print(f"   第一个聊天室ID: {room_id}")
        else:
            print("❌ 获取聊天室列表失败")
    except Exception as e:
        print(f"❌ 获取聊天室列表失败: {e}")
    
    # 测试创建聊天室
    print("\n5. 测试创建聊天室...")
    try:
        response = requests.post(f"{BASE_URL}/rooms", data={"name": "测试聊天室"})
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            room_data = response.json()
            print(f"✅ 聊天室创建成功: {room_data}")
        else:
            print("❌ 聊天室创建失败")
    except Exception as e:
        print(f"❌ 创建聊天室失败: {e}")
    
    print("\n🎉 API测试完成！")
    print(f"📱 现在可以访问 http://localhost:8000 来测试聊天功能")

if __name__ == "__main__":
    test_api()
