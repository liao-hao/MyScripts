#!/usr/bin/env python3
# toolbox.py

import argparse
import json
import subprocess
import sys
import os
import shutil
import socket
import random
import string
import hashlib
import base64
from urllib.parse import quote, unquote


def kill_port(port):
    """杀死指定端口的进程"""
    try:
        # 在 Mac 上查找端口对应的进程
        cmd = f"lsof -i :{port} | grep LISTEN | awk '{{print $2}}'"
        process = subprocess.check_output(cmd, shell=True).decode().strip()

        if process:
            # 杀死进程
            subprocess.run(["kill", "-9", process])
            print(f"成功终止端口 {port} 的进程 (PID: {process})")
        else:
            print(f"端口 {port} 没有被占用")
    except subprocess.CalledProcessError:
        print(f"端口 {port} 没有被占用")
    except Exception as e:
        print(f"发生错误: {str(e)}")


def update_toolbox():
    """更新工具箱到 PATH 目录"""
    try:
        # 获取当前脚本路径
        current_path = '/Users/liaohao/PycharmProjects/MyScripts/toolbox.py'
        # 目标路径
        target_path = '/usr/local/bin/tb'

        # 检查权限
        if not os.access('/usr/local/bin', os.W_OK):
            print("需要管理员权限来更新工具箱")
            print("请使用: sudo tb update")
            return

        # 复制文件
        shutil.copy2(current_path, target_path)
        # 确保目标文件可执行
        os.chmod(target_path, 0o755)
        print(f"工具箱已更新到: {target_path}")

    except Exception as e:
        print(f"更新失败: {str(e)}")


def format_json(json_str):
    """格式化 JSON 字符串"""
    try:
        parsed = json.loads(json_str)
        formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
        print(formatted)
    except json.JSONDecodeError:
        print("无效的 JSON 格式")
    except Exception as e:
        print(f"发生错误: {str(e)}")


def get_local_ip():
    """获取本机IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        print(f"本机IP地址: {ip}")
    except Exception as e:
        print(f"获取IP地址失败: {str(e)}")


def generate_password(length=16):
    """生成随机密码"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(length))
    print(f"生成的密码: {password}")


def calculate_md5(file_path):
    """计算文件MD5值"""
    try:
        with open(file_path, 'rb') as f:
            md5 = hashlib.md5()
            while chunk := f.read(8192):
                md5.update(chunk)
        print(f"文件: {file_path}")
        print(f"MD5: {md5.hexdigest()}")
    except Exception as e:
        print(f"计算MD5失败: {str(e)}")


def base64_encode(text):
    """Base64编码"""
    try:
        encoded = base64.b64encode(text.encode()).decode()
        print(f"编码结果: {encoded}")
    except Exception as e:
        print(f"编码失败: {str(e)}")


def base64_decode(text):
    """Base64解码"""
    try:
        decoded = base64.b64decode(text).decode()
        print(f"解码结果: {decoded}")
    except Exception as e:
        print(f"解码失败: {str(e)}")


def url_encode(text):
    """URL编码"""
    try:
        encoded = quote(text)
        print(f"编码结果: {encoded}")
    except Exception as e:
        print(f"编码失败: {str(e)}")


def url_decode(text):
    """URL解码"""
    try:
        decoded = unquote(text)
        print(f"解码结果: {decoded}")
    except Exception as e:
        print(f"解码失败: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description='命令行工具箱')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    # 添加 update 命令
    update_parser = subparsers.add_parser('update', help='更新工具箱')
    # 配置 kill-port 命令
    kill_parser = subparsers.add_parser('kill-port', help='杀死指定端口的进程')
    kill_parser.add_argument('port', type=int, help='端口号')

    # 配置 format-json 命令
    format_parser = subparsers.add_parser('json', help='格式化 JSON')
    format_parser.add_argument('json_str', help='JSON 字符串')

    # 添加新的命令解析器
    ip_parser = subparsers.add_parser('ip', help='获取本机IP地址')

    pwd_parser = subparsers.add_parser('pwd', help='生成随机密码')
    pwd_parser.add_argument('-l', '--length', type=int, default=16, help='密码长度')

    md5_parser = subparsers.add_parser('md5', help='计算文件MD5值')
    md5_parser.add_argument('file', help='要计算MD5的文件路径')

    b64_parser = subparsers.add_parser('b64', help='Base64编解码')
    b64_parser.add_argument('action', choices=['encode', 'decode'], help='编码或解码')
    b64_parser.add_argument('text', help='要处理的文本')

    url_parser = subparsers.add_parser('url', help='URL编解码')
    url_parser.add_argument('action', choices=['encode', 'decode'], help='编码或解码')
    url_parser.add_argument('text', help='要处理的文本')

    args = parser.parse_args()

    if args.command == 'update':
        update_toolbox()
    elif args.command == 'killport':
        kill_port(args.port)
    elif args.command == 'json':
        format_json(args.json_str)
    elif args.command == 'ip':
        get_local_ip()
    elif args.command == 'pwd':
        generate_password(args.length)
    elif args.command == 'md5':
        calculate_md5(args.file)
    elif args.command == 'b64':
        if args.action == 'encode':
            base64_encode(args.text)
        else:
            base64_decode(args.text)
    elif args.command == 'url':
        if args.action == 'encode':
            url_encode(args.text)
        else:
            url_decode(args.text)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
