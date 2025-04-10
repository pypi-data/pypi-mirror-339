from flask import current_app, url_for
from werkzeug.utils import cached_property
from PIL import Image
import os
import io
import base64
import mimetypes
from urllib.parse import quote

class ImageCompressor:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('IMAGE_COMPRESSION_QUALITY', 85)
        app.config.setdefault('IMAGE_COMPRESSION_CACHE_DIR', 'compressed_images')
        app.config.setdefault('IMAGE_MAX_WIDTH', 1920)  # Default max width
        app.config.setdefault('IMAGE_MAX_HEIGHT', 1080)  # Default max height
        app.config.setdefault('IMAGE_WEBP_ENABLED', True)  # Enable WebP by default
        app.config.setdefault('IMAGE_PROGRESSIVE', True)  # Enable progressive JPEG by default
        app.config.setdefault('IMAGE_PNG_OPTIMIZE', True)  # Enable PNG optimization
        app.config.setdefault('IMAGE_PNG_COMPRESSION_LEVEL', 6)  # PNG compression level (0-9)
        app.jinja_env.globals.update({
            'compressed_image': self.compressed_image,
            'responsive_image': self.responsive_image,
            'webp_image': self.webp_image
        })
        
        # Create cache directory if it doesn't exist
        self._ensure_cache_dir(app)

    def _ensure_cache_dir(self, app):
        """Ensure the cache directory exists."""
        cache_dir = os.path.join(app.static_folder, app.config['IMAGE_COMPRESSION_CACHE_DIR'])
        os.makedirs(cache_dir, exist_ok=True)

    def _get_image_format(self, img):
        """Determine the best format for the image."""
        if img.format == 'PNG':
            return 'PNG'
        elif img.format in ('JPEG', 'JPG'):
            return 'JPEG'
        return img.format

    def _resize_image(self, img, max_width=None, max_height=None):
        """Resize image while maintaining aspect ratio."""
        if max_width is None:
            max_width = current_app.config['IMAGE_MAX_WIDTH']
        if max_height is None:
            max_height = current_app.config['IMAGE_MAX_HEIGHT']
            
        width, height = img.size
        if width > max_width or height > max_height:
            ratio = min(max_width/width, max_height/height)
            new_size = (int(width * ratio), int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        return img

    def _compress_image(self, image_path, quality=None, max_width=None, max_height=None, format=None):
        """Compress and optionally resize image using Pillow."""
        with Image.open(image_path) as img:
            # Determine format if not specified
            if format is None:
                format = self._get_image_format(img)
            
            # Convert to appropriate mode based on format
            if format == 'JPEG':
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    # Create white background for transparent images
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
            elif format == 'PNG' and img.mode not in ('RGBA', 'LA', 'P'):
                img = img.convert('RGBA')
            
            # Resize if needed
            img = self._resize_image(img, max_width, max_height)
            
            # Create in-memory buffer
            output = io.BytesIO()
            
            # Prepare save options based on format
            save_kwargs = {'optimize': True}
            
            if format == 'JPEG':
                save_kwargs.update({
                    'quality': quality or current_app.config['IMAGE_COMPRESSION_QUALITY'],
                    'progressive': current_app.config['IMAGE_PROGRESSIVE']
                })
            elif format == 'PNG':
                save_kwargs.update({
                    'optimize': current_app.config['IMAGE_PNG_OPTIMIZE'],
                    'compress_level': current_app.config['IMAGE_PNG_COMPRESSION_LEVEL']
                })
            
            img.save(output, format=format, **save_kwargs)
            return output.getvalue(), format

    def compressed_image(self, filename, quality=None, max_width=None, max_height=None, lazy=True):
        """Generate HTML for a compressed image with optional resizing.
        
        Args:
            filename (str): Path to the image file relative to static folder
            quality (int, optional): Compression quality (0-100)
            max_width (int, optional): Maximum width in pixels
            max_height (int, optional): Maximum height in pixels
            lazy (bool): Whether to add loading="lazy" attribute
        
        Returns:
            str: HTML img tag with optimized image
        """
        if quality is None:
            quality = current_app.config['IMAGE_COMPRESSION_QUALITY']
        
        # Ensure quality is within valid range
        quality = max(0, min(100, quality))
        
        # Get the full path to the original image
        static_folder = current_app.static_folder
        original_path = os.path.join(static_folder, filename)
        
        if not os.path.exists(original_path):
            return f'<img src="{url_for("static", filename=filename)}" alt="Image">'
        
        # Create cache directory path
        cache_dir = os.path.join(static_folder, current_app.config['IMAGE_COMPRESSION_CACHE_DIR'])
        
        # Get original image format
        with Image.open(original_path) as img:
            original_format = self._get_image_format(img)
        
        # Create a unique filename for the compressed version
        base, ext = os.path.splitext(filename)
        size_suffix = f"_{max_width}x{max_height}" if max_width or max_height else ""
        compressed_filename = f"{base}_compressed_{quality}{size_suffix}{ext}"
        cache_path = os.path.join(cache_dir, compressed_filename)
        
        # Check if compressed version exists in cache
        if not os.path.exists(cache_path):
            try:
                # Compress the image
                compressed_data, format = self._compress_image(
                    original_path, quality, max_width, max_height, original_format
                )
                
                # Save compressed version
                os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                with open(cache_path, 'wb') as f:
                    f.write(compressed_data)
            except Exception as e:
                current_app.logger.error(f"Error compressing image {filename}: {str(e)}")
                return f'<img src="{url_for("static", filename=filename)}" alt="Image">'
        
        # Generate WebP version if enabled and original is JPEG
        webp_src = ""
        if current_app.config['IMAGE_WEBP_ENABLED'] and original_format == 'JPEG':
            webp_filename = f"{base}_compressed_{quality}{size_suffix}.webp"
            webp_path = os.path.join(cache_dir, webp_filename)
            
            if not os.path.exists(webp_path):
                try:
                    webp_data, _ = self._compress_image(
                        original_path, quality, max_width, max_height, 'WEBP'
                    )
                    with open(webp_path, 'wb') as f:
                        f.write(webp_data)
                except Exception as e:
                    current_app.logger.error(f"Error creating WebP version of {filename}: {str(e)}")
            
            webp_src = f'<source srcset="{url_for("static", filename=os.path.join(current_app.config["IMAGE_COMPRESSION_CACHE_DIR"], webp_filename))}" type="image/webp">'
        
        # Generate HTML with WebP support and lazy loading
        img_src = url_for('static', filename=os.path.join(current_app.config['IMAGE_COMPRESSION_CACHE_DIR'], compressed_filename))
        loading = 'loading="lazy"' if lazy else ''
        
        return f'<picture>{webp_src}<img src="{img_src}" {loading} alt="Image"></picture>'

    def responsive_image(self, filename, sizes=None, quality=None, lazy=True):
        """Generate a responsive image with srcset.
        
        Args:
            filename (str): Path to the image file relative to static folder
            sizes (list): List of (width, quality) tuples for different sizes
            quality (int): Default quality for sizes not specified
            lazy (bool): Whether to add loading="lazy" attribute
        """
        if sizes is None:
            sizes = [(800, 85), (1200, 75), (1600, 65)]
        
        srcset = []
        for width, q in sizes:
            img_tag = self.compressed_image(filename, quality=q, max_width=width, lazy=False)
            # Extract the src from the img tag
            src = img_tag.split('src="')[1].split('"')[0]
            srcset.append(f"{src} {width}w")
        
        sizes_attr = 'sizes="(max-width: 800px) 100vw, (max-width: 1200px) 50vw, 33vw"'
        loading = 'loading="lazy"' if lazy else ''
        
        return f'<img srcset="{", ".join(srcset)}" {sizes_attr} {loading} alt="Responsive Image">'

    def webp_image(self, filename, quality=None, max_width=None, max_height=None, lazy=True):
        """Generate a WebP image with JPEG fallback.
        
        Args:
            filename (str): Path to the image file relative to static folder
            quality (int, optional): Compression quality (0-100)
            max_width (int, optional): Maximum width in pixels
            max_height (int, optional): Maximum height in pixels
            lazy (bool): Whether to add loading="lazy" attribute
        """
        return self.compressed_image(filename, quality, max_width, max_height, lazy) 