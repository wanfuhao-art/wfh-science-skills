# FLOW.md 模板（状态板：阶段 + 任务图 + 决策台账 + 未决问题）

> wfh-research 共享包 · 2026-11-13
> 位置：`research/<slug>/FLOW.md`
> 写入者：`wfh-tickets` 创建任务区与初始状态；`wfh-close` 更新任务状态；`wfh-ask`（status 模式）只读；`wfh-next` 生成提示词后写「下一步」；`wfh-grill` / `wfh-spec` / `wfh-tickets` 收尾时也写「下一步」。
> 状态计算、冲突与同步的行为以 [state_protocol.md](state_protocol.md) 为准；ARS 来源和字段预检以 [ars_handoff_protocol.md](ars_handoff_protocol.md) 为准。本文件维护布局与阶段定义。
> 原则：**一个文件看全貌；状态只从产物和任务文件推导，不凭记忆。**

---

## 0. 默认中文进度摘要

写入进度的动作在标题后、原 `Status` 等字段前维护一段中文说明，回答“现在做到哪、下一步做什么、是否缺材料”。摘要由已核验记录推导，不成为新事实源，不放第二条可执行命令；唯一执行指令仍在 `## 下一步` 五字段。更新前核对图和完成证据，内容冲突按状态协议停写。

使用固定注释界定摘要范围：`<!-- wfh:summary:start -->` 与 `<!-- wfh:summary:end -->`；只改这两个注释之间的派生文本，不把用户在摘要外的段落当生成内容。旧文件无此块时，在标题后新增块，原字段和章节保持原样。示例：

```markdown
<!-- wfh:summary:start -->
现在已确认研究范围，正在核对界面表征。下一步是补齐对照组测试记录，拿到后检查它是否支持当前解释。
<!-- wfh:summary:end -->
```

grill 初始化和确认、spec 合成、tickets 安排、next 准备及 close 同步时可写摘要；next 只新增这一派生块的写权限，不修改其他阶段或图字段。status 和咨询不写，发现摘要过时只在回复给重算结果。执行会话只写目标声明产出，由发起方同步进度。摘要及用户回复遵循 [研究者界面](user_output_protocol.md)；后续布局为内部状态，不原样贴给研究者。

## 1. 这份文件是什么

`FLOW.md` 是课题的状态板：一页看到阶段、任务图、决策台账、未决问题和下一步。它不复制 `BRIEF.md` 的研究内容，也不复制 MDR 的理由；它只做**索引与状态**。

| 写 | 不写 |
|---|---|
| 阶段状态、当前任务、frontier | 论文正文 |
| 任务图（ID / 状态 / blockers / 执行方式 / 产出） | 任务文件的六层细节 |
| 决策台账（已确认行） | MDR 全文 |
| 未决问题（带消费任务） | 新的研究决策 |
| 下一步启动提示词 | 历史对话 |

判断标准：**新会话只读 `FLOW.md` + 一条任务文件 + 该任务声明的输入，能不能开始干活？** 能，就够。

---

## 2. 状态字段

```markdown
Status: stage-<N>-<state>
Current stage: <N> — <阶段名>
Current task: <Tnn> — <标题>（<状态>）
Frontier: <Tnn, Tnn, ...>
Updated: YYYY-MM-DD
```

- `N`：1–8，见 §3。
- `state`：`active` / `waiting-user` / `blocked` / `done` / `todo`。
  - `active`：阶段内正在执行任务。
  - `waiting-user`：等待用户确认、补录或裁决。
  - `blocked`：等待人工测量、ARS 或外部资源。
  - `done`：阶段产出与校验都完成。
  - `todo`：阶段尚未开始。
- `Current task`：下一个要执行的任务；默认取 frontier 中的 tracer bullet 或用户指定的任务。
- `Frontier`：所有 `status: todo` 且 blockers 全部有效 `done` 的任务；完成证明与实际可启动性的区别见 `state_protocol.md` §3。`wfh-ask`（status 模式）只在回复重算，不写缓存；`wfh-tickets` 写初始值，`wfh-close` 同步后写缓存。
- `Updated`：最后一次改 `FLOW.md` 的日期。

---

## 3. 阶段表（固定 8 阶段）

| # | 阶段 | 产出 | 校验 |
|---|---|---|---|
| 1 | 盘问与决策 | `TERMS.md`、`decisions/LEDGER.md`、`decisions/MDR-*.md` | 台账有确认日期；无「frontier 未完成」 |
| 2 | Brief 合成 | `BRIEF.md` | `## RQ Brief` + Schema 1 四字段 + claim ledger |
| 3 | 任务图 | `tasks/T*.md`、`FLOW.md` 任务区 | 无环；每条任务五要素齐全；用户确认粒度 |
| 4 | 任务执行 | `tasks/T*.md`（六层记录）、`tasks/assets/` | 每条任务的验收标准 |
| 5 | 成稿整合 | `artifacts/05-draft.md` | 终端 `integrate` 任务通过；全部 claim 任务 `done`；引用键齐全 |
| 6 | 审稿 | `artifacts/06-review-report.md` | ARS `academic-paper-reviewer` |
| 7 | 改稿 | `artifacts/07-revision-roadmap.md`、`artifacts/09-response.md` | `revision` 任务逐条通过；终端 `integrate` 复检 |
| 8 | 定稿 | 格式化稿 + AI disclosure | `format-convert` + `disclosure` |

- 阶段状态只用 `done` / `active` / `waiting-user` / `blocked` / `todo`。
- 阶段 2 有未决项时状态仍写 `done`，在「校验」列写「含 N 项未决」；未决项不阻塞阶段 3，但必须进「未决问题」区。
- 阶段 4 是任务图执行期；不按「先做完所有分析再写所有正文」推进，按任务逐条推进。
- 阶段 5 与 7 由任务图中的 `integrate` / `revision` 任务驱动；阶段 6 与 8 由 ARS 主导，wfh 只记录状态与产物路径。

---

## 4. 任务图

```markdown
## 任务图

| Task | 标题 | 类型 | 状态 | Blocked by | 执行方式 | 产出 | 会话预算 |
|---|---|---|---|---|---|---|---|
| T01 | <标题> | claim | todo | — | direct | `tasks/T01-<slug>.md` | M |
| T02 | <标题> | prep | todo | — | human | `tasks/T02-<slug>.md` | S |
| T03 | <标题> | claim | todo | T01, T02 | direct | `tasks/T03-<slug>.md` | M |
| T04 | 成稿整合 | integrate | todo | T01, T02, T03 | `ARS:academic-paper:full` | `artifacts/05-draft.md` | L |
```

任务类型：`claim` / `prep` / `ec` / `integrate` / `revision`；`human` 是执行方式，不是类型。`integrate` 是终端整合任务（阶段 5 与阶段 7 各一次）；`revision` 是阶段 7 的单条审稿意见簇任务，编号用 `R01` 起。

### 4.1 状态 token

与任务文件一致：`todo` / `doing` / `done` / `blocked` / `dropped`。

- `human` 任务的 `S` / `M` 指 AI 会话预算，人工机时另计；可在表下用 `*` 标注。

### 4.2 Frontier

- `frontier = { T | T.status = todo 且 T 的所有 blockers 均为有效 done }`。有效完成证明按 `state_protocol.md` §3 核对。
- `blocked` 任务即使 blockers 都 `done`，也不进 frontier；单独列为「等待外部资源」。
- `doing` 任务不进 frontier；它是当前任务。
- `done` / `dropped` 不进 frontier。
- 初始 frontier 由 `wfh-tickets` 写；之后由 `wfh-ask`（status 模式）重算、`wfh-close` 更新。

### 4.3 无环

- 任务图必须是有向无环图。
- `wfh-tickets` 落盘前做拓扑排序；`wfh-ask`（status 模式）每次读取时重查。
- 发现环 → `TASK_GRAPH_CYCLE`；在响应中报告图无效并停止放行，先修图。status 不向 `FLOW.md` 写无效标记。

### 4.4 任务行与任务文件的关系

- `FLOW.md` 的任务行是**视图**；任务文件是**事实源**。
- 两者冲突时任务文件提供 canonical 候选依据；先报告具体差异并停止，不猜修。只有用户明确授权同步后才按已核验任务文件修 FLOW，详见 `state_protocol.md` §2。
- 任务行只写索引信息；验收标准、六层记录、完成记录在任务文件里。

---

## 5. 决策台账

```markdown
## 决策台账

> 从 `decisions/LEDGER.md` 同步；不在这里新增决策。只列已确认行；未决行放「未决问题」。

| ID | 决策 | 选择 | 理由 | 可逆性 | 影响章节 |
|---|---|---|---|---|---|
| D01 | <决策> | <选择> | <用户理由> | 高 / 中 / 低 | <Method / Results / ...> |
```

- 只列 `状态: 已确认` 的行；`未决` / `待确认` 行进「未决问题」。
- 已确认行里仍有 `[UNRESOLVED]` 子值时（如 D10 的倍率），台账保留该行，同时在「未决问题」区单列。
- `LEDGER.md` 缺失时，只列 `BRIEF.md` 的「方法决策」表，并在标题下标「来源：BRIEF，未同步 LEDGER」；不造决策。
- 不复制 MDR 的选项与证据；MDR 编号可写在「决策」列或另加 `MDR` 列。
- 台账与 `LEDGER.md` 冲突 → 以 `LEDGER.md` 为准，列出冲突，请用户裁决。

---

## 6. 未决问题

```markdown
## 未决问题

> 每条必须写「消费任务」；没有消费任务的未决项 = 任务图缺口。

- [UNRESOLVED] <字段>：<为什么未决>；消费任务：<Tnn>；解决者：<用户 / 实验 / 文献 / 下游 ARS>
- [待核验] <事实>：<已查来源；为什么没查到>；消费任务：<Tnn>；核验方式：<...>
```

- 从 `BRIEF.md` 的「未决问题」与「待核验事实」原样带入。
- 每条必须映射到任务图中的一个任务（见 `tickets_template.md` §6.7）。
- 解决后不删除行；改成具体值 / 来源，并在 `FLOW.md` 的「修订记录」留痕。

---

## 7. 下一步

这是**唯一持久位置**：新会话只看这一节，就知道下一条命令、输入、产出和失败回退。每个技能收尾时都必须更新它；`wfh-ask`（status 模式）负责检查它是否与任务图一致。

```markdown
## 下一步

- 命令：`/wfh-next T03`
- 输入：`tasks/T03-literature-evidence.md`、`tasks/assets/T01/TB-C1-01.md`
- 产出：`tasks/T03-literature-evidence.md`、`tasks/assets/T03/TB-LIT-01.md`
- 失败时：缺文献 → 补 `prep` 任务；claim 被证伪 → `/wfh-grill` 重开 D04
- 更新于：YYYY-MM-DD
- 备注：（用户手写，技能不覆盖）
```

- 命令必须是可直接执行的一条：`/wfh-*`、`ARS:<skill>:<mode>` 或人工动作。
- 输入 / 产出写精确路径；不写「见任务文件」这类模糊指向。
- `失败时` 至少写一个回退路径；claim 失败必须指向回环，不写「重试」了事。
- 更新时机：`wfh-grill` / `wfh-spec` / `wfh-tickets` / `wfh-next` / `wfh-close` / `wfh-implement-spec` 的收尾。
- 保留「备注」里的用户手写内容；不覆盖旧备注。
- 「下一步」指向的任务必须存在，且处于 frontier 或合法的 `doing`；指向 `done` / `dropped` / 不存在 / 既不在 frontier 也不是 `doing` 时，`wfh-ask` 报 `NEXT_STEP_DRIFT`，展示记录值与计算值；不静默改。
- 启动提示词只引用 `FLOW.md` + 目标任务文件 + 任务声明输入 + 必要共享协议；不引用历史对话。
- ARS 按 `ars_handoff_protocol.md` 判来源及模式；适用的字段值预检不通过 → `HANDOFF_INCOMPLETE` / `rejected_by: wfh-precheck` / `ars_invoked: false`。其他模式在执行会话读其真实要求，不全套 Schema 1。next 只生成提示词，不实际调用 ARS。

---

## 8. 模板

```markdown
# WFH Research Flow: <课题标题>

Status: stage-4-active
Current stage: 4 — 任务执行
Current task: T01 — <标题>（todo）
Frontier: T01, T02, T07
Updated: YYYY-MM-DD

## 阶段

| # | 阶段 | 状态 | 产出 | 校验 |
|---|---|---|---|---|
| 1 | 盘问与决策 | done | `TERMS.md` / `decisions/LEDGER.md` / `decisions/MDR-*.md` | 台账确认日期 YYYY-MM-DD |
| 2 | Brief 合成 | done | `BRIEF.md` | `## RQ Brief` + 四字段 + claim ledger |
| 3 | 任务图 | done | `tasks/T*.md` | 无环；五要素齐全；用户确认 |
| 4 | 任务执行 | active | `tasks/T*.md` / `tasks/assets/` | 每条任务验收标准 |
| 5 | 成稿整合 | todo | `artifacts/05-draft.md` | 阶段4的 claim/prep/ec 全部有效 done；整合另验收 |
| 6 | 审稿 | todo | `artifacts/06-review-report.md` | ARS reviewer |
| 7 | 改稿 | todo | `artifacts/07-revision-roadmap.md` / `artifacts/09-response.md` | 逐条回应 |
| 8 | 定稿 | todo | 格式化稿 + disclosure | format-convert + disclosure |

## 任务图

| Task | 标题 | 类型 | 状态 | Blocked by | 执行方式 | 产出 | 会话预算 |
|---|---|---|---|---|---|---|---|
| T01 | <标题> | claim | todo | — | direct | `tasks/T01-<slug>.md` | M |
| T02 | <标题> | prep | todo | — | human | `tasks/T02-<slug>.md` | S |
| T03 | <标题> | claim | todo | T01, T02 | direct | `tasks/T03-<slug>.md` | M |

## 决策台账

> 从 `decisions/LEDGER.md` 同步；不在这里新增决策。

| ID | 决策 | 选择 | 理由 | 可逆性 | 影响章节 |
|---|---|---|---|---|---|
| D01 | <决策> | <选择> | <理由> | 中 | Method |

## 未决问题

- [UNRESOLVED] <字段>：<为什么>；消费任务：<Tnn>；解决者：<用户>
- [待核验] <事实>：<已查来源>；消费任务：<Tnn>；核验方式：<...>

## 下一步

- 命令：`/wfh-next T01`
- 输入：`tasks/T01-<slug>.md`
- 产出：`tasks/T01-<slug>.md`、`tasks/assets/T01/`
- 失败时：缺输入 → 补 `prep` 任务；claim 被证伪 → `/wfh-grill` 重开对应决策
- 更新于：YYYY-MM-DD
- 备注：

## 修订记录

| 日期 | 变更 | 原因 |
|---|---|---|
| YYYY-MM-DD | 初版 | `wfh-tickets` 落盘任务图与初始状态 |
```

---

## 8.5 阶段 1–2 的初始状态

为了让「下一步」从盘问阶段起就有唯一位置，`wfh-grill` 建工作区时创建最小 `FLOW.md`：

| 字段 / 区 | 初始值 |
|---|---|
| `Status` | `stage-1-active` |
| `Current stage` | `1 — 盘问与决策` |
| `Current task` | `—` |
| `Frontier` | `—` |
| `Updated` | 创建日期 |
| 阶段 1 | `active` |
| 阶段 2–8 | `todo` |
| 任务图 / 决策台账 / 未决问题 | 空表或占位；台账在确认门后从 `LEDGER.md` 同步 |
| 下一步 | 命令 `/wfh-grill`（继续 frontier）；确认后改为 `/wfh-spec` |
| 修订记录 | 初版一行 |

- `wfh-spec` 落盘后：阶段 1 改 `done`、阶段 2 改 `done`、`Status` 改 `stage-3-active`，下一步写 `/wfh-tickets`。
- `wfh-tickets` 落盘后：按 §9 改为 `stage-4-active`。
- 已有 `FLOW.md` 时只增量更新，不覆盖用户手写内容。

---

## 9. 初始状态（`wfh-tickets` 落盘时）

`wfh-tickets` 写 `FLOW.md` 时，按以下规则填：

| 字段 / 区 | 初始值 |
|---|---|
| `Status` | `stage-4-active` |
| `Current stage` | `4 — 任务执行` |
| `Current task` | `T01 — <标题>（todo）` |
| `Frontier` | 所有无 blockers 的 `todo` 任务；通常含 T01 |
| `Updated` | 落盘日期 |
| 阶段 1 | `done`；校验写台账确认日期 |
| 阶段 2 | `done`；有未决项在「校验」列写「含 N 项未决」 |
| 阶段 3 | `done`；校验写「无环；五要素齐全；用户确认」 |
| 阶段 4 | `active` |
| 阶段 5–8 | `todo` |
| 任务图 | 每条任务一行；状态全部 `todo`（用户已开始的任务可写 `doing`） |
| 决策台账 | 从 `LEDGER.md` 同步已确认行 |
| 未决问题 | 从 `BRIEF.md` 带入，逐条写消费任务 |
| 下一步 | 写全五字段：命令 `/wfh-next T01`、输入、产出、失败时、更新于；不要只写一句建议 |
| 修订记录 | 追加一行「初版 / wfh-tickets 落盘任务图与初始状态」 |

- 阶段 3 的 `done` 以「用户确认粒度、依赖、合并 / 拆分」为前提；未确认不落盘。
- 初始 `Status` 是 `stage-4-active`：任务图已落盘，下一阶段是执行。
- 若 `BRIEF.md` 有未决项，阶段 2 状态仍写 `done`，在「校验」列写「含 N 项未决」；不阻塞阶段 4，但未决项必须在任务图中有消费任务。

---

## 10. 更新规则

1. **任务文件是事实源。** `FLOW.md` 是视图；冲突先报告并停止，按 `state_protocol.md` §2 处理，不能因 canonical 身份而自动猜修。
2. **状态只从产物推导。** 任务 `done` 必须有完成记录与验收结果；不能凭「感觉做完了」。
3. **改状态时追加修订记录。** 日期 / 变更 / 原因；next 保存提示词在「下一步」节内记日期与旧内容，并按 §0 同步中文摘要，不改其他节。
4. **不删除任务行。** 取消的任务标 `dropped`，保留行与原因。
5. **frontier 每次重算。** 不手工维护 frontier；用 blockers 与状态推导。
6. **未决项不消失。** 解决后改成具体值 / 来源，保留行与修订记录。
7. **阶段不跳级。** 阶段 4 未完成不进阶段 5；阶段 5 未完成不进阶段 6。
8. **不写研究内容。** `FLOW.md` 不写正文、不写新决策、不写文献综述。
9. **下一步与 frontier / doing 一致。** 每次改任务状态后重写「下一步」；`wfh-ask` 发现指向不存在、`done` / `dropped`、或既不在 frontier 也不是 `doing` 的任务时报 `NEXT_STEP_DRIFT`，展示记录值与计算值，不静默改。

---

## 11. 给 04（status / next / close）的接口

三个入口现已实现；以下是布局接口摘要，执行细节统一见 `state_protocol.md`。

### 11.1 `wfh-ask`（status 模式，只读）

输入：`FLOW.md` + `tasks/T*.md` / `tasks/R*.md` + 产物路径。

输出：

1. 当前阶段 / 阶段状态；
2. 当前任务；
3. frontier（按 §4.2 重算）；
4. 缺失产物（任务声明了产出但文件不存在）；
5. 阻塞项（`blocked` 任务与原因）；
6. 未决问题（带消费任务）；
7. 一句下一步建议；
8. FLOW「下一步」与重算 frontier / doing 的一致性；指向不存在、`done` / `dropped`、或既不在 frontier 也不是 `doing` 的任务时报 `NEXT_STEP_DRIFT`，展示记录值与计算值。

不写任何文件。

### 11.2 `wfh-next`（生成提示词并写「下一步」）

输入：`FLOW.md` + 一条任务文件 + 任务声明的输入。

输出：可复制的启动提示词；随后写 `## 下一步`（五字段），保留用户备注。此节含：

- 要读的文件清单（`FLOW.md`、任务文件、任务输入）；
- 任务的六层要求与验收标准；
- 执行方式（`direct` / `ARS:<skill>:<mode>` / `human`）；
- 若为 ARS 任务：按交接协议判来源、做适用模式预检；缺值按 wfh-precheck 归属停止。附未来执行会话的 Skill 调用草案；明确本次未调用 ARS。

不读历史对话；不改任务状态；除 §0 中文摘要外不改其他节。

### 11.3 `wfh-close`（校验 + 更新）

输入：任务文件 + 产出。

输出：

1. 按原验收标准逐条读取证据内容，判定 pass / fail / unresolved 并指向证据；
2. 全部通过且依赖和确认齐全 → `result: complete`，任务 `done`，追加完成记录；
3. 未通过 → `result: partial`（doing）或 `result: blocked`（blocked），保留 unresolved 与解除条件；
4. 重算 frontier；更新 `FLOW.md` 任务行、`Status`、`Current task`、`Updated`、`下一步`；
5. claim 失败按 `state_protocol.md` §6.1 分类；`CLAIM_REFUTED` / `DESIGN_INVALID` 写 `decisions/REOPEN-*.md`；
6. 追加修订记录。

不修改任务主张、原验收标准或 `BRIEF.md`；发现 claim 问题 → 建议回 `wfh-spec`。close 不执行 ARS 研究任务，wfh 验收完成不代表 ARS PASS 或完整内部审计通过。
