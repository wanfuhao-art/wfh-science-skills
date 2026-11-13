---
name: wfh-spec
description: "把 wfh-grill 的盘问产物合成 research/<slug>/BRIEF.md（ARS Handoff Schema 1 四字段 + claim ledger + 材料学扩展），不重新访谈，缺项标 [UNRESOLVED]。用于盘问确认后的 Brief 合成、交接 ARS academic-paper 前的准备；English triggers: synthesize research brief, research spec, wfh-spec, brief from grilling. 不用于继续盘问（用 wfh-grill），不用于切任务（用 wfh-tickets），不用于写作（用 ARS academic-paper）。"
---

# wfh-spec — Brief 合成

> wfh-research 套件的交接层入口。
> 本技能只做「把已确认的盘问产物压成 Brief」，不重新访谈、不做新决策、不写正文。

---

## 定位

- 这是 matt `to-spec` 的**科研版**：读对话与产物，合成 `BRIEF.md`，**不再提问研究决策**。
- 上游是 `wfh-grill` 的确认门；下游是 ARS `academic-paper` 的 `intake_agent` 与 `wfh-tickets`。
- 只写 `BRIEF.md` 一个文件；不改 `TERMS.md` / `LEDGER.md` / MDR，不写 `FLOW.md` / `tasks/` / `artifacts/`。
- **不依赖 matt 插件**；不引入代码 / GitHub / PR / TDD 概念。

### 与相邻技能的分工

| 用户状态 | 用什么 |
|---|---|
| 还没问清楚，决策未定 | `wfh-grill` |
| 盘问已确认，要把决策压成 Brief | **本技能** |
| 已有 Brief，要切任务 | `wfh-tickets` |
| 要检索、写作、审稿、改稿 | ARS 对应技能 |

---

## 何时用 / 不用

**用**：

- `wfh-grill` 已过确认门，`decisions/LEDGER.md` 已落盘；
- 用户已有 `TERMS.md` / MDR / 台账，要交给 ARS 写作；
- Brief 需要更新（决策修订、未决项补录）。

**不用**：

- 决策还没定、或台账未确认 → 先 `wfh-grill`；
- 要重新讨论 RQ / 贡献 / 设计 / 分析 → `wfh-grill`（本技能不重新访谈）；
- 要切任务 → `wfh-tickets`；
- 要写正文 / 提纲 → ARS `academic-paper`。

---

## 输入

**必需**（同一工作区 `research/<slug>/`）：

- `decisions/LEDGER.md`：已确认的决策台账（确认门后写入）。

**可选**：

- `TERMS.md`：构念定义；
- `decisions/MDR-*.md`：方法决策记录；
- 已有 `BRIEF.md`（增量更新）；
- 用户在本次调用中直接给的材料或 FINER 评分。

**开始前先读**：上述全部文件。能从事产物回答的，不再问用户。

---

## 输出

| 文件 | 写入时机 |
|---|---|
| `research/<slug>/BRIEF.md` | 用户确认后（默认）；用户明确要草稿时先写 `状态：草稿`，确认后改 `已确认` |

**不写**：`TERMS.md`、`decisions/*`、`FLOW.md`、`tasks/`、`artifacts/`。

---

## 执行前必读（共享包，唯一协议来源）

按顺序读（括号内为项目根路径；两者指向同一文件）：

1. [`../wfh-research/references/spec_template.md`](../wfh-research/references/spec_template.md)（`.claude/skills/wfh-research/references/spec_template.md`）— BRIEF.md 模板、Schema 1 映射、claim ledger 与材料学扩展写法
2. [`../wfh-research/references/grilling_protocol.md`](../wfh-research/references/grilling_protocol.md) §7.3 / §8.5 — 台账字段与确认状态的含义
3. 准备交给 ARS 或说明下一步时：读 [`../wfh-research/references/ars_handoff_protocol.md`](../wfh-research/references/ars_handoff_protocol.md) — 区分外部作者材料与 ARS 内部 handoff，检查必需值并声明来源。
4. 需要核对术语 / MDR 语义时：[`../wfh-research/references/terms_template.md`](../wfh-research/references/terms_template.md)、[`../wfh-research/references/mdr_template.md`](../wfh-research/references/mdr_template.md)

**不要凭记忆执行。** 本文件只写入口、流程与边界；模板细节以共享包为准。

---

## 流程

### 1. 预检

1. 找 `research/*/decisions/LEDGER.md`：
   - 只有一个 → 用它；
   - 多个 → 问用户选哪个（这是本技能允许的提问之一）；
   - 没有 → `GRILL_NOT_CONFIRMED`，停（见错误处理）。
2. 读台账，确认：
   - 有 `确认日期`；
   - 没有「frontier 未完成」标记；
   - 决策行状态为 `已确认`（`未决` / `待确认` 行不算已定）。
3. 读 `TERMS.md`、`decisions/MDR-*.md`、已有 `BRIEF.md`。
4. 向用户报一行输入清单：台账 N 行 / TERMS N 条 / MDR N 份 / 已有 Brief 有或无。

### 2. 抽取

按 `spec_template.md` §2 的映射表，把产物抽成 Brief 字段。每条记录来源：

| 抽取项 | 来源 |
|---|---|
| RQ | 用户原话；否则 D01 + D03 + D04 + D05 合成 |
| 子问题 | RQ 拆解 + D07 + MDR 后续影响 |
| FINER | 台账 FINER 节 / 用户本次补录 |
| scope 六轴 | 期刊 / 证据来源 / 设计 / 样本 / 局限 / 时间线等决策 + TERMS 包含 / 排除（台账 ID 以实际为准） |
| claim ledger | RQ 拆解 + D01 / D04 / D07 / D10 / D12 + MDR + TERMS |
| 方法决策 | D05 / D07 / D09 + MDR |
| 证伪 | D12 + 每条 claim |
| 材料学四字段 | 证据来源 / 设计 / 测试条件（电压、倍率、温度）等决策 + MDR / TERMS（台账 ID 以实际为准） |
| 未决 / 待核验 | 台账同名节 + TERMS / MDR 中的标记 |

抽取时：

- 只搬运、组织和压缩；**不新增**用户没说过的主张、理由或数值；
- 同一字段多个来源冲突 → 记入冲突清单，不自行选一个；
- 找不到来源的字段 → 留 `[UNRESOLVED]`。

### 3. 组装

严格按 `spec_template.md` §3 的骨架写。硬性结构：

- `## RQ Brief` 标题；
- 四个必需字段：`research_question` / `sub_questions` / `finer_scores` / `scope`；
- claim ledger 四列：主张 / 证据状态 / 验证方式 / 风险；
- 材料学四字段：材料体系 / 电压窗口 / 倍率 / 温度。

### 4. 完整性校验

逐项过 `spec_template.md` §4 的规则，输出一张检查表：

| 检查 | 结果 |
|---|---|
| `## RQ Brief` 存在 | ✅ / ❌ |
| 四个必需字段存在 | ✅ / ❌ |
| 子问题 2–5 条 | ✅ / ❌ / `[UNRESOLVED]` |
| FINER 五项 1–5，评分人 = 用户 | ✅ / ❌ / `[UNRESOLVED]` |
| scope 六行齐全 | ✅ / ❌ |
| claim ledger ≥1 条，四列齐全 | ✅ / ❌ |
| 每条 claim 有溯源 | ✅ / ❌ |
| 材料学四字段存在 | ✅ / ❌ / 不适用 |
| 每个 `[UNRESOLVED]` 都汇总到未决问题 | ✅ / ❌ |
| 本次未提出研究决策问题 | ✅ |

任一项 ❌ 且不能靠标 `[UNRESOLVED]` 解决 → 不进入确认门，先修。

### 5. 确认门

输出：

1. **Brief 摘要**：RQ 一句；子问题 N 条；FINER 状态；scope 四轴一句话；claim N 条；未决 N 项；待核验 N 项。
2. **未决清单**：每条 `[UNRESOLVED]` 一行，写清哪个字段、为什么、谁能解决。
3. **冲突清单**（如有）：字段 / 两个值 / 各自来源。
4. **一句提问**：

   > 以上 claim ledger、未决项与 FINER 是否就是你要交给 ARS 的交接缝？确认后写入 `BRIEF.md`。未决项可以现在补录（只补值，不展开讨论），也可以保持 `[UNRESOLVED]` 带进下游。

5. **停下。** 不写正文、不切任务、不调 ARS。

本门只确认**交接缝**（claim ledger + 未决 + FINER），不逐字确认整份 Brief 的措辞；措辞问题在落盘后按「修订记录」增量更新。

允许在确认门做的：

- 补录 FINER 分数（只接收用户给的分数，不提示、不建议、不评价）；
- 补录材料学字段；
- 裁决产物冲突；
- 确认 / 修改 Brief 措辞。

不允许：

- 追问 RQ、贡献、设计、分析等研究决策；
- 替用户补任何值。

### 6. 落盘

1. 写 `research/<slug>/BRIEF.md`，`状态：已确认`。
2. 已有 `BRIEF.md`：先读，保留用户手改；变更写进「修订记录」；不静默覆盖。
3. 更新 `FLOW.md`：阶段 1 `done`、阶段 2 `done`、`Status: stage-3-active`；「下一步」= `/wfh-tickets`（命令 / 输入 / 产出 / 失败时 / 更新于），保留用户备注。
4. 提示下一步：`/wfh-tickets`（切任务）或 ARS `academic-paper`（写作）。

---

## 硬规则

1. **零重复访谈**：不问 13 题树里的任何研究决策；只允许问工作区选择、产物冲突裁决、Brief 确认、缺项补录。
2. **缺项标 `[UNRESOLVED]`，不猜填**：尤其 FINER 与材料学数值。
3. **FINER 只来自用户**：不代填、不建议、不评价、不排序；用户只给部分，其余保持未决。
4. **claim 必须可溯源**：无来源的主张不写入 ledger，放进未决问题。
5. **不改上游产物**：`TERMS.md` / `LEDGER.md` / MDR 只读。
6. **不写正文 / 提纲 / 任务**；只更新 `FLOW.md` 的阶段状态与「下一步」，不改任务区、决策台账与未决问题。
7. **冲突不静默裁决**：列出两个值与来源，请用户定。
8. **`[待核验]` 原样带入**，不升级为确定结论。
9. **不引入代码 / GitHub / PR / TDD 概念**。
10. **不改 ARS 文件、不接 `nature-*`、不依赖 matt 插件**。

---

## 错误处理

| 情况 | 动作 |
|---|---|
| `LEDGER.md` 不存在 | `GRILL_NOT_CONFIRMED`：停；说明本技能只合成已确认的盘问产物；建议 `/wfh-grill`。不凭对话记忆造台账 |
| 台账存在但未确认（无确认日期 / 标「frontier 未完成」） | 默认停；用户明确要求「按当前台账先合成草稿」→ 写 `状态：草稿`，未确认决策在 Brief 中标「未确认」，不冒充已确认 |
| `TERMS.md` 缺失 | 不阻塞；术语节写「无 `TERMS.md`：盘问未产生需定义的构念」，不代写定义 |
| MDR 缺失 | 不阻塞；方法决策只引台账行，MDR 列填 `—`；不补写 MDR |
| FINER 缺失 | `[UNRESOLVED]`；确认门提供补录；不代填、不建议分数 |
| 材料学字段缺失且课题是材料学 | `[UNRESOLVED]`；不猜电压窗口 / 倍率 / 温度 |
| 非材料学课题 | 四字段填「不适用（非材料学课题）」并写依据；不算缺项 |
| 产物之间冲突 | 列出冲突（字段 / 两个值 / 各自来源），停在该字段，请用户裁决；不以「较新」「较详细」为由自行选一个 |
| 已有 `BRIEF.md` | 先读；增量更新；保留用户手改；冲突问用户；修订记录追加一行 |
| 用户要求顺便写提纲 / 切任务 | 拒绝：本技能只写 `BRIEF.md`；指向 `wfh-tickets` / ARS |
| 用户要求对 FINER 给建议分 | 拒绝：FINER 是用户判断；只解释五项含义，不给分 |
| 用户要求补写 RQ / 贡献 / 设计 | 拒绝：这是重新访谈；指向 `wfh-grill` |
| ARS 不可用 | 本技能不需要 ARS；提示下游时说明 `ARS_NOT_AVAILABLE`，不静默降级 |

---

## 结束前自检

- [ ] 只读了产物，没有重新访谈？
- [ ] `## RQ Brief` + 四个必需字段齐全？
- [ ] FINER 全部来自用户或 `[UNRESOLVED]`？
- [ ] claim ledger 四列齐全、每条有溯源？
- [ ] 材料学四字段存在（值 / 不适用 / `[UNRESOLVED]`）？
- [ ] 所有未决项都在正文与汇总中各出现一次？
- [ ] 没有改 `TERMS.md` / `LEDGER.md` / MDR？
- [ ] 没有写正文 / 提纲 / 任务？
- [ ] 没有引入软件工程流程概念？

---

## 下一步

- 确认后 → `/wfh-tickets`：把 claim ledger 切成任务图（该技能由套件后续 ticket 提供；未实现前可先按任务模板手动整理）。
- 准备写作 → 先按 [ars_handoff_protocol.md](../wfh-research/references/ars_handoff_protocol.md) 检查必需值和来源，再将 Brief 作为外部作者材料交给 ARS `academic-paper` 普通 intake；已有值供导入，未提供的配置仍待确认。四字段标签不保证接收成功。本技能到此只说明路径，不调用 ARS、不创建回执或 Passport。
- 需要补文献 → ARS `deep-research`。
