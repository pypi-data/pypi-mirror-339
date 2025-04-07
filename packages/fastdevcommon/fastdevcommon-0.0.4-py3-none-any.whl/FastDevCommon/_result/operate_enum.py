from enum import Enum


class MessageEnum(Enum):
    NOT_CREATE_TASK_ERROR = "任务创建失败"


class OperateCode(Enum):
    """返回code枚举"""

    SUCCESS = 1  # 成功
    WARNING = 2  # 友好提示
    CAN_TRY = 3  # 需要重试
    WAIT = 4  # 需要等待
    DENIED = 400  # 拒绝访问
    ERROR = 500  # 应用错误
