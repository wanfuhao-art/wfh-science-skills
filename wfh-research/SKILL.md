---
name: wfh-research
description: "wfh 科研套件的共享协议、模板和总览，供七个执行入口按需读取；不是独立工作流。"
disable-model-invocation: true
---

# wfh-research — 共享包

这是 ARS 的补丁层：wfh 整理决策、作者材料与任务状态，ARS 负责检索、写作、审稿、修订及格式转换。ARS 由独立插件提供，本仓库不包含 ARS 代码。本包只提供引用材料，不作为执行入口。

| 执行入口 | 当前职责 | 主要读物 |
|---|---|---|
| [wfh-ask](../wfh-ask/SKILL.md) | 不知道该用哪个，或想知道课题现在做到哪 | [路由协议](references/routing_protocol.md)、[生成索引](references/skills_index.md)、[状态协议](references/state_protocol.md) §1–4、[FLOW 布局](references/flow_template.md) |
| [wfh-grill](../wfh-grill/SKILL.md) | 已有方向，盘问并收敛决策 | [盘问协议](references/grilling_protocol.md)、[决策类别](references/decision_classes.md)、[术语模板](references/terms_template.md)、[MDR 模板](references/mdr_template.md)、[回环模板](references/reopen_template.md) |
| [wfh-spec](../wfh-spec/SKILL.md) | 把已确认台账合成 BRIEF | [Brief 模板](references/spec_template.md) |
| [wfh-tickets](../wfh-tickets/SKILL.md) | 从 Brief 切可验证任务；`revision` 模式切改稿任务 | [任务模板](references/tickets_template.md)、[FLOW 模板](references/flow_template.md) |
| [wfh-next](../wfh-next/SKILL.md) | 生成单条任务的新会话启动 / 恢复提示词 | [状态协议](references/state_protocol.md) §5 |
| [wfh-close](../wfh-close/SKILL.md) | 逐条证据验收，同步任务与 FLOW；claim 失败出回环包 | [状态协议](references/state_protocol.md) §6、[回环模板](references/reopen_template.md) |
| [wfh-implement-spec](../wfh-implement-spec/SKILL.md) | 编排：生成提示词 → 开新会话 → 自动验收 | [状态协议](references/state_protocol.md)、[任务模板](references/tickets_template.md) |

典型链路是决策收敛 → Brief → 任务图 → 状态（`wfh-ask`）/ 启动提示词 → 在任务边界内执行 → 验收 → 终端整合 → 审稿 → 改稿任务 → 定稿。已有记录从剩余工作继续，无需重走全链。七个入口均可由用户以同名 slash 调用；共享包本身只读。

向 ARS 交接、解释接收资格或验收实际调用时，读取 [ARS 交接协议](references/ars_handoff_protocol.md)：区分外部作者材料和内部 handoff；内容预检通过不等于 ARS 接收或审计通过。共享协议只在本包维护，迁移时将七个入口和本包作为同级目录一起移动。

索引由 [refresh_index.py](scripts/refresh_index.py) 从当前安装的注册表、真实命令文件和七个 wfh frontmatter 生成；ARS 根必须显式传入。更新或核对入口时使用 [路由协议的刷新步骤](references/routing_protocol.md)；不手改生成表。详细背景见 [SPEC](SPEC.md)，运行行为以对应入口和共享协议为准。
