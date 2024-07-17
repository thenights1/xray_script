## X-RAY+批量扫描+结果清洗+发送webhook

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/requests)

> 项目简介：基于python实现的xray脚本批量扫描+结果清洗+多个url合并到同一个html+通过webhook同步到飞书群😊
> 
> ✅xray批量扫描
> 
> ✅初步清洗漏扫结果，减少人力成本
> 
> ✅多个url仅生成一个html报告
> 
> ✅一键以表格格式发送到飞书机器人
> 
> ❌和资产测绘结合进行自动化漏扫（后续上新）

#### 项目背景

由于xray并不开源，无法直接在其源代码上进行更改来实现一些个性化的定制。而又由于生产环境的区别导致必须进行一些定制化的调整，并且xray误报率较高和没有危害性的漏洞报的较多，需要进行筛选减少人力成本，所以便有了这个项目。

#### 文件结构

- bat.py:  项目运行入口

- feishu.py:  发送到飞书相关的函数文件

- clean.py: 对xray结果进行筛选清洗

#### 快速开始

**使用环境**：

需要将项目里面的五个文件都放在xray脚本目录下，即可运行使用。

使用环境默认为linux，win需要自行更改脚本中相关的部分。

其中url.txt存放需要批量扫描的网址。

**运行**：

在xray的文件夹下使用命令：

```shell
python3 bat.py -o 711 -html 711
```

即可跑起来脚本，也可通过文末的定时启动shell来进行运行，建议用shell来运行。

其-o后的参数为json文件存储的文件夹，默认在当前路径下建立711文件夹

-html后的参数为合成的html文件的名字，即会生成711.html文件，具体路径在脚本中我是直接输出到了网站后端的目录，如果在其他环境中需要**自行更改**

#### 关于筛选标准

这里我用到的筛选标准如下：

位于clean.py文件夹下：

![](https://blogkkk-1319553185.cos.ap-shanghai.myqcloud.com/img/20240711143822.png)

只针对一些可能造成危害的漏洞方向来进行筛选。

#### 关于高危和中危判断标准：

位于feishu.py文件中，这里我只将含有poc和cmd注入的当作高危漏洞，其余当做中危，低危暂时忽略。

![](https://blogkkk-1319553185.cos.ap-shanghai.myqcloud.com/img/20240711144038.png)

#### 定期扫描配置

```shell
设置每两天晚上九点开始，凌晨三点结束任务
#!/bin/bash

cd /your_xray_path

# Generate filename with date

FILENAME="output_$(date +'%Y%m%d')"

# Run the Python script with the generated filename as argument, in the background

python3 /your_xray_path/bat.py -o "$FILENAME" -html "$FILENAME" &

# Capture the PID of the background process

PID=$!

# Save the PID to a file

echo $PID > /tmp/my_script.pid

# Wait until tomorrow 3:00 AM

sleep $((24 * 60 * 60 - $(date +%s) + $(date -d '03:00 tomorrow' +%s)))

# Check if the process is still running and kill it if necessary

if ps -p $PID > /dev/null; then
    echo "Killing process $PID"
    kill $PID
    pkill xray
fi

```

后续通过

crontab -e 即可设置定时命令，填入如下信息即可,即可实现每隔两天扫描一次，晚上九点开始扫描，凌晨三点还未结束就kill进程，保证不影响业务需求。

```shell
0 21 */2 * * /your_path/run_script.sh
```