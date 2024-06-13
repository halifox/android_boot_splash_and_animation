### Splash Image Converter

这个 Python 脚本可以将 PNG 图片转换为 `splash.img` 格式的 Boot Splash 文件。

### 使用方法

1. **准备图片**: 将要转换的 PNG 图片命名为 `splash.png` 并放置在脚本所在目录下。

2. **运行脚本**: 使用 Python 执行脚本。

   ```bash
   python logo_gen_v4.py
   ```

3. **输出**: 脚本将在 `out/` 目录下生成名为 `splash.img` 的 Boot Splash 文件。

### 功能描述

该脚本执行以下主要步骤：

- **生成头部信息**: 创建用于 Boot Splash 文件的头部信息，包括图像宽度、高度、压缩标志和块数量。

- **RLE24 压缩**: 如果选择了 RLE24 压缩（默认启用），将对图像进行压缩处理。

- **获取图像数据**: 将输入的 PNG 图像转换为适合于 `splash.img` 格式的数据。

- **输出 Boot Splash 文件**: 将生成的头部信息和图像数据写入到 `splash.img` 文件中。

### 环境要求

- Python 3.x
- Pillow (Python 图像处理库, 可通过 `pip install Pillow` 安装)

### 注意事项

- 在运行脚本之前，请确保 `splash.png` 图片文件位于脚本的同一目录中。
- 输出文件将保存在 `out/` 目录中。如需更改输出路径，请在脚本中相应位置进行调整。

### 示例

假设 `splash.png` 是一个 1920x1080 的 PNG 图片。执行脚本后，将在 `out/` 目录下生成 `splash.img` 文件，该文件可用于特定设备的启动画面。

### 许可证

该项目基于 MIT 许可证发布 - 可查看 [LICENSE](LICENSE) 文件获取详细信息。
