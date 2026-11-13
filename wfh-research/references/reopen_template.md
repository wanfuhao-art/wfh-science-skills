# 回环包模板（REOPEN）

> wfh-research 共享包 · 2026-11-13
> 写入者：`wfh-close`（claim 被证伪或设计不成立时）
> 读取者：`wfh-grill`（执行重开）、`wfh-spec`（更新 Brief）、`wfh-tickets`（重切任务）
> 位置：`research/<slug>/decisions/REOPEN-<NNNN>-<slug>.md`
> 编号四位递增，不复用、不重排、不删除；关闭后保留文件，在「处理记录」追加结果。

---

## 1. 什么时候写

close 的失败分类为 `CLAIM_REFUTED` 或 `DESIGN_INVALID` 时：

- 证据与 claim 冲突；
- 设计无法支持该 claim（样本、测量、对照、识别策略不成立）；
- 关键前提被证伪，导致依赖它的 claim 链断裂。

不写的情况：`EXECUTION_FAILURE`（重跑本任务）与 `EVIDENCE_GAP`（补 prep / 等外部返回物）。

写之前先向用户展示草案并确认分类；用户不确认就只记 unresolved，不写包。

---

## 2. 模板

```markdown
# REOPEN-0001: <一句话说明重开什么>

- 课题 slug：<slug>
- 日期：YYYY-MM-DD
- 状态：open / accepted / rejected / closed
- 来源任务：T<nn>
- 分类：CLAIM_REFUTED / DESIGN_INVALID

## 触发证据

- 未通过的验收标准（逐条照录）：
  - ...
- 证据位置：
  - `tasks/assets/T<nn>/...`
- 为什么不是执行问题：
  - ...

## 受影响的主张

| Claim | 原文 | 影响 |
|---|---|---|
| C<nn> | <照录 BRIEF> | 被否定 / 强度需下调 / 需替换 |

## 受影响的决策

| 决策 ID | 原选择 | 为什么受影响 | 建议动作 |
|---|---|---|---|
| D<nn> | <照录 LEDGER> | ... | 重开 / 修订 / 保留 |

## 受影响的任务

| Task | 原状态 | 影响 | 建议动作 |
|---|---|---|---|
| T<nn> | done / doing / todo | ... | 重切 / 降级 / 取消 |

## 建议路径

1. `/wfh-grill`：重开 D<nn> 这一支；
2. `/wfh-spec`：更新 BRIEF 的 claim ledger 与未决项；
3. `/wfh-tickets`：重切 T<nn> / T<nn>。

## 处理记录

| 日期 | 动作 | 结果 |
|---|---|---|
| YYYY-MM-DD | close 写入 | open |
```

---

## 3. 规则

1. **只记录，不裁决。** 回环包不替用户决定重开哪一支；`建议路径` 是候选，不是结论。
2. **不改上游。** close 只写包，不改 `BRIEF.md` / `TERMS.md` / `LEDGER.md` / MDR / 其他任务。
3. **证据可指向。** 每条触发证据写精确路径与小节 / 行；不写「结果不支持」这类无指向判断。
4. **分类可质疑。** 用户可以把 `CLAIM_REFUTED` 改成 `EVIDENCE_GAP`；改后在「处理记录」留痕。
5. **关闭要留痕。** 重开完成后，`wfh-grill` 在「处理记录」写 `accepted` / `rejected` 与日期；不删除文件。
6. **编号不复用。** 即使包被 rejected，编号也保留。
