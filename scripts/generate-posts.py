#!/usr/bin/env python3
"""Generate blog posts to reach 40 articles total (skips existing slugs)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docs" / "posts"

POSTS = [
    # ── 技术 · Flutter / Dart (6) ──
    {
        "cat": "技术",
        "slug": "flutter-ffi-c-interop",
        "title": "Flutter FFI 与 C 互操作：从 dlopen 到内存所有权",
        "date": "2025-02-14",
        "tags": ["Flutter", "FFI", "Dart"],
        "excerpt": "梳理 Dart FFI 调用 C 库时符号加载、结构体布局与指针生命周期的常见陷阱。",
        "body": r"""
# Flutter FFI 与 C 互操作

移动与桌面场景常需复用既有 C/C++ 能力：编解码、传感器 SDK、游戏引擎碎片。Dart 2.12+ 的 `dart:ffi` 提供稳定 ABI，但**所有权**与**线程**仍是事故高发区。

## 最小可用示例

```dart
import 'dart:ffi';
import 'dart:io';

typedef NativeAdd = Int32 Function(Int32 a, Int32 b);
typedef DartAdd = int Function(int a, int b);

void main() {
  final lib = DynamicLibrary.open(Platform.isMacOS ? 'libadd.dylib' : 'libadd.so');
  final add = lib.lookupFunction<NativeAdd, DartAdd>('add');
  print(add(2, 40));
}
```

## 结构体与内存对齐

C 侧 `struct SensorFrame` 的 padding 必须与 Dart `@Packed` / 字段顺序一致。建议用 `ffigen` 从头文件生成绑定，避免手写偏移错误。

## 回调与 Isolate

C 回调若跨线程触发 Dart 代码，应通过 `NativePort` 或把结果投递回主 Isolate。切勿在回调里直接操作 Flutter Widget 树。

## 实践建议

1. 用 `Arena` 批量分配、统一 `release`。
2. 为每个 native 句柄建立 Dart 侧 `Finalizer`。
3. 在 CI 里对 Android/iOS/macOS 三端做 smoke test。

FFI 不是银弹，但用好它能让 Flutter 真正「全栈到原生边界」。
""",
    },
    {
        "cat": "技术",
        "slug": "flutter-isolates-concurrency",
        "title": "Flutter Isolate：并发模型与消息传递实战",
        "date": "2025-03-02",
        "tags": ["Flutter", "Dart", "并发"],
        "excerpt": "对比 Isolate 与线程池思维，说明 compute、ReceivePort 与后台解析大 JSON 的模式。",
        "body": r"""
# Flutter Isolate 实战

Dart 单线程事件循环保证 UI 顺滑，CPU 密集任务必须 offload。

## compute 与 Isolate.run

```dart
final parsed = await Isolate.run(() => heavyParse(bytes));
```

Flutter 3.7+ 推荐 `Isolate.run` 替代部分 `compute` 场景，语义更清晰。

## 双向通信

```dart
final port = ReceivePort();
await Isolate.spawn(worker, port.sendPort);
port.listen((msg) => print(msg));
```

复杂流水线可引入 `IsolateNameServer` 做注册发现。

## 常见误区

- 试图在 Isolate 间共享可变对象（应序列化消息）。
- 在 UI Isolate 做图像解码（用 `decodeImageFromList` 仍可能卡帧，应后台化）。

Isolate 是「无共享内存的 actor」——理解这一点，并发设计会简单很多。
""",
    },
    {
        "cat": "技术",
        "slug": "flutter-riverpod-architecture",
        "title": "Riverpod 2.x：依赖注入与 UI 解耦架构笔记",
        "date": "2025-03-18",
        "tags": ["Flutter", "Riverpod", "架构"],
        "excerpt": "用 Provider 组合替代 InheritedWidget 泥球，讨论 AsyncNotifier 与 family 参数化。",
        "body": r"""
# Riverpod 架构笔记

`flutter_riverpod` 把状态提升为可测试的图结构，而不是散落在 Widget 树里。

## 核心概念

```dart
@riverpod
Future<User> user(UserRef ref, String id) async {
  return ref.watch(apiProvider).fetchUser(id);
}
```

`ref.watch` 建立依赖；`ref.listen` 处理副作用；`ref.read` 仅用于一次性动作（如按钮 onPressed）。

## 与 Repository 分层

- **Presentation**: ConsumerWidget
- **Application**: Notifier / AsyncNotifier
- **Data**: Repository + DataSource

测试时用 `ProviderContainer(overrides: [...])` 注入假实现，无需 pump 整棵 Widget 树。

## 反模式

全局 `read` 触发刷新却不 `watch`，导致 UI 不更新；在 `build` 里 `read` 网络请求。

Riverpod 强迫你把数据流画清楚——这正是中大型 Flutter 项目需要的纪律。
""",
    },
    {
        "cat": "技术",
        "slug": "flutter-impeller-skia",
        "title": "Impeller 渲染管线：Flutter 图形栈的一次重构",
        "date": "2025-04-05",
        "tags": ["Flutter", "渲染", "Impeller"],
        "excerpt": "简述 Impeller 相对 Skia 在着色器预编译、光栅化与 jank 上的取舍。",
        "body": r"""
# Impeller 与 Skia

Impeller 是 Flutter 为降低**首帧着色器编译卡顿**而引入的渲染后端，尤其针对 Vulkan/Metal。

## 设计动机

Skia 运行时 JIT 着色器在移动端可能造成「神秘掉帧」。Impeller 倾向**离线生成**管线状态对象（PSO），把不确定性前移。

## 对开发者的影响

- 自定义 `FragmentProgram` 仍可用，但需关注后端差异。
- 复杂 Path 与模糊效果在旧设备上应做性能 profiling。

## 调试手段

`flutter run --enable-impeller`（平台默认策略随版本变）配合 DevTools Performance 观察 GPU 线程。

渲染栈变迁说明：Flutter 不只是在写 Widget，而是在经营一条跨平台的 GPU 流水线。
""",
    },
    {
        "cat": "技术",
        "slug": "flutter-widget-rebuild-performance",
        "title": "Widget 重建优化：从 RepaintBoundary 到 ListView 懒加载",
        "date": "2025-04-22",
        "tags": ["Flutter", "性能"],
        "excerpt": "用 Profile 模式定位 rebuild 热点，总结 const、Key 与 itemExtent 策略。",
        "body": r"""
# Widget 重建优化

## 诊断流程

1. `flutter run --profile`
2. DevTools → Performance → 「Track rebuilds」
3. 观察 `build` 次数是否随父节点频繁刷新而飙升

## 手段清单

| 手段 | 场景 |
|------|------|
| `const` 构造 | 静态子树 |
| `RepaintBoundary` | 动画隔离重绘 |
| `ListView.builder` | 长列表 |
| `AutomaticKeepAliveClientMixin` | Tab 保活 |

## ListView 陷阱

给 `itemExtent` 可让滚动跳变计算更便宜；图片列表配合 `cacheWidth/Height` 降采样。

性能优化不是提前崇拜微优化，而是**用数据证明 rebuild 值得被消灭**。
""",
    },
    {
        "cat": "技术",
        "slug": "dart-null-safety-migration",
        "title": "Dart 空安全迁移：Sound null safety 语义深潜",
        "date": "2025-05-10",
        "tags": ["Dart", "Flutter"],
        "excerpt": "解释 promoted flow analysis、late 与可空泛型的边界行为。",
        "body": r"""
# Dart 空安全

Sound null safety 在编译期消灭大量 NPE。

```dart
String? name;
void greet() {
  if (name == null) return;
  print(name.length); // promoted to String
}
```

## late 与 ! 运算符

`late final` 适合延迟注入；`!` 是断言非空，滥用等于回归 NPE 赌运气。

## 迁移策略

1. `dart migrate` 生成草案
2. 先升 SDK 约束
3. 从叶子 package 向上游推进

空安全让 API **被迫表达可空性**——这是类型系统送给移动开发者最实在的礼物之一。
""",
    },
    # ── 技术 · Kotlin (5) ──
    {
        "cat": "技术",
        "slug": "kotlin-coroutines-structured-concurrency",
        "title": "Kotlin 协程：结构化并发与作用域取消",
        "date": "2025-01-20",
        "tags": ["Kotlin", "协程"],
        "excerpt": "从 CoroutineScope、Job 层次与 supervisorScope 谈取消传播与异常聚合。",
        "body": r"""
# Kotlin 结构化并发

协程不是「轻量线程」口号，而是一套**带生命周期**的并发抽象。

```kotlin
class DetailViewModel : ViewModel() {
    private val scope = viewModelScope
    fun load() = scope.launch {
        val user = async { repo.user() }
        val posts = async { repo.posts() }
        _ui.value = Ui(user.await(), posts.await())
    }
}
```

`viewModelScope` 在 `onCleared` 自动 `cancel`，避免泄漏。

## supervisorScope

子任务失败不拖垮兄弟任务，适合「多源聚合」仪表盘。

## 与 Flutter 对照

Dart Isolate 无共享状态；Kotlin 协程共享内存但用挂起函数串起异步——选型取决于平台与团队栈。
""",
    },
    {
        "cat": "技术",
        "slug": "kotlin-flow-vs-rxjava",
        "title": "Kotlin Flow 对比 RxJava：冷流、背压与操作符心智",
        "date": "2025-02-08",
        "tags": ["Kotlin", "Flow"],
        "excerpt": "说明 StateFlow、SharedFlow 与 Observable 在 UI 状态层的映射关系。",
        "body": r"""
# Flow vs RxJava

Flow 默认是**冷流**：收集才执行，利于资源节约。

```kotlin
fun ticker(): Flow<Int> = flow {
    var i = 0
    while (true) {
        emit(i++)
        delay(1000)
    }
}
```

`stateIn` / `shareIn` 把冷流热化，供多收集器订阅。

## 背压

`buffer`、`conflate` 处理生产快于消费；Android UI 常配合 `repeatOnLifecycle` 避免后台收集。

新项目优先 Flow；维护遗留 Rx 可用 `kotlinx-coroutines-rx2` 桥接。
""",
    },
    {
        "cat": "技术",
        "slug": "kotlin-multiplatform-mobile",
        "title": "Kotlin Multiplatform Mobile：共享逻辑与原生 UI 边界",
        "date": "2025-03-12",
        "tags": ["Kotlin", "KMP"],
        "excerpt": "评估 expect/actual、网络层下沉与 Compose Multiplatform 的现状与坑。",
        "body": r"""
# KMM 边界

KMP 擅长共享：**序列化模型、仓库、业务规则**；UI 仍多平台原生或 Compose Multiplatform。

```kotlin
// commonMain
expect class PlatformLogger {
    fun log(msg: String)
}
```

## 与 Flutter 对比

Flutter 共享 UI + 逻辑；KMP 共享逻辑 + 原生 UI——组织技能栈不同。

## 工程化

用 `commonTest` 跑纯 Kotlin 测试；版本对齐 Kotlin、Gradle、SKIE（Swift 互操作）需锁定 BOM。

选型没有绝对赢家，只有团队现有产能曲线。
""",
    },
    {
        "cat": "技术",
        "slug": "kotlin-delegation-properties",
        "title": "Kotlin 属性委托：lazy、observable 与 map 存储",
        "date": "2025-04-01",
        "tags": ["Kotlin"],
        "excerpt": "拆解 Delegates.notNull 在 Fragment 视图绑定里的典型写法与生命周期。",
        "body": r"""
# 属性委托

```kotlin
val name: String by lazy { expensive() }
var title: String by observable("") { _, old, new ->
    println("$old -> $new")
}
```

`by viewBinding()`（Android）把样板代码收敛到委托。

自定义委托需实现 `getValue`/`setValue` 操作符，可嵌入校验、缓存、加密读写的横切逻辑。

委托是 Kotlin **语法糖背后的语义压缩**，读懂它可读遍半本 Android 开源库。
""",
    },
    {
        "cat": "技术",
        "slug": "kotlin-sealed-when-exhaustive",
        "title": "Kotlin 密封类：代数数据类型与穷尽 when",
        "date": "2025-05-02",
        "tags": ["Kotlin", "类型系统"],
        "excerpt": "用 sealed interface 建模 UI 状态机，与 Swift enum associated value 对照。",
        "body": r"""
# 密封类与穷尽 when

```kotlin
sealed interface Result<out T> {
    data class Ok<T>(val value: T) : Result<T>
    data class Err(val cause: Throwable) : Result<Nothing>
}

fun <T> Result<T>.fold(onOk: (T) -> Unit, onErr: (Throwable) -> Unit) = when (this) {
    is Result.Ok -> onOk(value)
    is Result.Err -> onErr(cause)
}
```

编译器保证分支穷尽，重构新增子类时编译器会逼你改全 `when`。

这与 Swift `enum`、Rust `enum` 同族，是**把状态机写进类型**的正道。
""",
    },
    # ── 技术 · Swift (5) ──
    {
        "cat": "技术",
        "slug": "swift-async-await-task",
        "title": "Swift 并发：async/await 与 Task 取消协作",
        "date": "2025-01-28",
        "tags": ["Swift", "并发"],
        "excerpt": "讨论 TaskGroup、优先级反转与在 View 生命周期中绑定任务。",
        "body": r"""
# Swift async/await

```swift
func loadFeed() async throws -> [Post] {
    try await withThrowingTaskGroup(of: Post.self) { group in
        for id in ids {
            group.addTask { try await api.post(id) }
        }
        return try await group.reduce(into: []) { $0.append($1) }
    }
}
```

`Task.checkCancellation()` 应在长循环中周期性调用。

## UI 绑定

`.task { await vm.load() }` 在 SwiftUI 视图消失时自动取消，优于裸 `Task {}` 泄漏风险。
""",
    },
    {
        "cat": "技术",
        "slug": "swift-actor-isolation",
        "title": "Swift Actor：数据竞争与 MainActor 边界",
        "date": "2025-02-20",
        "tags": ["Swift", "Actor"],
        "excerpt": "解释 actor 串行化、nonisolated 与 @MainActor 标注 UI 代码的实践。",
        "body": r"""
# Swift Actor

```swift
actor ImageCache {
    private var store: [URL: Data] = [:]
    func data(for url: URL) -> Data? { store[url] }
    func insert(_ data: Data, for url: URL) { store[url] = data }
}
```

Actor 把可变状态关进**串行邮箱**，编译器阻止外部直接并发读写。

`@MainActor` 标记 ViewModel/UI 层，跨 actor 调用需 `await`，语义比 GCD 队列清晰。

与 Kotlin 协程、Go channel 对照学习，可建立统一「隔离」词汇表。
""",
    },
    {
        "cat": "技术",
        "slug": "swiftui-state-observation",
        "title": "SwiftUI 状态：@Observable 与 Observation 框架迁移",
        "date": "2025-03-25",
        "tags": ["Swift", "SwiftUI"],
        "excerpt": "从 ObservableObject 到 @Observable 宏，减少 objectWillChange 样板。",
        "body": r"""
# SwiftUI 状态观察

iOS 17+ `@Observable` 取代部分 `ObservableObject`：

```swift
@Observable
final class BookStore {
    var books: [Book] = []
    func refresh() async { books = await api.fetch() }
}
```

View 对属性的读取被跟踪，细粒度刷新，减轻无效 `body` 重算。

迁移时留意与 `EnvironmentObject` 混用期的边界；UIKit 桥接仍可用 `UIHostingController`。
""",
    },
    {
        "cat": "技术",
        "slug": "swift-protocol-oriented-design",
        "title": "Swift 面向协议编程：扩展优于继承",
        "date": "2025-04-12",
        "tags": ["Swift", "协议"],
        "excerpt": "用 protocol extension 提供默认实现，谈 PAT 与类型擦除容器。",
        "body": r"""
# 面向协议编程

```swift
protocol Loggable {
    func log(_ message: String)
}
extension Loggable {
    func log(_ message: String) { print("[\(Self.self)] \(message)") }
}
```

默认实现让协议像「可组合能力模块」。

存在类型（PAT）需 `any Loggable` 或类型擦除包装 `AnyLogger`，是 Swift 泛型设计的代价。

与 Kotlin interface 默认方法、Go 小接口哲学相通。
""",
    },
    {
        "cat": "技术",
        "slug": "swift-memory-arc-weak-unowned",
        "title": "Swift ARC：strong、weak、unowned 与闭包捕获",
        "date": "2025-05-15",
        "tags": ["Swift", "内存"],
        "excerpt": "用循环引用图解释 capture list 与 delegate 弱引用模式。",
        "body": r"""
# ARC 内存管理

```swift
network.fetch { [weak self] result in
    guard let self else { return }
    self.render(result)
}
```

`weak` 用于可能为 nil 的 delegate；`unowned` 用于生命周期同步、非可选关系（误用会 UAF）。

Instruments Leaks + Memory Graph 是验证手段，别只靠 `[weak self]` 咒语。
""",
    },
    # Fix typo in one entry - I had " "技术" with space - fix in script before run

    # ── 技术 · Go (4) ──
    {
        "cat": "技术",
        "slug": "go-context-cancellation",
        "title": "Go context.Context：超时、取消与请求作用域",
        "date": "2025-02-02",
        "tags": ["Go", "context"],
        "excerpt": "贯穿 HTTP handler、gRPC 与 worker 池的取消传播惯例。",
        "body": r"""
# context.Context

```go
ctx, cancel := context.WithTimeout(parent, 3*time.Second)
defer cancel()
req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
```

**不要把 Context 存在 struct 字段里**——Go 文档明确反对；应作为函数首参 `ctx context.Context` 传递。

`context.WithCancelCause`（Go 1.20+）让取消原因可观测，利于分布式追踪。
""",
    },
    {
        "cat": "技术",
        "slug": "go-channels-select-patterns",
        "title": "Go channel 与 select：并发模式集锦",
        "date": "2025-03-08",
        "tags": ["Go", "并发"],
        "excerpt": "fan-in、超时 select、done channel 关闭语义与 nil channel 陷阱。",
        "body": r"""
# channel 模式

```go
select {
case v := <-ch:
    handle(v)
case <-time.After(time.Second):
    return errors.New("timeout")
case <-ctx.Done():
    return ctx.Err()
}
```

关闭 channel 表示「不再有值」；接收方用 `v, ok := <-ch` 判断。

用 `errgroup` 管理一组 goroutine 生命周期，比裸 channel 更不易泄漏。
""",
    },
    {
        "cat": "技术",
        "slug": "go-interfaces-composition",
        "title": "Go 接口：隐式实现与小接口哲学",
        "date": "2025-04-18",
        "tags": ["Go", "接口"],
        "excerpt": "从 io.Reader 到仓储抽象，讨论接口应定义在消费方一侧。",
        "body": r"""
# Go 接口

```go
type Store interface {
    Save(ctx context.Context, b Blog) error
}
```

接口越小，mock 越简单。Go 习惯**在用时定义接口**，而非先画巨大 UML。

空接口 `any` 与泛型（Go 1.18+）分工：能类型参数化就别滥用 `any`。
""",
    },
    {
        "cat": "技术",
        "slug": "go-modules-vendor-workflow",
        "title": "Go Modules 与 vendor：依赖可复现构建",
        "date": "2025-05-20",
        "tags": ["Go", "工程化"],
        "excerpt": "go.work 多模块、replace 指令与私有 module proxy 配置要点。",
        "body": r"""
# Go Modules 工程化

```bash
go mod tidy
go test ./...
```

企业内网用 `GOPRIVATE` + Athens 代理；`go mod vendor` 在离线构建环境仍有价值。

`go.work` 适合 monorepo 本地联调多个 module，勿提交含绝对路径的 work 文件到公开仓库。
""",
    },
    # ── 技术 · Python (4) ──
    {
        "cat": "技术",
        "slug": "python-asyncio-event-loop",
        "title": "Python asyncio：事件循环、Task 与 aiohttp 实战",
        "date": "2025-02-25",
        "tags": ["Python", "asyncio"],
        "excerpt": "区分协程与线程池 offload，避免在 async 函数里阻塞调用。",
        "body": r"""
# asyncio 实战

```python
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

asyncio.run(main())
```

`asyncio.to_thread` 把 CPU/阻塞 IO 踢进线程池，保持 loop 畅通。

勿在 async 路由里直接 `time.sleep`——那是性能静音器。
""",
    },
    {
        "cat": "技术",
        "slug": "python-typing-generics-protocol",
        "title": "Python 类型系统：Protocol、Generic 与静态检查",
        "date": "2025-03-30",
        "tags": ["Python", "typing"],
        "excerpt": "用 mypy 严格模式约束动态语言边界，Structlog + TypedDict 示例。",
        "body": r"""
# Python typing

```python
from typing import Protocol

class Repository(Protocol):
    def get(self, id: str) -> Post: ...

def render(repo: Repository, id: str) -> str:
    return repo.get(id).title
```

`Protocol` 实现结构化子类型；`Generic[T]` 表达容器不变性。

`mypy --strict` 在 CI 里渐进启用，比事后补类型便宜。
""",
    },
    {
        "cat": "技术",
        "slug": "python-dataclass-slots",
        "title": "Python dataclass：slots、frozen 与性能取舍",
        "date": "2025-04-28",
        "tags": ["Python"],
        "excerpt": "对比 attrs/pydantic，谈配置模型与 API DTO 分层。",
        "body": r"""
# dataclass 进阶

```python
@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float
```

`frozen` 可哈希；`slots` 降内存、禁动态属性。

API 边界用 Pydantic 校验；内部领域用轻量 dataclass，避免全家桶 ORM 化。
""",
    },
    {
        "cat": "技术",
        "slug": "cross-platform-mobile-2025",
        "title": "跨平台移动开发 2025：Flutter、KMP 与原生三角",
        "date": "2025-05-25",
        "tags": ["Flutter", "Kotlin", "Swift"],
        "excerpt": "从团队技能、包体、生态与 FFI 四个维度做技术选型矩阵。",
        "body": r"""
# 跨平台选型矩阵

| 维度 | Flutter | KMP | 双原生 |
|------|---------|-----|--------|
| UI 一致性 | 高 | 中 | 低 |
| 原生能力 | FFI/Platform Channel | 直接 | 最好 |
| 包体 | 中偏大 | 中 | 基准 |
| 热更新 | 受限 | 受限 | 商店策略 |

没有银弹：金融强监管可能偏原生；内容型产品 Flutter 效率高；已有大量 Kotlin 业务逻辑可 KMP 下沉。

用**团队主语言 + 发布节奏**倒推技术，而不是倒过来。
""",
    },
    # ── 阅读 (6) ──
    {
        "cat": "阅读",
        "slug": "reading-slowly-in-digital-age",
        "title": "数字时代的慢阅读：为何我们读不完一本书",
        "date": "2025-01-10",
        "tags": ["阅读", "随笔"],
        "excerpt": "从注意力经济谈断网阅读、纸书触感与批注习惯如何改变理解深度。",
        "body": r"""
# 慢阅读

推送把阅读切成碎片，我们误把「看过标题」当作「读过书」。

我尝试每周留出两个**无屏幕小时**：只带一本纸书与一支铅笔。划线不是装饰，而是与作者对话的脚印。

慢不等于少读，而是给大脑留白，让概念之间发生连接——这在扫描 API 文档时同样适用：深读一章胜过收藏十篇。
""",
    },
    {
        "cat": "阅读",
        "slug": "notes-on-meditations",
        "title": "读《沉思录》札记：斯多葛与工程师的日常",
        "date": "2025-02-18",
        "tags": ["阅读", "哲学"],
        "excerpt": "把「控制二分法」映射到需求变更、线上事故与代码评审情绪。",
        "body": r"""
# 《沉思录》札记

马可·奥勒留写给自己，不是写给别人。这种私密性让句子像日志。

工程师版本：**可控**——测试、沟通、复盘；**不可控**——评审语气、市场窗口。

事故夜里，先问「我现在能做什么」，而不是「谁该背锅」。这不是软弱，是把注意力从情绪迁回系统修复。
""",
    },
    {
        "cat": "阅读",
        "slug": "walden-one-chapter-a-week",
        "title": "每周一章《瓦尔登湖》：简朴作为一种练习",
        "date": "2025-03-15",
        "tags": ["阅读"],
        "excerpt": "梭罗的湖不是逃避，而是对消费默认值的质疑；与极简桌面相映。",
        "body": r"""
# 每周一章瓦尔登

梭罗若活在今日，大概会嘲笑我们买齐机械键盘却写不出三百字日记。

「简朴」不是苦行，而是**看清真正需要的工具**。我的编辑器插件删到只剩语法高亮与 Git，像给思想清障。

湖在麻省，也在每次关机后的安静里。
""",
    },
    {
        "cat": "阅读",
        "slug": "poetry-and-debugging",
        "title": "诗歌与调试：隐喻如何帮助理解复杂系统",
        "date": "2025-04-08",
        "tags": ["阅读", "技术文化"],
        "excerpt": "李白句式的留白与 gdb 单步，都是在有限符号里寻找因果。",
        "body": r"""
# 诗歌与调试

好诗留白，好代码也留白：函数名是隐喻，类型是约束，注释解释**为什么**而非**是什么**。

读一首绝句的五分钟，与定位一个空指针的五十分钟，都需要耐心。技术人不必假装只信逻辑——文学训练的是**切换视角**的能力。
""",
    },
    {
        "cat": "阅读",
        "slug": "translation-as-rereading",
        "title": "翻译即重读：在另一种语言里遇见作者",
        "date": "2025-05-05",
        "tags": ["阅读", "翻译"],
        "excerpt": "对比英中译本与原文节奏，谈技术文档本地化时的语义损耗。",
        "body": r"""
# 翻译即重读

译者在两个语言之间搭桥，损耗不可避免。读《小王子》中英对照，会发现「驯养」与 tame 的温度差。

技术文档翻译同理：deadline 不能直译成「死线」；应说「截止日期」。好的本地化是**二次写作**，不是词典替换。
""",
    },
    # ── 生活 (6) ──
    {
        "cat": "生活",
        "slug": "morning-walk-without-phone",
        "title": "不带手机的晨走：二十分钟重置注意力",
        "date": "2025-01-15",
        "tags": ["生活"],
        "excerpt": "把通勤前的时间还给身体与呼吸，而不是短视频。",
        "body": r"""
# 晨走

二十分钟即可。不听播客，不看步数排行榜。树、风、路口红灯的倒影，足够组成低带宽输入。

回来冲咖啡时，脑子反而更清楚——像重启了事件循环，清空了 UI 帧缓存。
""",
    },
    {
        "cat": "生活",
        "slug": "cooking-as-meditation",
        "title": "做饭当作冥想：切菜声与顺序感",
        "date": "2025-02-22",
        "tags": ["生活"],
        "excerpt": "厨房里的流水线与写代码的流水线，都需要准备与收尾。",
        "body": r"""
# 做饭

切洋葱要专注，否则会流泪——像处理指针。煮汤要小火，急不得，像等 CI 绿灯。

周末做一顿慢的，是对一周外卖的补偿。盘子洗完后厨房归零，心情也 commit 了。
""",
    },
    {
        "cat": "生活",
        "slug": "city-rain-season",
        "title": "城市的雨季：玻璃窗与延迟的地铁",
        "date": "2025-03-20",
        "tags": ["生活", "随笔"],
        "excerpt": "潮湿空气里写字，网速似乎也更慢半拍。",
        "body": r"""
# 雨季

雨声白噪声盖住键盘。玻璃窗上的水珠把街灯拆成散点，像 GPU 过载的 bloom。

地铁晚点时，不妨多读两页纸书。季节从不是背景，它参与情绪调度。
""",
    },
    {
        "cat": "生活",
        "slug": "desk-minimalism",
        "title": "桌面极简：少一件杂物，多一寸思考空间",
        "date": "2025-04-15",
        "tags": ["生活"],
        "excerpt": "只留键盘、显示器、笔记本与一杯水，线缆收纳的真实收益。",
        "body": r"""
# 桌面极简

杂物是未关闭的 tab。收纳线缆后，视觉噪音下降，切换任务的摩擦变小。

极简不是禁欲，而是让**工具各就其位**。就像代码仓库删掉 dead code，呼吸会轻一点。
""",
    },
    {
        "cat": "生活",
        "slug": "letter-to-future-self",
        "title": "写给一年后的自己：不追求酷，追求可持续",
        "date": "2025-05-08",
        "tags": ["生活"],
        "excerpt": "关于健康、储蓄、技术栈选择与仍然想写完的博客。",
        "body": r"""
# 给未来的信

亲爱的未来的我：

别追逐最炫框架，追逐能睡着的节奏。博客不必日更，但要诚实。Flutter、Kotlin、Swift 都只是笔，写的是你想记住的日子。

如果又开始熬夜，回来看这篇。
""",
    },
    # ── 收藏 (2) ──
    {
        "cat": "收藏",
        "slug": "developer-toolkit-2026",
        "title": "开发者工具箱收藏：编辑、调试、抓包与笔记",
        "date": "2025-03-01",
        "tags": ["收藏", "工具"],
        "excerpt": "整理 IDE、Charles、Obsidian、ripgrep 等长期驻留工具及使用场景。",
        "body": r"""
# 工具箱 2026

| 类别 | 工具 | 用途 |
|------|------|------|
| 编辑 | VS Code / Cursor | 通用 |
| 移动 | Android Studio, Xcode | 原生调试 |
| 跨端 | Flutter DevTools | 帧率 |
| 网络 | Charles / Proxyman | 抓包 |
| 笔记 | Obsidian | 双链 |
| 搜索 | ripgrep, fzf | 仓库内 |

工具越少，肌肉记忆越深。每季度审视是否可删一款。
""",
    },
    {
        "cat": "收藏",
        "slug": "flutter-learning-path",
        "title": "Flutter 学习路径收藏：从 Widget 到引擎",
        "date": "2025-04-02",
        "tags": ["收藏", "Flutter"],
        "excerpt": "官方文档、Flutter Apprentice、源码走读与 FFI 四条线并行建议。",
        "body": r"""
# Flutter 学习路径

1. **基础**：Widget 生命周期、布局约束、状态管理（Riverpod）
2. **进阶**：Platform Channel、FFI、性能 profiling
3. **源码**：`binding.dart`、`SchedulerBinding`、Impeller 文档
4. **实战**：一个完整 App + 测试 + CI

每周留半天读 release notes，比追网红库重要。
""",
    },
]

def fix_posts():
    for p in POSTS:
        if p["cat"].strip() != p["cat"]:
            p["cat"] = p["cat"].strip()

def write_post(p: dict):
    cat_dir = ROOT / p["cat"]
    cat_dir.mkdir(parents=True, exist_ok=True)
    path = cat_dir / f"{p['slug']}.md"
    if path.exists():
        return False
    tags_yaml = "\n".join(f"  - {t}" for t in p["tags"])
    content = f"""---
title: {p['title']}
date: {p['date']}
category: {p['cat']}
tags:
{tags_yaml}
excerpt: {p['excerpt']}
---
{p['body'].strip()}
"""
    path.write_text(content, encoding="utf-8")
    return True

def main():
    fix_posts()
    created = 0
    skipped = 0
    for p in POSTS:
        if write_post(p):
            created += 1
        else:
            skipped += 1
    total = len(list(ROOT.rglob("*.md")))
    print(f"created={created} skipped={skipped} total_md={total}")

if __name__ == "__main__":
    main()
