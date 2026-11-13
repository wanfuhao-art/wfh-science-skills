---
name: wfh-grill
description: "按轮盘问研究课题，收敛决策，边问边写 TERMS.md / MDR，结束时出决策台账并停在确认门。用于研究设计盘问、课题盘问、把模糊想法问清楚、投稿前决策自检；English triggers: grill a research idea, research design interview, decision convergence, wfh-grill. 不用于探索式 Socratic（用 ARS deep-research socratic），不用于直接写作（用 ARS academic-paper）。"
---

# wfh-grill — 科研盘问与决策收敛

> wfh-research 套件的决策层入口。
> 本技能只做「把决策问全、问快」，不写论文内容；生产由 ARS 完成。

---

## 定位

- 这是 matt `grill-with-docs` 的**科研版**：按轮盘问 + 即时落盘（`TERMS.md` / `MDR`），结束时出决策台账。
- 只做决策收敛；不做文献综述、不写 `BRIEF.md`、不写正文、不生成提纲。
- **不依赖 matt 插件。** 盘问协议自带，见共享包。
- 只处理科研决策与产物，不引入软件工程流程概念。

### 与 ARS Socratic 的分工

| 用户状态 | 用什么 |
|---|---|
| 不知道要研究什么，需要探索 | ARS `deep-research` socratic（非生成、一次一问） |
| 已有方向，要把决策定下来 | **本技能** |
| 决策已定，要写 Brief | `wfh-spec` |
| 要检索、写作、审稿、改稿 | ARS 对应技能 |

不要用本技能替代 Socratic；也不要在用户已经想清楚时硬走盘问。

---

## 何时用 / 不用

**用**：

- 只有一个模糊想法，需要问清贡献、证据、设计、分析；
- 课题方向大致定了，但研究设计、样本、报告规范还没定；
- 投稿前自检：主张强度、证伪条件、局限是否自洽；
- 已有材料散落在笔记里，需要收敛成一组可追溯的决策。

**不用**：

- 已经有 `BRIEF.md`，只差写作 → `wfh-spec` / ARS `academic-paper`；
- 需要系统检索与证据综合 → ARS `deep-research`；
- 收到审稿意见要回复 → ARS `academic-paper` revision；
- 只想润色文字 → ARS polishing 类模式。

---

## 输入

- **必需**：一个课题描述，一句话到一段话即可。
- **可选**：已有数据清单、笔记、之前论文、导师要求、目标期刊、已有 `research/<slug>/`。
- **开始前先读**：用户给的材料与工作区里已有的产物。能回答的节点直接标「已定」，不提问。

---

## 输出

工作区：项目根下 `research/<slug>/`。

| 文件 | 写入时机 |
|---|---|
| `TERMS.md` | 术语一确定就写（状态 `待确认`） |
| `decisions/MDR-<NNNN>-<slug>.md` | 决策过三门槛就写（状态 `草稿`） |
| `decisions/LEDGER.md` | 确认门通过后写 |

**不写**：`BRIEF.md`、`FLOW.md`、`tasks/`、`artifacts/`。这些由 `wfh-spec` / `wfh-tickets` / ARS 负责。

---

## 执行前必读（共享包，唯一协议来源）

按顺序读（括号内为项目根路径；两者指向同一文件）：

1. [`../wfh-research/references/grilling_protocol.md`](../wfh-research/references/grilling_protocol.md)（`wfh-research/references/grilling_protocol.md`）— 设计树 / frontier / 轮次 / 格式 / facts / 反谄媚 / 重开 / 确认门 / 默认 14 题
2. [`../wfh-research/references/decision_classes.md`](../wfh-research/references/decision_classes.md)（`wfh-research/references/decision_classes.md`）— 程序性 / 学科惯例 / 实质性
3. [`../wfh-research/references/terms_template.md`](../wfh-research/references/terms_template.md)（`wfh-research/references/terms_template.md`）— `TERMS.md` 模板
4. [`../wfh-research/references/mdr_template.md`](../wfh-research/references/mdr_template.md)（`wfh-research/references/mdr_template.md`）— MDR 模板与三门槛

**不要凭记忆执行。** 本文件只写入口、输入、输出与边界；协议冲突时以共享包为准。

---

## 流程

### 1. 建工作区

1. 从课题描述生成 slug：小写英文 / 数字 / 连字符，2–5 词（如 `ai-research-capability`）。slug 是程序性决策，可给建议，用户可改。
2. 创建 `research/<slug>/` 与 `research/<slug>/decisions/`。
3. 创建最小 `FLOW.md`（按 `flow_template.md` §8.5：`stage-1-active`，下一步 `/wfh-grill`）；已存在则只增量更新，不覆盖用户内容。
4. 若目录已存在：读入 `TERMS.md`、`decisions/LEDGER.md`、已有 MDR 与 `FLOW.md`，作为「已定」输入，从剩余 frontier 继续；**不覆盖**已有文件。
5. 若用户没给课题描述：先问一句课题是什么，不要空转建目录。

### 2. 建树

1. 以协议 §11 的 14 题默认树为起点，按课题增删。
2. 读用户材料，把已有答案的节点标「已定」。
3. 给每个待定节点标类别（`decision_classes.md`）与依赖。
4. 列出需要事实的节点，**并行**派 subagent 调查（协议 §4），不阻塞本轮。

### 3. 按轮问

1. 重算 frontier：只保留前置已定的节点。
2. 按协议 §2 的格式一次问完整个 frontier，然后**停下**。
3. 同一轮内不得有相互依赖的问题。
4. 依赖未返回事实的节点，下一轮再问。
5. 用户可按编号回答；不要要求用户复述问题。

格式速查（完整规则见协议 §2）：

```markdown
❓ **Q2 — 标题**
正文：这题决定什么、影响什么。
（a）… （b）… （c）…

➡️ **默认建议**：……。理由：……。**可推翻**。
```

实质性题用：

```markdown
⛔ **这一题没有建议**：……必须由你给出。我可以做的是：……。
```

### 4. 即时落盘

- 术语确定 → 立即按模板追加 `TERMS.md`（`待确认`）。
- 决策过三门槛 → 立即写 MDR（`草稿`）。
- 台账在对话内维护，不提前写 `LEDGER.md`。

### 5. 重开

新答案推翻旧决策时：

1. 下一轮开头明说重开了哪一支、影响哪些节点；
2. 受影响节点回到「待定」，重新进入 frontier；
3. 台账原行标 `已修订`，新决策用新 ID；
4. 受影响的 TERMS / MDR 更新并写修订记录；
5. 从回环包重开（跨会话）：读 `decisions/REOPEN-*.md`，按 `classification` 与 `affected_decisions` 重开对应分支；台账原行标 `已修订`，新决策用新 ID；在回环包「处理记录」写 `accepted` / `rejected` 与日期；受影响任务按 `recommended_path` 交给 `wfh-tickets` 重切。

### 6. 确认门

1. frontier 空（或用户明确接受剩余未决项）后，输出**完整决策台账** + 产物清单 + 未决 / 待核验项。
2. 问一句：「以上是否就是我们的共同理解？」
3. **停下。** 不写 Brief、不写正文、不调用 ARS 生产技能。
4. 用户确认后：写 `decisions/LEDGER.md`；`TERMS.md` / MDR 状态改 `已确认`；按 `flow_template.md` §8.5 把 `FLOW.md` 的阶段 1 改 `done`，写「下一步」= `/wfh-spec`（命令 / 输入 / 产出 / 失败时 / 更新于）；提示下一步 `/wfh-spec`。
5. 用户不确认：回到对应分支重开，不落盘台账。

---

## 硬规则

1. **实质性决策零推荐**：不排序、不给默认值、不写「通常」「建议」「更好的做法」。
2. **不问 agent 本可查到的事实**：期刊 scope / 字数 / 文章类型 / 报告规范 / 仪器信息 / 量表信息，派 subagent 查；查不到标 `[待核验]`，不编。
3. **连续 3 次接受推荐 → 下一道可推荐题强制不给建议**，并说明触发原因。
4. **术语一确定就写 `TERMS.md`；MDR 只过三门槛才写**。
5. **确认门之前不写 `BRIEF.md`、不写正文、不调 ARS 生产技能**。
6. **被推翻的决策必须重开并在台账标「已修订」**，不静默覆盖。
7. **不替用户回答未决项**：用户不答就标 `[UNRESOLVED]`，继续其他 frontier。
8. **只处理科研决策与产物，不引入软件工程流程概念**。
9. **不改 ARS 文件、不接 `nature-*`、不依赖 matt 插件**。
10. **FINER 只接收用户评分**：不代填、不建议、不评价、不排序；未评就标 `[UNRESOLVED]`，确认门记录用户接受。
10. **用户说「先到这」就停**：列出未问节点，标「frontier 未完成」，不假装达成共识。

---

## 错误处理

| 情况 | 动作 |
|---|---|
| 事实查不到 | `[待核验]` + 写清查了什么、为什么没查到；下游不得写成确定结论 |
| 用户不回答某题 | 标 `[UNRESOLVED]`，继续其他 frontier；不替答 |
| 用户要求对实质性决策给建议 | 说明这会绕过作者权边界；只列选项与代价，不选。即使用户坚持，也不替用户选；请用户自己给答案，或标 `[UNRESOLVED]` 留给下游 |
| 用户要求跳过盘问直接写 | 说明确认门；可缩短树（删掉不适用的节点），但不能跳过确认门 |
| 工作区已存在同名课题 | 读入已有产物，从剩余 frontier 继续；冲突时问用户，不覆盖 |
| 课题范围过大，4 轮问不完 | 轮首报告原因，问用户是否收窄 scope；不默默继续 |
| ARS 不可用 | 本技能不需要 ARS；只在提示下一步时说明 `ARS_NOT_AVAILABLE`，不静默降级 |

---

## 结束前自检

- [ ] 14 题（或增删后）≤4 轮问完？
- [ ] 零个「本可查到」的事实问题？
- [ ] 实质性决策零推荐？
- [ ] `TERMS.md`：有构念定义时至少 1 条，且有包含 / 排除；没有则说明为什么？
- [ ] 过三门槛的决策都有 MDR？没过门槛的只进台账？
- [ ] 台账完整，含未决项与待核验项？
- [ ] 停在确认门，没有提前动笔？
- [ ] `FLOW.md` 的阶段 1 与「下一步」已更新？
- [ ] 没有引入软件工程流程概念？

---

## 下一步

- 用户确认后 → `/wfh-spec`：把盘问产物合成 `BRIEF.md`（Schema 1 四字段 + claim ledger），**不再访谈**。该技能由套件后续 ticket 提供；未实现前可先按 `BRIEF.md` 的结构手动整理。
- 需要补文献 → ARS `deep-research`。
- 需要写作 / 审稿 / 改稿 → ARS `academic-paper` / `academic-paper-reviewer`。
