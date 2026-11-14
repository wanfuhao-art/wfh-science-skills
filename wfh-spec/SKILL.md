---
name: wfh-spec
description: "高级入口：把已确认的研究决定整理成研究方案，保留未决信息，不重复访谈。"
disable-model-invocation: true
---

# 整理研究方案

先读 [研究者界面](../wfh-research/references/user_output_protocol.md)。本高级入口负责单独整理、更新已有研究方案，独立于 `/wfh-grill`。默认 `/wfh` 收到明确的方案生成请求时，可按 [动作分派](../wfh-research/references/dispatch_protocol.md) §3.1 通过 Read 复用本实现，用户无需输入本命令。自动整理与手动整理使用同一模板、确认规则和原有路径。

## 判断与读取

- 定位已确认的决定记录；唯一课题自动选择，多个只问课题，无已确认记录则请作者先确认研究内容。
- 读已有决定、术语、重要方法记录和已有方案；不凭聊天记忆伪造确认。
- 合成时读 [方案模板](../wfh-research/references/spec_template.md) §1–4；落盘才读 §3 骨架；需要填好的样例时读 [方案示例](../wfh-research/references/spec_examples.md)。
- 核对确认语义才读 [盘问协议](../wfh-research/references/grilling_protocol.md) §7.3、§8；同步进度时读 [进度细节](../wfh-research/references/flow_details.md) §8.5。

## 动作与输出

1. 仅搬运、组织和压缩已有答案；每条说法保留来源和证据强度。缺值保留未决，冲突交作者裁决。
2. 按模板保留问题、主张、证据、验证方式和适用学科扩展；研究评分保留原始来源。ARS 所需字段按本次模式读取，不把四字段和 FINER 设成所有研究的统一门槛；决策语义按实际名称 / decision_key 定位。
3. 展示方案摘要、来源、未决和冲突；仅有已确认内容的组织与搬运时沿用原确认，不重复设置确认门。出现新增或改变含义的合成说法、冲突或新研究取舍时，请作者确认相应内容后再落盘。
4. 在授权范围增量写 BRIEF.md（研究方案），保留用户手改与修订历史；按进度协议同步阶段及下一步。
5. 只有确实交给生产扩展时才读 [交接协议](../wfh-research/references/ars_handoff_protocol.md)；本入口不实际调用生产技能。

## 边界

研究判断改变时回到研究设计；不新增结论、不写正文或步骤，不改原始术语和决定。作者可明确要求草稿，但不能把草稿或未决值冒充已确认、材料齐全或生产已接收。
