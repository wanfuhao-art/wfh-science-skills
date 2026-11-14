# ARS 内部链：保留原件、按当前契约恢复

> 只在实际 ARS 阶段产物或明确恢复内部流程时读取。外部作者材料及仅附文献库的调用见 [交接协议](ars_handoff_protocol.md)。

## 1. 原件与身份

保留原产物、Material Passport、实际 builder 回执和条件性 companion 的身份与内容。wfh 整理的研究方案仍是外部作者材料；完整字段、作者确认或文献库 Passport 不能将其变成 deep-research 阶段产物。

来源或恢复用途不清时核实，不能换标签避开校验；原件缺失时保留缺项，不填造 VERIFIED、实验声明、预注册状态或作者确认。

## 2. 当前工具与规则

读取实际 ARS 生产方和接收方的 Handoff Protocol、`shared/handoff_schemas.md`，以及该分支要求的支持文件。需要 builder 时先读当前协议与工具 `--help`，使用其实际参数；本文件不维护第二份 CLI、状态枚举或 Schema。

3.24.2 的规划产物回执定位于 `shared/references/cross_document_consistency_advisory_protocol.md`，指定 builder 为 `scripts/build_cross_document_consistency_advisory.py`。这只是版本基线导航，升级后以当前原文核对。执行工具仅限本次授权的来源、输入和产出，测试身份不能移入真实交接。

## 3. 责任与拒绝

wfh-spec 只整理方案，不构造内部身份。真正需要内部工具时由当前 ARS 流程负责，用户未提供的研究状态、声明或日期保持未决。工具成功只证明契约构造完成，不能证明研究有效或原生门禁通过。

实际调用被拒绝时记录 `rejected_by: ars-intake`、`ars_invoked: true`、准确缺项及原响应，停止受影响动作。回退和恢复按原生契约，不静默切换外部入口。
