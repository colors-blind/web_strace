# Strace Web 可视化平台需求文档

## 1. 项目目标

实现一个基于 `strace` 的实时 Web 可视化工具。

用户在运行：

```bash
strace your_program
```

时，系统能够：

- 自动采集 `strace` 输出
- 实时分析系统调用
- 统计调用耗时
- 标记潜在卡顿点
- 按 syscall 类型分类（IO / 网络 / 文件 / 进程 / 内存 等）
- 在 Web 页面中动态展示
- 支持实时刷新与历史查看

目标是让 `strace` 从：

```text
一堆难读的文本
```

变成：

```text
可观测、可分析、可定位问题的系统调用时间线
```

---

# 2. 使用场景

## 场景 1：定位程序卡顿

例如：

```bash
python app.py
```

发现程序偶尔卡住。

通过：

```bash
strace-web python app.py
```

可以看到：

| 时间 | syscall | 耗时 | 状态 |
|---|---|---|---|
| 12:01:22 | futex | 2.3s | ⚠️ 阻塞 |
| 12:01:25 | read | 1.8s | ⚠️ IO等待 |

快速发现：

- 锁竞争
- IO阻塞
- 网络超时

---

## 场景 2：分析启动慢

查看：

- 哪个文件打开最慢
- DNS 是否慢
- socket connect 是否超时
- 动态库加载耗时

---

## 场景 3：学习 Linux syscall

Web 页面可以：

- 对 syscall 分类
- 显示说明
- 高亮关键参数

适合学习：

- Linux
- 操作系统
- 性能分析

---

# 3. 核心功能

## 3.1 实时采集 strace 输出

### 支持命令

```bash
strace -tt -T -f
```

建议默认参数：

| 参数 | 含义 |
|---|---|
| -tt | 显示时间 |
| -T | 显示 syscall 耗时 |
| -f | 跟踪子进程 |

---

## 输入来源

支持：

### 方式 1：直接运行

```bash
strace-web python app.py
```

工具内部：

```bash
strace -tt -T -f python app.py
```

---

### 方式 2：附加进程

```bash
strace-web -p 1234
```

---

# 3.2 syscall 实时解析

## 示例输入

```text
12:00:01.123456 read(3, "...", 4096) = 1024 <0.000123>
```

解析结果：

```json
{
  "timestamp": "12:00:01.123456",
  "syscall": "read",
  "fd": 3,
  "duration": 0.000123,
  "result": 1024,
  "category": "io"
}
```

---

# 3.3 syscall 分类系统

## 分类目标

不同 syscall 使用不同颜色与图标。

---

## 分类示例

| 类型 | syscall |
|---|---|
| 文件 | open, close, stat |
| IO | read, write |
| 网络 | socket, connect, recvfrom |
| 进程 | fork, clone, execve |
| 内存 | mmap, brk |
| 同步 | futex, epoll_wait |
| 信号 | sigaction, kill |

---

## UI 示例

| syscall | 类型 | UI |
|---|---|---|
| read | IO | 蓝色 |
| connect | 网络 | 绿色 |
| futex | 同步 | 红色 |
| mmap | 内存 | 紫色 |

---

# 3.4 耗时分析

## 核心功能

统计 syscall 耗时：

```text
read -> 0.1ms
connect -> 3.2s
futex -> 5.1s
```

---

## 高耗时标记

可配置阈值：

| 阈值 | 行为 |
|---|---|
| >10ms | 黄色 |
| >100ms | 橙色 |
| >1s | 红色报警 |

---

## 卡顿检测

自动识别：

| 场景 | 判断 |
|---|---|
| futex 长时间 | 锁竞争 |
| read 很慢 | IO阻塞 |
| connect 超时 | 网络问题 |
| epoll_wait 长时间 | 空闲等待 |
| wait4 长时间 | 子进程等待 |

---

# 3.5 时间线视图（重点）

## 页面核心

类似：

```text
Chrome Trace
Perfetto
Jaeger
```

的 Timeline。

---

## 展示形式

```text
时间 →
|---- read ----|
      |--------------- futex ---------------|
                    |- write -|
```

---

## 支持

- 横向缩放
- 按线程查看
- 按 syscall 类型过滤
- hover 查看参数
- 点击查看详情

---

# 3.6 线程/进程视图

## 多线程支持

支持：

```bash
strace -f
```

展示：

```text
PID/TID
```

分组。

---

## 示例

```text
Thread 1001
  read
  write

Thread 1002
  futex
  epoll_wait
```

---

# 3.7 统计分析面板

## syscall TOP

| syscall | 次数 | 总耗时 |
|---|---|---|
| read | 10234 | 3.2s |
| futex | 345 | 12s |

---

## 分类统计

| 类型 | 占比 |
|---|---|
| IO | 35% |
| 网络 | 20% |
| 锁等待 | 40% |

---

## 慢调用排行

```text
Top Slow Syscalls
```

---

# 3.8 搜索与过滤

支持：

- 搜 syscall 名称
- 搜 PID
- 搜 FD
- 搜耗时范围

---

## 示例

```text
duration > 1s
```

---

# 3.9 历史记录

支持：

- 保存 trace session
- 导出 JSON
- 导出 HTML 报告

---

# 4. Web 前端设计

## 4.1 页面布局

### 左侧

过滤器：

- syscall 类型
- PID
- 时间范围

---

### 中间

Timeline 主视图。

---

### 右侧

详情面板：

- syscall 参数
- 耗时
- 调用结果
- 关联 fd/socket

---

# 4.2 实时刷新

推荐：

- WebSocket
- SSE

实时推送 syscall。

---

# 4.3 UI 风格

建议：

- 深色主题
- 类似 VSCode / Perfetto

---

## syscall 类型颜色

| 类型 | 颜色 |
|---|---|
| IO | 蓝 |
| 网络 | 绿 |
| 锁等待 | 红 |
| 内存 | 紫 |
| 文件 | 黄 |

---

# 5. 后端架构

## 5.1 数据流

```text
strace
   ↓
Parser
   ↓
Event Queue
   ↓
Analyzer
   ↓
WebSocket
   ↓
Frontend Timeline
```

---

# 5.2 Parser

建议：

- Rust
- Python
- Go

---

## 推荐原因

### Rust

适合：

- 高性能
- 流式解析
- 并发

### Python

适合：

- 快速原型
- regex 解析

---

# 5.3 Analyzer

负责：

- syscall 分类
- 卡顿检测
- 耗时聚合
- 统计

---

# 5.4 存储

可选：

| 存储 | 用途 |
|---|---|
| SQLite | 小型历史 |
| ClickHouse | 大规模 trace |
| JSON 文件 | 简单导出 |

---

# 6. 技术方案建议

## 前端

### 推荐

| 技术 | 原因 |
|---|---|
| React | 组件化 |
| Tailwind | 快速 UI |
| ECharts | 图表 |
| Canvas/WebGL | Timeline 高性能渲染 |

---

# 后端

## 推荐方案 1（简单）

```text
Python + FastAPI
```

适合：

- MVP
- 快速开发

---

## 推荐方案 2（高性能）

```text
Rust + Axum
```

适合：

- 实时大规模 trace
- 多线程

---

# 7. MVP（第一阶段）

建议先做：

## 必做

- strace 输出解析
- WebSocket 实时推送
- syscall 分类
- 耗时显示
- Timeline 页面

---

## 先不做

- AI 分析
- FlameGraph
- eBPF
- 分布式 trace

---

# 8. 后续扩展

## 8.1 eBPF 替代 strace

未来可：

```text
strace -> eBPF
```

优势：

- 更低开销
- 内核级追踪
- 更高吞吐

---

# 8.2 AI 分析

自动生成：

```text
程序主要阻塞在 futex
怀疑线程锁竞争
```

---

# 8.3 FlameGraph

生成：

- syscall flamegraph
- wait flamegraph

---

# 8.4 Chrome Trace 导出

导出：

```json
trace_event_format.json
```

直接导入：

- Perfetto
- Chrome Trace Viewer

---

# 9. 技术难点

## 难点 1：strace 输出不稳定

不同 Linux 版本：

- 输出格式不同
- syscall 参数不同

需要：

- 强健 parser

---

## 难点 2：高吞吐

高频 syscall：

```text
read/write
```

可能：

- 每秒几十万条

需要：

- 流式处理
- ring buffer
- 批量传输

---

## 难点 3：Timeline 渲染

大量事件：

- DOM 会卡

需要：

- Canvas
- WebGL

---

# 10. 最终目标

最终形成：

```text
Linux syscall observability platform
```

类似：

- Wireshark（网络）
- Jaeger（trace）
- Perfetto（性能）

但目标对象是：

```text
Linux syscall
```

