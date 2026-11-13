---
name: wfh-implement-spec
description: "高级入口：准备单个研究步骤，确认后在新会话开展，返回后逐项验收；每次只推进一步。"
disable-model-invocation: true
---

# 在接续会话开展一步

先读 [研究者界面](../wfh-research/references/user_output_protocol.md)，本入口保留显式确认接手说明的高级用法。

## 判断与输入

工作区唯一时自动选择，可指定步骤；未指定按 [状态协议](../wfh-research/references/state_protocol.md) §1–3 选择合法当前步骤。材料、前序证据和未决不齐就说明缺什么；人工步骤只给人工动作与返回物。

## 执行

1. 读取 [执行协议](../wfh-research/references/execution_protocol.md)，按顺序完成预检、确认、启动、等待和验收。
2. 准备说明时读 [接手入口](../wfh-next/SKILL.md) 与状态协议 §5；展示用户可理解的目标、输入、产出和验收，请确认后再开新会话。
3. `--dry-run` 只准备和展示，不写文件；`--resume` 从既有等待记录恢复；`--close <ID>` 只验收。
4. 返回完成消息后读实际证据，依 [验收入口](../wfh-close/SKILL.md) 和状态协议 §6 验收。
5. 需要生产能力才读 [交接协议](../wfh-research/references/ars_handoff_protocol.md)；没有真实调用不宣称生产完成。

## 边界与输出

保留既有等待记录路径；不轮询、不自动连跑、不代做实验或研究判断。会话工具不可用先解释实际限制，不能假称已启动。每步结束给中文结果与下一步，用户确认后才推进下一条。
