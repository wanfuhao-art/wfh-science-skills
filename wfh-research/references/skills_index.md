# ARS + wfh 路由索引（生成文件）

仅定位，不证明已读取、已加载、已验证或研究已执行。推荐前读取目标 SKILL 与模式要求的支持文件。

- 来源 ARS：`academic-research-skills@3.24.2`；运行时显式提供当前根，不保存安装路径。
- ARS 状态：LOCATED（宿主加载状态另查）
- 实际 ARS 模式记录：35；wfh 执行入口：8（默认 1，高级 7）；可读入口：8
- 来源指纹 SHA-256：`caf61b8f66ecd4451c25d700ee149aa7c884e8f80a831870b3818a0b522a33fe`；输入文件：277
- 刷新 / 只读检查：[路由协议](routing_protocol.md)；工具：[refresh_index.py](../scripts/refresh_index.py)

## 诊断

OK：已按当前来源生成；每次咨询仍需 --check。

## 8 个 wfh 执行入口（一个默认入口）

| 名称 | slash | frontmatter 描述 | 路径 | 主要支持协议 |
|---|---|---|---|---|
| wfh | /wfh | 科研默认入口：开始研究、问清想法、整理方案、安排步骤、查看进度、继续当前工作或验收结果；需要检索、综述、写作、审稿、改稿或格式整理时自动选择合适能力。用于‘我想研究……’‘现在做到哪了’‘继续’‘这一步做完了’‘帮我写引言’‘审稿意见回来了’‘这个结论站不住’‘卡住了’。已有课题直接接着做；用户明确指定其他能力时尊重其选择。 | [SKILL](../../wfh/SKILL.md) | [dispatch_protocol](dispatch_protocol.md)、[user_output_protocol](user_output_protocol.md)、[ars_intent_map](ars_intent_map.md) |
| wfh-ask | /wfh-ask | 高级只读入口：查看课题进度，或咨询现有材料接下来适合做什么。 | [SKILL](../../wfh-ask/SKILL.md) | [routing_protocol](routing_protocol.md)、[skills_index](skills_index.md)、[state_protocol](state_protocol.md)、[flow_template](flow_template.md) |
| wfh-close | /wfh-close | 高级入口：按真实证据验收当前步骤并更新进度；证据不支持原解释时重新讨论受影响的研究决定。 | [SKILL](../../wfh-close/SKILL.md) | [state_protocol](state_protocol.md)、[flow_template](flow_template.md)、[tickets_template](tickets_template.md)、[ars_handoff_protocol](ars_handoff_protocol.md)、[reopen_template](reopen_template.md) |
| wfh-grill | /wfh-grill | 高级入口：问清研究问题与设计，记录研究决定；已有答案不重复问，关键判断由研究者作出。 | [SKILL](../../wfh-grill/SKILL.md) | [grilling_protocol](grilling_protocol.md)、[decision_classes](decision_classes.md)、[terms_template](terms_template.md)、[mdr_template](mdr_template.md)、[reopen_template](reopen_template.md) |
| wfh-implement-spec | /wfh-implement-spec | 高级入口：准备单个研究步骤，确认后在新会话开展，返回后逐项验收；每次只推进一步。 | [SKILL](../../wfh-implement-spec/SKILL.md) | [state_protocol](state_protocol.md)、[tickets_template](tickets_template.md)、[ars_handoff_protocol](ars_handoff_protocol.md) |
| wfh-next | /wfh-next | 高级入口：准备当前步骤的接手或恢复说明，先检查材料和先后顺序；只准备，不执行。 | [SKILL](../../wfh-next/SKILL.md) | [state_protocol](state_protocol.md)、[tickets_template](tickets_template.md)、[ars_handoff_protocol](ars_handoff_protocol.md) |
| wfh-spec | /wfh-spec | 高级入口：把已确认的研究决定整理成研究方案，保留未决信息，不重复访谈。 | [SKILL](../../wfh-spec/SKILL.md) | [spec_template](spec_template.md)、[ars_handoff_protocol](ars_handoff_protocol.md) |
| wfh-tickets | /wfh-tickets | 高级入口：从已确认研究方案或审稿意见安排可验证的研究步骤，确认顺序、工作范围和验收要求。 | [SKILL](../../wfh-tickets/SKILL.md) | [tickets_template](tickets_template.md)、[flow_template](flow_template.md)、[spec_template](spec_template.md) |

## ARS 模式

路径均相对上方 ARS 根；升级或迁移后重新 refresh，索引不把旧缓存路径当默认安装。
下列 slash 只列当前 commands 文件中可核对的映射。无 slash 的行可用「请使用 academic-research-skills:<技能>，mode=<模式>，<请求>」。
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
