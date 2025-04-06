class CheckedException(Exception):
    """
    可检查异常类，继承自Exception。
    用于表示需要显式处理的异常情况。
    """
    def __init__(self, message: str):
        """
        初始化可检查异常。
        
        Args:
            message: 异常信息
        """
        self.message = message
        super().__init__(self.message)

class UnCheckedException(RuntimeError):
    """
    不可检查异常类，继承自RuntimeError。
    用于表示运行时异常，不需要显式处理。
    """
    def __init__(self, message: str, error_code: str = None, cause: Exception = None):
        """
        初始化不可检查异常。
        
        Args:
            message: 异常信息
            error_code: 错误代码，可选
            cause: 原始异常，可选
        """
        super().__init__(message)
        self.message = message
        self._error_code = error_code
        if cause is not None and not isinstance(cause, Exception):
            raise TypeError("cause must be an Exception instance")
        self._cause = cause

    @property
    def code(self) -> str:
        """
        获取错误代码。
        
        Returns:
            错误代码
        """
        return self._error_code

    @code.setter
    def code(self, value: str):
        """
        设置错误代码。
        
        Args:
            value: 错误代码
        """
        self._error_code = value

    @property
    def cause(self) -> Exception:
        """
        获取原始异常。
        
        Returns:
            原始异常
        """
        return self._cause

    @cause.setter
    def cause(self, value: Exception):
        """
        设置原始异常。
        
        Args:
            value: 原始异常
        """
        if not isinstance(value, Exception):
            raise TypeError("cause must be an Exception instance")
        self._cause = value 