# 导入所需的库
from PIL import Image  # 用于处理图像
import struct  # 用于将Python的数据类型转换为C语言的结构体格式

# 当该脚本作为主程序运行时，执行以下代码
if __name__ == "__main__":
    # 输入文件路径，这里是一个PNG格式的图像文件
    input_file = "splash.png"
    # 输出文件路径，将生成的图像数据保存到该文件
    output_file = "out/splash.img"

    # 打开输入图像文件并将其转换为RGB格式
    img = Image.open(input_file).convert("RGB")

    # 将图像数据转换为字节流
    body_data = img.tobytes()

    # 获取图像的宽度和高度
    width, height = img.size

    # 计算图像数据占用的实际块数（每个块512字节）
    # 这里加上511是为了确保向上取整
    real_size = (len(body_data) + 511) // 512

    # 创建一个512字节的头部数据，初始化为0
    header = bytearray(512)

    # 在头部的前8个字节写入魔数（Magic Number），用于标识文件格式
    header[:8] = b'SPLASH!!'

    # 使用struct.pack_into将宽度（width）打包为4字节的无符号整数（<I表示小端序）
    # 并将其写入头部的第8字节开始的位置
    struct.pack_into("<I", header, 8, width)

    # 将高度（height）打包为4字节的无符号整数，并写入头部的第12字节开始的位置
    struct.pack_into("<I", header, 12, height)

    # 写入压缩标志，这里设置为0，表示未压缩
    struct.pack_into("<I", header, 16, 0)

    # 写入图像数据占用的实际块数
    struct.pack_into("<I", header, 20, real_size)

    # 将头部数据转换为字节类型
    header_data = bytes(header)

    # 打开输出文件，以二进制写入模式
    with open(output_file, "wb") as f:
        # 将文件指针移动到4096字节处（即跳过前4096字节）
        f.seek(4096)
        # 写入头部数据
        f.write(header_data)
        # 写入图像数据
        f.write(body_data)

    # 打印成功信息，输出文件路径
    print(f"Image conversion successful. Output file: {output_file}")