---
name: wfh-tickets
description: "高级入口：从已确认研究方案或审稿意见安排可验证的研究步骤，确认顺序、工作范围和验收要求。"
disable-model-invocation: true
---

# 安排研究步骤

先读 [研究者界面](../wfh-research/references/user_output_protocol.md)。

## 判断与读取

- 默认从已确认方案与已有步骤增量安排；作者明确要求草稿时标明草稿状态。
- 改稿从意见原文、现有稿件及其来源开始，不把“收到意见”误当已回应；外部意见不要求先运行本地模拟审稿。
- 建图前读 [步骤规范](../wfh-research/references/tickets_template.md) §2–6 和 [状态规则](../wfh-research/references/state_protocol.md) §2–3；核对说法时读 [方案规则](../wfh-research/references/spec_template.md) §4.6。
- 写具体类型时读 [类型模板](../wfh-research/references/tickets_types.md) 对应类型；改稿读 §6.13，终端整合读 §6.14，格式迁移才读 §6.9。需要填好的样例时读 [任务样例](../wfh-research/references/tickets_examples.md)。
- 更新进度才读 [进度布局](../wfh-research/references/flow_template.md) §7 与 [进度细节](../wfh-research/references/flow_details.md) §8–9，不加载无关类型和示例。

## 动作与输出

1. 每条说法至少有一个可验证步骤，最小证据层和一个会话的边界完整；共用前置和人工测量单列。
2. 先走通一个材料现成的小步骤；材料不足先安排补件，不造数据。引用集中核验，机械迁移分批处理。
3. 核对唯一编号、依赖、无环、未决对应、执行方式和验收；保留旧编号和已取消记录。
4. 用中文展示完整步骤安排、需要先做什么、哪些需人工完成，请作者确认粒度及顺序并停下。
5. 确认后写 tasks/（步骤记录），同步 FLOW.md（进度文件）的图、阶段、未决和唯一下一步。
6. 改稿按意见簇组织，保留意见原文与作者回应策略，最后加整合检查；改科学说法先回到研究决定。

## 边界

不写论文正文、不代定研究判断、不执行生产，不改研究方案、术语和决定来源；已有课题只增量更新。
