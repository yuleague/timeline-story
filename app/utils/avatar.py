import os
import uuid
from PIL import Image
import io
from flask import current_app
from pathlib import Path
import secrets

class AvatarManager:
    """头像管理器，处理头像的上传、压缩、存储和修改"""
    
    AVATAR_DIR = 'static/images/avatar'
    DEFAULT_AVATAR = 'static/images/avatar/default.png'
    
    # 支持的图片格式
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    # 头像尺寸
    AVATAR_SIZES = {
        'small': (64, 64),
        'medium': (128, 128),
        'large': (256, 256),
        'original': None  # 保持原尺寸
    }
    
    @staticmethod
    def allowed_file(filename):
        """检查文件扩展名是否允许"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in AvatarManager.ALLOWED_EXTENSIONS
    
    @staticmethod
    def generate_filename(original_filename, user_id=None):
        """生成唯一的文件名"""
        # 生成UUID作为文件名
        ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'png'
        filename = f"{uuid.uuid4().hex}.{ext}"
        
        # 如果提供user_id，可以按用户ID组织目录
        if user_id:
            user_dir = str(user_id % 100)  # 使用用户ID的模来分散文件
            return os.path.join(user_dir, filename)
        
        return filename
    
    @staticmethod
    def get_avatar_path(filename=''):
        """获取头像存储路径"""
        # 获取项目根目录
        root_path = Path(current_app.root_path)
        avatar_path = root_path / AvatarManager.AVATAR_DIR
        
        # 确保目录存在
        avatar_path.mkdir(parents=True, exist_ok=True)
        
        if filename:
            # 如果文件名包含子目录，确保子目录存在
            if '/' in filename:
                subdir = avatar_path / os.path.dirname(filename)
                subdir.mkdir(parents=True, exist_ok=True)
            
            return avatar_path / filename
        
        return avatar_path
    
    @staticmethod
    def save_avatar(image_file, user_id=None):
        """
        保存头像图片
        
        Args:
            image_file: 上传的图片文件
            user_id: 用户ID（可选）
        
        Returns:
            dict: 包含各种尺寸头像URL的字典
        """
        if not AvatarManager.allowed_file(image_file.filename):
            raise ValueError("不支持的文件格式")
        
        # 生成文件名
        original_filename = AvatarManager.generate_filename(image_file.filename, user_id)
        
        # 读取图片
        try:
            img = Image.open(image_file.stream)
            
            # 转换为RGB模式（处理PNG透明度）
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # 保存各种尺寸的头像
            avatar_urls = {}
            
            for size_name, size in AvatarManager.AVATAR_SIZES.items():
                # 处理图片
                if size:
                    # 调整尺寸，保持宽高比
                    img_copy = img.copy()
                    img_copy.thumbnail(size, Image.Resampling.LANCZOS)
                    processed_img = img_copy
                else:
                    processed_img = img
                
                # 生成文件名
                if size_name == 'original':
                    filename = original_filename
                else:
                    name, ext = os.path.splitext(original_filename)
                    filename = f"{name}_{size_name}{ext}"
                
                # 保存图片
                filepath = AvatarManager.get_avatar_path(filename)
                
                # 根据扩展名选择格式和质量
                ext = Path(filename).suffix.lower()
                if ext in ['.jpg', '.jpeg']:
                    processed_img.save(filepath, 'JPEG', quality=85, optimize=True)
                elif ext == '.webp':
                    processed_img.save(filepath, 'WEBP', quality=85)
                else:
                    processed_img.save(filepath, optimize=True)
                
                # 存储URL
                avatar_urls[size_name] = f"/{AvatarManager.AVATAR_DIR}/{filename}"
            
            return {
                'success': True,
                'avatar_urls': avatar_urls,
                'primary_url': avatar_urls.get('medium')  # 默认使用中等尺寸
            }
            
        except Exception as e:
            raise Exception(f"图片处理失败: {str(e)}")
    
    @staticmethod
    def delete_avatar(avatar_url):
        """
        删除头像文件
        
        Args:
            avatar_url: 头像URL
        
        Returns:
            bool: 是否成功删除
        """
        try:
            if avatar_url == f"/{AvatarManager.DEFAULT_AVATAR}":
                # 默认头像不删除
                return True
            
            # 从URL提取文件名
            filename = avatar_url.replace(f"/{AvatarManager.AVATAR_DIR}/", "")
            if not filename:
                return False
            
            # 删除所有尺寸的文件
            filepath = AvatarManager.get_avatar_path(filename)
            if filepath.exists():
                filepath.unlink()
            
            # 删除其他尺寸的文件
            name, ext = os.path.splitext(filename)
            for size_name in ['small', 'medium', 'large']:
                size_filename = f"{name}_{size_name}{ext}"
                size_filepath = AvatarManager.get_avatar_path(size_filename)
                if size_filepath.exists():
                    size_filepath.unlink()
            
            return True
            
        except Exception as e:
            current_app.logger.error(f"删除头像文件失败: {str(e)}")
            return False
    
    @staticmethod
    def generate_default_avatar(username, user_id=None):
        """
        生成默认头像（基于用户名首字母）
        
        Args:
            username: 用户名
            user_id: 用户ID（可选）
        
        Returns:
            str: 头像URL
        """
        from PIL import Image, ImageDraw, ImageFont
        import random
        
        try:
            # 获取首字母
            first_char = username[0].upper() if username else 'U'
            
            # 颜色方案（基于首字母生成一致的颜色）
            colors = [
                "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
                "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"
            ]
            
            # 使用首字母的ASCII码选择颜色
            color_idx = ord(first_char) % len(colors)
            bg_color = colors[color_idx]
            
            # 创建图像
            img_size = 256
            img = Image.new('RGB', (img_size, img_size), color=bg_color)
            draw = ImageDraw.Draw(img)
            
            # 尝试加载字体
            try:
                # 使用系统字体
                font = ImageFont.truetype("arial.ttf", 120)
            except:
                # 备用字体
                font = ImageFont.load_default()
            
            # 计算文本位置
            text_bbox = draw.textbbox((0, 0), first_char, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (img_size - text_width) // 2
            y = (img_size - text_height) // 2
            
            # 绘制文本
            draw.text((x, y), first_char, fill="white", font=font)
            
            # 生成文件名
            filename = AvatarManager.generate_filename(f"{first_char}.png", user_id)
            filepath = AvatarManager.get_avatar_path(filename)
            
            # 保存图片
            img.save(filepath, 'PNG', optimize=True)
            
            return f"/{AvatarManager.AVATAR_DIR}/{filename}"
            
        except Exception as e:
            current_app.logger.error(f"生成默认头像失败: {str(e)}")
            return f"/{AvatarManager.DEFAULT_AVATAR}"
    
    @staticmethod
    def validate_preset_code(code):
        """验证预设码格式（6位数字）"""
        if not code or len(code) != 6:
            return False
        return code.isdigit()
    
    @staticmethod
    def validate_join_year(year):
        """验证加入年（1987-2015之间）"""
        try:
            year_int = int(year)
            return 1987 <= year_int <= 2015
        except (ValueError, TypeError):
            return False