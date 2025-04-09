"""
Scrapy-DrissionPage - 将Scrapy爬虫框架与DrissionPage网页自动化工具进行无缝集成
"""

__version__ = '1.0.3'

# 导出主要类
from DrissionPage import ChromiumPage, SessionPage
# 尝试导入新版本中的选项类
try:
    from DrissionPage import ChromiumOptions, SessionOptions
except ImportError:
    # 在新版本中，可能Options类已经被移除或重命名
    ChromiumOptions = None
    SessionOptions = None
    
from .spider import DrissionSpider
from .request import DrissionRequest
from .response import DrissionResponse
from .middleware import DrissionPageMiddleware
from .browser_manager import BrowserManager

# 导出工具类
from .utils import ModeSwitcher, EnhancedSelector

# 便捷导入
Chromium = ChromiumPage
Session = SessionPage

# 所有导出的类
__all__ = [
    'DrissionSpider',
    'DrissionRequest',
    'DrissionResponse',
    'DrissionPageMiddleware',
    'BrowserManager',
    'ChromiumPage',
    'SessionPage',
    'ChromiumOptions',
    'SessionOptions',
    'ModeSwitcher',
    'EnhancedSelector',
    'Chromium',
    'Session'
] 