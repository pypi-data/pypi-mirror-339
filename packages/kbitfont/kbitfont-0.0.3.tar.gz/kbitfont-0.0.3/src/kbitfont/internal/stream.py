from typing import BinaryIO


class Stream:
    source: BinaryIO

    def __init__(self, source: BinaryIO):
        self.source = source

    def read(self, size: int) -> bytes:
        values = self.source.read(size)
        if len(values) < size:
            raise EOFError()
        return values

    def read_int(self, size: int) -> int:
        return int.from_bytes(self.read(size), 'big', signed=True)

    def read_int8(self) -> int:
        return self.read_int(1)

    def read_int16(self) -> int:
        return self.read_int(2)

    def read_int32(self) -> int:
        return self.read_int(4)

    def read_uint(self, size: int) -> int:
        return int.from_bytes(self.read(size), 'big', signed=False)

    def read_uint8(self) -> int:
        return self.read_uint(1)

    def read_uint16(self) -> int:
        return self.read_uint(2)

    def read_uint32(self) -> int:
        return self.read_uint(4)

    def read_utf(self) -> str:
        size = self.read_uint16()
        return self.read(size).decode()

    def read_uleb128(self) -> int:
        value = 0
        shift = 0
        while True:
            data = self.read_uint8()
            value |= (data & 0x7F) << shift
            if (data & 0x80) == 0:
                break
            shift += 7
        return value

    def read_bitmap(self) -> list[list[int]]:
        bitmap = []
        height = self.read_uleb128()
        width = self.read_uleb128()
        repeat_count = 0
        repeat_color = None
        for _ in range(height):
            bitmap_row = []
            for _ in range(width):
                if repeat_count <= 0:
                    data = self.read_uint8()
                    repeat_count = data & 0x1F
                    if data & 0x20 != 0:
                        repeat_count <<= 5
                    color_type = data & 0xC0
                    if color_type == 0x00:
                        repeat_color = 0x00
                    elif color_type == 0x40:
                        repeat_color = 0xFF
                    elif color_type == 0x80:
                        repeat_color = self.read_uint8()
                    elif color_type == 0xC0:
                        repeat_color = None
                repeat_count -= 1
                color = self.read_uint8() if repeat_color is None else repeat_color
                bitmap_row.append(color)
            bitmap.append(bitmap_row)
        return bitmap

    def write(self, values: bytes) -> int:
        return self.source.write(values)

    def write_int(self, value: int, size: int) -> int:
        return self.write(value.to_bytes(size, 'big', signed=True))

    def write_int8(self, value: int) -> int:
        return self.write_int(value, 1)

    def write_int16(self, value: int) -> int:
        return self.write_int(value, 2)

    def write_int32(self, value: int) -> int:
        return self.write_int(value, 4)

    def write_uint(self, value: int, size: int) -> int:
        return self.write(value.to_bytes(size, 'big', signed=False))

    def write_uint8(self, value: int) -> int:
        return self.write_uint(value, 1)

    def write_uint16(self, value: int) -> int:
        return self.write_uint(value, 2)

    def write_uint32(self, value: int) -> int:
        return self.write_uint(value, 4)

    def write_utf(self, value: str) -> int:
        data = value.encode()
        return self.write_uint16(len(data)) + self.write(data)

    def write_uleb128(self, value: int) -> int:
        size = 0
        while value >= 0x80:
            size += self.write_uint8((value | 0x80) & 0xFF)
            value >>= 7
        size += self.write_uint8(value & 0xFF)
        return size

    def _write_bitmap_runs(self, no_repeat_colors: bytearray, repeat_count: int, repeat_color: int) -> int:
        size = 0
        if len(no_repeat_colors) > 0:
            n = len(no_repeat_colors)
            offset = 0
            while n >= 992:
                size += self.write_uint8(0xFF)
                size += self.write(no_repeat_colors[offset:offset + 992])
                offset += 992
                n -= 992
            if n >= 32:
                m = n >> 5
                size += self.write_uint8(0xE0 | m)
                m <<= 5
                size += self.write(no_repeat_colors[offset:offset + m])
                offset += m
                n -= m
            if n > 1:
                size += self.write_uint8(0xC0 | n)
                size += self.write(no_repeat_colors[offset:offset + n])
            if n == 1:
                color = no_repeat_colors[offset]
                if color == 0x00:
                    size += self.write_uint8(0x01)
                elif color == 0xFF:
                    size += self.write_uint8(0x41)
                else:
                    size += self.write_uint8(0x81)
                    size += self.write_uint8(color)
        if repeat_count > 0:
            if repeat_color == 0x00:
                base = 0x00
            elif repeat_color == 0xFF:
                base = 0x40
            else:
                base = 0x80
            pat = repeat_color != 0x00 and repeat_color != 0xFF
            while repeat_count >= 992:
                size += self.write_uint8(base | 0x3F)
                if pat:
                    size += self.write_uint8(repeat_color)
                repeat_count -= 992
            if repeat_count >= 32:
                m = repeat_count >> 5
                size += self.write_uint8(base | 0x20 | m)
                m <<= 5
                if pat:
                    size += self.write_uint8(repeat_color)
                repeat_count -= m
            if repeat_count > 0:
                size += self.write_uint8(base | repeat_count)
                if pat:
                    size += self.write_uint8(repeat_color)
        return size

    def write_bitmap(self, bitmap: list[list[int]]) -> int:
        size = 0
        height = len(bitmap)
        width = max(len(bitmap_row) for bitmap_row in bitmap) if height > 0 else 0
        size += self.write_uleb128(height)
        size += self.write_uleb128(width)
        no_repeat_colors = bytearray()
        repeat_count = 0
        repeat_color = None
        for bitmap_row in bitmap:
            if len(bitmap_row) < width:
                bitmap_row = bitmap_row + [0x00] * (width - len(bitmap_row))
            for color in bitmap_row:
                if repeat_count <= 0:
                    repeat_count = 1
                    repeat_color = color
                elif repeat_color == color:
                    repeat_count += 1
                elif repeat_count == 1:
                    no_repeat_colors.append(repeat_color)
                    repeat_color = color
                else:
                    size += self._write_bitmap_runs(no_repeat_colors, repeat_count, repeat_color)
                    no_repeat_colors.clear()
                    repeat_count = 1
                    repeat_color = color
        if repeat_count == 1:
            no_repeat_colors.append(repeat_color)
            repeat_count = 0
        size += self._write_bitmap_runs(no_repeat_colors, repeat_count, repeat_color)
        return size

    def seek(self, offset: int):
        self.source.seek(offset)

    def tell(self) -> int:
        return self.source.tell()
