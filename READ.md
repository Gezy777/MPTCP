# MPTCP-Vagrant 详细说明文档

## 目录
1. [项目概述](#项目概述)
2. [项目架构](#项目架构)
3. [文件结构说明](#文件结构说明)
4. [核心功能分析](#核心功能分析)
5. [使用流程](#使用流程)
6. [技术实现细节](#技术实现细节)
7. [MPTCP Hello 示例代码](#mptcp-hello-示例代码)
8. [网络拓扑](#网络拓扑)

---

## 项目概述

**mptcp-vagrant** 是一个用于测试 Multipath TCP (MPTCP) 的 Vagrant 虚拟机环境配置项目。它帮助用户在虚拟环境中搭建 MPTCP 测试平台，无需宿主机支持 MPTCP。

### 主要特点
- 自动创建两台 Fedora 虚拟机（client 和 server）
- 每台虚拟机配置 3 个独立的网络连接
- 自动配置 MPTCP 协议栈
- 包含多语言 MPTCP 使用示例代码

### 适用场景
- MPTCP 协议学习和实验
- MPTCP 应用程序开发和测试
- 网络多路径传输研究
- 无需物理多网卡环境的 MPTCP 测试

---

## 项目架构

```
mptcp-vagrant/
├── Vagrantfile              # Vagrant 虚拟机配置文件
├── README.md                # 项目说明文档
├── .gitmodules              # Git 子模块配置
├── .gitignore               # Git 忽略文件配置
├── scripts/                 # 脚本目录
│   ├── init.sh             # 初始化脚本：安装必要软件
│   └── init-mptcp.sh       # MPTCP 配置脚本
└── mptcp-hello/            # Git 子模块：MPTCP 示例代码
    ├── c/                  # C 语言示例
    ├── python/             # Python 示例
    ├── perl/               # Perl 示例
    ├── rust/               # Rust 示例
    ├── swift/              # Swift 示例
    └── objective-c/        # Objective-C 示例
```

---

## 文件结构说明

### 1. Vagrantfile
虚拟机配置的核心文件，定义了虚拟机的硬件规格、网络配置和操作系统版本。

**关键配置项：**

| 配置项 | 值 | 说明 |
|--------|-----|------|
| BOX_NAME | generic/fedora41 | 使用 Fedora 41 作为基础镜像 |
| 内存 | 2048 MB | 每台虚拟机分配 2GB 内存 |
| CPU | 2 核 | 每台虚拟机分配 2 个 CPU 核心 |

**虚拟机定义：**
- **client 虚拟机**：主机名为 `client`
- **server 虚拟机**：主机名为 `server`

### 2. scripts/init.sh
虚拟机初始化脚本，在虚拟机启动时自动执行。

**安装的软件包：**
```bash
sudo yum -y install pcp-zeroconf mptcpd iperf3 nc
sudo dnf -y install nginx
```

| 软件包 | 用途 |
|--------|------|
| pcp-zeroconf | 性能监控工具，用于监控网络流量 |
| mptcpd | MPTCP 守护进程 |
| iperf3 | 网络性能测试工具 |
| nc (netcat) | 网络调试工具 |
| nginx | Web 服务器，可用于测试 HTTP 请求 |

### 3. scripts/init-mptcp.sh
MPTCP 协议配置脚本，需要在 `vagrant up` 完成后手动执行。

**执行流程：**

#### Client 虚拟机配置
```bash
# 手动配置 IP 地址（防止 VirtualBox 未自动分配）
sudo ip addr add 192.168.56.100/24 dev eth1
sudo ip addr add 192.168.57.100/24 dev eth2
sudo ip addr add 192.168.58.100/24 dev eth3

# 启用 MPTCP
sudo sysctl net.mptcp.enabled=1

# 配置 MPTCP 限制
sudo ip mptcp limits set subflow 8
sudo ip mptcp limits set add_addr_accepted 8

# 添加 MPTCP 端点（子流模式）
sudo ip mptcp endpoint add 192.168.57.100 dev eth2 subflow
sudo ip mptcp endpoint add 192.168.58.100 dev eth3 subflow
```

#### Server 虚拟机配置
```bash
# 手动配置 IP 地址
sudo ip addr add 192.168.56.101/24 dev eth1
sudo ip addr add 192.168.57.101/24 dev eth2
sudo ip addr add 192.168.58.101/24 dev eth3

# 启用 MPTCP
sudo sysctl net.mptcp.enabled=1

# 配置 MPTCP 限制
sudo ip mptcp limits set subflow 8

# 添加 MPTCP 端点（信号模式）
sudo ip mptcp endpoint add 192.168.57.101 dev eth2 signal
sudo ip mptcp endpoint add 192.168.58.101 dev eth3 signal
```

**MPTCP 端点模式说明：**
- **subflow**：子流模式，主动创建额外的子流
- **signal**：信号模式，通过 MP_JOIN 消息通知对端创建子流

---

## 核心功能分析

### 1. 虚拟机网络配置

项目为每台虚拟机配置了 3 个私有网络接口：

| 网卡 | Client IP | Server IP | 网段 |
|------|-----------|-----------|------|
| eth1 | 192.168.56.100 | 192.168.56.101 | 192.168.56.0/24 |
| eth2 | 192.168.57.100 | 192.168.57.101 | 192.168.57.0/24 |
| eth3 | 192.168.58.100 | 192.168.58.101 | 192.168.58.0/24 |

这种设计模拟了拥有 3 条独立网络路径的场景，是测试 MPTCP 多路径传输的理想环境。

### 2. MPTCP 配置详解

#### sysctl 参数
```bash
net.mptcp.enabled=1
```
此参数启用内核的 MPTCP 支持。设置为 0 将禁用 MPTCP。

#### mptcp limits 命令
```bash
sudo ip mptcp limits set subflow 8
sudo ip mptcp limits set add_addr_accepted 8
```

| 参数 | 含义 |
|------|------|
| subflow | 最大子流数量 |
| add_addr_accepted | 可接受的添加地址数量 |

设置为 8 允许每个 MPTCP 连接最多创建 8 个子流。

#### mptcp endpoint 命令
```bash
sudo ip mptcp endpoint add <IP> dev <网卡> <模式>
```

此命令将指定的 IP 地址和网卡添加为 MPTCP 端点，使其可用于多路径传输。

---

## 使用流程

### 环境要求
- VirtualBox（https://www.virtualbox.org/wiki/Downloads）
- Vagrant（http://www.vagrantup.com/downloads.html）
- Git

### 快速开始

1. **克隆项目**
   ```bash
   git clone https://github.com/multipath-tcp/mptcp-vagrant.git
   cd mptcp-vagrant
   ```

2. **初始化子模块**
   ```bash
   git submodule update --init --recursive
   ```

3. **启动虚拟机**
   ```bash
   vagrant up
   ```
   此命令将：
   - 下载 Fedora 41 镜像
   - 创建并启动 client 和 server 虚拟机
   - 执行 init.sh 脚本安装必要软件

4. **配置 MPTCP**
   ```bash
   ./scripts/init-mptcp.sh
   ```

5. **连接到虚拟机**
   ```bash
   vagrant ssh client   # 连接到 client 虚拟机
   vagrant ssh server   # 连接到 server 虚拟机
   ```

6. **停止虚拟机**
   ```bash
   vagrant halt
   ```

### 验证 MPTCP 配置

在虚拟机中执行以下命令验证 MPTCP 是否正常工作：

```bash
# 检查 MPTCP 是否启用
cat /proc/sys/net/mptcp/enabled

# 查看 MPTCP 端点
ip mptcp endpoint show

# 查看 MPTCP 统计信息
ip mptcp stats show
```

---

## 技术实现细节

### MPTCP 工作原理

MPTCP (Multipath TCP) 是 TCP 的扩展协议（RFC 8684），允许单个 TCP 连接同时使用多条网络路径。

**关键特性：**
1. **透明性**：对应用层完全透明，无需修改应用程序
2. **协商机制**：在 TCP 三次握手时协商是否使用 MPTCP
3. **向后兼容**：如果一方不支持 MPTCP，会自动降级为普通 TCP

**连接建立过程：**
```
Client                          Server
  |                               |
  |------- SYN + MP_CAPABLE ----->|
  |                               |
  |<---- SYN-ACK + MP_CAPABLE ----|
  |                               |
  |----------- ACK -------------->|
  |                               |
  (MPTCP 连接建立完成)
  |                               |
  |------- MP_JOIN (eth2) ------> |  添加子流 1
  |------- MP_JOIN (eth3) ------> |  添加子流 2
  |                               |
```

### 网络流量监控

使用 `pmrep` 工具监控各网卡流量：

```bash
# 每秒采样一次，持续 10 秒
pmrep network.interface.in.bytes -t 1 -s 10
```

**示例输出：**
```
  n.i.i.bytes  n.i.i.bytes  n.i.i.bytes  n.i.i.bytes  n.i.i.bytes
           lo         eth0         eth1         eth2         eth3
       byte/s       byte/s       byte/s       byte/s       byte/s
        0.000        0.000    64017.342    46963.665    46195.048
```

当 MPTCP 正常工作时，可以看到 eth1、eth2、eth3 同时有数据传输。

---

## 网络拓扑

```
┌─────────────────────────────────────────────────────────────┐
│                        Host 物理机                            │
│                                                               │
│  ┌─────────────────────┐      ┌─────────────────────┐       │
│  │    Client VM        │      │    Server VM        │       │
│  │   (Fedora 41)       │      │   (Fedora 41)       │       │
│  │                     │      │                     │       │
│  │  eth1: 192.168.56.100│◄────┤ eth1: 192.168.56.101│       │
│  │                     │      │                     │       │
│  │  eth2: 192.168.57.100│◄────┤ eth2: 192.168.57.101│       │
│  │                     │      │                     │       │
│  │  eth3: 192.168.58.100│◄────┤ eth3: 192.168.58.101│       │
│  │                     │      │                     │       │
│  │  MPTCP Enabled      │      │  MPTCP Enabled      │       │
│  └─────────────────────┘      └─────────────────────┘       │
│         ▲                            ▲                      │
│         └──────────── 3 条独立网络路径 ─────────────┘        │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## MPTCP Hello 示例代码

mptcp-hello 子模块提供了多种编程语言使用 MPTCP 的示例。

### C 语言示例 (Linux)

**核心代码：**
```c
#ifndef IPPROTO_MPTCP
#define IPPROTO_MPTCP 262
#endif

int s = socket(AF_INET, SOCK_STREAM, IPPROTO_MPTCP);
```

**关键点：**
- 使用 `IPPROTO_MPTCP` (协议号 262) 替代 `IPPROTO_TCP`
- 如果创建失败，自动降级为普通 TCP

### Python 示例

**核心代码：**
```python
import socket
import errno

IPPROTO_MPTCP = 262  # 或使用 socket.IPPROTO_MPTCP (Python 3.10+)

def create_socket(sockaf):
    try:
        return socket.socket(sockaf, socket.SOCK_STREAM, IPPROTO_MPTCP)
    except OSError as e:
        if e.errno in (errno.ENOPROTOOPT, errno.EPROTONOSUPPORT, errno.EINVAL):
            return socket.socket(sockaf, socket.SOCK_STREAM, socket.IPPROTO_TCP)

# 使用示例
s = create_socket(socket.AF_INET)
s.connect(("test.multipath-tcp.org", 80))
```

### 其他语言支持

| 语言 | 说明 |
|------|------|
| Perl | 使用 Socket 模块，设置 IPPROTO_MPTCP |
| Rust | 使用 socket2 库或标准库 |
| Swift (macOS/iOS) | 使用 NSURLSession 配置 Multipath Service |
| Objective-C (iOS) | 配置 NSURLSession 的 multipathServiceType |

### mptcpize 工具

对于没有源代码访问权限的应用，可以使用 `mptcpize` 工具：

```bash
mptcpize run iperf3 -s  # 以 MPTCP 模式运行 iperf3 服务器
```

`mptcpize` 通过 `LD_PRELOAD` 机制拦截 `socket()` 系统调用，将 TCP socket 自动转换为 MPTCP socket。

---

## 测试建议

### 1. 基本连通性测试

```bash
# 在 client 虚拟机
ping -c 3 192.168.56.101  # 测试 eth1
ping -c 3 192.168.57.101  # 测试 eth2
ping -c 3 192.168.58.101  # 测试 eth3
```

### 2. MPTCP 性能测试

```bash
# 在 server 虚拟机启动 iperf3 服务器
mptcpize run iperf3 -s

# 在 client 虚拟机启动 iperf3 客户端
mptcpize run iperf3 -c 192.168.56.101

# 同时监控流量
pmrep network.interface.in.bytes -t 1 -s 10
```

### 3. Web 服务器测试

```bash
# 在 server 虚拟机启动 nginx
sudo systemctl start nginx

# 在 client 虚拟机使用 mptcpize 访问
mptcpize run curl http://192.168.56.101
```

---

## 常见问题

### Q1: 虚拟机启动后无法获取 IP 地址
**A:** 执行 `./scripts/init-mptcp.sh` 会手动配置 IP 地址

### Q2: MPTCP 连接降级为普通 TCP
**A:** 确保两台虚拟机都执行了 `init-mptcp.sh` 脚本

### Q3: 如何查看 MPTCP 是否生效
**A:** 使用 `ss -tin` 命令查看连接，MPTCP 连接会显示 `mptcp` 标志

---

## 参考资源

- [MPTCP RFC 8684](https://www.rfc-editor.org/rfc/rfc8684.html)
- [MPTCP 官方网站](https://mptcp.dev)
- [Linux Kernel MPTCP Wiki](https://github.com/multipath-tcp/mptcp_net-next/wiki)
- [mptcp-upstream-virtme-docker](https://github.com/multipath-tcp/mptcp-upstream-virtme-docker) - 适合内核开发者

---

## 总结

mptcp-vagrant 项目提供了一个完整的 MPTCP 测试环境：

1. **自动化部署**：通过 Vagrant 自动创建和配置虚拟机
2. **多路径模拟**：3 个独立网卡模拟真实多路径环境
3. **示例丰富**：包含多种编程语言的 MPTCP 使用示例
4. **易于使用**：简单的命令即可完成环境搭建

该项目是学习、研究和开发 MPTCP 应用的理想起点。
