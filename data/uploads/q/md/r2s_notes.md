# 基于r2s软路由部署iStoreOS解决文星（以后还有其他宿舍区）慧湖通宽带验证问题的通用方案（小白级逐步教程）

> **注意：本教程仅用于兴趣爱好分享交流，本文作者以及所有项目相关作者不对任何不当使用技术引起的后果负责。** 
> 
> 本着互联网开放交流共享的原则，作者专门整理了一点点个人实践心得，为网络通信技术爱好者和动手实践者提供一个小白教程(尽量使用可视化操作完成各个配置的修改)，以避免踩一些不必要的坑。如果有任何纰漏不完善的地方还请各位多多海涵，也欢迎评论提出各种建议。希望本教程对现在和未来的网络优化有所帮助
> 
> 本教程基于r2s入门软路由及以上配置，暂时不涉及路由器重新刷固件改软路由的方案（也许后面会更新）
>
> **参考文章链接：**
> + [检测原理：HuiHuBuTong](https://github.com/TianxinZhao/HuiHuBuTong)
> + [刷机教程：r2s安装istoreOS](https://www.bilibili.com/video/BV1vv4y1D71K/?t=3.117207&spm_id_from=333.1350.jump_directly&vd_source=d03e61540959009532833f4cca457930)
> + [UA修改：UA3F作者开发笔记](https://blog.sunbk201.site/posts/ua3f/)
> + [UA3F+Clash安装](https://sunbk201public.notion.site/UA3F-Clash-16d60a7b5f0e457a9ee97a3be7cbf557#48767e4449d7405099979fea2f999e8e)
> + [手动安装内核：shellClash](https://juewuy.github.io/bdaz/)
>


## 1. 准备材料

- **友善r2s 软路由设备**（必须需要有一张 SD 卡用于存储 iStoreOS 系统，无SD卡无法使用）：这是一个入门级别软路由硬件，某东裸机不带电源全新240，作者闲鱼上169购得，性能大约跑满800M带宽网络，文星500M绰绰有余。有一个LAN口一个WAN口。
- **MicroSD 卡和读卡器**（用于将 iStoreOS 系统刷入 SD 卡）：随便一张监控录像（行车记录仪）速率的sd卡就够用，品牌不限。尺寸是小卡。
- **电脑**（安装烧录工具及配置软路由）
- **必要的软件**：
  - [`iStoreOS 固件`](https://doc.linkease.com/zh/guide/istoreos/)用于安装软路由系统
  - `Win32DiskImager` 用于将 iStoreOS烧录到 SD 卡
  - `MobaXterm` 或其他 SSH 客户端, 或者直接使用ssh命令行
  - [`shellclash`](https://github.com/yang123me/ShellClash)用于配置透明路由代理，转发经过软路由的所有流量到`Ua3f`软件中处理，同时还可实现科学上网等功能
  - [`Ua3f`](https://github.com/SunBK201/UA3F)Github开源软件用于修改UA信息，该项目最大的优势是同时整合了clash代理软件，适当配置能够同时实现科学上网功能

## 2. 原理说明

检测原理详见于[Github Project HuiHuBuTong](https://github.com/TianxinZhao/HuiHuBuTong)

截止文档撰写日期`2024.09.10`为止，主要需要考虑的检测机制有如下三点：

> 以后不一定有效，文星还有可能持续更新检测机制

1. MAC地址克隆：主要用于让路由器能够伪装为光猫已认证的设备
2. TTL覆写：防止光猫检测到内网使用了路由器
3. UA信息修改：防止光猫检测到内网多个设备共享

本教程中，宿舍组网方案的网络结构拓扑图如下
![](image.png)
> 图来自[HuiHuBuTong](https://github.com/TianxinZhao/HuiHuBuTong)

## 3. 逐步教程

### Part1: 安装iStoreOS/OpenWrt系统

> 该部分视频教程详见（本文不再过多重复）：https://www.bilibili.com/video/BV1vv4y1D71K/?t=3.117207&spm_id_from=333.1350.jump_directly&vd_source=d03e61540959009532833f4cca457930

#### 烧录 iStoreOS 到 SD 卡

1. 下载 iStoreOS 固件并解压。
2. 使用 `Win32DiskImager` 软件将 iStoreOS 固件烧录到 SD 卡。
3. 将烧录完成的 SD 卡插入 r2s 软路由

#### 软路由启动和基础配置

**软路由启动**
1. 将 r2s 软路由连接到个人电脑的网络，用网线链接个人电脑网口和软路由的lan口，或者用将软路由lan口接入AP模式下WIFI的lan口（详情见下一节硬件连接方式），并接通电源启动。

**软路由基础配置**
1. 有限链接后可以在网络共享中心看到有线连接设备那有位置的网络，点属性配置ipv4协议，里面配置本地ip地址如192.168.100.1和子网掩码如255.255.255.0

**通过ssh登录**
1. 使用 `MobaXterm` 或其他 SSH 客户端连接到 r2s 软路由（默认 IP 地址为你刚刚配置`192.168.100.1`）。
2. 使用默认的用户名(root)和密码(password)登录到软路由。正确登录进去之后如下
![alt text](image-2.png)

**或者通过浏览器直接登录**
1.正常配置之后输入网址，即你配置好的（192.168.100.1），等待响应后你能看到这个页面![alt text](image-1.png)

### Part2: 修改硬件连接方式

  - 这里讲一下核心要点：我们寝室网络最终接线结构是和前文提到的用户网络的拓扑图相同的。但是在安装部署过程中，各项软件的下载安装依然需要连接网络。为了方便广大读者直接在软路由上安装和配置（如果您会手动下包安装然后再手动上传也可），这里最好是先正常登录接入软路由局域网。 
  - 由于友善r2s没有wifi功能，因此需要一个设备来构建WiFi，你也可以加购usbWIFI模块来解决。或者你也可以先暂时通过网线连接电脑，即`光猫->软路由Wan->软路由Lan->电脑`的结构。
  - 如果电脑没有网口，可以换为`光猫->软路由Wan->软路由Lan-> AP模式硬路由器Wan`的方法，通过连接WIFI来让电脑接入软路由所在局域网，正常也会出现hht登录认证，通过即可接入网络。
  >**如何把硬路由更换为AP（有线中继模式）：** 具体每个路由器情况不完全一样。核心方案就是登录到之前的路由器管理员后台，将路由器上网模式修改为有线中继模式，用网线连接r2s的lan口和AP模式路由器的Wan口，这个时候该硬路由仅仅起到了WIFI信号发射和接收器的作用

  具体接线如图所示：![alt text](ca41bc0de468bca2a5818ccfe89ad40.jpg)
  光猫接线：白色线为光猫2.5g入网口
  ![alt text](03ce7d299962327d005d1d3761cb8a3.jpg)
  r2s接线：白色另外一头为光猫，这头接入Wan口；黄色接入Lan口，另外一头为路由器
  ![alt text](edbd6803cfc975d0a8b4c98bf5b6050.jpg)
  路由器接线：黄色接入路由器Wan口，其余接线为寝室其他设备
>PS：以tplink为首的众多路由器已经将早年“下放”的基本功能如静态路由等功能移除了，这也是作者认为在解决当前问题旁路由方案可行性不高的直接原因，即大部分AP模式的路由器并不能直接重定向流量到指定IP对应的网关，因此旁路由无法实现控制进入局域网的所有流量。事实证明确实如此，这是作者闲鱼99R买的N1电视盒子魔改的旁路由踩的坑

### Part3: 针对检测机制调整软路由核心配置

#### 修改软件源和自定义`DNS`（不是必须）
点击首页DNS按钮，选择自定义DNS，键入任意能够正常稳定服务的DNS即可，如：8.8.8.8/8.8.4.4
![alt text](image-14.png)
点击首页软件源按钮，可以在opkg连接不上时更换有响应的国内节点，一般节点都没啥问题，这个系统偶尔会因为未知原因连接不上opkg软件库

#### `MAC`地址克隆

为了让光猫以为接入上网的只有一台已经认证过的设备，因此修改软路由WAN口的MAC地址为之前单独连接并且认证过的设备即可

> 注意：本文后面所述的连接光猫均指的是插入光猫的2.5g插口，注意不要插到其他接口如千兆、IPTV等。

**查找已认证设备的MAC地址**
1. 把任意一台设备直接连接到光猫，wifi/有线均可。wifi可以用ap模式的路由器直接连接在光猫上实现
2. 点击打开wifi设置，找到网络属性（这里以学校网络情况为例），点开翻到最下面找到物理地址（MAC）并记录
![alt text](image-7.png)
![alt text](image-8.png)

**修改光猫接入WAN口的MAC地址**
1. 打开iStoreOS后台管理员页面，并登录
![alt text](image-3.png)
2.点击左边侧边栏-> 网络 -> 接口
![alt text](image-4.png)
3. 找到WAN口点击编辑,注意对应接口是eth0还是eth1，在作者这里是eth0
![alt text](image-5.png)
4. 修改Wan口对应的MAC地址，修改后选择保存并应用
![alt text](image-6.png)

#### 修改 `TTL` 值

根据原理说明数据包每经过一个路由器ttl值就会发生变化，该步骤是为了保证通过光猫的所有网络包的 TTL 值一致，防止被检测到路由器。


1. TTL 规则固定如下

```bash
   iptables -t mangle -A POSTROUTING -j TTL --ttl-set 128
```
2. 添加办法

- **方案1：**
   **istoreOS管理员界面设置**
   找到网络 -> 防火墙 选择自定义规则，直接粘贴代码，点右下角保存，接着重启防火墙
   ![alt text](image-9.png)
   ![alt text](image-10.png)
   ![alt text](image-11.png)

- **方案2：**
**命令行添加**
   使用ssh或者点击主页里的终端，进入ssh。编辑 `/etc/firewall.user` 文件：
   ```bash
   vi /etc/firewall.user
   ```

   然后将以下内容添加到文件末尾：
   ```bash
   iptables -t mangle -A POSTROUTING -j TTL --ttl-set 128
   ```

   保存并退出编辑器，然后重新启动防火墙服务：
   ```bash
   /etc/init.d/firewall restart
   ```

#### 修改 `User-Agent` 信息

使用 `UA3F` 工具进行 HTTP `User-Agent` 修改，以绕过路由器检测。

1. 安装 UA3F 工具：

- **方案1：**
   **Release页面下载Ua3f**
   访问ua3f [release下载页面](https://github.com/SunBK201/UA3F/releases) 选择你的硬件架构，不同架构使用的软件包不一样，笔者这里使用的是软路由r2s软路由架构为arm64。
   ![alt text](image-12.png)
   使用scp或者ssh客户端将下载下来的`.ipk`文件传给路由器
   或者使用网页端上传：选择系统 -> 文件传输
   ![alt text](image-13.png)

   **安装Ua3f的依赖软件**
   紧接Release页面下载方案
   ```bash
      opkg update
      opkg install curl libcurl luci-compat
   ```

- **方案2：**
   **使用作者提供的下载脚本，统一安装**
   详见[下载命令](https://github.com/SunBK201/UA3F)
   ```bash
   opkg update
   opkg install curl libcurl luci-compat
   export url='https://blog.sunbk201.site/cdn' && sh -c "$(curl -kfsSl $url/install.sh)"
   service ua3f reload
   ```


2. 启动 `UA3F` 服务并配置自定义 `User-Agent`：
- **方案1：**
  正确安装 `Ua3f` 软件后刷新管理员页面，在服务一栏会出现该选项卡，如图所示
  ![alt text](image-15.png)
  勾选enabled启动服务，`User-Agent`自己随意改，默认FFF，其他不修改。点右下角保存并应用即可
- **方案2：**
  习惯命令行的同学直接参考 [Ua3f说明文档](https://github.com/SunBK201/UA3F#%E4%BD%9C%E4%B8%BA%E5%90%8E%E5%8F%B0%E6%9C%8D%E5%8A%A1%E8%BF%90%E8%A1%8C)


### Part4: 配置局域网内代理，强制转发局域网内所有流量到`Ua3f`监听端口（此步非常重要）

该步骤教程来源于ua3f作者提供的安装文档，详情查阅[参考文档](https://sunbk201public.notion.site/UA3F-Clash-16d60a7b5f0e457a9ee97a3be7cbf557#48767e4449d7405099979fea2f999e8e)。作者已经非常详细地说明如何安装，本文不再赘述。

>在这里笔者个人选择shellclash来实现透明代理，对于小白来说也许openclash会好用一些，UI也会和istoreOS集成，整体更美观。
- **注意**：本文中Clash均选择加载Meta内核
- 如果出现shellclash/openclash内核自动下载错误，参考文档：[手动安装内核](https://juewuy.github.io/bdaz/)

- 在选择 `导入外部配置文件链接`步骤时，建议改为 `本地上传完整配置文件`。
![alt text](image-16.png)
- 自行手动下载写好的yaml配置文件上传到路径`/tmp/`。这里给到作者提供的clash代理配置（作者的cdn需要梯子才能快速访问）
- 一共有三种配置，这里只列举了不带科学上网的版本，[详情访问](https://github.com/SunBK201/UA3F?tab=readme-ov-file#clash-%E5%8F%82%E8%80%83%E9%85%8D%E7%BD%AE)
```yaml
#--------------------------------------------------------------------------------------#
# Written by SunBK201
# https://github.com/SunBK201/UA3F
#--------------------------------------------------------------------------------------#
mixed-port: 7890
#--------------------------------------------------------------------------------------#
ipv6: false
mode: rule
#--------------------------------------------------------------------------------------#
dns:
#--------------------------------------------------------------------------------------#
proxies:
  - name: "ua3f"
    type: socks5
    server: 127.0.0.1
    port: 1080
    url: http://connectivitycheck.platform.hicloud.com/generate_204
    udp: false
#--------------------------------------------------------------------------------------#
proxy-providers:
#--------------------------------------------------------------------------------------#
proxy-groups:
#--------------------------------------------------------------------------------------#
rules:
  - PROCESS-NAME,ua3f,DIRECT
  - NETWORK,udp,DIRECT
  - MATCH,ua3f
#--------------------------------------------------------------------------------------#
rule-providers:
#--------------------------------------------------------------------------------------#
parsers:
#--------------------------------------------------------------------------------------#
```
- 如果正确配置好后记得启动服务，笔者之前不止一次忘记手动启动从而出现断网的情况。另外建议配置定时任务，选择定时重启，这样可以减少维护成本。


## 4. 调试注意事项

1. 部署过程中建议按照笔者顺序进行来修改，中途可能被光猫检测到路由器而出现封号情况（1分钟），系正常情况，自行灵活应对。建议在部署过程中，全程不要有任何第二个设备接入局域网，只有已经认证的电脑接入。
2. 安装完成后，主要测试能否正常上网，可以使用网络测速等在线工具。
3. 多尝试使用网页里查看防火墙的配置是否正常运行，是否有流量经过。![alt text](image-17.png)
4. 多多检查日志是否有报错信息，[info]和[warning]都可以忽略
5. 如果遇到添加防火墙配置过程中，访问管理员页面被服务器拒绝的情况。可以采取如下措施来暂时恢复访问：
   1. 登录ssh或者浏览器访问http://192.168.100.1:7681/
   2. 输入用户名和密码（密码为暗文不显示是正常的）
   3. 输入``` /etc/init.d/firewall stop ```暂时关闭防火墙，进行相关调整。重启防火墙使用``` /etc/init.d/firewall restart ```

## 5. 总结与感悟

特别感谢[HuiHuBuTong](https://github.com/TianxinZhao/HuiHuBuTong)作者开源的检测原理；感谢[UA3F](https://blog.sunbk201.site/posts/ua3f/)作者开发的核心工具和详细教程对这条笔记的梳理和完善给予了很多启发。

**特别强调**：本教程本着开源共享自由交流的原则撰写，仅供兴趣爱好分享和学习交流。任何不当使用技术的行为所造成的后果，作者不负任何责任。笔者是非通讯专业的外行，这次也是出于兴趣爱好进行了一些有益的尝试。但是对于很多工具背后的技术细节和原理并不足够充分了解，如果存在一些隐患也请各路大佬多多批评指正。同时如果您觉得本文有帮助，也请低调分享，感谢支持。