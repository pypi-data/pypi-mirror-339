# slock

`slock` 是一个用于简化并发控制的 Python 库，提供基于键的粒度锁管理。它利用 `BaseKey` 类为不同的键创建独立的锁，确保线程安全。通过上下文管理器
`lock`，可以轻松地在多线程环境中控制资源的访问。

## 特性

- **基于键的粒度锁管理**：为不同的键创建独立锁，避免资源竞争。
- **线程安全**：确保在多线程环境下对资源的安全访问。
- **简单易用**：通过上下文管理器 `lock`，无需显式管理锁的获取和释放。
- **高效**：使用 `WeakValueDictionary` 来存储锁，避免内存泄漏。

## 安装

通过 `pip` 安装：

```bash
pip install slock
```

# 使用示例
## 简单示例
```python
from slock import BaseKey, lock


# 自定义键
class MyKey(BaseKey):
    """
    使用类和初始化时的 key 作为锁的唯一标识。
    当类和 key 完全相同时，线程会等待锁释放才能继续执行。
    类名和 key 的组合用于生成锁的标识符，不涉及引用关系，主要用于区分不同资源。
    """
    pass


# 创建一个键对象
my_key = MyKey(key="resource_1") #key 用于唯一标识一个资源。它是锁的最小单元，可以为空，默认情况下 key 为 None，此时锁的标识由类名生成。

# 使用锁来同步访问资源
with lock(my_key):
    # 你的并发操作代码
    print("Accessing resource_1 safely")
```

## 使用 slock 解决竞争
```python
from slock import BaseKey, lock
import threading


# 定义资源键
class ResourceKey(BaseKey):
    """
    使用类和初始化时的 key 作为锁的唯一标识。
    当类和 key 完全相同时，线程会等待锁释放才能继续执行。
    类名和 key 的组合用于生成锁的标识符，不涉及引用关系，主要用于区分不同资源。
    """
    pass

# 共享资源
shared_resource = 0


# 模拟线程安全的资源增加
def increment():
    global shared_resource
    with lock(ResourceKey("shared_resource")):  # 创建资源键 使用锁避免竞争
        shared_resource += 1

# 存储线程
threads: list[threading] = []

# 创建并启动多个线程
for i in range(10000):
    thread: threading = threading.Thread(target=increment)
    thread.start()
    threads.append(thread)

# 等待所有线程完成
for thread in threads:
    thread.join()

# 输出最终的结果
print(f"最终共享资源的值：{shared_resource}")
```
# 使用async
```python
from slock.async_lock import lock, get_lock
```