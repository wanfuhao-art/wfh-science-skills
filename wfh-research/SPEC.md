# wfh-research 设计规格（SPEC）

> 由 matt `to-spec` 从当前对话合成，**不再访谈**。
> 日期：2026-11-13
> 状态：待确认（验证接缝）
> 说明：本项目没有 issue tracker，也不引入 GitHub 概念；按 matt 的 local-markdown 回退，规格落在共享包内。
> 2026-11-13 更新：`wfh-status` 已并入 `wfh-ask` 的 status 模式；下文出现的 `wfh-status` 为历史设计记录。当前可执行入口为 6 个。

---

## Problem Statement

ARS 在生产端很强（检索、写作、审稿、改稿、格式、可审计），但有四个缺口：

1. **决策收敛慢。** Socratic 是非生成、一次 1–2 问、每层至少 2 轮；`plan` 按章节走，6 章至少 12 轮。用户已经想清楚的部分也要走完。
2. **没有任务图。** Pipeline 是横向阶段（研究→写作→审稿），阶段内部是一个黑箱；写作阶段仍会在一个会话里越写越长，上下文爆掉。
3. **没有决策与术语的持久层。** 术语定义、方法决策只存在于对话或一次性产物里；跨会话后无法追溯“为什么选乙腈、为什么这个电压窗口”。
4. **没有“我现在该用哪个”的入口。** ARS 35 个 mode + 7 个新技能，用户记不住；现有 routing 只处理输入歧义，不处理用户迷茫。

matt 的 `grilling` / `grill-with-docs` / `to-spec` / `to-tickets` / `ask-matt` 正好补这四块，但它面向代码：`GLOSSARY.md` / ADR、issue tracker、git worktree、TDD、PR。直接照搬会把科研工作流变成软件工程。

---

## Solution

一个科研专用的 **6 技能套件**，前缀 `wfh-`，加一个共享包 `wfh-research`：

| 技能 | 对应 matt | 职责 |
|---|---|---|
| `wfh-grill` | `grill-with-docs` | 按轮盘问 + 即时写 `TERMS.md` / `decisions/MDR-*.md` / 决策台账 |
| `wfh-spec` | `to-spec` | 把对话合成 `BRIEF.md`，不再访谈 |
| `wfh-tickets` | `to-tickets` | 切成“最小可验证主张单元”的任务图 |
| `wfh-ask` | `ask-matt` | 在 ARS 35 个 mode + 6 个 wfh 模式之间给一条路径 |
| `wfh-ask`（status 模式） | paper-pipeline `status` | 读 `FLOW.md`，报告阶段 / 当前任务 / frontier / 缺失产物 |
| `wfh-next` | paper-pipeline `next` | 生成新会话启动提示词 |
| `wfh-close` | paper-pipeline `close` | 校验任务产出，更新 `FLOW.md` |
| `wfh-research` | 共享包（类似 `nature-shared`） | 总览、共享协议、模板、路由索引；不执行具体动作 |

生产仍由 ARS 完成；wfh 只决定“什么时候、拿什么输入、调哪个 ARS 模式”。

---

## User Stories

### A. 盘问与决策（`wfh-grill`）

1. 作为一个只有模糊机理假设的研究者，我想让系统按轮次盘问，以便在 3–4 轮内把研究设计问全，而不是 15 轮。
2. 作为一个研究者，我想让每个问题都带一个可推翻的默认建议，以便我只用判断接受 / 否决 / 修正。
3. 作为一个研究者，我想让系统把程序性决策、学科惯例、实质性决策分开，以便它不会替我做贡献声明或机理归因。
4. 作为一个研究者，我想让系统自己查期刊 scope、字数、文章类型、报告规范，以便我不回答本可查到的事实。
5. 作为一个研究者，我想让术语一确定就写进 `TERMS.md`，以便构念定义不随上下文丢失。
6. 作为一个研究者，我想让系统只在满足三门槛时写 MDR，以便决策记录不泛滥。
7. 作为一个研究者，我想在盘问结束前看到决策台账并确认，以便系统不会在共识未达成时动笔。
8. 作为一个研究者，我想让系统在我连续接受推荐时提醒我，以便我不会变成应声虫。
9. 作为一个研究者，我想让系统在答案推翻旧决策时重开分支，以便决策树自洽。
10. 作为一个研究者，我想让系统用边界案例压力测试构念，以便“循环寿命”“CEI”有可操作定义。
11. 作为一个研究者，我想让系统在实质性决策上不给建议，以便研究贡献仍然是我的。

### B. Brief 合成（`wfh-spec`）

12. 作为一个研究者，我想让系统把盘问对话合成 `BRIEF.md` 而不再访谈，以便我不重复回答。
13. 作为一个研究者，我想让 Brief 含 claim ledger（主张 / 证据状态 / 验证方式 / 风险），以便我知道每条主张还缺什么。
14. 作为一个研究者，我想让 Brief 的内容字段参考 ARS Schema 1，以便预检后由 `academic-paper` 普通 intake 读取已有答案，并以实际接收结果判断配置去重。
15. 作为一个研究者，我想让缺的字段标 `[UNRESOLVED]` 而不是被猜填，以便未决问题被下游看到。
16. 作为一个研究者，我想让 FINER 分数由我自己打，以便系统不替我判断研究价值。
17. 作为一个研究者，我想让 Brief 保留材料学扩展字段（电池体系、电压窗口、倍率、温度），以便社会科学字段不会卡住我。

### C. 任务图（`wfh-tickets`）

18. 作为一个研究者，我想让系统把 Brief 切成“最小可验证主张单元”，以便每条任务能独立回答“这条主张站得住吗”。
19. 作为一个研究者，我想让每条任务声明 blocked by，以便我知道哪些能并行、哪些必须等。
20. 作为一个研究者，我想让每条任务声明执行方式（ARS / direct / human），以便系统不假装能替我做湿实验。
21. 作为一个研究者，我想让每条任务能在新会话里完成，以便上下文不随论文变长而爆掉。
22. 作为一个研究者，我想让系统先做预加工（数据清洗、检索、量表核对），再做主张链，以便写作不被杂活打断。
23. 作为一个研究者，我想让全局机械改动（术语替换、引用格式切换）走 expand–contract，以便不把全文改乱。
24. 作为一个研究者，我想在任务图落盘前确认粒度、依赖、合并 / 拆分，以便任务图符合我的写作习惯。

### D. 路由（`wfh-ask`）

25. 作为一个记不住 35 个 ARS mode 的研究者，我想问“我现在该用哪个”，以便得到一条路径、一个命令、一条反模式。
26. 作为一个研究者，我想让路由在推荐前读对应 `SKILL.md`，以便它不凭记忆瞎说技能功能。
27. 作为一个研究者，我想让路由只覆盖 ARS + wfh，不接 `nature-*`，以便范围清晰。
28. 作为一个研究者，我想让路由在 ARS 不可用时明确报错，以便系统不静默降级。

### E. 状态板与会话交接（`wfh-status` / `wfh-next` / `wfh-close`）

29. 作为一个研究者，我想用 `wfh-status` 看到当前阶段、当前任务、frontier、缺失产物，以便我知道下一步。
30. 作为一个研究者，我想用 `wfh-next` 生成新会话启动提示词，以便我只读任务需要的文件。
31. 作为一个研究者，我想用 `wfh-close` 校验任务产出并更新 `FLOW.md`，以便状态板不漂移。
32. 作为一个研究者，我想让 `FLOW.md` 同时记阶段、任务图、决策台账、未决问题，以便一个文件看全貌。
33. 作为一个研究者，我想让 `wfh-next` 在启动提示词里带上 ARS Schema 校验，以便缺字段时停下而不是凭记忆补。

### F. 与 ARS 衔接

34. 作为一个研究者，我想让 wfh 只整理参考 Schema 1 的外部 Brief 和三样新产物，Schema 2–8 由 ARS 生产；ARS 内部 Passport 与回执遵守各自契约，以便来源与验证状态不混淆。
35. 作为一个研究者，我想让 wfh 不调用 `academic-pipeline`（除非我明确要一口气跑完），以便任务图不被另一个编排器接管。
36. 作为一个研究者，我想让 wfh 不改 ARS 文件、不 fork，以便 ARS 升级不冲突。
37. 作为一个研究者，我想让 ARS 的 `intake_agent` 能自动识别 `BRIEF.md`，以便不重复问已经答过的配置。

### G. 领域适配与安全

38. 作为一个材料研究者，我想让 `TERMS.md` 记录操作定义、包含 / 排除、来源 / 方法，以便构念可核验。
39. 作为一个材料研究者，我想让 MDR 记录“为什么选乙腈、为什么 LCO vs LNO、为什么这个电压窗口”，以便 Methods / Limitations / Response 有素材。
40. 作为一个研究者，我想让系统不编造引用、查不到就标 `[待核验]`，以便文献可信。
41. 作为一个研究者，我想让系统保留 ARS 的反谄媚检查，以便盘问不退化成点头。
42. 作为一个研究者，我想让系统在确认门之前不写正文，以便共识未达成时不动笔。

---

## Implementation Decisions

### 1. 套件结构

```
.claude/skills/
├── wfh-research/                 # 共享包，不执行具体动作
│   ├── SKILL.md                  # 总览：6 个技能怎么串
│   └── references/
│       ├── grilling_protocol.md  # frontier / 轮次 / 推荐 / facts-decisions / 确认门
│       ├── decision_classes.md   # 程序性 / 学科惯例 / 实质性
│       ├── terms_template.md     # TERMS.md 模板
│       ├── mdr_template.md       # MDR 模板与三门槛
│       ├── spec_template.md      # 外部 Brief 模板（内容字段参考 Schema 1）
│       ├── ars_handoff_protocol.md # 来源判定、内容预检、Skill 调用与内部链边界
│       ├── tickets_template.md   # tasks/T*.md 模板
│       ├── flow_template.md      # FLOW.md 模板
│       └── skills_index.md       # ARS + wfh 的路由索引（自动生成）
├── wfh-grill/SKILL.md
├── wfh-spec/SKILL.md
├── wfh-tickets/SKILL.md
├── wfh-ask/SKILL.md
├── wfh-status/SKILL.md
├── wfh-next/SKILL.md
└── wfh-close/SKILL.md
```

共享包是**唯一的协议来源**；6 个技能只写自己的入口、输入、输出和边界，不复制协议。这样避免 6 份规则漂移。

### 2. 命名与调用

- 所有技能用 `wfh-` 前缀，避免与 ARS / 其他技能混淆。
- 每个技能可独立斜杠调用：`/wfh-grill`、`/wfh-spec`、`/wfh-tickets`、`/wfh-ask`、`/wfh-next`、`/wfh-close`。
- `wfh-research` 是共享包/总览，不是执行入口；需要总览时读它的 `SKILL.md`。
- 自然语言触发也要支持（例如“盘一下这个想法” → `wfh-grill`），但斜杠命令是精确入口。

### 3. 产物布局

```
research/<slug>/
├── FLOW.md                 # 状态板：阶段 + 任务图 + 决策台账 + 未决问题
├── BRIEF.md                # Schema 1 RQ Brief + claim ledger + 材料学扩展
├── TERMS.md                # 构念 / 操作定义 / 包含 / 排除 / 来源
├── decisions/
│   ├── LEDGER.md           # 决策台账（确认过的决策）
│   └── MDR-0001-*.md       # 方法决策记录（三门槛）
├── tasks/
│   └── T01-*.md            # 一个任务一个文件
└── artifacts/
    ├── 01-rq-brief.md
    ├── 02-bibliography.md
    ├── 03-synthesis.md
    ├── 05-draft.md
    ├── 06-review-report.md
    ├── 07-revision-roadmap.md
    └── 09-response.md
```

`artifacts/` 里 Schema 2–8 的产物由 ARS 写；wfh 只写 `BRIEF.md`、`TERMS.md`、`decisions/`、`tasks/`、`FLOW.md`。

### 4. 与 ARS 的三层衔接

1. **文件契约**：`BRIEF.md` 是 wfh 整理的外部作者材料，含 `## RQ Brief` 与参考 Schema 1 的四个必需字段（`research_question`、`sub_questions`、`finer_scores`、`scope`）。先按共享 `ars_handoff_protocol.md` 校验值；标题或字段齐全不保证 ARS 接受，也不代表已验证内部 handoff。
2. **Skill 调用**：任务声明 `执行方式: ARS:<skill>:<mode>` / `direct` / `human`；`wfh-next` 或 `wfh-close` 按此调用 ARS 的 `wfh-science-skills:*` 技能。外部材料以真实来源和文件路径进入普通 intake；真正的 ARS 内部链保留并校验 Passport、current #672 receipt 与条件性 companion。
3. **会话交接**：`wfh-next` 生成启动提示词，只读 `FLOW.md` + 任务文件 + 任务声明的输入；调用前按 Schema 校验，缺必需值报 `HANDOFF_INCOMPLETE`、列缺项并停止。分别记录 wfh 预检与 ARS intake 的拒绝；成功导入需实际响应证据，不能以首错停止时“没重复提问”冒充。

### 5. 数据契约

- 内容字段复用 ARS Schema 1–8；不另造一套。wfh Brief 是外部材料，内部 handoff 身份及附属产物要求另按 `references/ars_handoff_protocol.md` 和当前 ARS 原文判定。
- Schema 1 的 `scope.population` / `timeframe` / `geography` 做领域映射：材料体系 / 循环窗口 / N/A。
- 新增三套模板：`TERMS.md`、`decisions/MDR-*.md`、`tasks/T*.md`；它们不属于 ARS Schema，但作为上下文被 ARS 模式读取。
- `BRIEF.md` 的 `finer_scores` 由用户打分；平均 <3.0 或任一项 <2 时标红，建议回到 `wfh-grill`。

### 6. 三分法决策

| 类别 | 例子 | 能否给推荐 |
|---|---|---|
| 程序性 | 期刊格式、字数、结构模板、引用风格、检索策略 | ✅ 给默认建议，可推翻 |
| 学科惯例 | 样本量惯例、报告规范、统计呈现格式、伦理流程 | ✅ 给“惯例 + 建议”，标注为惯例 |
| 实质性 | RQ、贡献声明、机理归因、理论框架、结果解释、伦理立场、作者顺序 | ❌ 不给推荐，只问 |

### 7. 盘问协议

- **frontier**：每轮只问前置已定的问题；答案会重排树。
- **格式**：`❓ Qn — 标题` + 正文 + `➡️ 默认建议`；实质性决策用 `⛔ 这一题没有建议`。
- **facts**：派 subagent 查期刊、报告规范、仪器/量表信息；不阻塞本轮；查不到标 `[待核验]`。
- **确认门**：frontier 空后先出决策台账，用户确认才落盘。
- **反应声虫**：连续 3 次接受推荐 → 下一题不给推荐；整场 yes-rate > 80% 时提示。
- **重开**：新答案推翻旧决策时，下一轮重开该分支并在台账标“已修订”。

### 8. 任务图规则

- 纵向切片 = **最小可验证主张单元**：一条主张 → 证据 → 分析 → 图/表 → 一段正文 → 引用。
- 每条任务必须：独立可验证、能塞进一个新会话、声明 `blocked by`、声明 `执行方式`、有验收标准。
- **tracer bullet**：第一条任务先跑通一条完整主张链，再复制到其他主张。
- **expand–contract**：全局术语替换、引用格式切换、时态统一等机械改动，按“新形式并存 → 分批迁移 → 删除旧形式”处理。

### 9. 状态板 `FLOW.md`

```markdown
# WFH Research Flow: <标题>

Status: stage-<N>-<state>
Current stage: ...
Current task: ...

## 阶段
| # | 阶段 | 状态 | 产出 | 校验 |

## 任务图
| Task | 状态 | Blocked by | 执行方式 | 产出 |

## 决策台账
| ID | 决策 | 选择 | 理由 | 可逆性 | 影响章节 |

## 未决问题
- [UNRESOLVED] ...

## 下一步
（wfh-next 生成的启动提示词）
```

### 10. 路由索引

- `wfh-ask` 读 `wfh-research/references/skills_index.md`，索引来源：ARS `MODE_REGISTRY.md` + 7 个 `wfh-*` 的 frontmatter。
- 索引只存 name / description / path / 一句话适用场景。
- 推荐前必须读对应 `SKILL.md`；不许凭记忆描述。
- `wfh-ask refresh` 重新生成索引。
- **不索引 `nature-*`**。

### 11. 语言与输出

- 技能说明中文优先，保留英文触发词。
- 研究产物跟随论文语言；材料学论文通常英文，`TERMS.md` 可中英并列。
- 所有产物 Markdown；DOCX/LaTeX/PDF 由 ARS `format-convert` 负责。

### 12. 边界

- 不改 ARS 文件、不 fork、不往 ARS 缓存写东西。
- 不接 `nature-*`。
- 不调用 `academic-pipeline`，除非用户明确要“一口气跑完”，此时退出任务图模式。
- 不引入 issue tracker、GitHub、git worktree、PR、TDD。
- `wfh-grill` 使用自己的 `grilling_protocol.md`，不依赖 matt 插件必须安装；matt 的 `grilling` 只在显式要求时作为参考。

### 13. 错误处理

- `HANDOFF_INCOMPLETE`：Schema 必需字段缺失/值未决或无效，停止并列出缺项；记录拒绝方是 wfh-precheck 还是 ars-intake，前者不调用 ARS。内部 handoff 的额外缺项按当前 ARS 契约处理。
- `[UNRESOLVED]`：Brief 中未决项，带进下游。
- `[待核验]`：事实未核实，不许写成确定结论。
- `ARS_NOT_AVAILABLE`：ARS 插件不可用，明确报错，不静默降级。

---

## Testing Decisions

### 最高接缝

只测一条端到端链路：**`wfh-grill → wfh-spec → wfh-tickets → wfh-status/next → ARS handoff`**。不按单个技能的措辞或内部步骤测试。理想情况下这是唯一的接缝；如果某段协议需要单独验证，优先用合成案例而不是新增测试层。

### 什么算好测试

- 只测外部行为：产物是否存在、字段是否齐全、任务是否能独立执行、ARS 是否能消费。
- 不测模型输出的具体句子。
- 每个测试都要能在一次会话里跑完，且不依赖真实实验数据（真实案例除外）。

### 测试用例

1. **合成盘问**：以“AI 辅助科研对研究者能力的影响”为题，`wfh-grill` 应在 ≤4 轮内问完 13 个规划问题；不得问任何 agent 本可查到的事实；实质性决策不得出现推荐；结束时生成 `TERMS.md`、至少 1 条 MDR、决策台账，并停在确认门。
2. **合成 Brief**：`wfh-spec` 从上述对话生成 `BRIEF.md`，含 Schema 1 四个必需字段 + claim ledger；不得重新访谈；缺项标 `[UNRESOLVED]`；FINER 分数来自用户。
3. **合成任务图**：`wfh-tickets` 生成 ≥6 条任务；每条有 `blocked by`、`执行方式`、验收标准；任务图无环；每条声明“一个会话可完成”。
4. **状态板闭环**：`wfh-status` 报告 frontier；`wfh-next` 生成只读任务输入的提示词；`wfh-close` 校验产出并更新 `FLOW.md`；frontier 正确推进。
5. **路由**：对“我有审稿意见”“我有个模糊想法”“我要投稿”三种输入，`wfh-ask` 各给一条路径、一个命令、一条反模式；推荐前读取对应 `SKILL.md`。
6. **真实案例（电池课题）**：以“乙腈电解液中 LCO 与 LNO 循环寿命差异的机理研究”为题，检查 `TERMS.md` 覆盖 LCO/LNO/CEI/循环寿命/过渡金属溶解；MDR 覆盖乙腈选择、电压窗口、LCO vs LNO 对照；claim ledger 含 C1–C4；任务图含 `human` 类型的 XPS/ICP-MS 任务与正确的 blocking edges。
7. **ARS 交接**：wfh 外部 Brief 经内容预检后，以明确来源交给 `academic-paper` 普通 intake，实际接受并导入已有配置；未提供配置仍可问。相同前置条件只删 Scope，wfh 预检须列 `scope` 并报 `HANDOFF_INCOMPLETE`；ARS 直接输入若也拒绝，单独记录其缺项和原因。保留 FINER 未决拒绝样本。内部链的 Passport/#672 门禁继续有效，不靠假身份或命令跳过；单次提示词测试不宣称确定性稳定。
8. **反谄媚与完整性**：连续 3 次接受推荐后，下一题无推荐；任何文献事实必须有来源或 `[待核验]`；不得编造引用。

### 先例

- ARS 的 `plugin-evals/` 与 `evals/heldout/`：用固定案例检查行为边界。
- matt 的 “It's working if” 清单：用可观察行为判断技能是否生效。
- 已删除的 `paper-pipeline` 的交接校验规则：Schema 必需字段缺失时停止，不凭记忆补。

---

## Out of Scope

- v2 执行编排：并行 frontier、subagent 调度、自动合并。
- `nature-*` 技能集成。
- 修改或 fork ARS。
- issue tracker、GitHub、git worktree、PR、TDD。
- 多人协作、实时共编。
- DOCX/LaTeX/PDF 生成（交给 ARS `format-convert`）。
- 英文优先的界面；本套件中文优先。
- `wfh-grill` 内部自动做完整文献检索（交给 `deep-research` 或事实 subagent，只做快速核查）。
- 实验室自动化、仪器控制、真实数据采集。

---

## Further Notes

### 风险与缓解

| 风险 | 缓解 |
|---|---|
| 推荐答案锚定用户，尤其在小领域 | 实质性决策不给推荐；连续接受 3 次后强制无推荐；台账记录“是否接受推荐” |
| `TERMS.md` 膨胀成 spec | 只记有争议/项目特有的构念；每条必须有包含/排除边界；不记教科书定义 |
| 任务切得太细，管理成本高于写作 | 默认按“主张链”切；用户可在 `wfh-tickets` 的确认步骤合并 |
| ARS 版本升级导致入口或 Schema 漂移 | 内容字段参考 Schema 1，入口及附属产物适用条件以当前 ARS 原文为准；升级后复测外部正例和缺项拒绝；内部链遵守 Passport/#672 契约 |
| 路由索引过期 | `wfh-ask refresh` 重新生成；推荐前读 `SKILL.md` |
| 用户把 `wfh-*` 误当成 ARS 本身 | `wfh-research/SKILL.md` 明确写“这是 ARS 的补丁层，不是替代品” |

### 成功标准

- `wfh-grill`：13 个规划问题 ≤4 轮问完；零个“本可查到”的事实问题；实质性决策零推荐。
- `wfh-spec`：零重复访谈；Schema 1 四字段齐全；`[UNRESOLVED]` 可见。
- `wfh-tickets`：每条任务一个新会话可完成；完成后能独立回答“这条主张站得住吗”。
- `wfh-ask`：3 轮内给出一条路径 + 一个命令 + 一条反模式。
- 真实案例：电池课题能跑通 `grill → spec → tickets → status/next`，且 `TERMS.md` / MDR / claim ledger 符合材料学写作习惯。

### 待定问题

- `wfh-grill` 是直接写 `FLOW.md` 的决策台账，还是只写 `decisions/LEDGER.md`、由 `wfh-close` 合并进 `FLOW.md`？
- `wfh-close` 只校验任务验收标准，还是也校验 Schema 1？
- v2 是否增加 `wfh-implement`（任务级执行入口），还是由 `wfh-next` 直接承担？
- `skills_index.md` 的自动生成脚本放在 `wfh-research/scripts/` 还是项目根 `scripts/`？
