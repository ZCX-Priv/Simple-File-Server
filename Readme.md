# 文件服务器

这是一个简单的文件服务器项目，允许用户通过HTTP协议访问和下载服务器上的文件。

## 项目结构

```
file-server/
├── run.bat         # Windows批处理文件，用于启动服务器
├── server/         # 服务器代码目录
│   └── server.py   # 主服务器Python脚本
└── README.md       # 项目说明文档
```

## 功能特点

- 提供基于HTTP的文件访问服务
- 支持文件浏览和下载
- 简单易用的部署方式

## 快速开始

### 前提条件

- Python 3.6+
- 确保已安装所需的Python依赖包

### 运行服务器

在Windows系统上，只需双击`run.bat`文件或在命令行中执行：

```bash
run.bat
```

或者直接运行Python脚本：

```bash
python server/server.py
```

### 访问服务器

服务器启动后，打开浏览器并访问：

```
http://localhost
```

## 配置

可以在`server.py`文件中修改以下配置：

- 端口号
- 服务目录
- 其他服务器参数

## 许可证

[MIT](LICENSE)
