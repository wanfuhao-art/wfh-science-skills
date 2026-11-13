# 整稿完整性自检（7 类失败模式）

> 只在验收 `integrate` 任务（阶段 5 / 7）或最终稿时读取；单个 `claim` / `prep` / `ec` / `revision` 任务用各自的验收标准，不套整套。
> 这是 wfh 层自检，不是 ARS 2.5 / 4.5 门禁，不颁发 PASS / VERIFIED。
> 定义以当前 ARS 根下 `academic-pipeline/references/ai_research_failure_modes.md` 为准；只在某项判不清或作者要求原文时读它。

---

## 1. 何时做

- 阶段 5 成稿整合、阶段 7 改稿后整合、阶段 8 定稿前。
- 作者明确要求「整稿检查」「投稿前自检」时。
- 只走单个 ARS 技能、不经过 `academic-pipeline` 时，这是 wfh 层唯一的整稿完整性检查。

## 2. 七项

| # | 失败模式 | 自检问题 | wfh 里看哪里 | 不通过时 |
|---|---|---|---|---|
| M1 | 实现错误通过自检 | 分析脚本 / 计算能否复算？图 / 表数值与记录是否一致？ | 任务 §3 分析、`tasks/assets/T<nn>/analysis/`、§4 图表数据源 | `partial`：复算或补验证；不能复算 → `blocked` |
| M2 | 编造引用 | 每条引用有来源和核验状态？`[待核验]` 是否还在？ | 任务 §6、`citation-report.md`、正文引用键 | `blocked`：补核验或删除；不得把 `[待核验]` 当已核验 |
| M3 | 编造实验结果 | 每个实验数值有原始记录 / 仪器返回物 / 样本 ID？ | §2 证据、`tasks/assets/T<nn>/raw/`、`prep` / `human` 完成记录 | `blocked`：等返回物；不猜数 |
| M4 | 走捷径 | 是否用文献 / 常识替代了本应采集的数据？对照 / 重复 / 空白是否齐？ | §2 证据状态、`prep` 任务、验收标准 | `partial`：补 `prep` 或降级结论 |
| M5 | 实现错误被说成新发现 | 异常结果是否先排除了 bug、校准、单位、样本问题？ | §3 替代解释、QC 记录、§4 图表 | 回环或降级 claim；不把异常直接写成机制 |
| M6 | 方法编造 | 方法描述来自实际执行记录，还是「应该这样做」？ | MDR、§3、`human` 日志、仪器参数 | `blocked`：补实际方法记录；不改写成未执行的方法 |
| M7 | 早期框架锁定 | 是否只收集支持原假设的证据？反例 / 替代解释是否记录？ | BRIEF 的证伪条件、claim ledger 风险列、`decisions/REOPEN-*` | 回环：先请作者确认重开哪个决定 |

## 3. 记录方式

在 `integrate` 任务的验收核对表里追加七行：

| 项 | 结果 | 证据位置 | 说明 |
|---|---|---|---|
| M1 | pass / fail / unresolved | <文件 + 小节 / 行> | <...> |
| M2 | pass / fail / unresolved | <...> | <...> |
| M3 | pass / fail / unresolved | <...> | <...> |
| M4 | pass / fail / unresolved | <...> | <...> |
| M5 | pass / fail / unresolved | <...> | <...> |
| M6 | pass / fail / unresolved | <...> | <...> |
| M7 | pass / fail / unresolved | <...> | <...> |

- 七项全部 pass 才能把 `integrate` 记为 `done`；任何 fail / unresolved 按 `state_protocol.md` §6.1 分类。
- 不把「没发现问题」写成「已通过 ARS 完整性门禁」。
- 用户可见回复只说明哪几项没通过、缺什么、下一步做什么；不打印整张表，除非作者要求。
- 面向用户用「引用核验 / 实验记录 / 分析复算 / 对照完整性 / 异常排查 / 方法记录 / 证伪条件」等说法，不出现 M1–M7 编号。

## 4. 与 ARS 门禁的关系

- 整稿会走 `academic-pipeline` 时，ARS 的 2.5 / 4.5 才是正式门禁；本自检是前置清理，不替代它。
- 只走单技能（如 `academic-paper`）时，本自检补上 wfh 层的整稿检查；通过也不等于 ARS VERIFIED。
