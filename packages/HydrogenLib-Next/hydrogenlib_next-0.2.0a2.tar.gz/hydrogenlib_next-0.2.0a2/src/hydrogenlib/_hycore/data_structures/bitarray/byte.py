from typing import Union


class Byte:
    """
    将8位整数映射为列表，支持位操作。
    索引从最低位开始。
    """
    def __init__(self, x):
        self.x = int(x) & 0xFF  # 限制为8位
        self.length = self.x.bit_length()

    def append(self, x: Union[bool, int] = 0):
        """在最高位添加一个位"""
        if self.length >= 8:
            raise ValueError("Byte is full, cannot append more bits")
        if x not in (0, 1):
            raise ValueError("Value must be 0 or 1")
        self.x = (self.x << 1) | x
        self.length += 1

    def lappend(self, x: Union[bool, int] = 0):
        """在最低位添加一个位"""
        if self.length >= 8:
            raise ValueError("Byte is full, cannot append more bits")
        if x not in (0, 1):
            raise ValueError("Value must be 0 or 1")
        self.x = (self.x >> 1) | (x << (self.length - 1))
        self.length += 1

    def pop(self):
        """移除最高位"""
        if self.length == 0:
            raise IndexError("Cannot pop from an empty Byte")
        self.x &= ~(1 << (self.length - 1))
        self.length -= 1

    def remove(self, index):
        """
        删除指定位置的位，高位向左补齐。
        """
        if not (0 <= index < self.length):
            raise IndexError("Index out of range")
        left = self.x >> (index + 1)
        right = self.x & ((1 << index) - 1)
        self.x = (left << index) | right
        self.length -= 1

    def insert(self, index, x: Union[bool, int] = 0):
        """
        在指定位置插入一个位，源高位向右移动。
        """
        if not (0 <= index <= self.length):
            raise IndexError("Index out of range")
        if x not in (0, 1):
            raise ValueError("Value must be 0 or 1")
        if index == self.length:
            self.append(x)
        else:
            left = self.x >> index
            right = self.x & ((1 << index) - 1)
            self.x = (left << 1 | x) << index | right
            self.length += 1

    def __getitem__(self, index):
        """获取指定位置的位值"""
        if not (0 <= index < self.length):
            raise IndexError("Index out of range")
        return (self.x >> index) & 1

    def __setitem__(self, index, value):
        """设置指定位置的位值"""
        if not (0 <= index < self.length):
            raise IndexError("Index out of range")
        if value not in (0, 1):
            raise ValueError("Value must be 0 or 1")
        self.x = (self.x & ~(1 << index)) | (value << index)

    def __str__(self):
        return f"{self.x}({bin(self.x)})-L({self.length})"

    def __len__(self):
        return self.length


if __name__ == '__main__':
    b = Byte(0b101010)
    print(b)
    b.insert(5, 1)
    print(b)

    print()

    b = Byte(0b101010)
    print(b)
    b.insert(2, 1)
    print(b)

    print()

    b = Byte(0b101010)
    b[0] = 1
    print(b)

    try:
        b.append(2)  # 测试非法值
    except ValueError as e:
        print(f"Error: {e}")

    try:
        b.remove(8)  # 测试非法索引
    except IndexError as e:
        print(f"Error: {e}")
