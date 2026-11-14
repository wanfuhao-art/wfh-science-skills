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
- `Current task`：下一个要执行的任务；优先级为合法 `doing` → 用户指定 → frontier 中首个可启动任务（与 `state_protocol.md` §3 一致）。
- `Frontier`：所有 `status: todo` 且 blockers 全部有效 `done` 的任务；完成证明与实际可启动性的区别见 `state_protocol.md` §3。`wfh-ask`（status 模式）只在回复重算，不写缓存；`wfh-tickets` 写初始值，`wfh-close` 同步后写缓存。
- `Updated`：最后一次改 `FLOW.md` 的日期。

---

## 3. 阶段目录（保留既有 8 个编号）

| # | 阶段 | 产出 | 校验 |
|---|---|---|---|
| 1 | 盘问与决策 | `decisions/LEDGER.md`；适用时有 `TERMS.md`、`decisions/MDR-*.md` | 台账有真实确认日期；未决项及作者接受的风险显式记录 |
| 2 | Brief 合成 | `BRIEF.md` | 已确认问题、主张、证据与验证方式；交接字段按当前 ARS 模式 |
| 3 | 任务图 | `tasks/T*.md`、`FLOW.md` 任务区 | 无环；每条任务五要素齐全；用户确认粒度 |
| 4 | 任务执行 | `tasks/T*.md`（六层记录）、`tasks/assets/` | 每条任务的验收标准 |
| 5 | 成稿整合 | `artifacts/05-draft.md` | 终端 integrate 通过；所需上游任务完成；引用键齐全；交付核对通过且适用原生检查记录齐全 |
| 6 | 审稿 | `artifacts/06-review-report.md` | ARS `academic-paper-reviewer` |
| 7 | 改稿 | `artifacts/07-revision-roadmap.md`、`artifacts/09-response.md` | `revision` 任务逐条通过；终端交付复检；原生检查状态明确 |
| 8 | 定稿 | 本次请求的格式化稿与适用声明 | 按实际模式核对交付及检查记录；不自动执行未请求的格式或声明 |

- 阶段状态只用 `done` / `active` / `waiting-user` / `blocked` / `todo`。阶段表是长期课题导航，不是所有请求的必经清单；未纳入范围的阶段保留 todo 并注记不适用及理由，不伪称 done。独立请求不创建此表。
- 阶段名是内部记录；面向用户时把「任务执行」说成「执行步骤」，把「任务图」说成「步骤安排」。
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

> 步骤已安排时每条写真实「消费任务」；尚在设计与方案阶段则写「待安排」，并说明影响及解决者。

- [UNRESOLVED] <字段>：<为什么未决>；消费任务：<Tnn>；解决者：<用户 / 实验 / 文献 / 下游 ARS>
- [待核验] <事实>：<已查来源；为什么没查到>；消费任务：<Tnn>；核验方式：<...>
```

- 从 `BRIEF.md` 的「未决问题」与「待核验事实」原样带入。
- 任务图建立后，每条必须映射到图中的一个真实任务（见 `tickets_template.md` §6.7）；设计与方案阶段尚无任务图时写“消费任务：待安排”，先保留影响和解决者，不为填编号造任务。
- 解决后不删除行；改成具体值 / 来源，并在 `FLOW.md` 的「修订记录」留痕。

---

## 7. 下一步

这是课题的**唯一持久下一步位置**：新会话从此节定位命令、输入、产出和失败回退；它不是扩大交付目标或自动连跑的授权。每个技能收尾时都必须更新它；`wfh-ask`（status 模式）负责检查它是否与任务图一致。

```markdown
## 下一步

- 命令：`/wfh-next T03`
- 输入：`tasks/T03-literature-evidence.md`、`tasks/assets/T01/TB-C1-01.md`
- 产出：`tasks/T03-literature-evidence.md`、`tasks/assets/T03/TB-LIT-01.md`
- 失败时：缺文献 → 补 `prep` 任务；claim 被证伪 → `/wfh-grill` 重开实际受影响的研究决定
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

## 8. 模板与细节

完整 FLOW 模板、阶段 1–2 初始状态、更新规则和 status / next / close 接口见 [进度细节](flow_details.md)；只在写完整模板、初始化或对接时读取。
