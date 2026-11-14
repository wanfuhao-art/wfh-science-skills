# FLOW.md 模板与更新细节

> 只在写完整模板、初始化、更新规则或对接 status / next / close 时读取；状态字段与任务图规则见 [进度模板](flow_template.md)。

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
| 2 | Brief 合成 | done | `BRIEF.md` | 已确认问题、主张、证据与验证；交接按当前模式 |
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

- 阶段 3 的 `done` 需有本次安排的授权依据；已确认目标内的机械拆分可沿用确认，涉及新的范围、预算、人工承诺或研究取舍才另行确认。
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
7. **按适用依赖推进。** 同一课题内的成稿整合遵守其真实前序；用户直接请求评审已有稿时无需补跑阶段 1–5。未执行阶段不标 done；是否继续执行以本次授权目标为准。
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
- 任务的适用最小层与原验收标准；
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
