---
id: f53094f4-6777-43f2-a3d2-4f98def2a830
created_at: 2026-09-17T12:03:17+08:00
---


# BeReady 文件组织与知识节点管理规范

> 本文是《BeReady 内容架构设计》的补充规范。
>
> 原始文档解决的是“BeReady 应该如何组织知识”；
> 本文进一步解决：
>
> - 知识如何落到文件系统
> - Level 如何与文件归属对应
> - 一个知识应该归哪个 Level
> - 父节点与子节点之间到底是什么关系
> - 分支如何长期增长
> - Markdown 文件与目录如何演化
> - Wikilink 如何管理跨树关系
> - Preservation 如何与知识主树分离
>
> 本文不改变原有的“Capability → Level → Knowledge”核心模型。

---

# 1. 总体原则

BeReady 的稳定认知模型为：

> **Capability → Level → Knowledge**

文件系统采用：

> **可自然生长的 Markdown 树**

Wikilink 负责：

> **表达知识之间的语义关系。**

Git 负责：

> **保存知识的长期演化历史。**

Metadata 负责：

> **描述知识节点的属性、状态与验证信息。**

Preservation 负责：

> **决定知识如何被保存、打包和传播。**

因此：

```text
用户认知
    │
    └── Capability
          │
          └── Level
                │
                └── Knowledge
                      │
                      └── subknowledge
```

对应：

```text
物理存储
    │
    └── Markdown Tree
              │
              └── Wikilink Network
```

---

# 2. Canonical Tree：唯一知识主树

BeReady 必须存在一棵唯一的：

> **Canonical Knowledge Tree**

即知识的正式物理归属树。

建议：

```text
capabilities/
├── water/
├── food/
├── fire/
├── shelter/
├── safety/
├── first-aid/
├── hygiene/
├── energy/
├── tools/
├── navigation/
├── communication/
└── ...
```

每个一级目录代表一个核心 Capability。

---

# 3. Capability 是主干

Capability 是知识树最稳定的一层。

例如：

```text
water
food
fire
shelter
safety
```

一个 Capability 内部可以持续增长，但不应该因为内部知识增加而改变其身份。

因此：

> **Capability 是长期稳定的知识主干。**

---

# 4. Level 是第二层稳定结构

每个 Capability 下根据能力发展设置：

```text
L1
L2
L3
...
Ln
```

例如：

```text
water/
├── L1/
├── L2/
├── L3/
├── L4/
└── L5/
```

Level 表示：

> **该 Capability 的能力发展位置。**

它不是统一的时间阶段，也不是所有 Capability 必须拥有相同数量的等级。

---

# 5. Level 是能力归属，不是知识难度

`L1`、`L2`、`L3` 不应简单理解成：

```text
简单 → 中等 → 困难
```

而应理解为：

```text
某 Capability 的能力发展路径
```

判断一个知识属于哪个 Level，应关注：

- 它解决什么能力问题
- 掌握它意味着获得什么能力
- 它有哪些前置条件
- 它需要什么资源与技术
- 它在该 Capability 的发展路径中处于什么位置

而不是单纯看：

- 文章有多长
- 技术有多复杂
- 有多少术语
- 有多少图片

---

# 6. 每个 Knowledge Node 只有一个 Canonical 归属

一个正式 Knowledge Node 应能够回答：

```text
它属于哪个 Capability？
它属于哪个 Level？
它的 Canonical Location 是哪里？
```

例如：

```text
capabilities/
└── water/
    └── L3/
        └── filtration.md
```

对应：

```yaml
capability: water
level: L3
```

目录与 Metadata 应保持一致。

如果：

```text
目录 = water/L3/
Metadata = capability: water, level: L2
```

则属于结构错误，应由工具检测。

---

# 7. “归属”与“使用”必须分开

一个知识可能被多个 Capability 使用，但只能拥有一个 Canonical 归属。

例如：

```text
容器
```

可能被：

```text
water
food
fire
hygiene
```

共同使用。

不能因此复制成：

```text
water/.../container.md
food/.../container.md
fire/.../container.md
```

而应选择一个 Canonical Location，其余位置通过 Wikilink 引用。

因此：

```text
使用关系 ≠ 归属关系
```

---

# 8. Level 归属与引用 Level 是两个概念

一个知识属于：

```text
water/L3/filtration
```

不代表只有 L3 才能引用它。

例如 L1 可以通过：

```markdown
进一步了解：

[[过滤]]
```

指向 L3 的知识。

因此：

```text
Canonical Level
    ↓
知识正式归属在哪里

Reference Level
    ↓
哪些 Level 会使用、引用它
```

两者必须分开。

---

# 9. 不因为被低 Level 使用，就复制到低 Level

例如：

```text
water/L3/filtration/
```

可能被 L1 的入门内容引用。

不能因此建立：

```text
water/L1/filtration.md
```

否则会形成两个 Canonical Node。

正确方式是：

```text
L1
 │
 └── [[过滤]]
          │
          ↓
         L3
```

L1 可以针对自身能力范围解释“为什么需要过滤”，但不复制过滤知识本体。

---

# 10. 不因为知识基础，就强行归入 L1

“基础知识”与“L1 归属”不是同义词。

一个知识即使是其他高级知识的基础，也可能在当前 Capability 中属于 L3。

因此不能使用：

> “它很基础，所以应该放 L1。”

作为唯一判断依据。

---

# 11. Level 不要求所有知识严格逐级依赖

Level 提供纵向能力结构，但知识之间的真实关系由 Wikilink 表达。

例如：

```text
L2
 ├── → L3
 ├── → tools
 ├── → materials
 └── → evidence
```

不要求所有知识都必须：

```text
L1 → L2 → L3
```

逐级链接。

因此：

> **Level 是能力结构；Wikilink 是知识关系。**

---

# 12. 不为了“归档”而复制同一知识到多个 Level

如果多个文件实际上是在描述同一个 Knowledge Node，只是面向不同 Level 的说明，不应简单复制成：

```text
L1/filtration-basic.md
L2/filtration-intermediate.md
L3/filtration-advanced.md
```

应该先判断：

> 这是一个知识节点在不同深度上的表达，还是三个真正不同的知识节点？

如果是同一个知识：

```text
[[过滤]]
```

保持一个 Canonical Node。

如果确实是三个不同的能力节点，则分别定义其 Canonical Level。

---

# 13. Level 目录中的 index.md 是正式节点

例如：

```text
water/
└── L3/
    └── index.md
```

这里的 `index.md` 代表：

> **Water Capability 的 L3 能力节点。**

它不是单纯 README。

它应该说明：

- L3 解决什么能力问题
- 这一 Level 包含哪些主要知识
- 如何进一步深入
- 与其他 Level 有什么关系

---

# 14. Capability 的 index.md 是正式节点

例如：

```text
water/index.md
```

代表：

> **Water Capability 本身。**

它可以说明：

```text
水能力是什么
L1 → L2 → L3 → ...
主要知识
相关 Capability
```

因此：

```text
water/index.md
```

也是 Knowledge Node，而不只是目录说明。

---

# 15. 关键修正：物理子目录 ≠ 自动知识子节点

这是本规范的重要边界。

例如：

```text
water/
└── L3/
    └── filtration/
        ├── index.md
        ├── ceramic.md
        └── sand.md
```

从物理结构上看：

```text
ceramic.md
```

位于：

```text
filtration/
```

下面。

但真正的知识模型关系必须是：

```text
过滤
  ├── 陶瓷过滤
  └── 砂滤
```

只有当这种关系确实代表：

> **“陶瓷过滤是过滤这个知识节点的组成/细分/子知识”**

时，才能称为知识子节点。

不能仅因为文件放在某目录下，就认定它是父节点的子知识。

因此：

> **目录嵌套是物理事实；父子知识关系是语义事实。**

二者通常一致，但概念上不能混为一谈。

---

# 16. 关键修正：子节点不自动继承 Capability 与 Level

上一版“子节点默认继承父节点 Capability 与 Level”的表述过于绝对，应修正为：

> **子节点可以继承父节点的 Capability 与 Level 作为默认归属，但这种继承必须经过语义确认，而不是由物理目录自动决定。**

例如：

```text
water/L3/filtration/
├── index.md
├── ceramic.md
└── sand.md
```

通常可以解释为：

```text
water
  ↓
L3
  ↓
过滤
  ├── 陶瓷过滤
  └── 砂滤
```

此时：

```text
陶瓷过滤
砂滤
```

可以自然拥有：

```text
capability: water
level: L3
```

但真正原因是：

> 它们是 Water L3 中“过滤”知识的细分。

**不是因为它们恰好位于 `water/L3/filtration/` 目录里。**

---

# 17. 子节点归属的正确判断顺序

一个子节点的 Canonical 归属应按照以下顺序判断：

```text
父节点
  │
  ↓
这个知识是否真正属于父节点的语义范围？
  │
  ├── 否 → 不应作为子节点
  │
  └── 是
       │
       ↓
它是否仍属于父节点的 Capability？
       │
       ├── 是
       │    ↓
       │  判断是否继承 Level
       │
       └── 否
            ↓
          重新确定 Canonical Capability
```

对于 Level：

```text
是否仍处于父节点代表的能力发展范围？
        │
        ├── 是 → 可以继承父节点 Level
        │
        └── 否 → 应重新确定 Level
```

因此：

> **继承是语义判断后的默认结果，不是目录规则。**

---

# 18. 子节点可以与父节点处于同一 Level，也可以不同

最常见情况是：

```text
water/L3/filtration/
├── ceramic.md
├── sand.md
└── charcoal.md
```

这些子节点与父节点同属 L3。

但也存在这样的情况：

```text
water/L3/
└── filtration/
    ├── index.md
    └── advanced-maintenance.md
```

如果 `advanced-maintenance` 实际代表的是一个更高 Level 的能力，那么不能因为它是 `filtration` 的子知识，就强行标记：

```yaml
level: L3
```

这时应该重新判断结构。

可能的正确结果是：

```text
water/
├── L3/
│   └── filtration/
│       └── index.md
└── L4/
    └── filtration-maintenance/
```

或者，如果它只是 L3 过滤知识中的一个高级技术细节：

```text
water/L3/filtration/
└── advanced-maintenance.md
```

并仍属于 L3。

关键判断不是：

> “它是父节点的子节点吗？”

而是同时判断：

> **它是什么知识，以及它在 Capability 的能力发展中处于哪里。**

---

# 19. 父子关系与 Level 关系是两个维度

必须允许：

```text
父子关系
```

与：

```text
Level 关系
```

相互独立。

例如：

```text
过滤
 ├── 陶瓷过滤
 ├── 砂滤
 └── 膜过滤
```

表达知识上的：

```text
包含 / 细分
```

而：

```text
L2 → L3
```

表达：

```text
能力发展
```

因此：

```text
父子 ≠ Level 升级
```

更不能把：

```text
子节点
```

理解成：

```text
更高级节点
```

---

# 20. 目录深度不等于 Level

例如：

```text
water/L3/filtration/membrane/maintenance/cleaning.md
```

目录很深，但仍可能属于：

```text
Capability = water
Level = L3
```

目录深度表达的是：

```text
知识结构深度
```

Level 表达的是：

```text
能力发展位置
```

二者必须解耦。

---

# 21. 子节点也不自动继承父节点的全部 Metadata

例如父节点：

```yaml
status: verified
preservation: P1
```

不能简单规定：

```text
所有子节点自动 verified
所有子节点自动 P1
```

原因是：

- 子节点可能拥有自己的证据
- 子节点可能有不同验证状态
- 子节点可能有不同风险
- 子节点可能有不同 Preservation 需求

因此：

> **结构性归属可以继承，事实性与状态性 Metadata 必须独立判断。**

可以区分：

```text
结构属性
    Capability
    Level
    Parent

事实属性
    status
    evidence
    risk
    preservation
```

前者可以有默认继承逻辑，后者不应无条件继承。

---

# 22. 推荐的 Metadata 继承模型

对于子节点，可以采用：

```text
Parent
  │
  ├── capability → 默认继承
  ├── level      → 默认继承
  │
  ├── status     → 独立判断
  ├── evidence   → 独立判断
  ├── risk       → 独立判断
  └── preservation → 独立判断
```

其中：

> “默认继承”不是“不可改变”。

如果子节点实际发生 Capability 或 Level 边界变化，应明确覆盖或重新归属。

---

# 23. 一个子节点不能用“继承”掩盖错误归属

例如：

```text
water/L3/filtration/
└── charcoal.md
```

如果这个文件实际主要讲的是：

> 木炭的制造方法、燃料用途、材料性质

而不是：

> 木炭作为过滤材料的使用

那么就不能因为目录结构而自动归入：

```text
water/L3
```

应该判断：

```text
这个知识的 Canonical Home 是哪里？
```

如果真正属于：

```text
fire
materials
tools
```

等其他知识领域，则应重新归属，并通过：

```markdown
[[木炭]]
```

与过滤建立关系。

---

# 24. “父节点下面”应有明确的语义边界

一个节点适合作为父节点的子节点，至少应该满足：

```text
它是父节点知识的自然细分
```

例如：

```text
过滤
 ├── 陶瓷过滤
 ├── 砂滤
 └── 活性炭过滤
```

属于自然细分。

而：

```text
过滤
 ├── 容器
 ├── 水源
 ├── 火
 └── 木材
```

即使这些内容都是过滤过程中可能需要的东西，也不应该自动成为：

```text
过滤
```

的子节点。

它们更可能是：

```text
过滤
 ├── 需要 → [[容器]]
 ├── 依赖 → [[水源]]
 └── 相关 → [[火]]
```

因此：

> **“相关”不能伪装成“子节点”。**

---

# 25. 子节点与 Wikilink 的边界

判断一个知识应该成为子节点还是 Wikilink，可以问：

### 如果它回答：

> “这是这个知识的一部分/一种具体形式/一个自然细分。”

那么适合成为：

```text
子节点
```

### 如果它回答：

> “这个知识与另一个独立知识存在依赖、需要、替代、相关或前置关系。”

那么应该使用：

```text
Wikilink
```

例如：

```text
过滤
 ├── 陶瓷过滤
 ├── 砂滤
 └── 膜过滤
```

而：

```text
过滤
 ├── 需要 → 容器
 ├── 依赖 → 水源
 └── 前置 → 沉淀
```

应该通过关系表达。

---

# 26. 一个知识不能因为“方便放置”而成为子节点

文件系统维护时最危险的行为之一是：

> “这个知识跟当前内容有关，就放这里。”

这会逐渐把目录变成杂物箱。

因此：

```text
有关
```

不是成为子节点的充分条件。

必须满足：

```text
有关
+
自然属于该节点的语义范围
```

才适合作为子节点。

否则使用 Wikilink。

---

# 27. 跨 Capability 子节点原则上不应通过目录嵌套解决

例如：

```text
water/L3/filtration/
└── fire.md
```

如果 `fire` 是一个独立 Capability，就不应该因为过滤过程中可能涉及火，而把：

```text
fire
```

作为：

```text
filtration
```

的子节点。

应保持：

```text
capabilities/
├── water/
└── fire/
```

然后：

```text
[[火]]
```

连接二者。

这样 Canonical Tree 保持清晰，Knowledge Graph 负责表达真实依赖。

---

# 28. 同 Capability 不代表一定同 Level

即使两个节点都属于：

```text
water
```

也不代表它们必须处于同一个 Level。

例如：

```text
water/L1/drinking.md
water/L3/filtration.md
```

它们可以存在关系：

```text
drinking
   ↓
需要 → filtration
```

但：

```text
drinking
```

并不会因为链接到：

```text
filtration
```

而自动升级到 L3。

---

# 29. 同 Level 也不代表一定是父子节点

例如：

```text
water/L3/
├── filtration.md
└── storage.md
```

它们同属：

```text
water/L3
```

但二者可能只是并列知识。

并不意味着：

```text
filtration
    ↓
storage
```

或者：

```text
storage
    ↓
filtration
```

如果没有自然的知识包含关系，就保持并列。

---

# 30. Level 与文件归属的最终判断模型

新增一个知识时，按以下顺序判断：

```text
新知识
  │
  ↓
是否已有相同 Knowledge Node？
  │
  ├── 是 → 扩展 / 修改已有节点
  │
  └── 否
       │
       ↓
确定 Canonical Capability
       │
       ↓
确定 Canonical Level
       │
       ↓
是否属于某个已有节点的自然细分？
       │
       ├── 是 → 成为该节点子节点
       │
       └── 否 → 成为该 Level 的直接节点
       │
       ↓
判断与其他知识的关系
       │
       └── Wikilink
```

注意：

> **先确定知识本身的 Canonical 归属，再决定它是否作为某节点的子节点。**

不能反过来：

> “先把文件放进某目录，再认为它继承该目录的归属。”

---

# 31. 节点裂变

简单节点：

```text
filtration.md
```

增长后：

```text
filtration/
├── index.md
├── ceramic.md
├── sand.md
└── charcoal.md
```

这里：

```text
filtration.md
```

与：

```text
filtration/index.md
```

代表同一个逻辑 Knowledge Node。

裂变改变的是：

```text
物理组织
```

而不是自动改变：

```text
Capability
Level
```

---

# 32. 节点裂变不等于 Level 升级

例如：

```text
filtration.md
```

扩展成：

```text
filtration/
├── index.md
├── ceramic.md
├── sand.md
├── charcoal.md
└── membrane.md
```

这只说明：

> 过滤知识变得更加丰富。

不意味着：

```text
L3 → L4
```

Level 是否变化必须单独判断。

因此：

```text
Node Expansion
```

和：

```text
Level Advancement
```

是两个独立事件。

---

# 33. index.md 是聚合节点本身

例如：

```text
filtration/
├── index.md
├── ceramic.md
└── sand.md
```

`index.md` 代表：

> 过滤这个知识节点。

它可以介绍：

- 过滤是什么
- 主要方法
- 方法之间的区别
- 进入具体子知识的入口
- 与其他知识的关系

---

# 34. 不为了整理而增加目录

不要建立：

```text
methods/
resources/
tools/
materials/
principles/
```

等统一目录。

只有当知识本身形成自然分支时才增加目录。

原则：

> **知识发生结构性分叉，才增加结构；管理者需要整理，不是增加目录的理由。**

---

# 35. 一个节点表达一个自然概念

例如：

```text
过滤
陶瓷过滤
砂滤
储水
```

应该尽量成为用户能够自然理解的知识节点。

不要把数据库字段或内部管理概念直接变成目录层级。

---

# 36. Wikilink 必须能够承受物理重构

最初：

```text
filtration.md
```

后来：

```text
filtration/index.md
```

引用：

```markdown
[[过滤]]
```

仍然应该解析到同一个逻辑节点。

因此：

> **Wikilink 指向逻辑 Knowledge Node，而不是绑定脆弱的物理路径。**

---

# 37. 一个 Knowledge Node 只有一个 Canonical 来源

即使它：

- 被多个 Capability 使用
- 被多个 Level 引用
- 出现在多个 Scenario
- 出现在多个 Preservation Pack

仍然只有一个正式来源。

形成：

```text
Knowledge Node
      │
      ├── Canonical Location → 1
      ├── References        → N
      ├── Scenarios         → N
      └── Preservation      → N
```

---

# 38. Resource 不成为固定目录分类

Resource、Tool、Material 等优先作为关系表达。

例如：

```text
过滤
 ├── 需要 → [[容器]]
 ├── 需要 → [[滤材]]
 └── 依赖 → [[水源]]
```

而不是：

```text
filtration/
└── resources/
```

除非这些资源本身已经发展成独立的知识体系。

---

# 39. Scenario 不建立第二知识树

例如：

```text
scenarios/
├── earthquake.md
├── blackout.md
└── water-outage.md
```

Scenario 通过 Wikilink 组合现有知识：

```markdown
[[水]]
[[卫生]]
[[食物]]
[[安全]]
```

不复制 Capability Tree。

---

# 40. 推荐目录

```text
beready/
│
├── capabilities/
│   ├── water/
│   │   ├── index.md
│   │   ├── L1/
│   │   │   └── index.md
│   │   ├── L2/
│   │   │   └── index.md
│   │   └── L3/
│   │       ├── index.md
│   │       ├── boiling.md
│   │       ├── filtration.md
│   │       └── storage.md
│   │
│   ├── food/
│   ├── fire/
│   ├── shelter/
│   └── ...
│
├── scenarios/
│   ├── earthquake.md
│   ├── blackout.md
│   └── ...
│
└── ...
```

随着增长：

```text
L3/
├── index.md
├── boiling.md
├── filtration/
│   ├── index.md
│   ├── ceramic.md
│   ├── sand.md
│   └── charcoal.md
└── storage/
    ├── index.md
    └── containers.md
```

---

# 41. Frontmatter

建议：

```yaml
---
title: 陶瓷过滤
level: L3
capability: water
status: verified
preservation: P1
tags:
  - water
  - filtration
---
```

其中：

```text
capability
level
```

描述 Canonical 归属。

而：

```text
status
preservation
evidence
risk
```

描述知识状态与其他属性。

---

# 42. Metadata 的继承原则

Metadata 可以分为三类：

### A. 归属属性

```text
capability
level
parent
```

可以根据父子语义关系提供默认值。

### B. 知识事实属性

```text
evidence
sources
conditions
risk
```

必须针对具体节点判断。

### C. 生命周期 / 分发属性

```text
status
preservation
```

原则上独立判断，不因为父节点改变就自动改变。

因此：

> **父子结构可以提供默认上下文，但不能让父节点的 Metadata 无条件覆盖子节点。**

---

# 43. 结构校验

CI / AI 可以检查：

```text
Capability 是否合法
Level 是否合法
目录与 Metadata 是否一致
父子知识关系是否合理
Wikilink 是否断裂
是否存在重复节点
是否存在孤立节点
是否存在跨 Capability 的错误嵌套
是否存在不合理的目录膨胀
```

特别应该检查：

> **“目录嵌套是否被错误地当成知识继承？”**

---

# 44. AI 的组织职责

AI 可以：

```text
新节点归属建议
Level 建议
父子关系建议
重复检测
拆分建议
Wikilink 建议
结构异常检测
```

例如：

> `water/L3/filtration/charcoal.md` 可能同时涉及“过滤中的活性炭”和“木炭制造”，建议确认其 Canonical Knowledge 是否仍属于过滤节点。

但 AI 只能提出建议。

最终通过：

```text
Draft
 ↓
Human Review
 ↓
Git PR
 ↓
Merge
```

完成结构变更。

---

# 45. Preservation 不属于 Canonical Tree

Canonical Tree 回答：

> 知识应该住在哪里？

Preservation 回答：

> 知识应该保存和传播到什么程度？

因此：

```text
P0
P1
P2
P3
```

不应该成为第二套正式知识树。

---

# 46. Preservation 可以生成派生视图

例如：

```text
Canonical Tree
      ↓
Preservation Metadata
      ↓
Build
      ↓
Essential Pack
Offline Pack
Survival Pack
Resilience Pack
Rebuild Pack
```

这些都是：

> Canonical Tree 的派生视图。

不能成为第二个事实来源。

---

# 47. Preservation 可以自动解析依赖

未来可以实现：

```text
A
 ↓
需要 B
 ↓
B 进入 Pack
```

从而生成真正可用的知识包。

因此 Preservation 不只是：

```text
复制 P0 文件
```

而可以成为：

> **基于知识关系生成最小可用知识集合。**

---

# 48. Git 记录结构变化

以下变化都应该进入 Git 历史：

```text
新增节点
删除节点
重命名
节点裂变
Level 调整
Capability 调整
父子关系调整
Wikilink 调整
Metadata 调整
```

尤其是：

```text
L2 → L3
```

这种 Level 变化，应记录：

```text
谁
何时
为什么
依据什么
```

---

# 49. Level 调整与节点裂变必须区分

例如：

```text
filtration.md
```

变成：

```text
filtration/
├── index.md
└── ceramic.md
```

是：

```text
Node Expansion
```

而：

```text
water/L3/filtration/
```

移动到：

```text
water/L4/filtration/
```

是：

```text
Level Reassignment
```

两者不能混为一谈。

---

# 50. 最终的父子边界

可以用下面这组规则作为长期维护的硬边界：

```text
物理父子
    ≠
知识父子
```

```text
知识父子
    ≠
Level 父子
```

```text
目录继承
    ≠
Metadata 全量继承
```

正确关系是：

```text
物理目录
    ↓
提供候选结构

知识语义
    ↓
确认父子关系

Capability / Level 模型
    ↓
确认 Canonical 归属

Metadata
    ↓
描述具体节点状态

Wikilink
    ↓
表达跨节点关系
```

---

# 51. 最终模型

```text
                         BeReady
                            │
                    ┌───────┴───────┐
                    │               │
                用户认知模型      存储模型
                    │               │
              Capability       Markdown Tree
                    │               │
                  Level          Node
                    │               │
                Knowledge      ┌────┴────┐
                    │          │         │
                子知识        文件       目录
                    │                    │
                    └──────┬─────────────┘
                           │
                    需要语义确认
                           │
                    Knowledge Relation
                           │
                      Wikilink Graph


        ┌─────────────────────────────────┐
        │             Metadata             │
        │ capability / level / status      │
        │ evidence / risk / preservation   │
        └────────────────┬────────────────┘
                         │
                         ↓
                    Preservation
                         │
                         ↓
                  Packs / Storage


                         │
                         ↓
                        Git
                         │
                Review / PR / History
```

---

# 52. 最终规则摘要

> **1. Capability 是知识主干。**

> **2. Level 是 Capability 的能力发展纵轴。**

> **3. Level 不是单纯的知识难度。**

> **4. 每个 Knowledge Node 只有一个 Canonical Capability 和一个 Canonical Level。**

> **5. 一个知识被谁使用，不决定它归谁。**

> **6. 物理目录嵌套不自动等于知识父子关系。**

> **7. 只有自然的语义细分才构成真正的父子知识关系。**

> **8. 子节点可以默认继承父节点的 Capability / Level，但继承来自语义确认，而不是目录本身。**

> **9. 子节点不自动继承父节点全部 Metadata。**

> **10. Evidence、Risk、Status、Preservation 等应针对具体节点独立判断。**

> **11. 父子关系不等于 Level 升级关系。**

> **12. 同一个 Level 下的节点不一定存在父子关系。**

> **13. 跨 Capability 的独立知识不应为了方便而嵌套到另一个 Capability 中。**

> **14. “相关”不等于“子节点”；相关关系优先使用 Wikilink。**

> **15. Level 以下不设置统一的 methods/resources/tools/materials 分类。**

> **16. 简单知识从一个 Markdown 文件开始。**

> **17. 知识形成自然分支后，可以裂变成 `index.md + children`。**

> **18. 节点裂变不自动改变 Level。**

> **19. 目录深度不等于 Level。**

> **20. Wikilink 负责知识网络，不负责替代 Canonical Tree。**

> **21. 同一个 Knowledge Node 只有一个 Canonical 来源。**

> **22. Scenario 是组合入口，不建立第二知识树。**

> **23. Preservation 是派生的保存 / 传播维度，不建立第二事实来源。**

> **24. Git 保存结构变化与知识演化历史。**

> **25. AI 可以提出归属和结构建议，但最终结构由人工 Review 决定。**

最终可以把整个文件系统的核心边界压缩成一句话：

> **目录告诉我们“它暂时放在哪里”，知识语义决定“它真正是什么”，Capability 与 Level 决定“它正式归属于哪里”，Wikilink 决定“它还与什么有关”。**

这使 BeReady 能够在长期增长中保持一个非常重要的性质：

> **文件可以移动、节点可以裂变、目录可以重构，但知识的逻辑身份、能力归属和知识关系不会因为物理整理而混乱。**