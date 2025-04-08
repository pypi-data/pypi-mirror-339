from typing import Optional

from mag_tools.model.common.justify_type import JustifyType


class DataFormat:
    def __init__(self, justify_type: JustifyType = JustifyType.LEFT, decimal_places: int = 2,
                 decimal_places_of_zero: int = 1, pad_length: Optional[int] = None, scientific: bool = False):
        """
        数据格式
        :param justify_type: 对齐方式
        :param decimal_places: 小数位数
        :param decimal_places_of_zero: 小数为0时的小数位数
        """
        self.justify_type = justify_type
        self.decimal_places = decimal_places if decimal_places is not None else 0
        self.decimal_places_of_zero = decimal_places_of_zero if decimal_places_of_zero is not None else 0
        self.pad_length = pad_length if pad_length is not None else 0
        self.scientific = scientific

    def __str__(self):
        """
        返回 DataFormat 实例的字符串表示。
        :return: DataFormat 实例的字符串表示。 """
        return f"DataFormat({', '.join(f'{key}={value}' for key, value in vars(self).items())})"
