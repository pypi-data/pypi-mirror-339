# 灵巧手DexHand SDK 接口文档

# DexHand SDK 接口文档

## 简介

DexHand SDK 以UDP通信方式和底层灵巧手通信，控制灵巧手设备，以IP地址为唯一标识操作。

默认左手<192.168.137.39>

默认右手<192.168.137.19>

## 版本更新记录

|  版本号  |  日期  |  作者  |  更新内容  |  备注  |
| --- | --- | --- | --- | --- |
|  0.0.1  |  2025-03-06  |   |  初版  |   |

## 协议定义

## 接口描述

所有 DexHand 相关接口均封装在 FdHand 命名空间下。

提供python接口

提供c++接口

### Ret 枚举类

定义了枚举类 Ret，用于返回接口操作结果。

```c++
enum class Ret
{
    SUCCESS = 0,
    FAIL = -1,
    TIMEOUT = -2
};
```

### DexHand 接口类

#### init

初始化 DexHand 灵巧手设备，扫描已连接所有设备。

```c++
Ret init(int flg = 0);
```

##### 参数:

flg (int, 默认 0): 初始化标志，保留扩展。

##### 返回值:

Ret::SUCCESS: 成功 Ret::FAIL: 失败 Ret::TIMEOUT: 超时

#### get\_ip\_list

获取已连接设备的 IP 地址列表。一个IP地址对应一个灵巧手。

```c++
std::vector<std::string> get_ip_list();
```

##### 返回值:

ip 列表

#### get\_name

获取设备名称。 名称定义： Inspire：                   “FSH” DexHand-FDH6：    “fdhv1” DexHand-FDH12：  “fdhv2”

```c++
std::string get_name(std::string ip);
```

##### 参数:

ip (std::string): 目标设备 IP。

##### 返回值:

设备名称（字符串）。

#### get\_type

获取设备类型。 类型定义： Inspire：      “Hand” FDH6：        “FDH-6L”，“FDH-6R” FDH12：      “FDH-12L”，“FDH-12R”

```c++
std::string get_type(std::string ip);
```

##### 参数:

ip (std::string): 目标设备 IP。

##### 返回值:

设备类型（字符串）。

#### get\_driver\_ver

获取驱动固件版本号，格式：0.0.0.0

```c++
std::string get_driver_ver(std::string ip);
```

##### 参数:

ip (std::string): 目标设备 IP。

##### 返回值:

驱动版本号（字符串）。

#### get\_hardware\_ver

获取机械PCB版本号，格式：0.0.0.0

```c++
std::string get_hardware_ver(std::string ip);
```

##### 参数:

ip (std::string): 目标设备 IP。

##### 返回值:

硬件版本号（字符串）。

#### get\_errorcode

获取设备错误代码。一个vector数组，对应所有的错误码，具体错误码定义值参考错误码文档

```c++
std::vector<long> get_errorcode(std::string ip);
```

##### 参数:

ip (std::string): 目标设备 IP。

##### 返回值:

错误代码列表。

#### set\_pos

设置目标设备位置。6/12自由度长度列表。某个位置不控制写-1

6自由度对应位置和范围如下所示:

食指1：0-1

中指2：0-1

无名指3：0-1

小指4：0-1

拇指5-6: 0-1

![9307f54f11cf62aec0eaafa7c15dbca1.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/Lk3lb87vpPB7qm96/img/ced86988-6093-44c7-9a7a-9daba2cab154.png)

12自由度对应位置和范围如下图所示：

食指1-3：0-1750，0-1780，0-576

中指4-5：0-1750，0-1780

无名指6-7：0-1750， 0-1780

小指8-9：0-1750， 0-1780

拇指10-12：0-1700，0-1700，0-1700

![6619f2c6adfa7e33d0637ff93545d3b7.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/Lk3lb87vpPB7qm96/img/59960772-f358-418e-a791-9ecc25f5baed.png)

![afc2981d4548ea0f7088560f28568283.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/Lk3lb87vpPB7qm96/img/cebc09ef-8e92-4f1f-9401-7b306563e2ea.png)

```c++
Ret set_pos(std::string ip, std::vector<float> pos);
```

##### 参数:

ip (std::string): 目标设备 IP。 pos (std::vector<float>): 目标位置（浮点数列表）。

##### 返回值:

Ret::SUCCESS: 成功 Ret::FAIL: 失败

##### 参考示例

```c++
int main(int argc, char **argv)
{
    DexHand hand;

    Ret ret = hand.init();
    if (ret != Ret::SUCCESS)
    {
        std::cout << "[hand.init] init failed" << std::endl;
        return -1;
    }
    std::cout << "[hand.init] init success" << std::endl;

    std::vector<float> pos = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    std::vector<std::string> ip_list = hand.get_ip_list();
    for (auto &ip : ip_list)
    {
        Ret ret = dexHand.set_pos(ip, pos);
        if (ret != FdHand::Ret::SUCCESS)
        {
            std::cout << "设置位置失败" << std::endl;
        }
    }

    return 0;
}
```

#### fast\_set\_pos

快速设置目标设备位置。

```c++
Ret fast_set_pos(std::string ip, std::vector<float> pos);
```

##### 参数:

ip (std::string): 目标设备 IP。 pos (std::vector<float>): 目标位置（浮点数列表）。

##### 返回值:

Ret::SUCCESS: 成功 Ret::FAIL: 失败

#### get\_pos

获取目标设备当前位置。

```c++
std::vector<float> get_pos(std::string ip);
```

##### 参数:

ip (std::string): 目标设备 IP。

##### 返回值:

目标位置（浮点数列表），通信失败返回空列表。

#### clear\_errorcode

清除设备错误代码。

```c++
Ret clear_errorcode(std::string ip);
```

##### 参数:

ip (std::string): 目标设备 IP。

##### 返回值:

Ret::SUCCESS: 成功 Ret::FAIL: 失败

#### get\_ts\_matrix

获取传感器矩阵数据。

```c++
std::vector<std::vector<uint8_t>> get_ts_matrix(std::string ip);
```

##### 参数:

ip (std::string): 目标设备 IP。

##### 返回值:

传感器矩阵数据（二维向量），通信失败返回空列表。

#### set\_hand\_config

设置设备配置。

```c++
Ret set_hand_config(std::string ip, std::string config);
```

##### 参数:

ip (std::string): 目标设备 IP。 config (std::string): 设备配置（JSON 格式）。

##### 返回值:

Ret::SUCCESS: 成功 Ret::FAIL: 失败

#### get\_hand\_config

获取设备配置。

```c++
std::string get_hand_config(std::string ip);
```

##### 参数:

ip (std::string): 目标设备 IP。

##### 返回值:

设备配置（JSON 格式）。

config (std::string): JSON 格式的配置信息。 返回值: Ret::SUCCESS: 成功 Ret::FAIL: 失败

#### reboot

重启设备。

```c++
Ret reboot();
Ret reboot(std::string ip);
```

##### 参数:

ip (std::string, 可选): 目标设备 IP，不指定时重启所有设备。

##### 返回值:

Ret::SUCCESS: 成功 Ret::FAIL: 失败

#### enable

启用设备。

```c++
Ret enable();
Ret enable(std::string ip);
```

##### 参数:

ip (std::string, 可选): 目标设备 IP，不指定时启用所有设备。

##### 返回值:

Ret::SUCCESS: 成功 Ret::FAIL: 失败

#### disable

失能设备。

```c++
Ret disable();
Ret disable(std::string ip);
```

##### 参数:

ip (std::string, 可选): 目标设备 IP，不指定时失能所有设备。

##### 返回值:

Ret::SUCCESS: 成功 Ret::FAIL: 失败

#### calibration

设备自校准。

```c++
Ret calibration();
Ret calibration(std::string ip);
```

##### 参数:

ip (std::string, 可选): 目标设备 IP，不指定时校准所有设备。

##### 返回值:

Ret::SUCCESS: 成功 Ret::FAIL: 失败

## 接口支持列表

|  interface  |  inspire  |  fdh6  |  fdh12  |
| --- | --- | --- | --- |
|  init  |  √  |  √  |  √  |
|  get\_ip\_list  |  √  |  √  |  √  |
|  get\_name  |  √  |  √  |  √  |
|  get\_type  |  √  |  √  |  √  |
|  get\_driver\_ver  |  √  |  √  |  √  |
|  get\_hardware\_ver  |  √  |  √  |  √  |
|  get\_errorcode  |  √  |  √  |  √  |
|  set\_pos  |  √  |  √  |  √  |
|  get\_pos  |  √  |  √  |  √  |
|  fast\_set\_pos  |  √  |  √  |  √  |
|  clear\_errorcode  |  √  |  √  |  √  |
|  get\_ts\_matrix  |   |   |  √  |
|  get\_hand\_config  |  √  |  √  |  √  |
|  set\_hand\_config  |   |   |   |
|  reboot()  |   |  √  |   |
|  reboot(ip)  |   |  √  |   |
|  enable()  |   |  √  |  √  |
|  enable(ip)  |   |  √  |  √  |
|  disable()  |   |  √  |  √  |
|  disable(ip)  |   |  √  |  √  |
|  calibration()  |   |   |  √  |
|  calibration(ip)  |   |   |  √  |

## python参考示例

### 环境安装

conda 创建python环境

```shell
conda create -n pypitest python==3.10
conda activate pypitest
```

安装依赖库

```shell
# pybind11
pip install pybind11

# develop版本安装
pip install -i https://test.pypi.org/simple/ dexhandpy==0.0.36

# release 版本安装
pip install dexhandpy
```

conda list 查看库

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/1GXn4Bo3JGyQODQ4/img/517b3461-94b8-4776-94a6-1bed5e9f46b1.png)

### python接口调用示例

```python
import dexhandpy.fdexhand as fdh
import time

dh = fdh.DexHand()
result = fdh.Ret

# 初始化扫描设备
ret = dh.init()
if ret == result.SUCCESS:
    print("Successfully initialized DexHand")
else:
    print(f"Failed to initialize DexHand, error code {ret}")

# 获取设备ip列表
sers = dh.get_ip_list()
print(f"ser list: {sers}")

# 获取设备信息
for ser in sers:
    print(dh.get_name(ser))
    print(dh.get_type(ser))
    print(dh.get_driver_ver(ser))
    print(dh.get_hardware_ver(ser))

# 获取设备错误码
for ser in sers:
    err = dh.get_errorcode(ser)
    print(f"ip: {ser}, err: {err}")

# 设备校准
if dh.calibration() == result.SUCCESS:
    print("Calibrated successfully")
else:
    print("Failed to calibrate")

# 获取位置
for ser in sers:
    recv_pos = dh.get_pos(ser)
    print(f"{ser}: pos {recv_pos}")

# 设置位置
for ser in sers:
    m_name = dh.get_name(ser)
    send_pos = []
    if m_name == "fdhv2":
        send_pos = [0] * 12
    else:
        send_pos = [0] * 6
    
    ret = dh.set_pos(ser, send_pos)
    if ret != result.SUCCESS:
        print(f"{m_name}: failed to set pos {ser}")

# 清除错误码
for ser in sers:
    ret = dh.clear_errorcode(ser)
    if ret != result.SUCCESS:
        print(f"{ser}: failed to clear error")

# 获取触摸数据
for ser in sers:
    data = dh.get_ts_matrix(ser)
    print(f"tactile sensor data: {data}")

# 获取手配置信息
for ser in sers:
    data = dh.get_hand_config(ser)
    print(f"hand config: {data}")

# 使能
ret = dh.enable()
if ret != result.SUCCESS:
    print(f"failed to enable hand")

# 失能
ret = dh.disable()
if ret != result.SUCCESS:
    print(f"failed to disable hand")

# 重启设备
ret = dh.reboot()
if ret != result.SUCCESS:
    print(f"failed to reboot hand")

```

## c++参考示例

```c++
#include "dexhand.h"
using namespace FdHand;

int main()
{
    DexHand hand;
    /* 初始化 */
    Ret ret = hand.init();
    if (ret != Ret::SUCCESS)
    {
        std::cout << "[hand.init] init failed") << std::endl;
        return -1;
    }

    /* 获取ip列表 */
    std::vector<std::string> ip_list = hand.get_ip_list();
    std::cout << "[hand.get_ip_list] ip list size: " << ip_list.size() << std::endl;
    for (auto &ip : ip_list)
    {
        std::cout << ip << std::endl;
    }

    /* 校准 */
    ret = hand.calibration();
    if (ret != Ret::SUCCESS)
    {
        std::cout << "[hand.calibration] calibration failed" << std::endl;
    }

    std::string hand_config = "{\"method\":\"SET\",\"reqTarget\":\"/config\",\"property\":\"\",\"DHCP_enable\":false,\"static_IP\":[192, 168, 137, 39]}";
    for (std::string ip : ip_list)
    {
        hand.set_hand_config(ip, hand_config);
    }

    /* 获取错误码 */
    for (std::string ip : ip_list)
    {
        std::vector<long> err = hand.get_errorcode(ip);
        std::cout << "ip: " << ip << "  ";
        for (long e : err)
        {
            std::cout << e << "  ";
        }
    }

    std::vector<float> index_start = {0, -1, -1, -1, -1, -1};
    std::vector<float> index_end = {1000, -1, -1, -1, -1, -1};
    std::vector<float> middle_start = {-1, 0, -1, -1, -1, -1};
    std::vector<float> middle_end = {-1, 1000, -1, -1, -1, -1};
    std::vector<float> ring_start = {-1, -1, 0, -1, -1, -1};
    std::vector<float> ring_end = {-1, -1, 1000, -1, -1, -1};
    std::vector<float> little_start = {-1, -1, -1, 0, -1, -1};
    std::vector<float> little_end = {-1, -1, -1, 1000, -1, -1};
    std::vector<float> thumb_start = {-1, -1, -1, -1, 0, -1};
    std::vector<float> thumb_end = {-1, -1, -1, -1, 1000, -1};
    std::vector<float> roll_start = {-1, -1, -1, -1, -1, 0};
    std::vector<float> roll_end = {-1, -1, -1, -1, -1, 1000};

    std::vector<std::vector<float>> pos_list = {index_start, index_end, middle_start, middle_end, ring_start, ring_end, little_start, little_end, thumb_start, thumb_end, roll_start, roll_end};

    for (std::vector<float> pos : pos_list)
    {
        for (std::string ip : ip_list)
        {
            ret = hand.set_pos(ip, pos);
            if (ret != Ret::SUCCESS)
            {
                print_error("[hand.set_pos] set pos failed");
                return -1;
            }
        }
        usleep(400000);
    }

    /* 清除错误码 */
    for (std::string ip : ip_list)
    {
        Ret ret = hand.clear_errorcode(ip);
        if (ret != Ret::SUCCESS)
        {
            print_error("[hand.clear_errorcode] clear errorcode failed");
        }
    }

    /* 使能设备 */
    ret = hand.enable();
    if (ret != Ret::SUCCESS)
    {
        std::cout << "[hand.enable] enable failed" << std::endl;
    }
    /* 失能设备 */
    ret = hand.disable();
    if (ret != Ret::SUCCESS)
    {
        std::cout << "[hand.disable] disable failed" << std::endl;
    }

    /* 重启设备 */
    ret = hand.reboot();
    if (ret != Ret::SUCCESS)
    {
        std::cout << "[hand.reboot] reboot failed" << std::endl;
    }

    return 0;
}
```