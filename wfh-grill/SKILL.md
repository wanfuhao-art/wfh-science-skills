---
name: wfh-grill
description: "高级入口：问清研究问题与设计，比较有依据的候选，记录研究决定；术语与重要方法决定按需生成，已有答案不重复问。确认后交付讨论记录，不生成研究方案，不代替 wfh-spec。"
disable-model-invocation: true
---

# 问清研究设计并记录决定

先读 [研究者界面](../wfh-research/references/user_output_protocol.md)。wfh 主持研究问题和设计的收敛，不因想法模糊就默认交给另一套完整访谈。本高级入口的边界是研究讨论及其记录，研究方案整理属于独立的高级步骤。

## 判断与读取

- 先读已有材料和确认记录；已有答案跳过，只问会影响当前目标的未定选择。缺研究描述时先问研究内容与手头材料。
- 盘问前读 [盘问协议](../wfh-research/references/grilling_protocol.md) §1–8 与 [决定分类](../wfh-research/references/decision_classes.md)；排轮读 [盘问树](../wfh-research/references/grilling_tree.md)，收尾读协议 §9 和 [盘问自检](../wfh-research/references/grilling_failures.md)。
- 查文献或事实时按 [能力选择](../wfh-research/references/ars_intent_map.md) 调 ARS 补证，不让其重开设计访谈。作者明确要苏格拉底式探索才由 ARS 主持，并遵守其原生模式边界。

## 动作与输出

1. 按依赖问当前可答的问题，研究类型只加载适用分支；题数与轮数作为负担提示，不作为必须填满的表。
2. 给出有依据的候选、推荐理由、限制与备选，区分事实、惯例与推断；关键研究决定请作者确认，保留作者原始评分与来源。
3. 术语确定后按 [术语模板](../wfh-research/references/terms_template.md) 记录，重要决定过三门槛才读 [决定记录模板](../wfh-research/references/mdr_template.md)。不为凑一组文件创建空术语表或给每个小决定单独建文件。
4. 展示研究决定、理由、风险、未决与待核验内容，请作者确认。提前结束时可整理标为未确认的讨论记录，不冒充已确认方案。
5. 确认后按盘问协议 §8.4 保存 `decisions/LEDGER.md`（研究决策记录），更新适用术语和重要决定的确认状态，按 [进度细节](../wfh-research/references/flow_details.md) §8.5 同步 `FLOW.md`（研究进度）。
6. 用中文用途链接实际记录，说明未决事项和下一步。本入口不生成或更新 `BRIEF.md`，不读取方案整理实现，不安排详细步骤或开始论文生产；需要整理方案时可另用高级 `/wfh-spec`。
7. 默认 `/wfh` 读取本实现时先完成同样的讨论与记录，再由默认入口按 [动作分派](../wfh-research/references/dispatch_protocol.md) §3.1 判断是否已有明确的方案生成请求。自动衔接由默认入口负责，不改变本高级入口的功能边界。
8. 回环时读 [回环模板](../wfh-research/references/reopen_template.md) 和盘问协议 §6，保留旧决定及修订关系。只读设计咨询不强制落盘或建立课题。

科学解释可以推荐，证据支持程度如实说明；作者的伦理声明、署名同意、实验返回物与确认不能代造。文件路径、兼容字段和 ARS 交接方式保持原样。
