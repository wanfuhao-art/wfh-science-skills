---
name: wfh-implement-spec
description: "执行 wfh 任务图中的单条任务：生成可编辑的启动提示词，用户确认后开启新会话执行，会话结束后自动按 wfh-close 逐条验收，并在每个任务后停下等用户确认。用于把 wfh-next 和 wfh-close 合成一条命令、推进阶段 4 的 claim/prep 任务、逐条跑任务图；English triggers: implement spec, execute task, run task, wfh implement, wfh-implement-spec, run this task, start the task session. 不用于重新盘问（用 wfh-grill）、不用于切任务（用 wfh-tickets）、不用于直接写正文（用 ARS academic-paper）。"
---

# wfh-implement-spec — 任务执行与自动验收

> wfh 任务图的执行层入口。
> 本技能把 `wfh-next` 的提示词生成、`start_session` 的新会话启动、`wfh-close` 的证据验收合成一条命令；不重新做研究决策，不写正文。

---

## 定位

- 输入：一个已存在的 `research/<slug>/` 工作区和一个任务 ID（如 T03）。
- 输出：一段经用户确认的启动提示词、一个新会话、一次 wfh-close 验收记录。
- 上游：`wfh-tickets` 的任务图；下游：`wfh-ask`（status 模式）/ `wfh-next` / `wfh-close`。
- 本技能只编排，不替代：
  - `wfh-next` 的提示词规则（`state_protocol.md` §5）；
  - `wfh-close` 的验收规则（`state_protocol.md` §6）；
  - ARS 的生产技能（deep-research / academic-paper / reviewer 等）。

### 与相邻入口的分工

| 用户状态 | 用什么 |
|---|---|
| 只想生成提示词，自己拿去新会话跑 | `wfh-next` |
| 想一条命令完成「生成提示词 → 开新会话 → 自动验收」 | **本技能** |
| 任务已完成，只想验收 | `wfh-close` |
| 想看 frontier / 阻塞 | `wfh-ask`（status 模式） |
| 要改研究决策 / 任务图 | `wfh-grill` / `wfh-tickets` |

---

## 何时用 / 不用

**用**：

- 任务图已落盘，目标任务的 `Blocked by` 已满足；
- 你希望执行前能修改提示词，执行后自动验收；
- 你想逐条推进阶段 4，但不想手动复制粘贴两次。

**不用**：

- 目标任务被阻塞或缺输入 → 先补依赖 / 输入；
- 目标任务是 `human` → 本技能只列人工动作，不开会话；
- 你只想看状态 → `wfh-ask`（status 模式）；
- 你要重新盘问或改 claim → `wfh-grill` / `wfh-spec`。

---

## 输入

**必需**：

- 工作区：`research/<slug>/`（唯一时自动选择；多个时问用户）。
- 任务 ID：如 `T03`。

**可选**：

- `--dry-run`：只生成并展示提示词，不启动会话、不写状态文件。
- `--close <ID>`：跳过提示词生成，只对指定任务执行 wfh-close 验收（用于手动启动会话后的补验收）。
- `--resume`：读取 `.wfh-implement-spec/pending.json`，继续等待或验收未完成的任务。

---

## 输出

| 文件 / 动作 | 写入时机 |
|---|---|
| `.wfh-implement-spec/prompts/<ID>.md` | 用户确认提示词后 |
| `.wfh-implement-spec/pending.json` | 启动新会话前 |
| 新会话（`start_session`） | 用户确认提示词后 |
| 任务文件 + `FLOW.md` 的验收更新 | 会话结束后，按 wfh-close 规则 |

**不写**：`BRIEF.md`、`TERMS.md`、`decisions/*`、其他任务文件、正文。

---

## 执行前必读（共享协议，唯一规则来源）

1. [`../wfh-research/references/state_protocol.md`](../wfh-research/references/state_protocol.md) §1–6 — 工作区、图校验、frontier、提示词结构、验收规则。
2. [`../wfh-next/SKILL.md`](../wfh-next/SKILL.md) — 提示词生成的入口与边界。
3. [`../wfh-close/SKILL.md`](../wfh-close/SKILL.md) — 验收的入口与边界。
4. ARS 任务另读 [`../wfh-research/references/ars_handoff_protocol.md`](../wfh-research/references/ars_handoff_protocol.md)。
5. 需要核对字段布局时读 [`../wfh-research/references/tickets_template.md`](../wfh-research/references/tickets_template.md)、[`flow_template.md`](../wfh-research/references/flow_template.md)。

**不要凭记忆执行。** 本文件只写编排顺序；提示词与验收的细节以共享协议为准。

---

## 流程

### 1. 预检

1. 定位工作区：用户指定 `research/<slug>/` 就用它；未指定只查 `research/*/FLOW.md`，唯一才选，多个问用户，无则 `FLOW_NOT_FOUND`。
2. 读 `FLOW.md`、目标任务文件、任务明确声明的输入。
3. 校验图：ID 唯一、任务行与文件一致、无环、无重复边；冲突报 `FLOW_TASK_CONFLICT` / `TASK_GRAPH_CYCLE`，停。
4. 校验目标：
   - `done` / `dropped`：说明已关闭，需用户明确重开后再启动。
   - `blocked` 或任一 blocker 未有效 done：报 `TASK_BLOCKED`，列 blocker 与缺件，停。
   - `human`：不启动会话，输出人工动作 / 返回物 / 核验方式，停。
   - 缺声明输入：报 `INPUT_MISSING`，列缺项，停。
   - `todo` / `doing` 且输入齐：继续。

### 2. 生成提示词

按 `state_protocol.md` §5 的结构生成，额外加一段「执行会话边界」：

- 本会话只执行 `<ID>`，只读提示词列出的文件；
- 不调用 `wfh-close`（由发起会话统一验收）；
- 不修改其他任务、`BRIEF.md`、`TERMS.md`、`decisions/*`；
- 结束时报告：产出路径、逐条证据位置、结论、未决项、是否完成。

ARS 任务按交接协议写调用草案；`direct` 任务写分析步骤；`human` 任务不生成提示词。

### 3. 用户确认（硬门）

1. 把完整提示词放在代码块里展示。
2. 明确说：「你可以直接修改这段提示词；确认后我再开新会话。」
3. **停下。** 不启动会话、不写状态文件。
4. 用户确认后，使用用户修改后的版本；用户要求改，就改完再确认。

### 4. 启动新会话

1. 用 `ToolSearch` 加载 `mcp__ccd_session__start_session`（若未加载）。
2. 调用：
   - `initiation: "user_asked"`
   - `context: "fresh"`
   - `use_worktree: false`
   - `title: "<ID> — <任务标题>"`
   - `name: "<id-lower>-exec"`（如 `t03-exec`）
   - `prompt: <确认后的提示词>`
3. 不传 `target: "cloud"`、`environment`、`repository`、`initiation: "offer"`。
4. 若 `start_session` 不可用或被拒：回退为「把提示词复制到新会话」，并告诉用户完成后运行 `/wfh-implement-spec --close <ID>`。

### 5. 记录等待状态

写 `research/<slug>/.wfh-implement-spec/pending.json`：

```json
{
  "task_id": "T03",
  "task_file": "tasks/T03-literature-evidence.md",
  "session_name": "t03-exec",
  "session_id": "local_...",
  "started_at": "2026-11-13T00:00:00+08:00",
  "status": "waiting",
  "expected_outputs": ["tasks/T03-literature-evidence.md", "tasks/assets/T03/TB-LIT-01-literature-matrix.md"]
}
```

同时把确认后的提示词写入 `.wfh-implement-spec/prompts/<ID>.md`。

然后结束本轮，告诉用户会话已启动。**不要轮询。**

### 6. 等待会话结束

- 新会话结束一轮时，宿主会发 `<side-sessions-event>`，引用其最新报告的前 400 字。
- 收到事件后：
  1. 读事件报告；若会话在提问、报告阻塞或缺输入 → 转告用户，**不验收**，等用户回答或让用户继续该会话。
  2. 若报告说任务完成 → 读 `FLOW.md`、目标任务、`pending.json` 声明的产出，进入第 7 步。
  3. 若会话失败或没有产出 → 报 `SESSION_INCOMPLETE`，不编造，问用户重试还是转人工。
- 不要用 `CronCreate`、`ScheduleWakeup`、`/loop` 或 `gh` 轮询；事件是唯一唤醒信号。

### 7. 自动验收（wfh-close）

按 `state_protocol.md` §6 逐条核对：

1. 读 FLOW、目标任务、声明输入、产出、完成记录。
2. 逐条列 `标准 | pass / fail / unresolved | 证据位置 | 理由 | 缺件/解决者`。
3. ARS 任务：核对真实 Skill 调用与响应；只有提示词不算。
4. 结果：
   - 全部 pass + 依赖有效 + 必要用户确认齐全 → `complete`，任务 `done`；
   - 有未通过 → `partial`，任务 `doing`；
   - 缺数据 / 人工 / 用户确认 / ARS 契约 / 依赖 → `blocked`，写解除条件。
5. 先展示核对结果，再更新目标任务与 FLOW 的授权字段；不改原验收标准，不代填数据。
6. 更新 `pending.json` 的 `status` 为 `closed`，追加 `result` 和日期。

### 8. 收束

1. 报：任务 ID、result、逐条通过情况、更新了哪些文件、新的 frontier。
2. **停下**，问用户是否继续下一条任务；不自动启动下一条。
3. 若用户说继续，回到第 1 步，用新的任务 ID。

---

## 硬规则

1. **提示词未确认，不启动会话。**
2. **每个任务后停下**，不自动连跑。
3. **`human` 任务不开会话**；只列人工动作、返回物、核验方式。
4. **`blocked` / 缺输入不开会话**；先补依赖或输入。
5. **验收不改标准、不代填数据、不把提示词当 ARS 回执。**
6. **不改 `BRIEF.md` / `TERMS.md` / `decisions/*` / 其他任务。**
7. **不轮询**；只靠 `<side-sessions-event>` 唤醒。
8. **不改 wfh 共享包和六个入口**；本技能是独立编排层。
9. **不把合成 fixture 当真实证据**；合成测试只在测试工作区有效。
10. **会话失败不编造结果**；报 `SESSION_INCOMPLETE`，让用户决定重试或转人工。

---

## 错误处理

| 情况 | 动作 |
|---|---|
| `FLOW_NOT_FOUND` | 停；说明只查 `research/*/FLOW.md`，请用户给路径 |
| `TASK_NOT_FOUND` | 停；列出 FLOW 中可用 ID |
| `TASK_BLOCKED` | 停；列 blocker 的 ID / 状态 / 缺件 |
| `INPUT_MISSING` | 停；列缺项与解决者 |
| `TASK_HUMAN` | 不启动会话；输出人工动作清单 |
| `TASK_CLOSED` | 说明 done/dropped；需用户明确重开 |
| `SESSION_START_FAILED` | 回退为手动复制提示词；给 `--close` 命令 |
| `SESSION_INCOMPLETE` | 不验收；报告会话状态与缺件，问用户重试 / 转人工 |
| `STATE_CHANGED` | 读取后被其他会话改动；停，报原值与位置，不覆盖 |
| `ARS_NOT_AVAILABLE` | ARS 任务保持 blocked；不降级为 direct |
| 用户改提示词 | 用改后版本；重新确认后再启动 |
| 用户要求连跑下一条 | 说明本技能每个任务后停；用户可逐条调用 |

---

## 结束前自检

- [ ] 目标任务已确认不是 blocked / human / done？
- [ ] 提示词包含精确文件清单、六层、执行方式、产出、验收、未决、失败处理？
- [ ] 用户在启动前明确确认了提示词？
- [ ] `start_session` 参数没有 cloud / environment / repository / offer？
- [ ] `pending.json` 已写，且不轮询？
- [ ] 收到 side-sessions-event 后先判断会话是否真的完成？
- [ ] 验收逐条有证据，结果 token 正确？
- [ ] 只改了目标任务与 FLOW 的授权字段？
- [ ] 每个任务后停下，没有自动连跑？

---

## 下一步

- 验收通过后 → `/wfh-ask`（status 模式）看新 frontier，或 `/wfh-implement-spec <下一条>`。
- 需要手动补验收 → `/wfh-implement-spec --close <ID>`。
- 只想生成提示词 → `/wfh-next <ID>`。
- 需要改任务图 → `/wfh-tickets`；需要改研究决策 → `/wfh-grill`。
