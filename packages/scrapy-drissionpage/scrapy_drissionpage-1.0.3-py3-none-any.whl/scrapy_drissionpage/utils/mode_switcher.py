"""
模式切换工具 - 提供在DrissionPage的d模式和s模式之间切换的工具
"""

from typing import Union, Optional
import logging
from DrissionPage import ChromiumPage, SessionPage


class ModeSwitcher:
    """
    模式切换工具类
    
    提供在DrissionPage的d模式和s模式之间切换的工具方法
    """
    
    logger = logging.getLogger(__name__)
    
    @staticmethod
    def to_session(page: ChromiumPage) -> SessionPage:
        """
        将ChromiumPage转换为SessionPage
        
        参数:
            page: ChromiumPage实例
            
        返回:
            SessionPage: 转换后的SessionPage实例
        """
        if not isinstance(page, ChromiumPage):
            ModeSwitcher.logger.error("输入参数必须是ChromiumPage实例")
            raise TypeError("输入参数必须是ChromiumPage实例")
        
        try:
            # 直接从浏览器获取session对象
            if hasattr(page, 'session'):
                session = page.session
                ModeSwitcher.logger.info(f"已获取 {page.url} 关联的session对象")
                return session
            
            # 创建新的SessionPage，继承cookies
            cookies = page.cookies
            session = SessionPage()
            
            # 设置cookies
            for cookie in cookies:
                # 在新版本中，cookies设置方式可能不同
                if 'name' in cookie and 'value' in cookie:
                    session.set.cookies = {cookie['name']: cookie['value']}
                else:
                    session.set.cookies = cookie
            
            # 访问相同的URL
            current_url = page.url
            session.get(current_url)
            
            ModeSwitcher.logger.info(f"已手动将 {current_url} 数据转移到SessionPage")
            return session
            
        except Exception as e:
            ModeSwitcher.logger.error(f"模式切换失败: {e}")
            raise
    
    @staticmethod
    def to_chromium(page: SessionPage, browser: Optional[ChromiumPage] = None) -> ChromiumPage:
        """
        将SessionPage转换为ChromiumPage
        
        参数:
            page: SessionPage实例
            browser: 可选的ChromiumPage实例，用于创建新标签页
            
        返回:
            ChromiumPage: 转换后的ChromiumPage实例
        """
        if not isinstance(page, SessionPage):
            ModeSwitcher.logger.error("输入参数必须是SessionPage实例")
            raise TypeError("输入参数必须是SessionPage实例")
        
        try:
            # 创建新的浏览器标签页
            if browser is None:
                browser = ChromiumPage()
                new_tab = browser.latest_tab
            else:
                new_tab = browser.new_tab()
            
            # 获取cookies
            cookies = page.cookies
            
            # 设置cookies
            for cookie in cookies:
                # 处理不同格式的cookie
                if isinstance(cookie, dict):
                    if 'name' in cookie and 'value' in cookie:
                        new_tab.set.cookies = {cookie['name']: cookie['value']}
                    else:
                        new_tab.set.cookies = cookie
                else:
                    new_tab.set.cookies = cookie
            
            # 访问相同的URL
            current_url = page.url
            new_tab.get(current_url)
            
            ModeSwitcher.logger.info(f"已手动将 {current_url} 从SessionPage转移到ChromiumPage")
            return new_tab
            
        except Exception as e:
            ModeSwitcher.logger.error(f"模式切换失败: {e}")
            raise 