"""
浏览器管理器 - 负责创建和管理浏览器实例
"""

import logging
from threading import RLock
from typing import Optional, Dict, Any

from DrissionPage import ChromiumPage, SessionPage, ChromiumOptions


class BrowserManager:
    """
    浏览器管理器类
    
    负责创建和管理浏览器实例，支持共享浏览器和会话
    """
    
    def __init__(self, settings):
        """
        初始化浏览器管理器
        
        参数:
            settings: Scrapy设置对象
        """
        self.settings = settings
        self._browser = None
        self._session = None
        self._lock = RLock()  # 添加线程锁，确保线程安全
        self.logger = logging.getLogger(__name__)
    
    def get_browser(self) -> ChromiumPage:
        """
        获取浏览器实例
        
        如果浏览器实例不存在，则创建新的实例
        
        返回:
            ChromiumPage: 浏览器实例
        """
        with self._lock:  # 使用线程锁保护共享资源
            if self._browser is None:
                self.logger.info("创建新的浏览器实例")
                
                # 获取浏览器初始化模式
                init_mode = self.settings.get('DRISSIONPAGE_INIT_MODE', 'new')
                
                if init_mode == 'new':
                    # 使用ChromiumOptions配置浏览器
                    options = ChromiumOptions()
                    
                    # 配置浏览器路径
                    browser_path = self.settings.get('DRISSIONPAGE_BROWSER_PATH')
                    if browser_path:
                        options.set_browser_path(browser_path)
                    
                    # 配置无头模式
                    if self.settings.get('DRISSIONPAGE_HEADLESS', True):
                        options.headless = True
                    
                    # 配置Chrome启动参数
                    chrome_args = self.settings.get('DRISSIONPAGE_CHROME_OPTIONS', [])
                    for arg in chrome_args:
                        options.set_argument(arg)
                    
                    # 配置隐身模式
                    if self.settings.get('DRISSIONPAGE_INCOGNITO', False):
                        options.incognito = True
                    
                    # 配置下载路径
                    download_path = self.settings.get('DRISSIONPAGE_DOWNLOAD_PATH')
                    if download_path:
                        options.set_download_path(download_path)
                    
                    # 配置加载模式
                    load_mode = self.settings.get('DRISSIONPAGE_LOAD_MODE', 'normal')
                    if load_mode in ('normal', 'eager', 'none'):
                        options.set_load_mode(load_mode)
                    
                    # 配置超时时间
                    timeout = self.settings.get('DRISSIONPAGE_TIMEOUT')
                    if timeout:
                        options.timeouts = {
                            'page_load': timeout,
                            'script': timeout,
                            'implicit': timeout
                        }
                    
                    # 配置重试
                    retry_times = self.settings.get('DRISSIONPAGE_RETRY_TIMES')
                    retry_interval = self.settings.get('DRISSIONPAGE_RETRY_INTERVAL')
                    if retry_times and retry_interval:
                        options.set_retry(retry_times, retry_interval)
                    
                    # 配置代理
                    proxy = self.settings.get('DRISSIONPAGE_PROXY')
                    if proxy:
                        options.set_proxy(proxy)
                    
                    # 创建浏览器实例
                    try:
                        self.logger.info(f"创建ChromiumPage，使用配置: {options}")
                        self._browser = ChromiumPage(options)
                            
                    except Exception as e:
                        self.logger.error(f"创建浏览器实例失败: {e}")
                        raise
                        
                elif init_mode == 'connect':
                    # 连接到已有的浏览器实例
                    host = self.settings.get('DRISSIONPAGE_CONNECT_HOST', '127.0.0.1')
                    port = self.settings.get('DRISSIONPAGE_CONNECT_PORT', 9222)
                    
                    try:
                        # 支持直接传入端口号
                        if isinstance(port, int):
                            self._browser = ChromiumPage(port)
                        else:
                            self._browser = ChromiumPage(f'{host}:{port}')
                    except Exception as e:
                        self.logger.error(f"连接到浏览器实例失败: {e}")
                        raise
                else:
                    raise ValueError(f"不支持的浏览器初始化模式: {init_mode}")
            
            return self._browser
    
    def get_session(self) -> SessionPage:
        """
        获取会话实例
        
        如果会话实例不存在，则创建新的实例
        
        返回:
            SessionPage: 会话实例
        """
        with self._lock:  # 使用线程锁保护共享资源
            if self._session is None:
                self.logger.info("创建新的会话实例")
                
                # 创建会话选项
                session_options = {}
                
                # 获取会话选项
                user_agent = self.settings.get('DRISSIONPAGE_USER_AGENT')
                if user_agent:
                    session_options['user_agent'] = user_agent
                    
                # 获取超时设置
                timeout = self.settings.get('DRISSIONPAGE_TIMEOUT')
                if timeout:
                    session_options['timeout'] = timeout
                    
                # 获取重试次数
                retry_times = self.settings.get('DRISSIONPAGE_RETRY_TIMES')
                if retry_times:
                    session_options['retry'] = retry_times
                    
                # 获取重试间隔
                retry_interval = self.settings.get('DRISSIONPAGE_RETRY_INTERVAL')
                if retry_interval:
                    session_options['retry_interval'] = retry_interval
                
                # 创建会话实例
                try:
                    self._session = SessionPage(**session_options)
                    
                    # 设置代理
                    proxy = self.settings.get('DRISSIONPAGE_PROXY')
                    if proxy:
                        self._session.set.proxy = proxy
                        
                except Exception as e:
                    self.logger.error(f"创建会话实例失败: {e}")
                    raise
            
            return self._session
    
    def set_proxy(self, proxy: Optional[str]) -> None:
        """
        设置代理
        
        参数:
            proxy: 代理地址，如 'http://user:pass@host:port'，None表示清除代理
        """
        with self._lock:
            # 设置浏览器代理
            if self._browser is not None:
                try:
                    self._browser.set.proxy = proxy
                    self.logger.info(f"浏览器代理已设置为: {proxy}")
                except Exception as e:
                    self.logger.error(f"设置浏览器代理失败: {e}")
            
            # 设置会话代理
            if self._session is not None:
                try:
                    self._session.set.proxy = proxy
                    self.logger.info(f"会话代理已设置为: {proxy}")
                except Exception as e:
                    self.logger.error(f"设置会话代理失败: {e}")
    
    def close(self) -> None:
        """
        关闭浏览器和会话实例
        """
        with self._lock:
            # 关闭浏览器
            if self._browser is not None:
                if self.settings.get('DRISSIONPAGE_QUIT_ON_CLOSE', True):
                    try:
                        self.logger.info("关闭浏览器实例")
                        # 支持force参数强制关闭
                        force = self.settings.get('DRISSIONPAGE_FORCE_CLOSE', False)
                        self._browser.quit(force=force)
                    except Exception as e:
                        self.logger.error(f"关闭浏览器实例失败: {e}")
                self._browser = None
            
            # 关闭会话
            if self._session is not None:
                if self.settings.get('DRISSIONPAGE_QUIT_SESSION_ON_CLOSE', True):
                    try:
                        self.logger.info("关闭会话实例")
                        self._session.close()
                    except Exception as e:
                        self.logger.error(f"关闭会话实例失败: {e}")
                self._session = None
    
    def __del__(self):
        """
        析构函数，确保资源被正确释放
        """
        self.close() 