### Android 启动动画转换器

这个 Python 脚本可以将单张图片转换为 Android 启动动画的 zip 文件。

### 使用方法

1. **准备图片**: 将你的图片文件 `bootanimation.png` 放置在与脚本相同的目录下。

2. **运行脚本**: 使用 Python 3 执行脚本。

   ```bash
   python make_boot_animation.py
   ```

3. **输出**: 执行后，脚本将在 `out/` 目录下生成名为 `bootanimation.zip` 的 zip 文件，其中包含生成的启动动画。

### 功能描述

该脚本执行以下步骤：

- **图片处理**: 打开 `bootanimation.png` 并获取其尺寸。

- **目录设置**: 创建必要的目录 (`out/bootanimation/part0` 和 `out/bootanimation/part1`)。

- **描述文件**: 生成 `desc.txt` 文件，描述动画序列和尺寸。

- **图片复制**: 将图片复制到动画的两个部分 (`part0` 和 `part1`)。

- **创建 zip 文件**: 创建一个不使用压缩的 zip 文件 (`bootanimation.zip`)，其中包含动画部分和描述文件。

### 环境要求

- Python 3.x
- Pillow (Python 图像处理库, `pip install Pillow`)

### 注意事项

- 在运行脚本之前，请确保 `bootanimation.png` 图片文件位于脚本的同一目录中。
- 脚本假定存在 `out/` 目录，用于存放生成的动画文件。

### 示例

假设 `bootanimation.png` 是一张分辨率为 1920x1080 的图片。执行脚本后，将在 `out/` 目录下生成 `bootanimation.zip` 文件，可以直接用作 Android 的启动动画。

关于 Android 启动动画的更多信息，请参考 [Android 开发者文档](https://developer.android.com/guide/topics/resources/boot-animation)。

### 许可证

该项目基于 MIT 许可证发布 - 可查看 [LICENSE](LICENSE) 文件获取详细信息。