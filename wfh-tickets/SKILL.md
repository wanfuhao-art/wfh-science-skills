---
name: wfh-tickets
description: "把 BRIEF.md 的 claim ledger 切成最小可验证主张单元的任务图，写 tasks/T*.md 与 FLOW.md 的任务区 / 初始状态；每条任务有 blocked by、执行方式（ARS / direct / human）、验收标准、产出路径、会话预算；落盘前先确认粒度、依赖、合并/拆分。用于 Brief 确认后的任务切分、写作前规划、判断哪些任务可并行；English triggers: split research brief into tasks, research task graph, wfh-tickets, tickets from brief. 不用于盘问（用 wfh-grill）、不用于合成 Brief（用 wfh-spec）、不用于写作（用 ARS academic-paper）。"
---

# wfh-tickets — 任务图切分

> wfh-research 套件的执行规划入口。
> 本技能只做「把 Brief 切成可独立执行、可独立验证的任务图」，不写正文、不做研究决策、不执行任务。

---

## 定位

- 这是 matt `to-tickets` 的**科研版**：把 `BRIEF.md` 的 claim ledger 切成「最小可验证主张单元」，每条任务能在新会话里独立完成。
- 上游是 `wfh-spec` 的已确认 `BRIEF.md`；下游是 `wfh-ask`（status 模式）/ `wfh-next` / `wfh-close` 与 ARS。
- 只写 `tasks/T*.md` 与 `FLOW.md` 的任务区 / 初始状态；不改 `BRIEF.md` / `TERMS.md` / `decisions/` / `artifacts/`。
- 任务文件的第 5 层只写目标章节、字数与边界句，**不写正文成品**。
- **不依赖 matt 插件**；不引入 issue tracker、GitHub、PR、TDD、git 概念。

### 与相邻技能的分工

| 用户状态 | 用什么 |
|---|---|
| 还没问清楚，决策未定 | `wfh-grill` |
| 盘问已确认，要合成 Brief | `wfh-spec` |
| 已有 Brief，要切成任务 | **本技能** |
| 已有任务图，要看当前该做什么 | `wfh-ask`（status 模式）/ `wfh-next`（04） |
| 任务完成，要校验并推进 | `wfh-close`（04） |
| 要检索、写作、审稿、改稿 | ARS 对应技能 |

---

## 何时用 / 不用

**用**：

- `BRIEF.md` 已确认，含 `## RQ Brief` 与 `## 主张清单（Claim Ledger）`；
- 要把 claim ledger 切成任务图，判断哪些能并行、哪些要等；
- 已有任务图，需要增量加任务（决策修订、新 claim、新证据）；
- 要在写作前确认粒度、依赖、合并 / 拆分。

**不用**：

- Brief 未确认或字段缺失 → 先 `wfh-spec`；
- 要改 RQ / 贡献 / 设计 / 分析 → `wfh-grill`（本技能不做研究决策）；
- 要写正文 / 提纲 → ARS `academic-paper`；
- 要执行任务 → 新会话按任务文件执行，或 `wfh-next` 生成启动提示词。

---

## 输入

**必需**（同一工作区 `research/<slug>/`）：

- `BRIEF.md`：`状态：已确认`；含 `## RQ Brief`、Schema 1 四字段、`## 主张清单（Claim Ledger）`。

**可选**：

- `TERMS.md`：术语与操作定义；
- `decisions/LEDGER.md`：决策台账（同步到 `FLOW.md`）；
- `decisions/MDR-*.md`：方法决策（任务输入）；
- 已有 `tasks/T*.md` / `FLOW.md`（增量更新）；
- 用户在本次调用中直接给的拆分偏好（粒度、并行、合并）。

**开始前先读**：上述全部文件。能从事产物回答的，不再问用户。

---

## 输出

| 文件 | 写入时机 |
|---|---|
| `research/<slug>/tasks/T01-<slug>.md` … | 用户确认任务图后 |
| `research/<slug>/FLOW.md` | 用户确认任务图后；写任务区 + 初始状态 |

**不写**：`BRIEF.md`、`TERMS.md`、`decisions/*`、`artifacts/*`、正文、提纲。

---

## 执行前必读（共享包，唯一协议来源）

按顺序读：

1. [`../wfh-research/references/tickets_template.md`](../wfh-research/references/tickets_template.md) — 任务文件模板、六层切片、字段规范、切分与建图规则
2. [`../wfh-research/references/flow_template.md`](../wfh-research/references/flow_template.md) — `FLOW.md` 模板、阶段表、任务图、初始状态、给 04 的接口
3. [`../wfh-research/references/spec_template.md`](../wfh-research/references/spec_template.md) §4.6 — claim ledger 的字段与证据状态含义
4. 需要核对术语 / MDR 语义时：[`../wfh-research/references/terms_template.md`](../wfh-research/references/terms_template.md)、[`../wfh-research/references/mdr_template.md`](../wfh-research/references/mdr_template.md)

**不要凭记忆执行。** 本文件只写入口、流程与边界；模板细节以共享包为准。

---

## 流程

### 1. 预检

1. 找 `research/*/BRIEF.md`：
   - 只有一个 → 用它；
   - 多个 → 问用户选哪个（这是本技能允许的提问之一）；
   - 没有 → `BRIEF_NOT_FOUND`，停（见错误处理）。
2. 读 Brief，确认：
   - `状态：已确认`；草稿 → `BRIEF_NOT_CONFIRMED`，除非用户明确要「按草稿切任务」；
   - `## RQ Brief` 存在，四个必需字段存在；
   - `## 主张清单（Claim Ledger）` 存在，≥1 条 claim，每条有 `溯源`；
   - claim 的 `验证方式` 可执行，不是「进一步研究」；不可执行 → `CLAIM_UNVERIFIABLE`，列出并停。
3. 读 `TERMS.md`、`decisions/LEDGER.md`、`decisions/MDR-*.md`；缺失不阻塞：
   - 无 `LEDGER.md` → `FLOW.md` 的决策台账只列 Brief 的「方法决策」表，标「来源：BRIEF，未同步 LEDGER」，不造决策；
   - 无 `TERMS.md` → 任务文件的术语输入写「无 `TERMS.md`」，不代写定义；
   - 无 MDR → 任务输入只引台账行，不补写 MDR。
4. 检查已有 `tasks/` / `FLOW.md`：
   - 没有 → 新建；
   - 有 → 增量模式：先读，保留用户手改，不重排编号，不删任务。
5. 向用户报一行输入清单：claim N 条 / 子问题 N 条 / 未决 N 项 / 待核验 N 项 / 已有任务 N 条。

### 2. 抽取

按 `tickets_template.md` §4–§5 的字段规范抽取。每条记录来源：

| 抽取项 | 来源 |
|---|---|
| claim 列表 | `## 主张清单（Claim Ledger）` 的 `C#` / 主张 / 证据状态 / 证据来源 / 验证方式 / 风险 / 溯源 |
| 子问题 | `**Sub-Questions**`；claim 与子问题的对应关系 |
| 未决项 | `## 未决问题` + `## 待核验事实` |
| 方法约束 | `## 方法决策` + MDR（电压窗口、倍率、温度、表征手段、对照设计） |
| 材料学字段 | `## 材料学扩展`（任务输入与图注要用） |
| 证伪条件 | `## 验证与证伪`（任务判定规则要用） |
| 术语 | `## 术语` + `TERMS.md`（正文用词与操作定义） |

抽取时：

- 只搬运、组织和压缩；**不新增** claim、证据、数值或研究决策；
- claim 无溯源 → `CLAIM_UNTRACEABLE`，不切任务；
- 子问题无对应 claim → 标 `SUBQ_UNMAPPED`，请用户补 Brief 或明确映射；
- 未决 / 待核验原样带入，不猜填。

### 3. 切分

按 `tickets_template.md` §6 执行。默认顺序：

1. **一主张一任务**：每条 claim 先建一个 `claim` 任务，任务主张照录 claim。
2. **拆**：按 §6.2 检查证据来源、图表数量、人工测量、会话预算、结论数量；需要拆就拆，并写清每个任务负责 claim 的哪一部分。
3. **合**：只在同一 claim 内合；合并后 ≤ `M`；不跨 claim。
4. **预加工**：识别共享数据清洗、文献检索、量表核对、IRB、仪器预约、前置决策；只被一条 claim 消费 → 并入该 claim 任务；被 ≥2 条消费 → 单独 `prep` 任务。例外：`human` 测量 / 仪器任务即使只被一条 claim 消费，也单独成任务（执行方式不同）。
5. **人工任务**：湿实验、仪器机时、外部数据、用户裁决、伦理审批；按 §6.5 写人工动作 / 返回物 / 核验方式 / 失败时。
6. **ARS 任务**：检索、事实核验、筛选、审稿、格式转换、引用核验；写全 `ARS:<skill>:<mode>`。
7. **未决映射**：每个 `[UNRESOLVED]` 转成决策任务或显式假设 + 降级规则；每个 `[待核验]` 落到一个任务的证据 / 引用层。
8. **tracer bullet**：选一条证据最现成、分析最简单、最能代表主张链的 claim 作 T01；T01 必须 `Blocked by: —`、六层完整、一个会话可完成。T01 的输入必须现成；若关键数据不存在，先补 `prep` 任务，不硬造。
9. **expand–contract**：全局机械改动按 §6.9 拆成 `expand` / `migrate` / `contract` 三个 `ec` 任务；内容改动不走 `ec`。

### 4. 建图

1. 按拓扑序分配 Task ID：T01 最先；后续尽量前置依赖在前；允许并行分支。
2. 写 `Blocked by`：只写任务 ID；`—` 表示无前置；不写「等数据」「等结果」。
3. 做一次拓扑排序：
   - 每次取走「所有 blockers 已完成」的任务；
   - 取不完 → `TASK_GRAPH_CYCLE`，列出环上的任务，停。
4. 检查每条任务：
   - 五要素齐全：`Blocked by` / `执行方式` / 验收标准 / 产出路径 / 会话预算；
   - 六层齐全；
   - 一个主执行方式；
   - 一个「这条主张站得住吗」的答案；
   - 独立验证只读任务文件 + 产出 + Brief 对应 claim 行。
5. 检查全局：
   - T01 是 tracer bullet；
   - 全局机械改动都在 `ec` 组；
   - 每个未决项都有消费任务；
   - 没有孤立 claim（每条 claim 至少一个任务）；
   - 没有孤立任务（每条任务至少对应一个 claim 或支撑关系）。

### 5. 确认门

输出以下内容，然后**停下**：

1. **任务图总表**：Task / 标题 / 类型 / Blocked by / 执行方式 / 产出 / 会话预算。
2. **边列表与拓扑序**：每条边一行；拓扑序一行。
3. **Tracer bullet 选择**：选哪条 claim、为什么、它的六层产出是什么。
4. **拆分 / 合并说明**：哪些 claim 拆了、为什么；哪些合了、为什么；哪些 `prep` / `human` / `ec` 是单独任务、为什么。
5. **未决映射**：每个 `[UNRESOLVED]` / `[待核验]` 对应哪个任务、怎么处理。
6. **一句提问**：

   > 这个粒度、依赖和合并 / 拆分是否可以落盘？需要合并、拆分、调整依赖或改执行方式的地方，请直接说。

允许在确认门做的：

- 合并 / 拆分任务；
- 调整 `Blocked by`；
- 改执行方式（`direct` / `ARS` / `human`）；
- 改任务标题、产出路径、会话预算；
- 确认或替换 tracer bullet。

不允许：

- 改 claim、加 claim、改 RQ / 贡献 / 设计 / 分析；
- 让本技能替用户定未决值；
- 在确认前写 `tasks/` 或 `FLOW.md`。

用户提出改 claim → 拒绝：这是研究决策，指向 `wfh-spec` / `wfh-grill`。

### 6. 落盘

1. 按 `tickets_template.md` §8 写 `tasks/T*.md`：
   - 每条任务一个文件；
   - 状态 `todo`；
   - 六层骨架 + 验收标准 + 完成记录（初始行「初始计划」）；
   - `prep` / `ec` 用对应模板。
2. 按 `flow_template.md` §8–§9 写 `FLOW.md`：
   - `Status: stage-4-active`；
   - 阶段 1–3 `done`，阶段 4 `active`，阶段 5–8 `todo`；
   - 任务图（每条任务一行）；
   - 决策台账（从 `LEDGER.md` 同步已确认行）；
   - 未决问题（从 `BRIEF.md` 带入，写消费任务）；
   - 下一步（占位；04 实现前手工填「从 T01 开始」）；
   - 修订记录（初版一行）。
3. 增量模式：
   - 先读已有 `tasks/` / `FLOW.md`；
   - 保留用户手改；
   - 不重排已有编号；新任务用最大编号 +1；
   - 取消的任务标 `dropped`，保留文件与原因；
   - `FLOW.md` 追加修订记录，不静默覆盖。
4. 落盘后向用户报：任务 N 条 / frontier / T01 / 下一步命令。

### 7. 结束

- 报一句：任务图已落盘；frontier 是哪些；建议从 T01 开始。
- 不执行任务、不调 ARS、不写正文。
- 下一步：`/wfh-ask`（status 模式）或直接按 T01 任务文件开始；需要新会话启动提示词时用 `/wfh-next`（04 实现后）。

---

## 任务切分规则摘要

完整规则见 `tickets_template.md` §6；以下是入口级摘要：

| 规则 | 要点 |
|---|---|
| 一主张一任务 | 每条 claim 至少一个 `claim` 任务；任务主张照录 claim |
| 纵向切片 | 主张 → 证据 → 分析 → 图 / 表 → 正文 → 引用，六层缺一不可 |
| 一个会话 | `S` / `M` / `L` 预算；超过 `L` 先拆 |
| 独立验证 | 只读任务文件 + 产出 + Brief 对应 claim 行 |
| 拆 | 证据来源可独立失败、多图、人工测量与分析、超预算、两个结论 |
| 合 | 只在同一 claim 内；合并后 ≤ `M`；不跨 claim |
| `prep` | 只被 ≥2 条 claim 消费才单独成任务；`human` 测量例外 |
| `human` | 写人工动作 / 返回物 / 核验方式 / 失败时；不代做 |
| `ARS` | 写全 `ARS:<skill>:<mode>`；不可用 → `ARS_NOT_AVAILABLE` |
| 未决 | 每个 `[UNRESOLVED]` 转决策任务或显式假设；每个 `[待核验]` 落到任务 |
| Tracer bullet | T01 必须是可立即执行的 claim 任务，六层完整，产出作样板 |
| Expand–contract | 全局机械改动拆 `expand` → `migrate` → `contract`；不改内容 |
| 无环 | 拓扑排序；有环 → `TASK_GRAPH_CYCLE`，停 |

---

## 硬规则

1. **只读上游，只写任务与 FLOW。** 不改 `BRIEF.md` / `TERMS.md` / `decisions/` / `artifacts/`。
2. **不新增 claim。** 每条 `claim` 任务必须溯源到 Brief 的 `C#`；无溯源 → 不切。
3. **不改研究决策。** 需要改 RQ / 贡献 / 设计 / 分析 → `wfh-grill`；需要改 Brief → `wfh-spec`。
4. **未决不静默。** 每个 `[UNRESOLVED]` 有消费任务；每个 `[待核验]` 有核验任务或核验步骤。
5. **不超一个会话。** 超过 `L` 先拆；不把「以后再说」写进任务。
6. **不造环。** 落盘前拓扑排序；有环停。
7. **T01 必须是 tracer bullet。** 不能执行就停下来补 `prep`，不硬造。
8. **全局机械改动只走 `ec`。** 内容改动不得混进 `ec`。
9. **`human` 不代做，`ARS` 不静默降级。** 人工任务写清返回物；ARS 不可用报 `ARS_NOT_AVAILABLE`。
10. **确认门先于落盘。** 未确认不写 `tasks/` / `FLOW.md`。
11. **不引入软件工程流程概念。** 不写 issue tracker、GitHub、PR、TDD、git worktree。
12. **不改 ARS、不接 `nature-*`、不依赖 matt 插件。**

---

## 错误处理

| 情况 | 动作 |
|---|---|
| `BRIEF.md` 不存在 | `BRIEF_NOT_FOUND`：停；说明本技能只从已确认 Brief 切任务；建议 `/wfh-spec` 或 `/wfh-grill` |
| Brief 是草稿 | `BRIEF_NOT_CONFIRMED`：停；建议先确认 Brief。用户明确要「按草稿切任务」→ 在 `FLOW.md` 标「草稿任务图」，不冒充已确认 |
| 缺 `## RQ Brief` / 四字段 / claim ledger | `BRIEF_INCOMPLETE`：列出缺项，停；不凭记忆补 |
| `LEDGER.md` 缺失 | 不阻塞；`FLOW.md` 台账只列 Brief 的「方法决策」表，标「来源：BRIEF，未同步 LEDGER」；不造决策 |
| `TERMS.md` 缺失 | 不阻塞；任务文件的术语输入写「无 `TERMS.md`」；不代写定义 |
| MDR 缺失 | 不阻塞；任务输入只引台账行，MDR 列填 `—`；不补写 MDR |
| claim 无 `溯源` | `CLAIM_UNTRACEABLE`：不切该 claim；列出缺溯源的 claim，建议回 `wfh-spec` |
| claim 的验证方式不可执行（如「进一步研究」） | `CLAIM_UNVERIFIABLE`：列出 claim；建议回 `wfh-spec` 补验证方式；不自行编造 |
| 子问题无对应 claim | `SUBQ_UNMAPPED`：列出子问题；请用户补 Brief 或明确映射；不自行造 claim |
| 任务图有环 | `TASK_GRAPH_CYCLE`：列出环上的任务与边，停；修图后重跑拓扑排序 |
| 任务超一个会话 | `TASK_TOO_BIG`：按 §6.2 拆；拆完再落盘 |
| 没有可执行的 tracer bullet | `NO_TRACER_BULLET`：停；说明哪条 claim 缺什么证据 / 决策；建议补 `prep` 或先解决阻塞项 |
| 未决项无消费任务 | `UNRESOLVED_UNMAPPED`：列出未决项；补决策任务或显式假设后再落盘 |
| 已有 `tasks/` / `FLOW.md` | 增量模式：先读、保留手改、不重排、不删除；新任务追加编号 |
| ARS 不可用 | `ARS_NOT_AVAILABLE`：ARS 任务保持 `blocked`；报错，不降级为 `direct` |
| 用户拒绝任务图 / 要求重切 | 按反馈重切，重新过确认门；不落盘；不改 claim |
| 用户要求改 claim / 加 claim | 拒绝：这是研究决策；指向 `wfh-spec` / `wfh-grill` |
| 用户要求顺便写正文 / 提纲 | 拒绝：本技能只切任务；指向 ARS `academic-paper` |
| 用户要求把全局改动塞进普通任务 | 拒绝：走 `ec` 组；说明 expand–contract 三阶段 |

---

## 结束前自检

- [ ] Brief 已确认，`## RQ Brief` + 四字段 + claim ledger 齐全？
- [ ] 每条 claim 至少一个任务，且任务主张照录 claim？
- [ ] 每条任务有 `Blocked by` / `执行方式` / 验收标准 / 产出路径 / 会话预算？
- [ ] 每条任务是六层纵向切片？
- [ ] 任务图无环，拓扑序可列出？
- [ ] T01 是 tracer bullet：`claim` 类型、`Blocked by: —`、六层完整、一个会话可完成？
- [ ] 每条任务 ≤ `L`，且独立可验证？
- [ ] 三种执行方式按需出现；`human` / `ARS` 写清返回物 / 完整调用？
- [ ] 全局机械改动都在 `ec` 组，三阶段依赖正确？
- [ ] 每个 `[UNRESOLVED]` / `[待核验]` 都有消费任务？
- [ ] 确认门已过，用户确认了粒度、依赖、合并 / 拆分？
- [ ] 只写了 `tasks/` 与 `FLOW.md`？
- [ ] 没有改 ARS 文件、没有引入软件工程流程概念？

---

## 下一步

- 任务图落盘后 → `/wfh-ask`（status 模式）查看 frontier；或直接按 `tasks/T01-*.md` 开始。
- 需要新会话启动提示词 → `/wfh-next`（04 实现后）。
- 任务完成 → `/wfh-close`（04 实现后）校验产出并推进 frontier。
- 需要写作 / 检索 / 审稿 → ARS 对应技能；任务文件里已写执行方式。
