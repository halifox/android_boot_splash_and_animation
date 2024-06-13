# 修改 Android 设备启动时显示的启动画面（Boot Splash）

准备与屏幕同分辨率的图片并命名为`splash.png`

> 注意 这张图片可能需要是 **竖屏** 和 PNG 格式

[脚本使用文档](./readme_logo_gen.md)

重启至引导加载程序模式并刷写自定义启动画面

```bash
# 通过 Android Debug Bridge (adb) 工具，将设备重新启动到引导加载程序 (bootloader) 模式。
adb reboot bootloader
# 使用 fastboot 命令行工具，将指定的启动画面图像文件 (splash.img) 刷写到设备的启动画面分区。
fastboot flash splash splash.img
```

# 修改 Android 设备开机动画（Boot Animation）

准备与屏幕同分辨率的图片并命名为`bootanimation.png`

[脚本使用文档](./readme_make_boot_animation.md)

修改或者替换 Android 设备的启动动画

```bash
# 尝试将指定的分区重新挂载为读写 (rw) 模式
# 如果失败则需要 禁用 Android 设备上的 dm-verity 文件完整性验证 见下文
adb remount
# 将本地计算机上的 bootanimation.zip 文件推送（复制）到 Android 设备的 /system/media/ 目录下，并将其命名为 bootanimation.zip。
adb push bootanimation.zip /system/media/bootanimation.zip
```

禁用 Android 设备上的 dm-verity 文件完整性验证  
禁用 dm-verity 可以允许修改系统分区而不会触发验证错误，但这也会降低设备的安全性。

```bash
adb disable-verity
adb reboot
```

### 许可证

该项目基于 MIT 许可证发布 - 可查看 [LICENSE](LICENSE) 文件获取详细信息。