# timeline-story

这是Timeline-story的一个分类仓库，专为使用 Flask 框架的web应用而设计的。

## 一、项目简介

### 1.1 关于毽球队（JQD）

### 1.2 关于Timeline.js

## 二、项目结构

python 3.11

## 三、项目部署

[部署服务器：Wispbype](https://wispbyte.com/client/dashboard)
&emsp;&ensp;&emsp13;
[访问地址](https://jqd.yuleague.cn)&emsp;&ensp;&emsp13;
解析：Cloudflare

入口文件：main.py

启动命令：

```
if [[ -d .git ]] && [[ "0" == "1" ]]; then git pull; fi; if [[ ! -z "" ]]; then pip install -U --prefix .local ; fi; if [[ -f /home/container/${REQUIREMENTS_FILE} ]]; then pip install -U --prefix .local -r ${REQUIREMENTS_FILE}; fi; /usr/local/bin/python /home/container/main.py
```

