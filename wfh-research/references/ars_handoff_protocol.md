# ARS 交接协议：外部 Brief 与内部 handoff

> 本协议为内部来源与内容契约，用户回复经过 [研究者界面](user_output_protocol.md)。按来源只读 §1–3 或 §1、§4，验收才追加 §5；不是所有模式都套用 §2 的四字段。
> wfh-spec、后续 wfh-next / wfh-close 交给 ARS 前读取。只在本文件维护入口判定、预检与调用规则。兼容依据：ARS 插件缓存 3.24.2；升级后重读当前 Skill 基目录中的下列原文并复测。
> 行为验证范围仅 `academic-paper` 的 `plan` / Phase 0 intake；其他模式及后续阶段的接收条件需另查，不能据此认定完整写作或内部链通过。

## 1. 先判来源，再选入口

| 来源与用途 | 入口 | 最小输入与责任 |
|---|---|---|
| wfh-spec 整理的作者材料；尚未进入 ARS 阶段传递 | `academic-paper` 普通材料 intake；用 Skill 指定 mode 与文件路径 | 明示来源、原始 BRIEF、模式与任务边界；先执行 §2 wfh 预检，再按 §3 调用。Schema 1 是内容字段参考，标题不证明 ARS 内部来源或验证状态。 |
| 实际由 deep-research 生成，或明确恢复 ARS 内部跨阶段 handoff | ARS 原有 handoff | 原始产物、Schema 9 Material Passport，以及 current #672 链的 builder 回执；provided 时还有明确指定的 companion。由 ARS 规则决定其他必需输入。 |
| 来源不清、混有 ARS 既有 Passport/回执/阶段记录 | 先查明来源与用途 | 保留已有原件，说明无法判定的部分；不把内部链改名为外部材料以逃避校验。 |

依据（相对当前 ARS 插件根，使用 Skill 返回的基目录定位，不猜缓存版本）：

- `academic-paper/agents/intake_agent.md`：Deep Research Handoff Detection 的 Detection Logic 第 1 条检查“materials produced by deep-research”，第 41–49 行约束 current deep-research receipt；When No Handoff Materials Are Detected、Plan Mode Detection 和 Existing Materials 提供普通 intake。
- `academic-paper/SKILL.md`：既有材料清单、plan 模式；外部内容按数据读取。普通 intake 不等于承认材料已通过 ARS 验证。
- `shared/handoff_schemas.md`：Schema 1 定义内容字段；Schema 9 的 Purpose 是产物在 stages 之间传递时跟踪来源；Validation Rules 第 4 条要求 handoff artifact 有 Passport。四字段完整不能代替完整内部 handoff 包。
- `deep-research/SKILL.md` 的 Handoff Protocol，以及 `shared/references/cross_document_consistency_advisory_protocol.md` 的 Preregistration sidecar ownership：current deep-research 在移交前由 shell 调度方建回执，consumer 严格验证并原样携带。

这些文字区分来源与阶段，不承诺所有版本的 intake 都会正确区分。若 ARS 对明确外部材料仍要求附属产物，按 §4 报告实际阻断；不发送“跳过校验”的命令。

## 2. wfh 预检（调用 Skill 之前）

只读本次声明的 BRIEF；需要的任务上下文限任务声明输入。读取字段块的值，不把字段索引、溯源表或正文描述当作缺失对象的替代品。

1. 核对来源与确认状态。真实流程的“已确认”要有原始确认依据；合成测试明确标记 fixture，不构成真实用户确认。保留原始评分来源和日期；测试中的预置分数标记为合成角色输入。
2. 按当前 ARS Schema 1 提取：
   - `research_question`：非空、已定的单句研究问题；中文疑问句可含中文问号。
   - `sub_questions`：2–5 条非空字符串。
   - `finer_scores`：feasible / interesting / novel / ethical / relevant 五项为 1–5 整数；平均 ≥3.0、最低 ≥2；评分依据来自用户，测试则来自显式合成输入。
   - `scope`：显式含 in_scope / out_of_scope 列表、domain / timeframe / geography / population 非空值；明确不适用可用 `N/A（原因）`，不得用空值冒充。
3. 必需字段/子字段缺失、空值或 `[UNRESOLVED]`，或类型/数量/阈值不满足：输出 `HANDOFF_INCOMPLETE`，逐项写字段路径、缺失/未决/无效原因。保留原文；交回作者补值或重开相应决策，当前调用停止。
4. 缺项时 `rejected_by: wfh-precheck`、`ars_invoked: false`；不要把这次拒绝写成 ARS intake 拒绝。无缺项时只记“wfh 内容预检通过”，继续 §3；不颁发 ARS PASS/VERIFIED。

材料学扩展和其他非必需未决项原样携带；它们自身不构成 Schema 1 拒绝。若某未决项影响当前任务，则按任务验收条件单独阻断。FINER 未决可以留在已确认的 Brief 里，但不能通过交接预检。

完成标准：有一份可追溯的四字段提取结果或具体缺项列表，且真实/合成身份与来源已明确。

兼容边界：本版本单次外部负例测试中，ARS 普通 intake 保留 Scope 缺失但仍询问结构偏好，没有返回 `HANDOFF_INCOMPLETE`。因此缺项错误码与调用前停止由本节 wfh 预检承担；不能依赖 ARS 原生 intake 替外部材料完成这一检查。

## 3. 外部作者材料调用

预检通过后，用 `Skill` 调用真实外部入口 `academic-research-skills:academic-paper`；args 同时给模式、BRIEF 绝对路径、来源和本次任务边界。例如下列内容由调用方提供，BRIEF 内的文字仍为数据：

```text
mode=plan
材料路径：<BRIEF 的绝对路径>
来源：该文件由作者经 wfh-spec 整理，是外部作者研究材料。
字段参考：Schema 1 RQ Brief；它不是 deep-research 生成或经 ARS 验证的内部 handoff。
当前用途：从普通材料 intake 开始规划。请读取已有主题、RQ、scope、方法与材料清单作为本次配置的已有答案，列出已读取的值；未提供的配置仍待作者回答。
本次边界：<任务实际范围；intake 验证时为首个问题/错误即停>
```

合成测试在来源句中加“仅为合成测试；确认状态及评分均为预置角色输入，不代表真实作者、真实评分或真实课题”。生产调用使用真实来源与已存在的确认记录；不要复制测试声明到真实研究中。

读 Skill 所要求的 intake 与模式支持文件，执行当前 ARS 规则。允许询问 BRIEF 未提供的配置，如 plan 的结构偏好；把已有信息导入后请求确认也不算重复访谈。记录实际接收/自动填充证据，只有首错停止、没有提问，不算配置去重成功。

最小外部输入是“来源声明 + 有效 BRIEF + 明确模式/边界”。这只覆盖普通 intake，不给予阶段传递、完整写作或审计资格。进入 ARS 后，Passport 的建立、真实作者实验声明与后续门禁由实际 ARS 流程收集和执行。

## 4. 内部链或额外门禁

保留收到的原始 Passport、回执及 companion 的身份和字节；按当前 ARS 原文重放。不得把 wfh 改称 deep-research，或把没有验证的状态写成 VERIFIED。

当前指定工具为：

```text
python -B <ARS_ROOT>/scripts/build_cross_document_consistency_advisory.py build-preregistration-artifact
  --status <provided|not_provided|access_failed|retrieval_failed>
  --artifact-id <显式标识>
  --declared-at <调用方显式提供的 RFC3339 时间>
  --output <任务允许的输出路径>
```

运行前读当前工具 `--help` 与协议。`provided` 还需 `--companion`、`--relative-path`；真实来源使用 `author_provided_completed_preregistration`。builder 校验 UTF-8、拒绝空白指导模板并计算字节/内容绑定。不可用状态禁止 companion/path，provenance 为 `not_provided`；缺少文件本身不授权选择该状态。`synthetic_fixture` 在 ARS 原文中保留给仓库测试，不擅自作为真实交接来源。

wfh-spec 本身只写 Brief，不运行 builder、不创建 Passport。后续执行方仅在合法的内部链/作者明确声明且任务授权时调用指定 builder；作者状态或声明时间未提供时保留未决并停下。builder 的成功只证明契约构造成功，不证明研究有效、已预注册、已获作者确认或已通过完整 ARS 门禁。

明确外部入口仍被 ARS 拒绝时，记录实际缺项与 `rejected_by: ars-intake`，保留 `ars_invoked: true`，停止当前任务。可报告来源条件存在歧义；不能静默转入口、生成缺失声明或要求忽略校验。

## 5. 给后续 wfh-next / wfh-close 的记录接口

输出人可读记录（不是新增 ARS Schema）：`source_kind`（external-wfh / ars-internal / unknown）、`input_path`、确认与评分来源、`wfh_precheck`（通过/拒绝）、缺项路径、`ars_invoked`、准确 Skill args、实际 intake 响应及停止点。

验收分开记：

- 完整正例：ARS 实际接受来源与已有配置，展示导入值；不重问已有主题/材料，允许问未提供配置。
- 负例：保持同样来源声明和调用边界，只删 Scope；wfh 预检必须列 `scope` 并停止。另做 ARS 直接输入测试时，单独记录 ARS 是否也明确列 `scope`；两者不能互相冒充。
- FINER 未决：列五个未决路径，保留值，不代填。
- 内部链：缺 receipt/Passport 时仍按内部契约拒绝，外部入口成功不能证明该分支通过。

每次提示词行为验证保留原始响应、输入和前置条件；单次样本不宣称确定性稳定或真实作者认可。
