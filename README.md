# wfh-science-skills

把研究想法变成可讨论的设计，再按证据推进到实际交付。wfh 主持研究问题与设计、维护决定和进度；ARS 提供文献检索、专业规划、写作、审稿和核验。设计借鉴 Matt skills，无需安装 Matt。

适用于自然科学、社会科学及交叉研究。共同骨架是研究问题、主张、证据和验证方式；实验、计算、定性、理论与综述只使用各自适用的要求。

## 快速开始

- 讨论研究方向：`/wfh 我想研究固态电池界面，请比较几个有依据的研究方向`。确认后保存讨论记录，研究方案仍是单独一步。
- 讨论后生成方案：`/wfh 帮我问清研究设计，确认后生成研究方案`。系统在研究决定确认后直接衔接整理，你不用再输入高级命令。
- 推进整个研究过程：`/wfh 带我把这个研究想法推进到论文初稿`。系统会衔接讨论、整理文档、安排步骤与实际研究；需要你作研究决定、确认专业配置或补实验材料时停下来说明。
- 直接办一件事：`/wfh 核对这份参考文献` 或 `/wfh 修改这段讨论，保持原结论边界`，不用先填完整研究方案。
- 持续推进：`/wfh 查清这三种解释分别有什么文献支持，交付一份比较`，会在约定目标内完成准备、调用和核对；需要研究取舍、关键确认或缺材料时停下。
- 查看课题：说“看看进度”；单说“继续”恢复当前步骤，不自动跑完整课题。

AI 可以提供有依据的候选与推荐；AI 建议、作者已确认和证据已支持分别记录。原始实验、作者自评及必要确认由研究者提供。

独立请求直接交付结果。设计讨论确认后给出研究决策记录、按需术语 / 重要方法决定和必要进度；研究方案由高级 `/wfh-spec` 单独整理。普通用户通过 `/wfh` 明确说要生成或整理方案时，系统会自动衔接，无需学习高级命令；仅讨论或回答“确认”不会触发生成。原有 BRIEF.md、decisions/LEDGER.md、FLOW.md 等路径及兼容字段保留，文档内增加中文阅读说明；长期课题日常主要查看进度，已有记录继续可用。

也可以直接说“看看进度”“只准备接手说明，先别执行”“先演示，不写文件”“恢复上次等待的工作”或“只验收，不补做”。系统保留各自的操作边界；普通用户无需学习高级命令和参数。

<details>
<summary>安装方法</summary>

在支持插件的 Claude Code / Claude Desktop 中添加本插件：

```text
/plugin marketplace add wanfuhao-art/wfh-science-skills
/plugin install wfh-science-skills
```

需要研究生产能力时添加 ARS：

```text
/plugin marketplace add Imbad0202/academic-research-skills
/plugin install academic-research-skills
```

安装后使用 `/wfh`；宿主要求完整名称时用 `/wfh-science-skills:wfh`。也可描述研究流程意图自动识别；明确指定 ARS 或其他技能时尊重选择。网络依赖本机代理时保持代理软件开启。

本地安装可把市场地址换成本仓库绝对路径。下载源码不等于宿主已加载技能。ARS 未启用时仍可整理研究和查看本地记录；日常使用无需 Python，索引维护才需要 Python 3。Word、PDF 等依赖按实际输出分支检查。
</details>

<details>
<summary>高级入口与已有课题</summary>

| 高级入口 | 用途 |
|---|---|
| `/wfh-ask` | 只读查看进度或咨询 |
| `/wfh-grill` | 问清设计、比较方案，记录术语与研究决定；不生成研究方案 |
| `/wfh-spec` | 整理已确认研究方案 |
| `/wfh-tickets` | 安排长期课题的可验证步骤 |
| `/wfh-next` | 只准备接手说明，不执行 |
| `/wfh-close` | 只验收，不补做研究 |
| `/wfh-implement-spec` | 手动确认后在接续会话执行指定一个步骤 |

FLOW.md（进度文件）、BRIEF.md（研究方案）、TERMS.md（术语说明）、decisions/（研究决定记录）、tasks/（步骤记录）保持原路径，旧编号无需重排。默认入口按交付目标推进；高级执行入口仍保留逐步控制。参见 [兼容与回退](MIGRATION.md)。
</details>

<details>
<summary>维护者资料与许可</summary>

- [融合设计与验证边界](docs/ARS-INTEGRATION.md)、[领域词汇](GLOSSARY.md)。
- [逐技能审查与本轮修复](docs/SKILLS-AUDIT.md) 记录九个技能的保留、升级和精简结论，以及离线验证范围。
- [设计历史](wfh-research/SPEC.md) 和旧 [可用性审计](docs/UX-AUDIT.md) 保留历史结论，现行行为以技能与共享协议为准。
- [索引工具](wfh-research/scripts/refresh_index.py)、[融合检查](wfh-research/evals/check_contracts.py) 与 [评估工具回归](wfh-research/evals/test_eval_tools.py) 供维护者使用；ARS 根由可靠来源显式传入。[协议场景](wfh-research/evals/evals.json) 是待演练的行为案例；文档或词汇检查通过不代表真实会话行为已验收。
- ARS 源码兼容基线为 3.24.2，读取源码、模拟调用与宿主真实运行分别记录。专业检查留在 ARS，wfh 核对实际交付和报告，不颁发其通过结论。
- 默认入口、七个高级入口、一个内部共享包共九个技能目录；本仓库不含 ARS 生产代码，不修改其安装目录。
- CC-BY-NC-4.0，© wanfuhao-art，见 [LICENSE](LICENSE)。盘问及步骤组织参考 mattpocock-skills，未包含其代码。
</details>
