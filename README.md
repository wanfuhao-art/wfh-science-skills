# wfh-science-skills

帮你问清研究问题、安排步骤、查看进度和验收结果。适用于材料、化学、生物和社会科学研究；检索、写作与审稿由外部科研扩展 ARS 提供。

## 快速开始

1. 安装本插件；需要检索、写作或审稿时，再安装 ARS（下方有安装方法）。
2. 输入 `/wfh 我想研究固态电池界面，但还没想清楚具体问题`。
3. 已有课题时直接说“看看进度”“继续”或“这一步做完了”，仍由同一个入口处理。
4. 默认只需看 FLOW.md（进度文件）：开头说明现在做到哪、下一步做什么；其他记录由系统维护。
5. 卡住时说“卡住了”：系统解释缺什么，并给一个现在能做的动作。

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

安装后在能加载插件的会话使用 `/wfh`。宿主要求完整名称时用 `/wfh-science-skills:wfh`；它们是同一入口。也可直接描述研究意图，由技能自动识别。网络依赖本机代理时保持代理软件开启。

本地安装可把市场地址换成本仓库绝对路径。下载源码不等于安装完成；ARS 未启用时仍可整理研究和查本地进度。wfh 的日常使用无需运行 Python；索引维护需要 Python 3。ARS 的具体输出可能需要额外工具，如生成 Word 的 Pandoc、生成 PDF 的排版编译器，只在需要时检查。
</details>

<details>
<summary>高级入口与已有课题</summary>

默认使用 `/wfh` 即可。旧入口仍保留，适合明确只做其中一个动作的人：

| 高级入口 | 用途 |
|---|---|
| `/wfh-ask` | 只读查看进度或咨询 |
| `/wfh-grill` | 问清研究设计 |
| `/wfh-spec` | 整理已确认的研究方案 |
| `/wfh-tickets` | 安排可验证步骤或改稿步骤 |
| `/wfh-next` | 只准备接手说明，先不执行 |
| `/wfh-close` | 只验收当前一步 |
| `/wfh-implement-spec` | 确认接手说明后在新会话开展一步 |

FLOW.md（进度文件）、BRIEF.md（研究方案）、TERMS.md（术语说明）、decisions/（研究决定记录）、tasks/（步骤记录）保持原路径。已有课题不需要改名或批量迁移。参见 [迁移说明](MIGRATION.md)。
</details>

<details>
<summary>维护者资料与许可</summary>

默认入口、七个高级入口、一个内部共享包共九个技能目录。研究判断、作者评分、实验数据和必要确认来自研究者；系统不能替代湿实验、凭空补结论或代作者投稿。

- [设计历史](wfh-research/SPEC.md)、[可用性审计](docs/UX-AUDIT.md)。
- [索引工具](wfh-research/scripts/refresh_index.py) 仅供维护；外部扩展由实际加载的根目录定位。
- ARS 兼容核实基线为 3.24.2；具体行为验证和未通过项见 [验证记录](docs/UX-TEST-RESULTS.md)。
- 本仓库不含 ARS 代码和研究数据，不修改 ARS 安装目录。
- CC-BY-NC-4.0，© wanfuhao-art，见 [LICENSE](LICENSE)。盘问及步骤组织设计参考 mattpocock-skills，未包含其代码。
</details>
