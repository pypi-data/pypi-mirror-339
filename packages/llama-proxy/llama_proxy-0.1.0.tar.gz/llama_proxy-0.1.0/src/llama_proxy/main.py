# Project Structure
'''
llama_proxy/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── proxy_manager.py
│   ├── health_scorer.py
│   ├── proxy_rotator.py
│   ├── rate_limiter.py
│   ├── captcha_solver.py
│   ├── traffic_shaper.py
│   └── request_executor.py
├── orchestration/
│   ├── __init__.py
│   └── proxy_orchestrator.py
├── simulation/
│   ├── __init__.py
│   ├── request_mutator.py
│   ├── geolocation_spoofer.py
│   └── tls_fingerprint_rotator.py
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── exceptions.py
│   └── logging.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_proxy_manager.py
│   ├── test_health_scorer.py
│   ├── test_proxy_rotator.py
│   ├── test_rate_limiter.py
│   ├── test_captcha_solver.py
│   ├── test_traffic_shaper.py
│   ├── test_request_executor.py
│   ├── test_proxy_orchestrator.py
│   ├── test_request_mutator.py
│   ├── test_geolocation_spoofer.py
│   └── test_tls_fingerprint_rotator.py
├── examples/
│   ├── __init__.py
│   ├── basic_usage.py
│   └── advanced_usage.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
'''

# llama_proxy/__init__.py
```python
"""
llama_proxy - A comprehensive proxy orchestration system.

This package provides a complete solution for proxy management, rotation,
health monitoring, and automated request handling with intelligent
proxy selection, rate limiting, traffic shaping, and CAPTCHA solving.
"""

__version__ = "0.1.0"

from llama_proxy.core.captcha_solver import CaptchaSolverClient
from llama_proxy.core.health_scorer import HealthScorer
from llama_proxy.core.proxy_manager import ProxyManager
from llama_proxy.core.proxy_rotator import ProxyRotator
from llama_proxy.core.rate_limiter import DistributedRateLimiter
from llama_proxy.core.request_executor import RequestExecutor
from llama_proxy.core.traffic_shaper import TrafficShaper
from llama_proxy.orchestration.proxy_orchestrator import ProxyOrchestrator
from llama_proxy.simulation.geolocation_spoofer import GeolocationSpoofer
from llama_proxy.simulation.request_mutator import RequestMutator
from llama_proxy.simulation.tls_fingerprint_rotator import \
    TLSFingerprintRotator
from llama_proxy.utils.config import Config
from llama_proxy.utils.exceptions import (CaptchaError, ConfigurationError,
                                          HealthCheckError, ProxyError,
                                          RateLimitError,
                                          RequestExecutionError)

__all__ = [
    "ProxyOrchestrator",
    "ProxyManager",
    "HealthScorer",
    "ProxyRotator",
    "DistributedRateLimiter",
    "CaptchaSolverClient",
    "TrafficShaper",
    "RequestExecutor",
    "RequestMutator",
    "GeolocationSpoofer",
    "TLSFingerprintRotator",
    "Config",
    "ProxyError",
    "HealthCheckError",
    "RateLimitError",
    "CaptchaError",
    "RequestExecutionError",
    "ConfigurationError",
]
```

# llama_proxy/utils/config.py
```python
"""Configuration management for llama_proxy."""

import json
import logging
import os
from typing import Any, Dict, List, Optional, Union

import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config:
    """
    Configuration manager for llama_proxy.
    
    This class handles loading configuration from environment variables,
    config files, and provides a unified interface for accessing configuration
    values throughout the application.
    
    Attributes:
        config (Dict[str, Any]): The loaded configuration values.
    """
    
    def __init__(
        self, 
        config_path: Optional[str] = None,
        env_prefix: str = "LLAMA_PROXY_",
        load_env: bool = True,
        required_vars: Optional[List[str]] = None
    ) -> None:
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Optional path to a JSON or YAML configuration file.
            env_prefix: Prefix for environment variables to load.
            load_env: Whether to load environment variables from .env file.
            required_vars: List of required configuration variables.
        
        Raises:
            ConfigurationError: If a required configuration variable is missing.
        """
        self.config: Dict[str, Any] = {}
        
        # Load environment variables from .env file if it exists
        if load_env:
            load_dotenv()
        
        # Load from config file if provided
        if config_path and os.path.exists(config_path):
            self._load_from_file(config_path)
        
        # Load from environment variables
        self._load_from_env(env_prefix)
        
        # Check for required variables
        if required_vars:
            self._validate_required(required_vars)
    
    def _load_from_file(self, config_path: str) -> None:
        """
        Load configuration from a file.
        
        Args:
            config_path: Path to the configuration file (JSON or YAML).
            
        Raises:
            ConfigurationError: If the file format is unsupported or can't be parsed.
        """
        try:
            _, ext = os.path.splitext(config_path)
            with open(config_path, "r") as f:
                if ext.lower() == ".json":
                    self.config.update(json.load(f))
                elif ext.lower() in [".yaml", ".yml"]:
                    self.config.update(yaml.safe_load(f))
                else:
                    logger.warning(f"Unsupported config file format: {ext}")
        except Exception as e:
            logger.error(f"Failed to load config from {config_path}: {e}")
            
    def _load_from_env(self, prefix: str) -> None:
        """
        Load configuration from environment variables.
        
        Args:
            prefix: Prefix for environment variables to load.
        """
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                try:
                    # Try to parse as JSON for complex types
                    self.config[config_key] = json.loads(value)
                except json.JSONDecodeError:
                    # Use as string if not valid JSON
                    self.config[config_key] = value
    
    def _validate_required(self, required_vars: List[str]) -> None:
        """
        Validate that all required configuration variables are present.
        
        Args:
            required_vars: List of required configuration variables.
            
        Raises:
            ConfigurationError: If a required configuration variable is missing.
        """
        from llama_proxy.utils.exceptions import ConfigurationError
        
        missing = [var for var in required_vars if var.lower() not in self.config]
        if missing:
            missing_vars = ", ".join(missing)
            raise ConfigurationError(f"Missing required configuration variables: {missing_vars}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: The configuration key.
            default: The default value to return if the key doesn't exist.
            
        Returns:
            The configuration value, or the default if the key doesn't exist.
        """
        return self.config.get(key.lower(), default)
    
    def __getitem__(self, key: str) -> Any:
        """
        Get a configuration value using dictionary access syntax.
        
        Args:
            key: The configuration key.
            
        Returns:
            The configuration value.
            
        Raises:
            KeyError: If the key doesn't exist.
        """
        return self.config[key.lower()]
    
    def __contains__(self, key: str) -> bool:
        """
        Check if a configuration key exists.
        
        Args:
            key: The configuration key.
            
        Returns:
            True if the key exists, False otherwise.
        """
        return key.lower() in self.config
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: The configuration key.
            value: The configuration value.
        """
        self.config[key.lower()] = value
    
    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a configuration value using dictionary access syntax.
        
        Args:
            key: The configuration key.
            value: The configuration value.
        """
        self.config[key.lower()] = value
    
    def as_dict(self) -> Dict[str, Any]:
        """
        Get the configuration as a dictionary.
        
        Returns:
            The configuration dictionary.
        """
        return self.config.copy()
```

# llama_proxy/utils/exceptions.py
```python
"""Custom exceptions for llama_proxy."""

from typing import Any, Dict, List, Optional


class LlamaProxyError(Exception):
    """Base exception for all llama_proxy errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize a LlamaProxyError.
        
        Args:
            message: Error message.
            details: Additional error details.
        """
        self.message = message
        self.details = details or {}
        super().__init__(message)


class ConfigurationError(LlamaProxyError):
    """Raised when there is a configuration error."""
    pass


class ProxyError(LlamaProxyError):
    """Raised when there is an error with a proxy."""
    
    def __init__(
        self, 
        message: str, 
        proxy_url: Optional[str] = None,
        response_code: Optional[int] = None,
        attempts: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a ProxyError.
        
        Args:
            message: Error message.
            proxy_url: The proxy URL that caused the error.
            response_code: HTTP response code if applicable.
            attempts: Number of attempts made if applicable.
            details: Additional error details.
        """
        self.proxy_url = proxy_url
        self.response_code = response_code
        self.attempts = attempts
        super().__init__(message, details)


class HealthCheckError(ProxyError):
    """Raised when a proxy health check fails."""
    
    def __init__(
        self, 
        message: str, 
        proxy_url: Optional[str] = None,
        health_score: Optional[float] = None,
        check_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a HealthCheckError.
        
        Args:
            message: Error message.
            proxy_url: The proxy URL that failed the health check.
            health_score: The health score of the proxy.
            check_type: The type of health check that failed.
            details: Additional error details.
        """
        self.health_score = health_score
        self.check_type = check_type
        details = details or {}
        details.update({
            "health_score": health_score,
            "check_type": check_type
        })
        super().__init__(message, proxy_url=proxy_url, details=details)


class RateLimitError(LlamaProxyError):
    """Raised when a rate limit is exceeded."""
    
    def __init__(
        self, 
        message: str, 
        host: Optional[str] = None,
        limit: Optional[int] = None,
        reset_time: Optional[float] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a RateLimitError.
        
        Args:
            message: Error message.
            host: The host that imposed the rate limit.
            limit: The rate limit value.
            reset_time: The time when the rate limit resets.
            details: Additional error details.
        """
        self.host = host
        self.limit = limit
        self.reset_time = reset_time
        details = details or {}
        details.update({
            "host": host,
            "limit": limit,
            "reset_time": reset_time
        })
        super().__init__(message, details)


class CaptchaError(LlamaProxyError):
    """Raised when there is an error with CAPTCHA solving."""
    
    def __init__(
        self, 
        message: str, 
        captcha_type: Optional[str] = None,
        provider: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a CaptchaError.
        
        Args:
            message: Error message.
            captcha_type: The type of CAPTCHA.
            provider: The CAPTCHA solving service provider.
            details: Additional error details.
        """
        self.captcha_type = captcha_type
        self.provider = provider
        details = details or {}
        details.update({
            "captcha_type": captcha_type,
            "provider": provider
        })
        super().__init__(message, details)


class RequestExecutionError(LlamaProxyError):
    """Raised when there is an error executing a request."""
    
    def __init__(
        self, 
        message: str, 
        url: Optional[str] = None,
        method: Optional[str] = None,
        status_code: Optional[int] = None,
        attempts: Optional[int] = None,
        proxies_tried: Optional[List[str]] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a RequestExecutionError.
        
        Args:
            message: Error message.
            url: The URL that was requested.
            method: The HTTP method that was used.
            status_code: The HTTP status code that was returned.
            attempts: The number of attempts that were made.
            proxies_tried: The list of proxies that were tried.
            details: Additional error details.
        """
        self.url = url
        self.method = method
        self.status_code = status_code
        self.attempts = attempts
        self.proxies_tried = proxies_tried or []
        details = details or {}
        details.update({
            "url": url,
            "method": method,
            "status_code": status_code,
            "attempts": attempts,
            "proxies_tried": proxies_tried
        })
        super().__init__(message, details)


class SimulationError(LlamaProxyError):
    """Raised when there is an error with request simulation."""
    
    def __init__(
        self, 
        message: str, 
        simulation_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a SimulationError.
        
        Args:
            message: Error message.
            simulation_type: The type of simulation that failed.
            details: Additional error details.
        """
        self.simulation_type = simulation_type
        details = details or {}
        details.update({
            "simulation_type": simulation_type
        })
        super().__init__(message, details)
```

# llama_proxy/utils/logging.py
```python
"""Logging utilities for llama_proxy."""

import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional, Union

# Define log levels with type safety
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


class JsonFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    
    This formatter converts log records to JSON format for easier parsing
    by log aggregation tools.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record as JSON.
        
        Args:
            record: The log record to format.
            
        Returns:
            The formatted log record as a JSON string.
        """
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }
        
        # Add extra fields from record
        for key, value in record.__dict__.items():
            if key not in [
                "args", "asctime", "created", "exc_info", "exc_text", "filename",
                "funcName", "id", "levelname", "levelno", "lineno", "module",
                "msecs", "message", "msg", "name", "pathname", "process",
                "processName", "relativeCreated", "stack_info", "thread", "threadName"
            ]:
                log_data[key] = value
        
        return json.dumps(log_data)


def configure_logging(
    level: Union[str, int] = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = False,
    log_to_console: bool = True
) -> None:
    """
    Configure logging for llama_proxy.
    
    Args:
        level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Optional path to a log file.
        json_format: Whether to use JSON formatting for logs.
        log_to_console: Whether to log to the console.
    """
    # Convert string level to int if needed
    if isinstance(level, str):
        level = LOG_LEVELS.get(level.upper(), logging.INFO)
    
    # Create the root logger
    logger = logging.getLogger("llama_proxy")
    logger.setLevel(level)
    logger.handlers = []  # Remove any existing handlers
    
    # Create formatter
    if json_format:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    # Add console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Add file handler if log file specified
    if log_file:
        os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: The name of the logger.
        
    Returns:
        A logger instance.
    """
    return logging.getLogger(f"llama_proxy.{name}")
```

# llama_proxy/core/proxy_manager.py
```python
"""Proxy management for llama_proxy."""

import json
import logging
import os
import random
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

import requests
from llama_proxy.utils.config import Config
from llama_proxy.utils.exceptions import ConfigurationError, ProxyError


@dataclass
class Proxy:
    """
    Data class representing a proxy with its configuration and metadata.
    
    Attributes:
        url (str): The proxy URL in format scheme://[user:pass@]host:port
        protocol (str): The proxy protocol (http, https, socks4, socks5)
        host (str): The proxy host
        port (int): The proxy port
        username (Optional[str]): The proxy username if authentication is required
        password (Optional[str]): The proxy password if authentication is required
        country_code (Optional[str]): The country code where the proxy is located
        city (Optional[str]): The city where the proxy is located
        asn (Optional[str]): The ASN of the proxy
        provider (Optional[str]): The proxy provider
        last_used (Optional[float]): Timestamp when the proxy was last used
        last_checked (Optional[float]): Timestamp when the proxy was last health checked
        active (bool): Whether the proxy is currently active
        health_score (float): The health score of the proxy (0.0 to 1.0)
        tags (Set[str]): Set of tags associated with the proxy
        metadata (Dict[str, Any]): Additional metadata for the proxy
    """
    
    url: str
    protocol: str
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    country_code: Optional[str] = None
    city: Optional[str] = None
    asn: Optional[str] = None
    provider: Optional[str] = None
    last_used: Optional[float] = None
    last_checked: Optional[float] = None
    active: bool = True
    health_score: float = 1.0
    tags: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_url(cls, url: str, **kwargs: Any) -> 'Proxy':
        """
        Create a Proxy instance from a URL.
        
        Args:
            url: The proxy URL in format scheme://[user:pass@]host:port
            **kwargs: Additional attributes for the Proxy
            
        Returns:
            A new Proxy instance
            
        Raises:
            ValueError: If the URL format is invalid
        """
        # Parse the URL
        match = re.match(
            r"^(https?|socks[45])://((?:[\w\-]+:[\w\-]+@)?[\w\-\.]+):(\d+)$",
            url
        )
        if not match:
            raise ValueError(
                f"Invalid proxy URL format: {url}. "
                f"Expected format: scheme://[user:pass@]host:port"
            )
        
        protocol, host_part, port_str = match.groups()
        
        # Parse authentication if present
        username = None
        password = None
        if '@' in host_part:
            auth_part, host = host_part.split('@', 1)
            if ':' in auth_part:
                username, password = auth_part.split(':', 1)
        else:
            host = host_part
        
        # Create the Proxy instance
        return cls(
            url=url,
            protocol=protocol,
            host=host,
            port=int(port_str),
            username=username,
            password=password,
            **kwargs
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Proxy to a dictionary.
        
        Returns:
            A dictionary representation of the Proxy
        """
        return {
            "url": self.url,
            "protocol": self.protocol,
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "country_code": self.country_code,
            "city": self.city,
            "asn": self.asn,
            "provider": self.provider,
            "last_used": self.last_used,
            "last_checked": self.last_checked,
            "active": self.active,
            "health_score": self.health_score,
            "tags": list(self.tags),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Proxy':
        """
        Create a Proxy instance from a dictionary.
        
        Args:
            data: A dictionary representation of a Proxy
            
        Returns:
            A new Proxy instance
        """
        # Convert tags from list to set if present
        if "tags" in data and isinstance(data["tags"], list):
            data = data.copy()
            data["tags"] = set(data["tags"])
            
        return cls(**data)
    
    def get_requests_format(self) -> Dict[str, str]:
        """
        Get the proxy in the format expected by the requests library.
        
        Returns:
            A dictionary with proxy settings for requests
        """
        protocol = self.protocol
        auth_part = ""
        
        # Add authentication if provided
        if self.username and self.password:
            auth_part = f"{self.username}:{self.password}@"
        
        # Format for socks proxies
        if protocol.startswith("socks"):
            return {
                "http": f"{protocol}://{auth_part}{self.host}:{self.port}",
                "https": f"{protocol}://{auth_part}{self.host}:{self.port}"
            }
        
        # Format for HTTP/HTTPS proxies
        return {
            protocol: f"{protocol}://{auth_part}{self.host}:{self.port}"
        }
    
    def update_health_score(self, score: float) -> None:
        """
        Update the health score of the proxy.
        
        Args:
            score: The new health score (0.0 to 1.0)
        """
        self.health_score = max(0.0, min(1.0, score))
        self.last_checked = time.time()


class ProxyManager:
    """
    Manager for loading, storing, and retrieving proxies.
    
    This class handles loading proxies from various sources, storing them
    in memory, and providing methods to retrieve proxies based on
    different criteria.
    
    Attributes:
        proxies (Dict[str, Proxy]): Dictionary of proxies indexed by URL
        config (Config): Configuration instance
        logger (logging.Logger): Logger instance
    """
    
    def __init__(self, config: Optional[Config] = None) -> None:
        """
        Initialize the ProxyManager.
        
        Args:
            config: Configuration instance
        """
        self.proxies: Dict[str, Proxy] = {}
        self.config = config or Config()
        self.logger = logging.getLogger("llama_proxy.proxy_manager")
        self._lock = threading.RLock()
        
        # Load proxies from configured sources
        self._load_initial_proxies()
    
    def _load_initial_proxies(self) -> None:
        """
        Load proxies from all configured sources.
        """
        # Load from environment variable
        self._load_from_env()
        
        # Load from file if configured
        proxy_file = self.config.get("proxy_file")
        if proxy_file and os.path.exists(proxy_file):
            self._load_from_file(proxy_file)
        
        # Load from API if configured
        proxy_api_url = self.config.get("proxy_api_url")
        proxy_api_key = self.config.get("proxy_api_key")
        if proxy_api_url:
            self._load_from_api(proxy_api_url, proxy_api_key)
        
        self.logger.info(f"Loaded {len(self.proxies)} proxies")
    
    def _load_from_env(self) -> None:
        """
        Load proxies from environment variables.
        
        Environment variables should be in the format:
        LLAMA_PROXY_PROXIES='["http://user:pass@host:port", "socks5://host:port"]'
        """
        proxies_str = self.config.get("proxies")
        if not proxies_str:
            return
        
        try:
            if isinstance(proxies_str, str):
                proxy_urls = json.loads(proxies_str)
            elif isinstance(proxies_str, list):
                proxy_urls = proxies_str
            else:
                self.logger.warning(f"Invalid proxies format: {type(proxies_str)}")
                return
                
            for url in proxy_urls:
                try:
                    proxy = Proxy.from_url(url)
                    self.add_proxy(proxy)
                except ValueError as e:
                    self.logger.warning(f"Invalid proxy URL: {url} - {e}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse proxies from environment: {e}")
    
    def _load_from_file(self, file_path: str) -> None:
        """
        Load proxies from a file.
        
        Args:
            file_path: Path to the file containing proxies
            
        The file can be:
        1. JSON list of proxy URLs: ["http://host:port", "socks5://host:port"]
        2. JSON list of proxy objects with full details
        3. Plain text file with one proxy URL per line
        """
        try:
            with open(file_path, "r") as f:
                content = f.read().strip()
                
            # Try parsing as JSON
            try:
                data = json.loads(content)
                
                # If it's a list of strings (URLs)
                if isinstance(data, list) and all(isinstance(x, str) for x in data):
                    for url in data:
                        try:
                            proxy = Proxy.from_url(url)
                            self.add_proxy(proxy)
                        except ValueError as e:
                            self.logger.warning(f"Invalid proxy URL: {url} - {e}")
                
                # If it's a list of dictionaries (full proxy objects)
                elif isinstance(data, list) and all(isinstance(x, dict) for x in data):
                    for proxy_dict in data:
                        try:
                            proxy = Proxy.from_dict(proxy_dict)
                            self.add_proxy(proxy)
                        except Exception as e:
                            self.logger.warning(f"Invalid proxy data: {proxy_dict} - {e}")
                
                else:
                    self.logger.warning(f"Unsupported format for initial_proxies in config: {config_proxies}")
        except Exception as e:
            self.logger.error(f"Failed to load proxies from file: {e}")
    
    def _load_from_api(self, api_url: str, api_key: Optional[str] = None) -> None:
        """
        Load proxies from an API.
        
        Args:
            api_url: URL of the API endpoint
            api_key: API key if required for authentication
        """
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # If it's a list of strings (URLs)
            if isinstance(data, list) and all(isinstance(x, str) for x in data):
                for url in data:
                    try:
                        proxy = Proxy.from_url(url)
                        self.add_proxy(proxy)
                    except ValueError as e:
                        self.logger.warning(f"Invalid proxy URL: {url} - {e}")
            
            # If it's a list of dictionaries (full proxy objects)
            elif isinstance(data, list) and all(isinstance(x, dict) for x in data):
                for proxy_dict in data:
                    try:
                        proxy = Proxy.from_dict(proxy_dict)
                        self.add_proxy(proxy)
                    except Exception as e:
                        self.logger.warning(f"Invalid proxy data: {proxy_dict} - {e}")
            
            else:
                self.logger.warning(f"Unsupported format for initial_proxies in config: {config_proxies}")
        except Exception as e:
            self.logger.error(f"Failed to load proxies from API: {e}")
    
    def add_proxy(self, proxy: Proxy) -> None:
        """
        Add a proxy to the manager.
        
        Args:
            proxy: The proxy to add
        """
        with self._lock:
            self.proxies[proxy.url] = proxy
    
    def remove_proxy(self, proxy_url: str) -> None:
        """
        Remove a proxy from the manager.
        
        Args:
            proxy_url: The URL of the proxy to remove
        """
        with self._lock:
            if proxy_url in self.proxies:
                del self.proxies[proxy_url]
    
    def get_proxy(self, proxy_url: str) -> Optional[Proxy]:
        """
        Get a proxy by URL.
        
        Args:
            proxy_url: The URL of the proxy to retrieve
            
        Returns:
            The proxy if found, None otherwise
        """
        with self._lock:
            return self.proxies.get(proxy_url)
    
    def get_random_proxy(self) -> Optional[Proxy]:
        """
        Get a random proxy from the manager.
        
        Returns:
            A random proxy if available, None otherwise
        """
        with self._lock:
            if not self.proxies:
                return None
            
            return random.choice(list(self.proxies.values()))
    
    def get_proxies(self) -> List[Proxy]:
        """
        Get all proxies in the manager.
        
        Returns:
            A list of all proxies
        """
        with self._lock:
            return list(self.proxies.values())
    
    def get_active_proxies(self) -> List[Proxy]:
        """
        Get all active proxies in the manager.
        
        Returns:
            A list of all active proxies
        """
        with self._lock:
            return [proxy for proxy in self.proxies.values() if proxy.active]
    
    def get_proxies_by_protocol(self, protocol: str) -> List[Proxy]:
        """
        Get all proxies with the specified protocol.
        
        Args:
            protocol: The proxy protocol (http, https, socks4, socks5)
            
        Returns:
            A list of proxies with the specified protocol
        """
        with self._lock:
            return [proxy for proxy in self.proxies.values() if proxy.protocol == protocol]
    
    def get_proxies_by_country(self, country_code: str) -> List[Proxy]:
        """
        Get all proxies located in the specified country.
        
        Args:
            country_code: The country code (ISO 3166-1 alpha-2)
            
        Returns:
            A list of proxies located in the specified country
        """
        with self._lock:
            return [proxy for proxy in self.proxies.values() if proxy.country_code == country_code]
    
    def get_proxies_by_tag(self, tag: str) -> List[Proxy]:
        """
        Get all proxies with the specified tag.
        
        Args:
            tag: The tag to filter by
            
        Returns:
            A list of proxies with the specified tag
        """
        with self._lock:
            return [proxy for proxy in self.proxies.values() if tag in proxy.tags]
    
    def get_proxies_by_metadata(self, key: str, value: Any) -> List[Proxy]:
        """
        Get all proxies with the specified metadata key-value pair.
        
        Args:
            key: The metadata key
            value: The metadata value
            
        Returns:
            A list of proxies with the specified metadata key-value pair
        """
        with self._lock:
            return [proxy for proxy in self.proxies.values() if proxy.metadata.get(key) == value]
    
    def get_proxies_by_health_score(self, min_score: float = 0.0) -> List[Proxy]:
        """
        Get all proxies with a health score greater than or equal to the specified minimum.
        
        Args:
            min_score: The minimum health score (0.0 to 1.0)
            
        Returns:
            A list of proxies with a health score greater than or equal to the specified minimum
        """
        with self._lock:
            return [proxy for proxy in self.proxies.values() if proxy.health_score >= min_score]
    
    def get_proxies_by_last_used(self, max_age: float) -> List[Proxy]:
        """
        Get all proxies that were last used within the specified maximum age.
        
        Args:
            max_age: The maximum age in seconds
            
        Returns:
            A list of proxies that were last used within the specified maximum age
        """
        with self._lock:
            now = time.time()
            return [proxy for proxy in self.proxies.values() if proxy.last_used and now - proxy.last_used <= max_age]
    
    def get_proxies_by_last_checked(self, max_age: float) -> List[Proxy]:
        """
        Get all proxies that were last checked within the specified maximum age.
        
        Args:
            max_age: The maximum age in seconds
            
        Returns:
            A list of proxies that were last checked within the specified maximum age
        """
        with self._lock:
            now = time.time()
            return [proxy for proxy in self.proxies.values() if proxy.last_checked and now - proxy.last_checked <= max_age]
    
    def update_proxy(self, proxy: Proxy) -> None:
        """
        Update a proxy in the manager.
        
        Args:
            proxy: The updated proxy
        """
        with self._lock:
            self.proxies[proxy.url] = proxy
    
    def update_proxies(self, proxies: List[Proxy]) -> None:
        """
        Update multiple proxies in the manager.
        
        Args:
            proxies: The list of updated proxies
        """
        with self._lock:
            for proxy in proxies:
                self.proxies[proxy.url] = proxy
    
    def clear_proxies(self) -> None:
        """
        Clear all proxies from the manager.
        """
        with self._lock:
            self.proxies.clear()
    
    def __len__(self) -> int:
        """
        Get the number of proxies in the manager.
        
        Returns:
            The number of proxies in the manager
        """
        with self._lock:
            return len(self.proxies)
    
    def __iter__(self) -> Iterator[Proxy]:
        """
        Get an iterator over all proxies in the manager.
        
        Returns:
            An iterator over all proxies in the manager
        """
        with self._lock:
            yield from self.proxies.values()
    
    def __contains__(self, proxy_url: str) -> bool:
        """
        Check if a proxy is in the manager.
        
        Args:
            proxy_url: The URL of the proxy to check
            
        Returns:
            True if the proxy is in the manager, False otherwise
        """
        with self._lock:
            return proxy_url in self.proxies
```