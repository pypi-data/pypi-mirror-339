import os
from configparser import ConfigParser
from typing import Dict, Any, Callable, List
from functools import wraps


class ConfigTool:
    _instance = None
    _config_file = os.path.join(os.path.expanduser("~"), "pyconfig", "config.ini")
    _listeners: Dict[str, List[Callable]] = {}
    _loaded = False

    def __new__(cls, config_file: str = None):
        if cls._instance is None:
            cls._instance = super(ConfigTool, cls).__new__(cls)
            cls._instance.config = ConfigParser()
            if config_file:
                cls._instance._config_file = config_file
            cls._instance._ensure_config_file()
        return cls._instance

    def _ensure_config_file(self):
        """确保配置文件存在，如果不存在则创建"""
        config_dir = os.path.dirname(self._config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
        if not os.path.exists(self._config_file):
            with open(self._config_file, "w", encoding="utf-8") as f:
                self.config.write(f)

    def load_config(self) -> bool:
        """加载配置文件"""
        if self._loaded:
            return True

        try:
            self.config.read(self._config_file, encoding="utf-8")
            self._loaded = True
            return True
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
            return False

    @staticmethod
    def get_section(section: str) -> Dict[str, str]:
        """获取指定section的所有配置项"""
        config = ConfigTool.get_instance()
        if not config.config.has_section(section):
            return {}
        return dict(config.config[section])

    @staticmethod
    def get_value(section: str, key: str, default: Any = None) -> Any:
        """获取指定section和key的配置值，支持自动类型转换"""
        config = ConfigTool.get_instance()
        if not config.config.has_section(section):
            return default

        value = config.config.get(section, key, fallback=default)
        if value is None:
            return default

        # 尝试自动类型转换
        try:
            if isinstance(default, bool):
                return config.config.getboolean(section, key, fallback=default)
            elif isinstance(default, int):
                return config.config.getint(section, key, fallback=default)
            elif isinstance(default, float):
                return config.config.getfloat(section, key, fallback=default)
        except ValueError:
            pass

        return value

    @staticmethod
    def set_value(section: str, key: str, value: Any) -> bool:
        """设置配置值"""
        try:
            config = ConfigTool.get_instance()
            if not config.config.has_section(section):
                config.config.add_section(section)
            config.config.set(section, key, str(value))
            config._notify_listeners(section, key, value)
            return True
        except Exception as e:
            print(f"设置配置值失败: {str(e)}")
            return False

    @staticmethod
    def set_values(section: str, values: Dict[str, Any]) -> bool:
        """批量设置配置值"""
        try:
            config = ConfigTool.get_instance()
            if not config.config.has_section(section):
                config.config.add_section(section)
            for key, value in values.items():
                config.config.set(section, key, str(value))
                config._notify_listeners(section, key, value)
            return True
        except Exception as e:
            print(f"批量设置配置值失败: {str(e)}")
            return False

    @staticmethod
    def save_config() -> bool:
        """保存配置到文件"""
        try:
            config = ConfigTool.get_instance()
            with open(config._config_file, "w", encoding="utf-8") as f:
                config.config.write(f)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
            return False

    @staticmethod
    def add_listener(section: str, key: str, callback: Callable[[str, str, Any], None]):
        """添加配置变更监听器"""
        config = ConfigTool.get_instance()
        key = f"{section}.{key}"
        if key not in config._listeners:
            config._listeners[key] = []
        config._listeners[key].append(callback)

    @staticmethod
    def remove_listener(
        section: str, key: str, callback: Callable[[str, str, Any], None]
    ):
        """移除配置变更监听器"""
        config = ConfigTool.get_instance()
        key = f"{section}.{key}"
        if key in config._listeners and callback in config._listeners[key]:
            config._listeners[key].remove(callback)

    def _notify_listeners(self, section: str, key: str, value: Any):
        """通知监听器配置变更"""
        key = f"{section}.{key}"
        if key in self._listeners:
            for callback in self._listeners[key]:
                try:
                    callback(section, key, value)
                except Exception as e:
                    print(f"执行监听器回调失败: {str(e)}")

    @classmethod
    def get_instance(cls, config_file: str = None) -> "ConfigTool":
        """获取配置工具实例"""
        if cls._instance is None:
            cls._instance = cls(config_file)
        elif config_file and cls._instance._config_file != config_file:
            # 如果提供了新的配置文件路径且与当前不同，则重新创建实例
            cls._instance = cls(config_file)
        return cls._instance

    @staticmethod
    def with_config(config_file: str = None):
        """配置加载装饰器

        Args:
            config_file: 配置文件路径，如果为None则使用默认路径
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 确保配置已加载
                ConfigTool.get_instance(config_file).load_config()
                return func(*args, **kwargs)

            return wrapper

        return decorator
