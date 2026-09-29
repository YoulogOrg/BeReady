---
id: 8cb55655-936b-4935-9f98-f8ec1d810273
created_at: 2026-09-17T11:28:15+08:00
updated_at: 2026-09-17T11:28:18+08:00
---


# BeReady 文件组织与知识节点管理规范

> 本文是《BeReady 内容架构设计》的补充规范。
>
> 原始文档解决的是“BeReady 应该如何组织知识”；
> 本文进一步解决：
>
> - 知识如何落到文件系统
> - 分支如何长期增长
> - 什么时候应该拆分节点
> - Markdown 文件与目录如何演化
> - Wikilink 如何管理跨树关系
> - Preservation 如何与知识主树分离
>
> 本文不改变原有的核心内容模型。

---

# 1. 总体原则

BeReady 的知识体系采用：

> **能力 → Level → 知识**

作为稳定的认知模型。

文件系统则采用：

> **可自然生长的 Markdown 树**

作为知识的物理组织方式。

Wikilink 负责：

> **连接不同知识节点。**

Git 负责：

> **保存知识的长期演化历史。**

Metadata 负责：

> **描述知识节点的状态、属性和传播要求。**

Preservation 负责：

> **决定知识如何被保存、打包和传播。**

因此：

```text
用户认知
    │
    └── 能力
          │
          └── Level
                │
                └── 知识
                      │
                      └── 子知识
```

对应：

```text
物理存储
    │
    └── Markdown 文件树
              │
              └── Wikilink 网络
```

外围再增加：

```text
Git
Metadata
Preservation
```

---

# 2. Canonical Tree：唯一知识主树

BeReady 必须存在一棵唯一的：

> **Canonical Knowledge Tree**

即知识的正式归属树。

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

其中每一个一级目录代表一个核心能力。

例如：

```text
capabilities/
└── water/
```

代表：

> 水这一项生存能力。

---

# 3. Capability 是主干

Capability 是整个知识树最稳定的一层。

例如：

```text
water
food
fire
shelter
safety
```

这些节点不应该因为内部知识增长而改变。

例如：

```text
water/
```

下面可以从几十个文件增长到数千个文件，但：

```text
water
```

仍然是同一个能力。

因此：

> **Capability 是长期稳定的知识主干。**

---

# 4. Level 是第二层稳定结构

每个 Capability 下，根据原始架构采用：

```text
L1
L2
L3
...
Ln
```

表示能力的发展。

例如：

```text
water/
├── L1/
├── L2/
├── L3/
├── L4/
└── L5/
```

Level 的含义保持原始架构中的定义：

> L1 是最低可行能力，随着 Level 提高，知识、技术、资源需求和自主能力逐渐增加。

Level 的数量不要求所有 Capability 一致。

例如：

```text
water/
├── L1
├── L2
├── L3
├── L4
└── L5
```

而另一项能力可能只有：

```text
fire/
├── L1
├── L2
└── L3
```

不得为了目录结构整齐而人为补充不存在的 Level。

---

# 5. Level 以下不再规定固定分类

这是本规范最重要的原则之一。

不要规定：

```text
L3/
├── methods/
├── resources/
├── tools/
├── materials/
└── principles/
```

作为所有 Level 的统一目录结构。

原因是：

> Resource、Tool、Material、Evidence 等已经属于知识关系或 Metadata，而不是用户理解知识的主分类。

因此 Level 以下应该：

> **让知识本身自然形成分支。**

例如：

```text
water/
└── L3/
    ├── boiling.md
    ├── filtration.md
    ├── disinfection.md
    └── storage.md
```

这是最初、最简单的状态。

---

# 6. 知识节点可以自然裂变

当某一个知识开始包含大量独立知识时，可以从：

```text
filtration.md
```

演化成：

```text
filtration/
├── index.md
├── ceramic.md
├── sand.md
├── charcoal.md
└── membrane.md
```

这称为：

> **Node Expansion / 节点扩展**

它不是重新分类，而是一个知识节点从简单状态成长为复杂状态。

因此：

```text
filtration.md
```

与：

```text
filtration/
├── index.md
├── ceramic.md
└── sand.md
```

在知识模型上属于同一个节点。

---

# 7. index.md 是聚合节点的正式入口

当一个 Markdown 文件扩展成目录时：

```text
filtration/
```

必须拥有：

```text
filtration/index.md
```

`index.md` 是该知识节点本身，而不是单纯的目录说明。

例如：

```markdown
# 过滤

过滤是处理水中悬浮物及特定污染物的一类方法。

## 方法

- [[陶瓷过滤]]
- [[砂滤]]
- [[活性炭]]
- [[膜过滤]]

## 相关能力

[[沉淀]]
[[消毒]]
[[储水]]
```

因此：

```text
filtration/index.md
```

应该回答：

> “过滤是什么，以及这个知识节点下面有哪些进一步知识？”

---

# 8. 文件节点与目录节点是同一种知识对象

一个 Node 可以有两种物理形态：

## 简单节点

```text
boiling.md
```

## 聚合节点

```text
filtration/
├── index.md
├── ceramic.md
└── sand.md
```

二者都属于 Knowledge Node。

区别只在于：

```text
简单节点
    ↓
当前内容足够简单

聚合节点
    ↓
内容已经形成独立分支
```

而不是两种不同的数据类型。

---

# 9. 节点裂变的判断标准

不应该使用严格的：

> “超过 N 个文件就必须拆分”

作为规则。

更合理的判断标准是：

> **当前节点的直接子节点是否仍然容易理解和浏览？**

可以使用一个软性参考：

```text
少量节点
    ↓
直接展开

节点开始明显增多
    ↓
观察是否形成自然群组

大量节点
    ↓
通常应该形成子节点
```

例如：

```text
L3/
├── boiling.md
├── filtration.md
├── disinfection.md
└── storage.md
```

非常容易理解。

当过滤继续增长：

```text
filtration/
├── ceramic.md
├── sand.md
├── charcoal.md
├── membrane.md
├── cloth.md
├── gravity.md
├── cartridge.md
└── ...
```

如果这些内容已经具有自己的结构，就应该进一步形成：

```text
filtration/
├── index.md
├── ceramic.md
├── sand.md
├── charcoal.md
└── membrane/
    ├── index.md
    ├── materials.md
    ├── construction.md
    └── maintenance.md
```

---

# 10. 不应该为了整理而增加目录层级

目录增加必须有知识上的理由。

不推荐：

```text
water/
└── L3/
    └── methods/
        └── purification/
            └── filtration/
                └── ceramic/
```

这种结构主要是在满足管理者的分类欲望，而不是表达知识关系。

更推荐：

```text
water/
└── L3/
    └── filtration/
        ├── ceramic.md
        ├── sand.md
        └── membrane.md
```

原则：

> **只有知识本身发生了新的分叉，才增加目录层级。**

---

# 11. 一个节点最多只表达一个自然概念

目录结构应该尽量对应人的自然理解。

例如：

```text
water
→ filtration
→ ceramic filtration
```

比：

```text
water
→ methods
→ purification
→ mechanical
→ ceramic
```

更容易理解。

目录名应该尽量使用普通用户能够理解的概念，而不是数据库式分类名。

---

# 12. 节点裂变不能破坏 WikiLink

这是文件系统长期演化最重要的保障机制之一。

例如最初：

```text
water/L3/filtration.md
```

其他内容引用：

```markdown
[[过滤]]
```

后来变成：

```text
water/L3/filtration/
├── index.md
├── ceramic.md
└── sand.md
```

原来的：

```markdown
[[过滤]]
```

仍然必须指向：

```text
filtration/index.md
```

而不是要求所有引用者修改路径。

因此：

> **Wikilink 应该引用知识节点，而不是依赖物理文件路径。**

物理结构可以变化：

```text
filtration.md
       ↓
filtration/index.md
```

逻辑节点仍然是：

```text
过滤
```

---

# 13. WikiLink 的基本职责

Wikilink 主要承担：

> **跨树连接。**

例如：

```markdown
[[过滤]]
[[容器]]
[[火]]
[[储水]]
[[滤材]]
```

这些链接不意味着目标必须位于当前目录附近。

例如：

```text
water/L3/filtration/
```

可以链接到：

```text
tools/containers/
materials/charcoal/
fire/fuel/
```

因此：

```text
目录树
    ↓
归属

WikiLink
    ↓
关系
```

---

# 14. 不要用 Wikilink 代替目录

虽然 Wikilink 能够建立网络，但不能因此让所有知识都处于平面结构：

```text
all/
├── water.md
├── filtration.md
├── ceramic.md
├── sand.md
├── charcoal.md
├── ...
```

这种结构会失去：

> “这个知识属于什么能力、什么 Level？”

因此：

> **Wikilink 是关系层，不是主导航层。**

---

# 15. 新知识进入系统时的判断流程

以后增加一个知识节点，可以使用以下判断：

```text
新知识
  │
  ├─ 是一个独立的核心能力？
  │       ↓
  │   新 Capability
  │
  ├─ 是某个能力的发展阶段？
  │       ↓
  │   对应 Level
  │
  ├─ 是当前节点的具体知识？
  │       ↓
  │   当前节点下新增子节点
  │
  └─ 只是与已有知识存在关系？
          ↓
      Wikilink
```

这可以成为贡献者最基本的内容组织规则。

---

# 16. 避免重复知识

如果一个知识已经存在：

```text
tools/containers/
```

那么水相关内容不要再创建：

```text
water/L3/filtration/container.md
```

而应该：

```markdown
需要：

[[容器]]
```

如果需要补充水场景下的特殊条件，可以在当前知识中说明：

```markdown
在过滤过程中，容器需要满足……

参见：

[[容器]]
```

因此：

> **能力归属只能有一个正式位置，跨能力使用通过 Wikilink 完成。**

---

# 17. Resource 不重新成为目录分类

原始架构已经确定：

> Resource 主要存在于知识关系中，而不是主要用户导航维度。

因此：

```text
过滤
 ├── 需要 → 容器
 ├── 需要 → 滤材
 └── 需要 → 水源
```

优先表达为：

```markdown
[[容器]]
[[滤材]]
[[水源]]
```

而不是：

```text
filtration/
└── resources/
    ├── container.md
    ├── filter-material.md
    └── water-source.md
```

除非未来某类资源本身已经发展成独立的知识体系。

---

# 18. 一个知识可以被多个能力引用

例如：

```text
tools/container.md
```

可以被：

```text
water
food
fire
hygiene
```

多个能力引用。

但物理上仍然只有：

```text
tools/container.md
```

一份。

形成：

```text
water ───────┐
food ────────┤
fire ────────┼──→ [[容器]]
hygiene ─────┘
```

这样能够避免知识复制。

---

# 19. Scenario 不建立第二套知识树

Scenario 仍然按照原始架构定位为：

> 组合型入口。

例如：

```text
scenarios/
├── earthquake.md
├── blackout.md
├── water-outage.md
└── supply-disruption.md
```

其中：

```markdown
# 停水

需要优先关注：

[[水]]
[[卫生]]
[[食物]]
[[安全]]
```

Scenario 不复制：

```text
scenarios/water/
scenarios/food/
scenarios/hygiene/
```

否则最终会产生两套甚至多套知识树。

---

# 20. 推荐的完整目录

在前期，可以保持非常简单：

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

随着知识增长：

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
    ├── containers.md
    └── tanks.md
```

自然演化。

---

# 21. 推荐的 Frontmatter

每个正式知识节点使用统一 Frontmatter：

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

建议最初保持字段少而稳定。

核心字段：

| 字段 | 用途 |
|---|---|
| `title` | 节点名称 |
| `capability` | 所属能力 |
| `level` | 所属 Level |
| `status` | 验证状态 |
| `preservation` | 保存优先级 |
| `tags` | 辅助检索 |

不要为了未来可能的需求一次加入大量字段。

---

# 22. Metadata 不取代目录

例如：

```yaml
capability: water
level: L3
```

用于机器理解和校验。

但用户看到：

```text
capabilities/water/L3/
```

仍然可以直接理解这个节点的归属。

因此：

> **目录提供人的直觉理解，Metadata 提供机器的结构理解。**

两者应该同时存在，而不是互相替代。

---

# 23. 可以增加结构校验机制

由于整个系统基于 Markdown 文件，因此非常适合通过工具自动检查。

例如 CI / AI Organizer 可以检查：

### Capability 校验

```text
每个节点是否属于一个 Capability？
```

### Level 校验

```text
Level 是否合法？
```

### 父子关系校验

```text
water/L3/filtration/
```

是否确实属于：

```text
water → L3
```

### Wikilink 校验

检查：

```text
[[过滤]]
```

是否存在。

### 重复节点检测

发现：

```text
water/L3/filtration.md
```

和：

```text
water/L3/filtering.md
```

可能表达同一个知识。

### 孤立节点检测

发现没有任何入口或引用的知识。

---

# 24. AI 可以成为“组织维护器”

原始架构已经把 AI 定位为 Organizer、Knowledge Gap Finder、Link Agent 等维护工具。

在文件树管理中，可以进一步用于：

```text
AI
 │
 ├── 新节点归属建议
 ├── Level 建议
 ├── 重复检测
 ├── 子节点拆分建议
 ├── Wikilink 建议
 ├── 孤立节点检测
 └── 目录膨胀提醒
```

例如：

> `water/L3/` 当前有 46 个直接节点，其中 18 个属于过滤相关知识，建议考虑将 `filtration` 从单文件扩展为聚合节点。

但：

> **AI 只能提出结构建议，不能自行改变 Canonical Tree。**

最终仍通过：

```text
Draft
 ↓
Review
 ↓
Git PR
 ↓
Merge
```

完成。

---

# 25. Preservation 不属于 Canonical Tree

Canonical Tree 是：

```text
知识应该住在哪里
```

Preservation 是：

```text
知识应该保存和传播到什么程度
```

二者必须分开。

因此不建议：

```text
P0/
P1/
P2/
P3/
```

作为第二套正式知识分类。

更推荐：

```text
Canonical Tree
      │
      ↓
Preservation Metadata
      │
      ↓
构建 / 筛选
      │
      ├── Essential Pack
      ├── Offline Pack
      ├── Survival Pack
      ├── Resilience Pack
      └── Rebuild Pack
```

---

# 26. Preservation 可以驱动物理存储区域

如果未来确实需要独立的 Preservation 存储区域，可以产生：

```text
preservation/
├── P0-essential/
├── P1-survival/
├── P2-resilience/
└── P3-rebuild/
```

但这里的内容应该被理解为：

> **Canonical Tree 的保存视图 / 分发视图。**

而不是新的事实来源。

---

# 27. 同一个知识不应该存在两个事实来源

例如：

```text
capabilities/water/L1/drinking-water.md
```

是唯一正式来源。

如果它属于 P0：

```text
preservation/P0-essential/...
```

不应该再被人工维护一份独立 Markdown。

否则：

```text
Source A
Source B
```

最终一定会发生版本不一致。

原则：

> **Canonical Tree 只有一份；Preservation 可以有多个派生版本。**

---

# 28. Preservation 的生成应该尽可能自动化

例如：

```yaml
preservation: P0
```

构建系统自动：

```text
Canonical Tree
      ↓
读取 preservation
      ↓
选择节点
      ↓
解析 Wikilink
      ↓
补齐必要依赖
      ↓
生成 Pack
```

这样一个：

```text
P0 Essential
```

不一定只是简单复制所有 `P0` 节点。

未来甚至可以处理：

```text
A
 ↓
需要 B
 ↓
B 也必须进入 Pack
```

形成一个真正可用的最小知识集合。

---

# 29. 最重要的长期保障：不要让目录成为知识关系的唯一表达

最终模型应该是：

```text
                  Knowledge Graph
                       ▲
                       │
                 Wikilink / Relation
                       │
                       │
Canonical Tree ─────────┘
     │
     ├── Capability
     │      │
     │      └── Level
     │             │
     │             └── Knowledge Tree
     │
     └── Markdown
            │
            └── Git
```

目录树表达：

> **主要归属关系。**

Wikilink 表达：

> **语义关系。**

这两者共同构成 BeReady 的知识结构。

---

# 30. 最终的节点增长模型

一个知识节点的生命周期可以理解为：

```text
                    新知识
                       │
                       ↓
                  一个 Node
                       │
                ┌──────┴──────┐
                │             │
             内容简单       内容增长
                │             │
                ↓             ↓
             node.md      node/
                              │
                              ├── index.md
                              │
                              ├── child A
                              ├── child B
                              └── child C
                                      │
                              某个 Child 再增长
                                      │
                                      ↓
                                  child/
```

因此：

> **树不是一次设计完成的，而是知识增长留下的痕迹。**

---

# 31. 三个永远不应该改变的东西

即使 BeReady 从：

```text
100 节点
```

增长到：

```text
10,000 节点
```

甚至：

```text
100,000 节点
```

以下三个概念仍然保持稳定：

```text
Capability
    ↓
Level
    ↓
Knowledge
```

用户仍然可以：

```text
水
 ↓
L1
 ↓
L2
 ↓
L3
 ↓
过滤
 ↓
陶瓷过滤
```

内部的物理文件结构可以越来越复杂，但用户的基本理解不应该被迫改变。

---

# 32. 最终规则摘要

BeReady 文件组织可以浓缩为：

> **1. Capability 是主干。**

```text
water
food
fire
...
```

> **2. Level 是能力发展的稳定纵轴。**

```text
L1 → L2 → L3 → ... → Ln
```

> **3. Level 以下不设置固定分类。**

让知识自然生长。

> **4. 一个简单知识首先是 Markdown 文件。**

```text
filtration.md
```

> **5. 一个知识膨胀后，可以自然变成目录节点。**

```text
filtration/
├── index.md
└── ...
```

> **6. index.md 是聚合节点本身。**

> **7. 节点拆分必须来自知识自然分叉，而不是为了整理文件。**

> **8. Wikilink 负责跨树关系，不负责主分类。**

> **9. 同一个知识只保留一个 Canonical 来源。**

> **10. Resource、Tool、Material 等优先作为关系存在，不重新制造分类树。**

> **11. Scenario 是组合入口，不复制知识。**

> **12. Metadata 用于机器理解和自动校验。**

> **13. AI 可以建议整理，但不能成为最终结构决策者。**

> **14. Git 保存所有结构和内容变化。**

> **15. Preservation 是独立维度，是知识的保存与传播视图。**

> **16. Preservation Pack 从 Canonical Tree 自动生成，不成为第二套事实来源。**

---

# 33. 最终模型

```text
                         BeReady
                            │
                    ┌───────┴───────┐
                    │               │
              用户理解模型       系统存储模型
                    │               │
                Capability       Markdown Tree
                    │               │
                  Level         ┌────┴────┐
                    │           │         │
                 Knowledge    文件       目录
                    │           │         │
                子知识 ────────┴─────────┘
                    │
                    ↓
                 Wikilink
                    │
                    ↓
               Knowledge Graph


        ┌─────────────────────────────────┐
        │             Metadata             │
        │ Level / Status / Evidence / P   │
        └────────────────┬────────────────┘
                         │
                         ↓
                  Preservation
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
       Essential       Offline       Full Pack
          │
          ↓
       保存 / 传播


                         │
                         ↓
                        Git
                         │
              持续修改 / Review / PR
```

最终原则：

> **用树管理“知识在哪里”，用 Wikilink 管理“知识之间有什么关系”，用 Metadata 管理“知识是什么状态”，用 Git 管理“知识如何变化”，用 Preservation 管理“知识如何被保存和传播”。**

这套模型的目标不是让文件系统看起来最漂亮，而是保证：

> **今天的几十个节点，可以自然长成明天的几千个节点，而用户仍然用今天的方式理解它。**