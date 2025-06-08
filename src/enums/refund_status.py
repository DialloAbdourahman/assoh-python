from enum import Enum

class EnumRefundStatus(Enum):
    CREATED= 'CREATED'
    INITIATED = 'INITIATED'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'


