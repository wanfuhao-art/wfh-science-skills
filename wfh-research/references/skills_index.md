# ARS + wfh 路由索引（生成文件）

仅定位，不证明已读取、已加载、已验证或研究已执行。推荐前读取目标 SKILL 与模式要求的支持文件。

- 来源 ARS 根：`/Users/wanfuhao/Documents/ClaudeProjects/AI for science/.scratch/wfh-science-skills`
- ARS 状态：LOCATED（宿主加载状态另查）
- 实际 ARS 模式记录：35；wfh 预期入口：6；可读入口：6
- 来源指纹 SHA-256：`34727fd2b00377161c002bac6c5201a8aa1d9a3401659e8d5f8efb1a8fae4a7d`；输入文件：258
- 刷新 / 只读检查：[路由协议](routing_protocol.md)；工具：[refresh_index.py](../scripts/refresh_index.py)

## 诊断

OK：已按当前来源生成；每次咨询仍需 --check。

## 六个 wfh 执行入口

| 名称 | slash | frontmatter 描述 | 路径 | 主要支持协议 |
|---|---|---|---|---|
| wfh-grill | /wfh-grill | 按轮盘问研究课题，收敛决策，边问边写 TERMS.md / MDR，结束时出决策台账并停在确认门。用于研究设计盘问、课题盘问、把模糊想法问清楚、投稿前决策自检；English triggers: grill a research idea, research design interview, decision convergence, wfh-grill. 不用于探索式 Socratic（用 ARS deep-research socratic），不用于直接写作（用 ARS academic-paper）。 | [SKILL](../../wfh-grill/SKILL.md) | [grilling_protocol](grilling_protocol.md)、[decision_classes](decision_classes.md)、[terms_template](terms_template.md)、[mdr_template](mdr_template.md) |
| wfh-spec | /wfh-spec | 把 wfh-grill 的盘问产物合成 research/<slug>/BRIEF.md（ARS Handoff Schema 1 四字段 + claim ledger + 材料学扩展），不重新访谈，缺项标 [UNRESOLVED]。用于盘问确认后的 Brief 合成、交接 ARS academic-paper 前的准备；English triggers: synthesize research brief, research spec, wfh-spec, brief from grilling. 不用于继续盘问（用 wfh-grill），不用于切任务（用 wfh-tickets），不用于写作（用 ARS academic-paper）。 | [SKILL](../../wfh-spec/SKILL.md) | [spec_template](spec_template.md)、[ars_handoff_protocol](ars_handoff_protocol.md) |
| wfh-tickets | /wfh-tickets | 把 BRIEF.md 的 claim ledger 切成最小可验证主张单元的任务图，写 tasks/T*.md 与 FLOW.md 的任务区 / 初始状态；每条任务有 blocked by、执行方式（ARS / direct / human）、验收标准、产出路径、会话预算；落盘前先确认粒度、依赖、合并/拆分。用于 Brief 确认后的任务切分、写作前规划、判断哪些任务可并行；English triggers: split research brief into tasks, research task graph, wfh-tickets, tickets from brief. 不用于盘问（用 wfh-grill）、不用于合成 Brief（用 wfh-spec）、不用于写作（用 ARS academic-paper）。 | [SKILL](../../wfh-tickets/SKILL.md) | [tickets_template](tickets_template.md)、[flow_template](flow_template.md)、[spec_template](spec_template.md) |
| wfh-ask | /wfh-ask | 科研入口咨询与课题状态：不知道该用哪个 ARS / wfh 入口，或想知道课题现在做到哪、frontier、阻塞、缺件、未决，都用这个入口。输出取决于问题：路由问题给一条路径、一个可用命令和一条反模式；状态问题给阶段、frontier、startability、阻塞、缺件与未决。用于不知道用哪个技能、怎么用、已有工作如何续做、查看课题进度、检查状态板是否漂移、wfh-ask refresh；English: which research skill, research workflow advice, research task status, research frontier, wfh-ask. 只读，不执行；明确 ARS 命令或研究执行请求沿 ARS 原有路由，不由本入口抢占。 | [SKILL](../../wfh-ask/SKILL.md) | [routing_protocol](routing_protocol.md)、[skills_index](skills_index.md)、[state_protocol](state_protocol.md)、[flow_template](flow_template.md) |
| wfh-next | /wfh-next | 为一条科研任务生成可复制到新会话的启动或恢复提示词，限定为 FLOW、目标任务及声明输入；检查阻塞和 ARS 交接预检。用于接着做哪个任务、新会话如何接手、生成科研任务交接提示词；English: next research task, task handoff prompt, wfh-next。不自动开会话或执行任务；验收用 wfh-close。 | [SKILL](../../wfh-next/SKILL.md) | [state_protocol](state_protocol.md)、[tickets_template](tickets_template.md)、[ars_handoff_protocol](ars_handoff_protocol.md) |
| wfh-close | /wfh-close | 逐条用可追溯证据核对科研任务验收标准，记录 complete / partial / blocked，更新目标任务及 FLOW、重算 frontier。用于任务做完后的验收、收尾、产物缺件检查和推进状态板；English: close research task, verify task evidence, wfh-close。缺数据、实验结果或用户确认保留未决；不执行研究或生成缺失结果。 | [SKILL](../../wfh-close/SKILL.md) | [state_protocol](state_protocol.md)、[flow_template](flow_template.md)、[tickets_template](tickets_template.md)、[ars_handoff_protocol](ars_handoff_protocol.md) |

## ARS 模式

路径均相对上方 ARS 根；升级或迁移后重新 refresh，索引不把旧缓存路径当默认安装。
下列 slash 只列当前 commands 文件中可核对的映射。无 slash 的行可用「请使用 wfh-science-skills:<技能>，mode=<模式>，<请求>」。
`(pipeline)` 是编排入口而非命名模式；`resume_from_passport=<hash>` 是恢复参数，使用前须读其 opt-in 协议。

| Skill | mode / 入口 | 注册表产出与触发 | 路径 | 真实 slash 命令文件 |
|---|---|---|---|---|
| deep-research | `full` | APA 7.0 report, 3,000-8,000 words；"research [topic]", "deep research", "academic analysis" | `deep-research/SKILL.md` | 无；用技能名 + mode 请求 |
| deep-research | `quick` | Research brief, 500-1,500 words；"quick brief", "30 minute summary", "quick research" | `deep-research/SKILL.md` | 无；用技能名 + mode 请求 |
| deep-research | `review` | Reviewer report on provided text；"review this paper", "evaluate this paper", "assess this source" | `deep-research/SKILL.md` | 无；用技能名 + mode 请求 |
| deep-research | `lit-review` | Annotated bibliography + synthesis；"literature review", "annotated bibliography" | `deep-research/SKILL.md` | 无；用技能名 + mode 请求 |
| deep-research | `three-way-scan` | WHY/HOW/WHAT paper shortlist + cross-paper synthesis；"WHY HOW WHAT papers", "3W literature scan", "compare these papers" | `deep-research/SKILL.md` | `/ars-3w`（`commands/ars-3w.md`） |
| deep-research | `fact-check` | Claim-by-claim verification report；"verify claims", "fact-check", "evidence verification" | `deep-research/SKILL.md` | 无；用技能名 + mode 请求 |
| deep-research | `socratic` | Research Plan Summary + INSIGHT collection；"guide my research", "help me think through", "I'm not sure what to research" | `deep-research/SKILL.md` | 无；用技能名 + mode 请求 |
| deep-research | `systematic-review` | PRISMA 2020 report, 5,000-15,000 words；"systematic review", "meta-analysis", "PRISMA" | `deep-research/SKILL.md` | 无；用技能名 + mode 请求 |
| academic-paper | `full` | Complete paper draft (IMRaD or domain-appropriate)；"write a paper", "academic paper", "research paper" | `academic-paper/SKILL.md` | 无；用技能名 + mode 请求 |
| academic-paper | `plan` | Chapter Plan + INSIGHT collection (Socratic)；"guide my paper", "help me plan", "step by step paper" | `academic-paper/SKILL.md` | `/ars-plan`（`commands/ars-plan.md`） |
| academic-paper | `outline-only` | Detailed outline + evidence map；"paper outline", "just need an outline" | `academic-paper/SKILL.md` | `/ars-outline`（`commands/ars-outline.md`） |
| academic-paper | `revision` | Revised draft + point-by-point R&R responses；"revise paper", "incorporate reviewer feedback" | `academic-paper/SKILL.md` | `/ars-revision`（`commands/ars-revision.md`） |
| academic-paper | `revision-coach` | Reviewer path: Revision Roadmap + Response Letter Skeleton. Explicit real-committee variant: source-accounted concern tracker + placeholder response skeleton；"parse reviews", "I got reviewer comments", "track these committee comments" | `academic-paper/SKILL.md` | `/ars-revision-coach`（`commands/ars-revision-coach.md`） |
| academic-paper | `abstract-only` | Bilingual abstract (zh-TW + EN) + keywords；"write abstract" | `academic-paper/SKILL.md` | `/ars-abstract`（`commands/ars-abstract.md`） |
| academic-paper | `lit-review` | Annotated bibliography in paper format；"literature review paper", "write a lit review" | `academic-paper/SKILL.md` | `/ars-lit-review`（`commands/ars-lit-review.md`） |
| academic-paper | `format-convert` | Formatted document (LaTeX/DOCX-via-Pandoc/PDF/MD)；"convert to LaTeX", "convert citations to [format]" | `academic-paper/SKILL.md` | `/ars-format-convert`（`commands/ars-format-convert.md`） |
| academic-paper | `citation-check` | Citation error report；"check citations", "verify references" | `academic-paper/SKILL.md` | `/ars-citation-check`（`commands/ars-citation-check.md`） |
| academic-paper | `disclosure` | Default venue path: applicability/status bundle; policy-anchor path: anchor-specific render；"AI disclosure for [venue]", "generate AI usage statement" | `academic-paper/SKILL.md` | `/ars-disclosure`（`commands/ars-disclosure.md`） |
| academic-paper | `rebuttal-audit` | Advisory QA of an existing rebuttal draft (per-comment coverage + gaps + risk flags); no generation; no Schema 11 emission；"audit my response", "check my rebuttal", "did I miss any reviewer comment" | `academic-paper/SKILL.md` | `/ars-rebuttal-audit`（`commands/ars-rebuttal-audit.md`） |
| academic-paper-reviewer | `full` | 5 review reports + Editorial Decision + Revision Roadmap；"review paper", "peer review", "manuscript review" | `academic-paper-reviewer/SKILL.md` | `/ars-reviewer`（`commands/ars-reviewer.md`） |
| academic-paper-reviewer | `re-review` | Revision verification checklist + residual issues；"check revisions", "verification review" | `academic-paper-reviewer/SKILL.md` | 无；用技能名 + mode 请求 |
| academic-paper-reviewer | `quick` | Journal-Fit Reviewer quick assessment + key issues list；"quick review", "quick look" | `academic-paper-reviewer/SKILL.md` | 无；用技能名 + mode 请求 |
| academic-paper-reviewer | `methodology-focus` | In-depth methodology review；"check methodology", "focus on methods" | `academic-paper-reviewer/SKILL.md` | 无；用技能名 + mode 请求 |
| academic-paper-reviewer | `guided` | Socratic issue-by-issue dialogue；"guide me to improve", "walk me through issues" | `academic-paper-reviewer/SKILL.md` | 无；用技能名 + mode 请求 |
| academic-paper-reviewer | `calibration` | Explicit 3-paper directional readout or default full Calibration Report + tier-scoped disclosure；"calibrate reviewer", "measure reviewer accuracy" | `academic-paper-reviewer/SKILL.md` | 无；用技能名 + mode 请求 |
| academic-pipeline | `(pipeline)` | 10-stage orchestrated workflow；"academic pipeline", "research to paper", "full paper workflow" | `academic-pipeline/SKILL.md` | `/ars-full`（`commands/ars-full.md`） |
| academic-pipeline | `resume_from_passport=<hash>` | Resume a prior pipeline run from a Material Passport reset boundary. Opt-in (`ARS_PASSPORT_RESET=1`). See `academic-pipeline/references/passport_as_reset_boundary.md`.；"resume from passport", "continue pipeline from reset boundary" | `academic-pipeline/SKILL.md` | 无；用技能名 + mode 请求 |
| sr-screener | `protocol` | `screening_protocol.md` + `screening_config.json`, confirmed by the user；"turn my proposal into a screening protocol", "screening criteria" | `sr-screener/SKILL.md` | 无；用技能名 + mode 请求 |
| sr-screener | `quick` | Decision table in chat, labelled single-reviewer triage；"is this abstract eligible", "screen these abstracts" | `sr-screener/SKILL.md` | 无；用技能名 + mode 请求 |
| sr-screener | `pilot` | Calibration report (seeds, agreement, conflicts) + agreed protocol clarifications；"pilot the screening", "calibrate screening" | `sr-screener/SKILL.md` | 无；用技能名 + mode 请求 |
| sr-screener | `ta-screen` | Dual-review title/abstract decisions, screening log, RIS groups, PRISMA counts, methods draft；"title/abstract screening", "screen these papers" | `sr-screener/SKILL.md` | 无；用技能名 + mode 请求 |
| sr-screener | `ft-screen` | Full-text decisions with one reason per exclusion (page and section)；"full-text screening", "full-text eligibility" | `sr-screener/SKILL.md` | 无；用技能名 + mode 请求 |
| sr-screener | `adjudicate` | Advisory third-reviewer suggestions for a human screening set's conflicts；"resolve screening conflicts", "adjudicate Rayyan conflicts" | `sr-screener/SKILL.md` | 无；用技能名 + mode 请求 |
| sr-screener | `audit` | Exclusions a senior reviewer would advance, advisory；"audit my exclusions", "double-check excluded records" | `sr-screener/SKILL.md` | 无；用技能名 + mode 请求 |
| sr-screener | `report` | PRISMA 2020 counts, methods draft, RIS exports, `literature_corpus[]` handoff；"PRISMA flow numbers", "methods paragraph for the screening" | `sr-screener/SKILL.md` | 无；用技能名 + mode 请求 |

## 支持文件导航

导航指向真实目录；具体 mode 所需文件从 SKILL 对应分支读取，目录存在不等于模式契约已核验。

| Skill | 支持协议定位 |
|---|---|
| deep-research | `deep-research/SKILL.md`；`deep-research/references/`；`deep-research/agents/` |
| academic-paper | `academic-paper/SKILL.md`；`academic-paper/references/`；`academic-paper/agents/` |
| academic-paper-reviewer | `academic-paper-reviewer/SKILL.md`；`academic-paper-reviewer/references/`；`academic-paper-reviewer/agents/` |
| academic-pipeline | `academic-pipeline/SKILL.md`；`academic-pipeline/references/`；`academic-pipeline/agents/` |
| sr-screener | `sr-screener/SKILL.md`；`sr-screener/references/`；`sr-screener/agents/` |

wfh 支持协议见 [共享总览](../SKILL.md)。ARS 路由以当前根下 shared/references/routing_core.md 与 intent_clarification_protocol.md 为准。
