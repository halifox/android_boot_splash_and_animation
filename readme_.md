# 高通平台第一帧splash和Bootanimation修改

> https://blog.csdn.net/weixin_42237018/article/details/99678412

```
                                   高通平台第一帧splash和Bootanimation
```

_**A.Splash image**_/第一帧图像/开机logo\(有很多叫法，但比较官方的一般叫bootloader logo或者LK display logo\)  
替换LK display \(bootloader\) logo有两种方式  
a.利用平台自带的logo\_gen.py生成splash.img镜像，可以使用fastboot重新刷splash.img分区  
b.利用三方软件将.png转为bootable/bootloader/lk/platform/msm\_shared/include/splash.h头文件中的buffer并替换

方法b只适用于分辨率较低的图片（经测试临界点大概在320\*240左右），方法a适用于各种分辨率图片（.png）

看源码bootable/bootloader/lk/dev/fbcon/fbcon.c中的逻辑  
系统会先通过fetch\_image\_from\_partition\(\)获取.img格式镜像，如失败  
会去splash.h头文件获取数组，如果数组无效或者获取失败，会显示default fbimg

先说下生成splash.img的步骤

1.  需要符合屏幕分辨率的.png图像
2.  将图像放到目录device/qcom/common/display/logo，并确认该目录下有logo\_gen.py脚本
3.  python ./logo\_gen.py logo.png  
    如果遇到以下错误：  
    ![PIL报错](https://img-blog.csdnimg.cn/20190819152531628.png)  
    的话请安装Pillow 组件（pip install Pillow）
4.  在partition.xml添加splash分区
5.  在contents.xml添加splash.img  
    \<download\_file minimized=“true” fastboot=“true”>  
    \<file\_name>splash.img\</file\_name>  
    \<file\_path>LINUX/android/out/target/product/msm8937\_32go/\</file\_path>  
    \</download\_file>  
    Fastboot一定要为true否则无法fastboot烧录
6.  在编译脚本中把splash.img copy到代码out目录  
    PRODUCT\_COPY\_FILES += device/qcom/common/display/logo/splash.img:splash.img
7.  在打包脚本中把splash.img copy到pub out目录  
    cp -f LA.UM.7.6.2/LINUX/android/device/qcom/common/display/logo/splash.img R E L E A S E D I R / RELEASE\_DIR/ RELEASED​IR/TAR\_VER/LA.UM.7.6.2/LINUX/android/out/target/product/\$\{TARGET\_PRODUCT\}/
8.  如果按上面方法操作了还不生效，请打串口log看下是否有splash image相关报错，我在改的过程中碰到了header invalid的错误，最后发现是logo\_gen.py中header起始/终止地址有误。修改文件读取指针的位置后就ok了，一般有splash image报错都是由于生成脚本本身有问题  
    ![splash header报错](https://img-blog.csdnimg.cn/20190819152830132.png)  
    下面说下方法b,
9.  找到bootable/bootloader/lk/platform/msm\_shared/include/splash.h，会发现里面有三个buffer: imageBuffer\[\], imageBuffer\_rgb888\[\]和image\_batt888\[\]。生效的逻辑也在fbcon.c中：  
    #if DISPLAY\_TYPE\_MIPI  
    fbimg->image = \(unsigned char \*\)imageBuffer\_rgb888;  
    #else  
    fbimg->image = \(unsigned char \*\)imageBuffer;  
    #endif
10.  用三方工具将.png转为buffer, 我用的是Image2Lcd，转出来的buffer大小如果大于源码中buffer的大小，会有异常，可以通过降低输出图像的色彩位数减少buffer size\(不影响效果的前提下\)。如果需要修改buffer size上限，方法如下  
     a. 找到项目.dtsi, arch/arm/boot/dts/qcom/msmxxxx.dtsi

b. 在64位的版本中buffer地址为4M,  
reserved-memory \{<!-- -->  
…  
cont\_splash\_mem: splash\_region\@83000000 \{<!-- -->  
reg = \<0x0 0x90000000 0x0 0x1400000>;  
\};  
\}  
debug可以通过kernal log看是否有类似报错：  
\[ 0.000000\] memblock\_reserve: \[0x0000008e000000-0x00000090800000\] dma\_contiguous\_reserve\_area+0xdc/0x1e4  
\[ 0.000000\] cma: CMA: reserved 40 MiB at 0x000000008e000000 for cont\_splash\_mem  
\[ 0.000000\] reserved\[0x3\] \[0x0000008e000000-0x000000907fffff\], 0x2800000 bytes  
Kernal log添加方法如下：  
a. 在kernal 配置文件中扩大kernal log buffer的大小:  
// msm-perf\_defconfig  
CONFIG\_LOG\_BUF\_SHIFT=18  
b. 打开memblock debug  
//arch/arm/boot/dts/qcom/msmxxxx.dtsi  
chosen \{<!-- -->  
// bootargs = “boot\_cpus=0,1,2,3,4 sched\_enable\_hmp=1”;  
bootargs = “boot\_cpus=0,1,2,3,4 sched\_enable\_hmp=1 memblock=debug”; \};

3.  如果想删除第一帧的话，找到 arch/arm/boot/dts/qcom/msmxxxx-mdss.dtsi ,注掉以下行代码

mdss\_fb0: qcom,mdss\_fb\_primary \{<!-- -->  
cell-index = \<0>;  
compatible = “qcom,mdss-fb”;  
// qcom,mdss-fb-splash-logo-enabled;  
qcom,cont-splash-memory \{<!-- -->  
linux,contiguous-region = \<\&cont\_splash\_mem>;  
\};  
\};

_**B.Boot animation**_  
这个比较简单，甚至都没有什么需要debug的点  
1.bootanimation.zip由两部分组成（配置文件和图片文件夹）

a.desc.txt \- 动画配置文件，帧数循环次数，文件名称, 需注意文件格式需要改为ANSI

480 960 1 \- “480” 为动画播放宽度，”960”为动画播放高度，不确定的话可以用adb shell wm size或者adb shell dumpsys window displays看一下，”1”为fps值

p 1 0 part0 \- “p”是一个标志位, 说明当service.bootanim.exit属性为true时，不用等待所有图片播放完毕就跳出播放，第一位为”c”时，说明当service.bootanim.exit属性为true时，必须要等播放完成后才会跳出这部分。”1” 为循环次数，如果这个值为”0”的话，说明此部分动画会一直循环，直到service.bootanim.exit为true。”0”为播放完这部分的暂停，为0代表无暂停。”part0”为存放动画图片的文件夹名

p 0 0 part1

b.part0, part1个文件夹 \- 也可以手动根据需求添加part3,或者改文件夹名字

2.Zip/unzip bootaimation.zip的所有动作最好都在Linux环境下完成  
特别需要注意的是，压缩bootanimation.zip的时候压缩模式必须为存储模式：  
zip \-r \-0 bootanimation.zip part0 part1 desc.txt  
压缩完成后请用：  
Unzip \-t bootanimation检查压缩包是否完整

3.本地验证可以直接把存储模式的bootanimation.zip push到device的/system/media目录下验证

4.编译的话需要在.mk中将bootanimation.zip拷贝到system/media目录：  
PRODUCT\_COPY\_FILES += device/qcom/msm8937\_64/bootanimation.zip:system/media/bootanimation.zip