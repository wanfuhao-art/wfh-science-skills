---
name: wfh-next
description: "为一条科研任务生成可复制到新会话的启动或恢复提示词，限定为 FLOW、目标任务及声明输入；检查阻塞和 ARS 交接预检。用于接着做哪个任务、新会话如何接手、生成科研任务交接提示词；English: next research task, task handoff prompt, wfh-next。不自动开会话或执行任务；验收用 wfh-close。"
---

# wfh-next — 新会话提示词

先读 [共享状态协议](../wfh-research/references/state_protocol.md) §1–3、§5；需要核对字段布局才读 [任务模板](../wfh-research/references/tickets_template.md)。ARS 任务另读 [ARS 交接协议](../wfh-research/references/ars_handoff_protocol.md)。

定位工作区与可选目标 ID。仅读 FLOW、目标任务与其明确声明的输入，不读聊天历史或搜整个课题补背景。检查 FLOW 图与目标一致性、依赖完成证明、缺件及影响本任务的未决。指定目标被阻塞就解释原因并停；输入未声明不足以验证前置时列缺项，不偷读额外任务。

按共享协议 §5 输出完整提示词，包含精确文件清单、主张与六层要求、执行方式 / 预算、产出、逐条验收、未决、失败处理和收尾。ARS 来源先判 external-wfh / ars-internal / unknown；按适用模式预检具体值，保留内部链门禁。缺 Scope 或 FINER 未决归 wfh-precheck，不能说成 ARS 拒绝。其他模式只要求未来执行会话读取其真实契约，不强套 Schema 1。

生成提示词后更新 FLOW「下一步」五字段（命令 / 输入 / 产出 / 失败时 / 更新于），保留用户备注；不改其他节。不改任务状态，不执行研究任务，不自动启动新会话或实际调用 ARS。末尾写 `prompt_only: true; ars_invoked: false; task_executed: false; task_status_changed: false`。调用草案和预检通过都不是实际 intake 回执。
