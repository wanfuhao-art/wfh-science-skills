# BRIEF.md 科研方案模板与写法

> wfh-research 共享包 · 2026-11-13
> 位置：`research/<slug>/BRIEF.md`
> 上游：`TERMS.md`、`decisions/LEDGER.md`、`decisions/MDR-*.md`、盘问对话
> 下游：ARS `academic-paper` 普通作者材料 intake（按当前模式交接，见共享交接协议）；`wfh-tickets`（claim ledger）
> 原则：**只合成盘问产物，不重新访谈；缺项标 `[UNRESOLVED]`，不猜填。**

---

## 1. 这份文件是什么

`BRIEF.md` 把 `wfh-grill` 已经问定的决策压缩成**科研方案与外部作者研究材料**，以问题、主张、证据、验证为骨架，按需保留兼容 RQ 字段；它不引入新决策、不重新提问、不写正文。wfh 来源、用户确认、字段值有效与 ARS 已接受是不同状态；标题和兼容字段不赋予 ARS 内部 handoff 或已验证身份。准备直接交给 ARS 时，先读 [ars_handoff_protocol.md](ars_handoff_protocol.md)，按来源选入口并预检。

| 写 | 不写 |
|---|---|
| RQ、适用子问题、scope；契约要求时的 FINER | 文献综述 |
| claim ledger（主张—证据—验证—风险） | 正文段落 |
| 方法决策索引（链接 MDR） | MDR 全文 |
| 适用的研究类型扩展字段 | 任务图 / 提纲 |
| 未决项与待核验项 | 新的研究建议 |

判断标准：**下游拿到这份文件，能不能不再问「你要研究什么、边界在哪、凭什么说」？** 能，就够；不能，补字段，不是补正文。

生成入口为独立 `/wfh-spec`，或默认 `/wfh` 按 [动作分派](dispatch_protocol.md) §3.1 收到明确方案生成请求后复用 [方案整理实现](../../wfh-spec/SKILL.md)。单独 `/wfh-grill` 只保存讨论记录，不生成本方案。自动与手动整理共用本模板，保持 BRIEF.md 路径、`## RQ Brief` 及本次契约所需字段；阅读说明用中文，不用另建中文文件或替换字段来实现可读性。新增含义或冲突仍回到作者确认。来源清单只列实际使用的记录；没有适用术语或重要决定时省略相应索引，不链接不存在的 TERMS / MDR。

**显式草稿分支**：作者要求先整理草稿时，可基于有来源的未确认讨论 / 材料合成；逐项标明待确认、来源与冲突，未知值仍写未决，不虚构台账或确认日期。下文“已确认内容”要求用于正式方案；草稿允许呈现清楚标注的候选，不能将其写成作者已确认或证据已支持。草稿不替代已有正式方案，不将阶段 1–2 或步骤安排标完成、不放行生产；保存与进度遵守 flow_details 的草稿分支。

---

## 2. 与 ARS Schema 1 的对应

保留 `## RQ Brief` 及兼容字段，便于已有读取器复用；Brief 本身不无条件要求完整 Schema 1。实际交接先读 [ars_handoff_protocol.md](ars_handoff_protocol.md)，按来源、当前模式与任务契约准备必需输入，记录真实预检和 intake 结果，不将四字段升级为所有任务的统一门。

| 兼容字段 | 来源与收集条件 |
|---|---|
| `research_question` | 作者原话或已确认合成；引用 research_question 及相关 key + 真实 ID |
| `sub_questions` | 有助于拆解问题时记录；具体数量要求按目标契约 |
| `finer_scores` | 仅当前任务契约要求时收集；保留原作者评分及来源，AI 建议另列 |
| `scope` | 已确认研究边界；具体轴按研究类型和当前契约 |

适用必需项缺失标 `[UNRESOLVED]`；未启用的可选字段省略。用户确认、值有效、wfh 预检通过与 ARS 实际接受分别记录。必需缺项只影响对应动作，不以无关未决项阻断当前任务。

### 2.1 可选字段

`methodology_type`、`theoretical_framework`、`keywords`、`hypothesis`、`exclusion_criteria`、`sub_question_bindings`、`stakeholders`、`ethical_flags`、`socratic_insights`：

- 产物里有明确依据就填；
- 没有就**整行省略**，不标 `[UNRESOLVED]`（可选字段缺失不算未决）；
- 不为了填满而猜。

| 可选字段 | 可接受的来源 |
|---|---|
| `methodology_type` | research_design + analysis_strategy（实际 ID；含定性 / 定量 / 混合 / 理论 / 计算等） |
| `theoretical_framework` | 只有作者给出或明确确认才填 |
| `keywords` | 只从 RQ、子问题、TERMS 已出现的概念里选 5–10 个；不引入新概念，不足就少写 |
| `hypothesis` | 只有作者给出或明确确认才填 |
| `exclusion_criteria` | `scope.out_of_scope` 的同义展开 |
| `sub_question_bindings` | 只有子问题的 scope 与父 scope 不同时才填 |
| `stakeholders` | 只有作者给出或明确确认才填 |
| `ethical_flags` | ethics 及相关实际 ID |
| `socratic_insights` | 只有来自 socratic 对话才填 |

### 2.2 材料学扩展

仅材料课题需要时才出现本节。材料学扩展字段**不属于 Schema 1**，ARS 可忽略。放在独立小节 `## 材料学扩展（ARS 可忽略）`，不塞进 `scope` 四轴。

---

## 3. 模板

```markdown
# <课题标题> — Research Brief

- 课题 slug：<slug>
- 生成：YYYY-MM-DD
- 来源：`TERMS.md`、`decisions/LEDGER.md`、`decisions/MDR-*.md`、盘问对话
- 状态：草稿 / 已确认
- 入口身份：外部作者材料（由 wfh-spec 整理；非 ARS deep-research 产物）
- 字段参考：按需兼容 RQ Brief；交接模式：<实际模式 / 尚未选择>
- ARS 接收状态：尚未调用；用户确认和 wfh 预检结果分别记录

## 研究概览

<用中文简述研究问题、价值、主张边界、证据路线和验证办法；只复述已确认内容。>
<说明当前缺什么、由谁补充及影响哪一步；确认方案不等于主张已获支持。>

## RQ Brief

> 下列子问题、FINER 与范围轴按适用性及当前任务契约保留；扩展小节仅适用时出现。

**Research Question**: <一句疑问句；或 [UNRESOLVED]>

**Sub-Questions**:
1. <子问题 1>
2. <子问题 2>

**FINER Scores**: Feasible: <原作者值 / [UNRESOLVED]>, Interesting: <原作者值 / [UNRESOLVED]>, Novel: <原作者值 / [UNRESOLVED]>, Ethical: <原作者值 / [UNRESOLVED]>, Relevant: <原作者值 / [UNRESOLVED]>
- 作者原评分、评分人、日期与来源：<原值与出处；缺失如实标记>
- AI 评分建议（可选）：<建议值、来源、限制；与作者自评分列>

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
| 材料体系 | <... / [UNRESOLVED]> | <decision_key（真实 Dxx） / MDR-xxxx / TERMS> |
| 电压窗口 | <...> | <...> |
| 倍率 | <...> | <...> |
| 温度 | <...> | <...> |

## 问题陈述

<从读者 / 领域视角：现在缺什么、为什么重要。只写盘问中已确认的内容；不写文献综述。>

## 方案与贡献

- 贡献类型（contribution，实际 ID）：<理论 / 实证 / 方法 / 复现 / 应用>
- 本文主张什么：<一句话>
- 与现有工作的差异：<用户给出的差异；没有就 [UNRESOLVED]>

## 主张清单（Claim Ledger）

| # | 主张 | 证据状态 | 证据来源 | 验证方式 | 风险 | 溯源 |
|---|---|---|---|---|---|---|
| C1 | <明确范围、可检验或可论证> | <已验证 / 部分支持 / 待分析 / 推测 / [UNRESOLVED]> | <数据 / 实验 / 文献 / 用户材料> | <分析 / 实验 / 文献核对 / 论证 / 反例 / 可信度检查> | <最可能让这条主张站不住的因素> | <decision_key（真实 Dxx） / MDR-xxxx / TERMS / 用户原话> |

## 方法决策

| 决策 | 选择 | MDR | 影响章节 |
|---|---|---|---|
| <decision_key（真实 Dxx）决策名> | <选择> | <MDR-xxxx / —> | <Method / Results / Discussion / Limitations / Response> |

## 验证与证伪

- 适用的全局验证 / 证伪条件（validation，实际 ID）：<原文照录 / [UNRESOLVED]>
- 逐条主张的证伪信号：
  - C1：<什么结果会推翻它>
- 稳健性 / 替代解释：<来自 analysis_strategy（实际 ID） / MDR 后续影响 / [UNRESOLVED]>

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
| RQ | <用户原话 / research_question 及相关 key（真实 ID）> |
| Scope | <evidence_source / research_design 等（真实 ID）、TERMS> |
| Claim ledger | <contribution / claim_strength / validation（真实 ID）、MDR-0001> |
| 材料学扩展 | <evidence_source（真实 ID）、MDR-0001、TERMS> |

## 修订记录

| 日期 | 变更 | 原因 |
|---|---|---|
```

---

## 4. 写法规则

### 4.1 `research_question`

- 一句疑问句；不把两个问题塞进一句。
- 与 `scope` 自洽：RQ 提到的对象必须在 `In scope`；`Out of scope` 的内容不得出现在 RQ。
- 优先用用户原话；没有原话时可由 contribution、evidence_source、claim_strength、research_design 等已确认内容合成，标 key + 真实 ID，并在确认门让用户确认。用户不确认 → `[UNRESOLVED]`。
- 不把方法写进 RQ（反例：「用交叉滞后模型研究……」）。

### 4.2 `sub_questions`

- 按问题需要拆解；每条能被一条主张链独立回答，数量要求以当前交接契约为准。
- 不把方法写成问题（反例：「如何做回归？」）。
- 与 claim ledger 对应：每条子问题至少对应一条 claim；对应不上就说明子问题切错了，或标 `[UNRESOLVED]`。
- 子问题的 scope 与父 scope 不同时，才填可选字段 `sub_question_bindings`。

### 4.3 `finer_scores`

- 仅当前任务契约确需时收集五项；格式与阈值读取当前 ARS 模式原文，不在此硬编码。
- 原作者值、评分人、日期和来源保留；部分缺失如实标 `[UNRESOLVED]`，不补造作者自评。
- AI 可另列有来源的建议值、理由和限制；作者采纳也不能覆盖原评分或改写其来源。

### 4.4 `scope`

- `In scope` / `Out of scope` 对称：写进 in 的每个对象，out 里要有对应边界。
- `Domain`：学科 / 子领域，来自研究领域记录、publication_target（实际 ID）或 TERMS。
- `Timeframe`：数据或实验的时间窗；材料学可写循环窗口 / 测试区间；无时间维度写 `N/A（不适用原因）`。
- `Geography`：样本 / 数据来源地；材料学可写 `N/A（不适用原因）` 或实验室范围。
- `Population`：研究对象；材料学写材料体系。
- 按研究与当前契约保留适用轴；契约要求但不适用的轴写 `N/A（原因）`，必需但未知的轴写 `[UNRESOLVED]`。

### 4.5 材料学扩展

| 字段 | 写法 | 反例 |
|---|---|---|
| 材料体系 | 电极 / 电解液 / 对照体系，写清配比与对照 | 「电池材料」——不可判断 |
| 电压窗口 | 上下限 + 参比电极，如 `3.0–4.5 V vs Li/Li⁺` | 「高压」——没有数值 |
| 倍率 | C-rate 与充 / 放条件，如 `0.5C 充放` | 「常规倍率」 |
| 温度 | 数值 + 单位，如 `25 °C 与 45 °C` | 「室温」——未给数值 |

- 值来自证据来源、设计、测试条件（电压 / 倍率 / 温度）等决策，以及 MDR / TERMS；台账 ID 以实际为准。没有就 `[UNRESOLVED]`，不猜电压窗口、倍率或温度。
- 非材料学课题省略整节；材料课题也只保留适用字段，不为填模板制造未决项。
- 不把材料学字段塞进 `scope` 四轴；`scope.Population` 可写材料体系，适用扩展另列。

### 4.6 claim ledger

- 每条主张必须能溯源到 decision_key（真实 Dxx） / MDR / TERMS / 用户原话；**无来源的主张不得写入**，放进「未决问题」。
- 与 claim_strength（真实 ID）确认的主张范围一致；关联证据不能直接写成因果或机理已成立。理论与定性主张按论证前提、解释范围及可信度限定。
- 证据状态用固定词：`已验证` / `部分支持` / `待分析` / `推测` / `[UNRESOLVED]`。
- 验证方式须具体：分析、实验、文献核对、证明、反例、负例或可信度检查；按研究类型选用。
- 风险写具体失效模式（样本量不足、无法排除共同原因、仪器检出限），不写「可能有问题」。
- 至少 1 条；一条都提取不出 → 整表标 `[UNRESOLVED]` 并说明原因。

### 4.7 方法决策

- 只做索引：决策 / 选择 / MDR 编号 / 影响章节。
- 不复制 MDR 的选项、理由、证据；读者去读 MDR。
- 没有 MDR 的决策只写台账行，MDR 列填 `—`。

### 4.8 验证与证伪

- 全局验证 / 证伪条件来自 validation（真实 ID），原文照录；理论或定性可采用论证前提、反例与可信度条件。
- 每条 claim 写清何种证据、反例或可信度缺口会削弱或推翻它；适用但未定时标 `[UNRESOLVED]`。
- 稳健性 / 替代解释来自 analysis_strategy（真实 ID） / MDR 的「后续影响」；没有就标 `[UNRESOLVED]`。

### 4.9 未决问题

- 正文中每个未决**字段**都必须在这里汇总；同一字段的多处占位（如 FINER 五项）算一条，不重复列。
- 每条写清：哪个字段、为什么未决、谁能解决（用户 / 实验 / 文献 / 下游 ARS）。
- 不写「待补充」「待定」这种无信息量的条目。

### 4.10 待核验事实

- 从 TERMS / MDR / LEDGER 原样带入 `[待核验]`。
- 不升级为确定结论，不删除；核验后才改成具体来源。
- 写清已查来源与为什么没查到。

### 4.11 溯源

- 每个段落引用 decision_key + 真实 Dxx / MDR / TERMS / 用户原话；Dxx 只标身份。旧台账无 key 按标题和内容映射，歧义待确认，不猜 D04 含义、不批量迁移。
- 分列 AI建议、作者已确认、证据已支持；确认方案不能把待验证主张升级为事实。
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
