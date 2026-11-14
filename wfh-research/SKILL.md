---
name: wfh-research
description: "内部共享包：科研流程协议、模板和能力导航，供执行入口按需读取。"
disable-model-invocation: true
user-invocable: false
---

# 科研流程共享规则

本包不独立执行。wfh 主持研究设计、维护决定和进度，ARS 主持专业任务内规划与生产。独立小请求按需直接调用；长期课题才维护 FLOW.md（进度文件）。Matt 仅作为设计参考，ARS 原生契约和专业检查保持唯一来源。

| 动作发生时 | 读取 |
|---|---|
| 任一用户回复 | [研究者界面](references/user_output_protocol.md) |
| 失败回复 | [失败翻译](references/failure_translation.md)，只在失败时读 |
| 默认开始／推进／验收 | [动作分派](references/dispatch_protocol.md) |
| 咨询能力 | [分流协议](references/routing_protocol.md)、[生成索引](references/skills_index.md) |
| 研究设计 | [盘问协议](references/grilling_protocol.md) §1–6、§8、[决定分类](references/decision_classes.md)；排轮读 [盘问树](references/grilling_tree.md)，收尾读 [盘问自检](references/grilling_failures.md) |
| 写研究方案 | [方案模板](references/spec_template.md) §1–4 |
| 安排步骤 | [步骤规则](references/tickets_template.md) §2–6；写具体类型时读 [类型模板](references/tickets_types.md)，需要样例读 [任务样例](references/tickets_examples.md) |
| 查进度／准备／验收 | [状态协议](references/state_protocol.md) §1–4／§5／§6 |
| 整稿或终稿验收 | [交付检查](references/integrity_selfcheck.md)，只在 `integrate` 或最终稿时读，核对 ARS 实际检查记录 |
| 更新进度布局 | [进度模板](references/flow_template.md)；写完整模板或对接时读 [进度细节](references/flow_details.md) |
| 接续会话执行 | [执行协议](references/execution_protocol.md) |
| 选择研究生产能力 | [意图映射](references/ars_intent_map.md) |
| 调用生产或核验其结果 | [交接协议](references/ars_handoff_protocol.md) 对应来源分支；内部链读 [内部链](references/ars_internal_chain.md) |
| 结论或设计失败 | [回环模板](references/reopen_template.md) |

技能只加载当前分支要求的内容；不为了开始一个动作通读全包。术语和重要方法决定模板只在实际写入或语义核对时读取。内部字段、文件名和事实源保持兼容，研究者输出单独翻译。

[设计历史](SPEC.md) 保留原决策。[索引生成器](scripts/refresh_index.py) 只维护导航；ARS 根由可靠来源显式传入，文件可读不证明宿主已加载。
