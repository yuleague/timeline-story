#!/usr/bin/env python3
"""
创建头像目录和默认头像
"""
import os
import shutil
from pathlib import Path

# 创建头像目录结构
avatar_dir = Path("/static/images/avatar")
avatar_dir.mkdir(parents=True, exist_ok=True)

# 复制默认头像（如果没有）
default_avatar = avatar_dir / "default.png"
if not default_avatar.exists():
    # 创建简单的默认头像
    from PIL import Image, ImageDraw
    
    # 创建256x256的灰色头像
    img = Image.new('RGB', (256, 256), color='#cccccc')
    draw = ImageDraw.Draw(img)
    
    # 绘制一个简单的人形图标
    # 头部
    draw.ellipse([80, 40, 176, 136], fill='#999999')
    # 身体
    draw.rectangle([120, 136, 136, 180], fill='#999999')
    # 手臂
    draw.rectangle([80, 140, 120, 148], fill='#999999')
    draw.rectangle([136, 140, 176, 148], fill='#999999')
    # 腿
    draw.rectangle([120, 180, 128, 220], fill='#999999')
    draw.rectangle([128, 180, 136, 220], fill='#999999')
    
    img.save(default_avatar, 'PNG')
    print(f"✅ 创建默认头像: {default_avatar}")

print("✅ 头像目录结构创建完成")
print(f"   目录位置: {avatar_dir}")