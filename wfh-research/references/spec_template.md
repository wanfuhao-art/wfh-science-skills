# BRIEF.md 模板与写法（对齐 ARS Handoff Schema 1）

> wfh-research 共享包 · 2026-11-13
> 位置：`research/<slug>/BRIEF.md`
> 上游：`TERMS.md`、`decisions/LEDGER.md`、`decisions/MDR-*.md`、盘问对话
> 下游：ARS `academic-paper` 普通作者材料 intake（内容参考 Schema 1，入口见共享交接协议）；`wfh-tickets`（claim ledger）
> 原则：**只合成盘问产物，不重新访谈；缺项标 `[UNRESOLVED]`，不猜填。**

---

## 1. 这份文件是什么

`BRIEF.md` 把 `wfh-grill` 已经问定的决策压缩成**外部作者研究材料**，其内容字段参考 ARS Schema 1；它不引入新决策、不重新提问、不写正文。wfh 来源、用户确认、字段值有效与 ARS 已接受是不同状态；标题和四个标签不赋予 ARS 内部 handoff 或已验证身份。准备直接交给 ARS 时，先读 [ars_handoff_protocol.md](ars_handoff_protocol.md)，按来源选入口并预检。

| 写 | 不写 |
|---|---|
| RQ、子问题、FINER、scope | 文献综述 |
| claim ledger（主张—证据—验证—风险） | 正文段落 |
| 方法决策索引（链接 MDR） | MDR 全文 |
| 材料学扩展字段 | 任务图 / 提纲 |
| 未决项与待核验项 | 新的研究建议 |

判断标准：**下游拿到这份文件，能不能不再问「你要研究什么、边界在哪、凭什么说」？** 能，就够；不能，补字段，不是补正文。

---

## 2. 与 ARS Schema 1 的对应

| Schema 1 字段 | 本模板位置 | 来源 | 缺失时 |
|---|---|---|---|
| `research_question` | `## RQ Brief` → **Research Question** | 用户原话；没有原话时由 D01 + D03 + D04 + D05 合成，标「合成自 Dxx」 | `[UNRESOLVED]` |
| `sub_questions` | **Sub-Questions** | RQ 拆解 + D07 + MDR 的「后续影响」 | `[UNRESOLVED]`（少于 2 条视为未填） |
| `finer_scores` | **FINER Scores** | 用户打分（台账 FINER 节或确认时补录） | `[UNRESOLVED]`；**不得 AI 代填** |
| `scope` | **Scope** | 期刊 / 证据来源 / 设计 / 样本 / 局限 / 时间线等决策 + TERMS 的包含 / 排除（台账 ID 以实际为准） | 缺哪轴标哪轴 `[UNRESOLVED]` |

**区分结构与可交接状态**：字段标题与占位存在只能判「结构齐全」；值为 `[UNRESOLVED]` 时仍是「值未决」。Brief 可以经用户确认后保留未决，但交接前由 [ars_handoff_protocol.md §2](ars_handoff_protocol.md) 检查实际值；必需值未决时，wfh 预检报 `HANDOFF_INCOMPLETE` 并停止，不调用 ARS。预检通过也不等于 ARS 已接受；实际 intake 结果另记。

### 2.1 可选字段

`methodology_type`、`theoretical_framework`、`keywords`、`hypothesis`、`exclusion_criteria`、`sub_question_bindings`、`stakeholders`、`ethical_flags`、`socratic_insights`：

- 产物里有明确依据就填；
- 没有就**整行省略**，不标 `[UNRESOLVED]`（可选字段缺失不算未决）；
- 不为了填满而猜。

| 可选字段 | 可接受的来源 |
|---|---|
| `methodology_type` | D05 设计 + D07 分析（qualitative / quantitative / mixed） |
| `theoretical_framework` | 只有用户明确给出才填 |
| `keywords` | 只从 RQ、子问题、TERMS 已出现的概念里选 5–10 个；不引入新概念，不足就少写 |
| `hypothesis` | 只有用户明确给出才填 |
| `exclusion_criteria` | `scope.out_of_scope` 的同义展开 |
| `sub_question_bindings` | 只有子问题的 scope 与父 scope 不同时才填 |
| `stakeholders` | 只有用户明确给出才填 |
| `ethical_flags` | D13 / D14 |
| `socratic_insights` | 只有来自 socratic 对话才填 |

### 2.2 材料学扩展

材料学扩展字段**不属于 Schema 1**，ARS 可忽略。放在独立小节 `## 材料学扩展（ARS 可忽略）`，不塞进 `scope` 四轴。

---

## 3. 模板

```markdown
# <课题标题> — Research Brief

- 课题 slug：<slug>
- 生成：YYYY-MM-DD
- 来源：`TERMS.md`、`decisions/LEDGER.md`、`decisions/MDR-*.md`、盘问对话
- 状态：草稿 / 已确认
- 入口身份：外部作者材料（由 wfh-spec 整理；非 ARS deep-research 产物）
- 字段参考：ARS Schema 1（RQ Brief 内容结构；不声明内部 handoff 已通过）
- ARS 接收状态：尚未调用；用户确认和 wfh 预检结果分别记录

## RQ Brief

> Schema 1 字段：`research_question` · `sub_questions` · `finer_scores` · `scope`

**Research Question**: <一句疑问句；或 [UNRESOLVED]>

**Sub-Questions**:
1. <子问题 1>
2. <子问题 2>

**FINER Scores**: Feasible: <1–5 / [UNRESOLVED]>, Interesting: <1–5 / [UNRESOLVED]>, Novel: <1–5 / [UNRESOLVED]>, Ethical: <1–5 / [UNRESOLVED]>, Relevant: <1–5 / [UNRESOLVED]>
- 评分人：用户（YYYY-MM-DD）
- 阈值检查：平均 <X.X>（≥3.0）；最低 <X>（≥2）→ 通过 / 建议回 wfh-grill

**Scope**:
- In scope: <...>
- Out of scope: <...>
- Domain: <...>
- Timeframe: <...>
- Geography: <...>
- Population: <...>

## 材料学扩展（ARS 可忽略）

| 字段 | 值 | 来源 |
|---|---|---|
| 材料体系 | <... / 不适用（非材料学课题） / [UNRESOLVED]> | <Dxx / MDR-xxxx / TERMS> |
| 电压窗口 | <...> | <...> |
| 倍率 | <...> | <...> |
| 温度 | <...> | <...> |

## 问题陈述

<从读者 / 领域视角：现在缺什么、为什么重要。只写盘问中已确认的内容；不写文献综述。>

## 方案与贡献

- 贡献类型（Dxx）：<理论 / 实证 / 方法 / 复现 / 应用>
- 本文主张什么：<一句话>
- 与现有工作的差异：<用户给出的差异；没有就 [UNRESOLVED]>

## 主张清单（Claim Ledger）

| # | 主张 | 证据状态 | 证据来源 | 验证方式 | 风险 | 溯源 |
|---|---|---|---|---|---|---|
| C1 | <一句话、可证伪> | <已验证 / 部分支持 / 待分析 / 推测 / [UNRESOLVED]> | <数据 / 实验 / 文献 / 用户材料> | <分析 / 实验 / 文献核对> | <最可能让这条主张站不住的因素> | <Dxx / MDR-xxxx / TERMS / 用户原话> |

## 方法决策

| 决策 | 选择 | MDR | 影响章节 |
|---|---|---|---|
| <Dxx 决策名> | <选择> | <MDR-xxxx / —> | <Method / Results / Discussion / Limitations / Response> |

## 验证与证伪

- 全局证伪条件（D12）：<原文照录 / [UNRESOLVED]>
- 逐条主张的证伪信号：
  - C1：<什么结果会推翻它>
- 稳健性 / 替代解释：<来自 D07 / MDR 后续影响 / [UNRESOLVED]>

## 术语

只列索引，不复制定义；定义在 `TERMS.md`。

| 术语 | 状态 | TERMS 行 |
|---|---|---|
| <术语> | 已确认 / 待确认 / 已修订 | <行号或锚点> |

## 未决问题

- [UNRESOLVED] <字段>：<为什么未决；谁能解决（用户 / 实验 / 文献 / 下游）>

## 待核验事实

- [待核验] <事实>：<已查来源 / 为什么没查到>

## 溯源

| Brief 内容 | 来源 |
|---|---|
| RQ | <用户原话 / 合成自 D01、D04、D05> |
| Scope | <D03、D06、D10、TERMS> |
| Claim ledger | <D01、D04、D12、MDR-0001> |
| 材料学扩展 | <D03、MDR-0001、TERMS> |

## 修订记录

| 日期 | 变更 | 原因 |
|---|---|---|
```

---

## 4. 写法规则

### 4.1 `research_question`

- 一句疑问句；不把两个问题塞进一句。
- 与 `scope` 自洽：RQ 提到的对象必须在 `In scope`；`Out of scope` 的内容不得出现在 RQ。
- 优先用用户原话；没有原话时可由 D01 贡献类型 + D03 证据来源 + D04 主张强度 + D05 设计合成，句末标「（合成自 D01、D04、D05）」，并在确认门让用户确认。用户不确认 → `[UNRESOLVED]`。
- 不把方法写进 RQ（反例：「用交叉滞后模型研究……」）。

### 4.2 `sub_questions`

- 2–5 条；每条能被一条主张链独立回答。
- 不把方法写成问题（反例：「如何做回归？」）。
- 与 claim ledger 对应：每条子问题至少对应一条 claim；对应不上就说明子问题切错了，或标 `[UNRESOLVED]`。
- 子问题的 scope 与父 scope 不同时，才填可选字段 `sub_question_bindings`。

### 4.3 `finer_scores`

- 五项各为 1–5 的整数：Feasible / Interesting / Novel / Ethical / Relevant。
- **只来自用户**：AI 不填、不建议、不评价、不排序。用户只给部分 → 其余 `[UNRESOLVED]`。
- 写清评分人与日期；没有日期就写「用户补录，日期未记」。
- 阈值：平均 ≥3.0 且无单项 <2。不达标时写「建议回 wfh-grill」，并列出哪一项低；不改用户的分数。
- 用户在确认门补录时，只接收数字，不提示「一般打几分」。

### 4.4 `scope`

- `In scope` / `Out of scope` 对称：写进 in 的每个对象，out 里要有对应边界。
- `Domain`：学科 / 子领域，来自 D02 期刊或 TERMS。
- `Timeframe`：数据或实验的时间窗；材料学可写循环窗口 / 测试区间；无时间维度写 `N/A（不适用原因）`。
- `Geography`：样本 / 数据来源地；材料学可写 `N/A（不适用原因）` 或实验室范围。
- `Population`：研究对象；材料学写材料体系。
- 六行必须都在；缺哪轴就写 `[UNRESOLVED]`，不留空行。

### 4.5 材料学扩展

| 字段 | 写法 | 反例 |
|---|---|---|
| 材料体系 | 电极 / 电解液 / 对照体系，写清配比与对照 | 「电池材料」——不可判断 |
| 电压窗口 | 上下限 + 参比电极，如 `3.0–4.5 V vs Li/Li⁺` | 「高压」——没有数值 |
| 倍率 | C-rate 与充 / 放条件，如 `0.5C 充放` | 「常规倍率」 |
| 温度 | 数值 + 单位，如 `25 °C 与 45 °C` | 「室温」——未给数值 |

- 值来自证据来源、设计、测试条件（电压 / 倍率 / 温度）等决策，以及 MDR / TERMS；台账 ID 以实际为准。没有就 `[UNRESOLVED]`，不猜电压窗口、倍率或温度。
- 非材料学课题：四项都写「不适用（非材料学课题）」，并在「来源」列写依据（D02 学科 / 期刊）。
- 不把材料学字段塞进 `scope` 四轴；`scope.Population` 可写材料体系，但四字段仍单独列。

### 4.6 claim ledger

- 每条主张必须能溯源到 Dxx / MDR / TERMS / 用户原话；**无来源的主张不得写入**，放进「未决问题」。
- 主张强度与 D04 一致：D04 是关联，就不能写因果主张；D04 是描述，就不能写机制断言。
- 证据状态用固定词：`已验证` / `部分支持` / `待分析` / `推测` / `[UNRESOLVED]`。
- 验证方式必须可执行：分析、实验、文献核对；不写「进一步研究」。
- 风险写具体失效模式（样本量不足、无法排除共同原因、仪器检出限），不写「可能有问题」。
- 至少 1 条；一条都提取不出 → 整表标 `[UNRESOLVED]` 并说明原因。

### 4.7 方法决策

- 只做索引：决策 / 选择 / MDR 编号 / 影响章节。
- 不复制 MDR 的选项、理由、证据；读者去读 MDR。
- 没有 MDR 的决策只写台账行，MDR 列填 `—`。

### 4.8 验证与证伪

- 全局证伪条件来自 D12，**原文照录**，不改写、不加强、不弱化。
- 每条 claim 写一句「什么结果会推翻它」；写不出就标 `[UNRESOLVED]`。
- 稳健性 / 替代解释来自 D07 / MDR 的「后续影响」；没有就标 `[UNRESOLVED]`。

### 4.9 未决问题

- 正文中每个未决**字段**都必须在这里汇总；同一字段的多处占位（如 FINER 五项）算一条，不重复列。
- 每条写清：哪个字段、为什么未决、谁能解决（用户 / 实验 / 文献 / 下游 ARS）。
- 不写「待补充」「待定」这种无信息量的条目。

### 4.10 待核验事实

- 从 TERMS / MDR / LEDGER 原样带入 `[待核验]`。
- 不升级为确定结论，不删除；核验后才改成具体来源。
- 写清已查来源与为什么没查到。

### 4.11 溯源

- 每个 Brief 段落对应哪些 Dxx / MDR / TERMS / 用户原话。
- 合成内容标「合成」；用户补录标「用户补录 YYYY-MM-DD」。
- 溯源是 BRIEF 的审计线索：任何一句都能回到盘问产物。

---


## 5. 示例

需要填好的合成示例时读 [方案示例](spec_examples.md)；示例只演示格式，不是真实数据或真实确认。

---

## 6. 维护规则

1. **追加不覆盖。** 决策修订后更新对应段落，并在「修订记录」写变更与原因；不静默改。
2. **冲突以 `LEDGER.md` 为准。** TERMS / MDR / 台账三者不一致时，列出冲突（字段 / 两个值 / 各自来源），请用户裁决；不以「较新」「较详细」为由自行选一个。
3. **`[UNRESOLVED]` 与 `[待核验]` 不删。** 解决后改成具体值或来源，并在修订记录留痕。
4. **不膨胀。** 方法细节在 MDR，术语定义在 TERMS；BRIEF 只做索引与摘要。超过约 250 行时检查是否把正文或综述搬了进来。
5. **状态流转。** `草稿` → `已确认`；决策被推翻时回到 `草稿` 并重开相关段落。
6. **与上游交叉核对。** 发现 Brief 与 TERMS / MDR 用法不一致，立即提出，不静默改上游。
