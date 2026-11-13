# wfh-science-skills 可用性审计与重构方案

> 状态：方案 B 及验证边界已获维护者确认，进入实施。本文其余审计数据保留为改造前快照；原文件行号引用固定到基准提交，避免随入口压缩失效。
> 审计日期：2026-11-13；仓库基准：`4105918de626c0c7c118534b07cd60348f511763`，插件版本 3.0.1。
> 阅读对象：维护者。本文为核实内部契约必须引用原字段、模式名和诊断标记；这些引用不作为未来研究者界面的措辞。

## 1. 结论与证据边界

推荐方案 B：增加一个薄的默认入口 `/wfh`，让研究者用“开始、推进、验收”表达意图；旧七入口保留为高级用法。默认只展示进度文件 FLOW.md 的中文摘要，由系统维护其余记录；ARS 的模式选择、输入准备和结果解释由 wfh 承担。现有研究判断、证据、确认、回环和输入来源规则保留。

这不能只靠重命名实现：当前咨询入口明确只读，下一步入口只生成提示词，执行入口又要求先确认整段提示词。因此必须明确“咨询”和“执行”的授权边界，才能让“继续”真正推进。依据：[咨询入口](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-ask/SKILL.md#L39)、[提示词入口](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-next/SKILL.md#L14)、[执行确认](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-implement-spec/SKILL.md#L117)。

本轮核实分三类，不能相互冒充：

- **直接核实**：README、SPEC、全部八份 SKILL、全部共享协议与模板、索引及生成器；已跟踪文件统计；清单一致性；下载版 ARS 注册表及命令和相关契约；只读索引检查。
- **静态诊断**：从上述指令推出的界面负担、规则冲突和兼容风险。它们不等于真实用户已遇到的问题，也不等于已复现模型失败。
- **待实施验证**：八条非技术用户脚本、十段真实输出、默认入口触发、ARS 实际执行与接收、旧课题兼容。本轮没有把示例回复当成实际输出，没有运行科研流程。

用户另行要求把 ARS 文件包下载到当前文件夹，已完成。来源为官方仓库标签 [v3.24.2](https://github.com/Imbad0202/academic-research-skills/tree/v3.24.2)，提交 `fd5ff1b858374219b4d342e38587b66e18f61cbd`。标签对象为 `ecc156277f7a0f2e39110125ba8a41264cfac5de`；压缩包 SHA-256 为 `673e5f18d68b48789a3f413f6cac2db652aa70d5dd5afadf956db377de8d72d3`。

本地只读副本位于 [ARS 审计目录](../ars-audit-3.24.2-xijalnlx/)，来源记录见 [SOURCE.json](../ars-audit-3.24.2-xijalnlx/SOURCE.json)。这是下载资料，不是插件安装，不作为新的运行依赖，也不纳入 wfh 发布清单。没有写入本机已安装 ARS 的目录，没有执行下载包内的脚本。当前会话没有可调用的 ARS Skill，故没有声称拿到了 Skill 返回的根目录；改用下载副本遵循了用户后续指示。

## 2. 统计口径与现状诊断

### 2.1 可复核的规模

统计集合为审计开始时 `git ls-files` 所列文件；不计 `.git/`、原有未跟踪的 `docs/UX-REFACTOR-PROMPT.md`、本文和新下载的 ARS。行数为文件 LF 数；术语为不区分大小写的字面子串出现次数，因此包含标识符、路径和重复索引文字，不能等同于用户阅读次数。

| 项目 | 实测值 | 说明与依据 |
|---|---:|---|
| 已跟踪文件 | 27 个，5,210 行 | 含 LICENSE 417 行、`.gitignore` 3 行；与题述 5,207 行有 3 行差异，采用当前工作区实测值 |
| Markdown / Python / JSON | 25 个，4,790 行 | 不含上面两份文件 |
| 技能目录 | 8 个 | 两份发布清单列出的集合一致，见 [plugin.json](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/.claude-plugin/plugin.json#L12)、[marketplace.json](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/.claude-plugin/marketplace.json#L15) |
| 执行入口 | 7 个 | 共享包不执行研究，见 [共享总览](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/SKILL.md#L9) |
| references 全部 | 12 份，2,885 行 | 含自动生成索引 83 行 |
| 协议与模板 | 11 份，2,802 行 | 去掉生成索引；加上 SPEC 343 行后为 3,145 行，不直接沿用“约 3,300 行”的口径 |
| 最大模板 | 步骤模板 812 行 | [模板](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/tickets_template.md#L1) |
| 失败、诊断或失败分类标记 | 41 种 | 47 种大写下划线标识中，排除 4 种配置/文件/代码符号及 2 种成功标记；这不是“41 种同类错误码”的断言 |
| ARS | 5 个技能、35 条模式/入口记录、16 份命令文件 | [注册表](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:3)；35 条含一个整流程入口和一个恢复入口，不宜统称 35 个普通 mode |

| SKILL.md | 行数 | 是否超过 60 行 |
|---|---:|---|
| [wfh-ask](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-ask/SKILL.md) | 48 | 否 |
| [wfh-grill](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-grill/SKILL.md) | 201 | 是 |
| [wfh-spec](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-spec/SKILL.md) | 242 | 是 |
| [wfh-tickets](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-tickets/SKILL.md) | 377 | 是 |
| [wfh-next](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-next/SKILL.md) | 14 | 否 |
| [wfh-close](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-close/SKILL.md) | 22 | 否 |
| [wfh-implement-spec](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-implement-spec/SKILL.md) | 241 | 是 |
| [wfh-research](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/SKILL.md) | 25 | 否 |

原 README 的快速开始正文只有 **7 行**，已经满足 ≤15 行的数字要求，却列出五次命令调用、四种不同命令。问题在用户要自行判断流程，不在快速开始已经超长。依据：[README](../README.md:52)。

### 2.2 术语频次与真正的暴露位置

| 字面词 | 全部已跟踪 Markdown | 去除历史 SPEC 与生成索引后 |
|---|---:|---:|
| frontier | 115 | 101 |
| claim | 236 | 218 |
| Brief | 220 | 188 |
| MDR | 145 | 132 |
| ticket | 89 | 62 |
| claim ledger | 42 | 35 |
| tracer bullet | 13 | 12 |
| expand–contract | 6 | 4 |
| Schema | 51 | 30 |
| Passport | 21 | 11 |
| 回执 | 11 | 10 |
| blocked by | 25 | 20 |

题述五项主要术语频次在 Markdown 口径下可复现。若把脚本和 JSON 也算进去，Brief / MDR / ticket 分别是 223 / 146 / 97，不能混用统计集合。

频次用于定位，不用作简单删除指标。历史规格和内部状态可以保留原词；需要消除的是用户可见描述、默认报告、错误提示、确认文本与被原样展示的执行提示词中的暴露，例如：

- README 直接展示 `ARS_NOT_AVAILABLE`，还要求用户看 frontier，见 [README:31](../README.md:31)、[README:69](../README.md:69)。
- 入口 description 已含内部词，可能在用户选择技能时出现，见 [wfh-ask:3](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-ask/SKILL.md#L3)、[wfh-tickets:3](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-tickets/SKILL.md#L3)。
- 状态报告明令输出 `graph_valid`、`startability`、doing 与诊断标记，见 [wfh-ask:38](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-ask/SKILL.md#L38)。
- 确认门让用户核对“claim ledger、FINER、交接缝”，见 [wfh-spec:162](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-spec/SKILL.md#L162)；步骤确认还展示拓扑序和执行元数据，见 [wfh-tickets:178](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-tickets/SKILL.md#L178)。
- 提示词入口只有 14 行，却要求在收尾输出四个机器标记，说明压短入口不自动等于界面简单，见 [wfh-next:14](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-next/SKILL.md#L14)。

### 2.3 七个入口承担的实际行为

| 现有入口 | 已核实行为 | 用户要自行承担的衔接 |
|---|---|---|
| wfh-ask | 分咨询与状态，只读；明确执行请求交给目标流程 | 看完建议再选择入口；[依据](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-ask/SKILL.md#L10) |
| wfh-grill | 读已有答案，按依赖分轮提问，确认研究决定后记录 | 确认后被提示另调方案合成；[依据](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-grill/SKILL.md#L143) |
| wfh-spec | 合成已确认信息，不重访谈；另有方案确认 | 确认后再选切步骤或写作；[依据](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-spec/SKILL.md#L153) |
| wfh-tickets | 从方案或审稿意见切步骤，确认后记录，不执行 | 再选择查询、生成提示词或开始执行；[依据](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-tickets/SKILL.md#L227) |
| wfh-next | 限定输入、预检、生成提示词，更新唯一“下一步” | 用户自行拿提示词去执行；[依据](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-next/SKILL.md#L10) |
| wfh-close | 按真实证据验收并同步，失败分类，必要时先确认回环 | 不代做缺失工作，也不自动启动后一步；[依据](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-close/SKILL.md#L12) |
| wfh-implement-spec | 展示完整提示词、确认、开新会话、事件返回后验收 | 缺宿主能力时要求手动复制及补验收；[依据](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-implement-spec/SKILL.md#L117) |

这里保留的研究确认有意义；让用户选择内部入口、审阅整段机械提示词则是可调整的界面成本。不能把二者一起删掉。

### 2.4 多文件、加载量和安装门槛

**文件多，默认展示也多，但“用户必须手动维护所有文件”没有得到支持。** 协议已规定技能写入术语、决定和进度；进度模板甚至明确不手工维护可做步骤集合。用户应提供研究判断、评分、实验返回物和确认，而不是承担同步工作。依据：[盘问记录](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/grilling_protocol.md#L263)、[进度更新](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/flow_template.md#L292)、[人工工作](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/tickets_template.md#L215)。真正的问题是确认门与报告把内部文件、字段和统计全部搬到用户面前。

**渐进加载已有局部实现，应保留。** 纯状态查询不读 ARS 索引；下一步只读目标及声明输入。相反，盘问入口强制读取四份共 911 行的协议模板，加入口本身共 1,112 行；切步骤强制读两份共 1,163 行模板，加入口本身已有 1,540 行，还未计方案对应章节。依据：[状态分流](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-ask/SKILL.md#L41)、[限定输入](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-next/SKILL.md#L10)、[盘问必读](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-grill/SKILL.md#L73)、[切步骤必读](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-tickets/SKILL.md#L84)。这是声明的读取量，不是实测 token 成本，也不能推成每次都读完整仓库。

**交接协议不是无用审计内容。** 92 行中确有来源判定、内容预检、普通输入与内部链的区分和接收证明要求，见 [交接协议:8](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/ars_handoff_protocol.md#L8)、[交接协议:25](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/ars_handoff_protocol.md#L25)、[交接协议:63](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/ars_handoff_protocol.md#L63)。应按输入来源分支加载，并把用户反馈翻译成人话，不应为简洁删除原有门禁。

**两个插件是生产能力的安装边界；Python 要按用途说明。** README 明说 Python 3 仅供索引脚本，见 [README:84](../README.md:84)。wfh 的盘问、方案整理和本地查进度不应因未安装 ARS 全部停摆；现有盘问也明确不需要 ARS，见 [wfh-grill:179](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-grill/SKILL.md#L179)。ARS 的具体生产分支仍可能需要解释器、转换工具等，不能承诺所有操作都无需 Python。

### 2.5 索引不可移植：已实际复核

生成文件第 5 行写入本机缓存绝对路径。生成器虽然把 ARS 导航写成相对根路径，却仍把根目录直接渲染到正文；来源指纹的键对外部文件使用绝对路径，对下载在仓库内的文件又使用相对仓库路径。移动同一份源文件也会改变指纹。依据：[生成索引](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/skills_index.md#L5)、[指纹算法](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/scripts/refresh_index.py#L184)、[根目录渲染](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/scripts/refresh_index.py#L191)。

实际执行：

```bash
python3 -I wfh-research/scripts/refresh_index.py --ars-root /Users/wanfuhao/Documents/ClaudeProjects/wfh-science-skills/ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2 --check
```

实际输出及退出码：

```text
INDEX_STALE: refresh required; no files written
exit code: 1
```

随后只在内存调用仓库生成器，比对旧索引与下载根生成内容：两份均为 83 行，诊断为空、读取 260 份输入；**仅第 5 行根目录和第 8 行指纹不同**。这是本轮的检查基线失败，不是实现后的验收结果；未刷新任何仓库文件，也不证明 ARS 已在宿主加载。

### 2.6 ARS 原文核对带来的额外发现

ARS 的 16 份命令文件已逐份读取：13 份生产模式命令和 3 份阅读声明/缓存维护命令，不能把 16 个命令都当作研究模式。模式命令要求先加载真实核心技能，例如 [审稿命令](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/commands/ars-reviewer.md:7)、[改稿命令](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/commands/ars-revision.md:8)。

- **命名空间有实质性错配。** 官方命令使用 `academic-research-skills:<核心技能>`；wfh 当前生成器的无斜杠备用示例却写 `wfh-science-skills:<核心技能>`，SPEC 的调用说明也保留了这个旧前缀。生成器解析时兼容两种前缀，不代表错误前缀能在宿主成功调用。依据：[生成器:151](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/scripts/refresh_index.py#L151)、[生成器:200](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/scripts/refresh_index.py#L200)、[SPEC:176](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/SPEC.md#L176)。实施时以实际外部插件身份和真实命令为准，不继续输出错误示例。
- **章节新写没有明确的原生模式。** 写作技能的模式表没有单节模式；指南还把“只要特定章节”排除在整篇模式外，却未指明那个专用模式。写作 agent 能按大纲逐节写、调整先后顺序，但默认仍要求完整稿。不能把“引言先写”推成“只写引言并结束”已获保证。依据：[模式表](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/academic-paper/SKILL.md:332)、[指南](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/academic-paper/references/mode_selection_guide.md:51)、[写作 agent](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/academic-paper/agents/draft_writer_agent.md:55)。已有稿件只改引言则可按改稿分支的精确范围处理，见 [改稿适用范围](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/academic-paper/references/mode_selection_guide.md:103)。
- **返修的作者判断不能自动代填。** 未结构化意见通常先整理回应路线；已有明确修改意图和授权时可直接改稿。当前回应组织器要求作者逐条表态并指定修改位置，不能从意见严重程度推断全部接受。旧外部审稿说明仍有“默认全部接受”的句子，存在上游文本冲突；wfh 采用保留作者逐条判断的边界，不改 ARS 原文。依据：[作者裁定](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/academic-paper/agents/revision_coach_agent.md:204)、[旧说明](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/academic-pipeline/references/external_review_protocol.md:77)。
- **格式输出的工具依赖分支不同。** 核心提示技能不统一要求 Python；实际 DOCX 需要 Pandoc，实际 PDF 需要具体编译路径和字体；修改补丁、核验等脚本另有解释器和库要求。没有对应工具时不冒充已经交付目标文件。依据：[安装说明](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/docs/SETUP.md:17)、[DOCX](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/academic-paper/agents/formatter_agent.md:109)、[PDF](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/academic-paper/agents/formatter_agent.md:747)。
- **外部来源识别仍需实测。** intake 按若干常见材料标题识别交接输入；外部笔记也可能有同名标题。保存真实来源，不用标题伪造内部身份；给外部方案的来源说明是否被实际接收，仍要观察响应。依据：[识别条件](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/academic-paper/agents/intake_agent.md:29)、[内部检查](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/academic-paper/agents/intake_agent.md:41)。

ARS 的路由次序为明确意图优先、跨阶段且无明确目标才澄清，筛选另有显式意图边界，见 [路由核心](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/shared/references/routing_core.md:14)。审稿配置本身有需要用户确认的研究检查点，自动选择能力不等于绕过它，见 [配置确认](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/academic-paper-reviewer/SKILL.md:222)。这些大多是提示层约束，文本存在不证明运行时已强制执行，见 [控制可用性](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/docs/CONTROL_AVAILABILITY.md:101)。

## 3. 需要随界面重构澄清的协议冲突

以下是文本冲突与风险，不宣称已复现运行故障。处理范围限于默认入口和进度展示必需的语义澄清；不借本次重构重写全部状态模型。

| 问题 | 双方依据 | 方案处理 |
|---|---|---|
| 盘问既禁止又要求写 FLOW | [入口:69](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-grill/SKILL.md#L69)、[入口:92](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-grill/SKILL.md#L92)、[协议:298](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/grilling_protocol.md#L298) | 明确合法写入者：初始化、确认研究决定后可同步阶段、摘要和下一步 |
| 方案合成既禁止又要求写 FLOW | [入口:17](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-spec/SKILL.md#L17)、[入口:184](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-spec/SKILL.md#L184) | 统一为只合成方案正文，同时允许限定进度字段的同步 |
| 进度冲突既自动修视图又要求停下 | [步骤模板:101](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/tickets_template.md#L101)、[状态协议:23](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/state_protocol.md#L23) | 保持冲突停写；用中文展示两个值和可执行修复动作，不自行裁决 |
| 阶段 5 的整合步骤可能被“全部步骤完成才进入阶段 5”卡住 | [步骤模板:302](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/tickets_template.md#L302)、[状态协议:48](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/state_protocol.md#L48) | 说明阶段完成所指的步骤集合；用合成图检验阶段转换，不能只改文案 |
| 改稿用 R 编号，部分读取说明只写 T | [改稿编号](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/tickets_template.md#L298)、[状态接口](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/flow_template.md#L310) | 状态与验收覆盖 T、R 两类已有路径，不改名 |
| 不重排编号与按顺序重排的要求冲突 | [编号规则](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/tickets_template.md#L85)、[建图规则](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/tickets_template.md#L269) | 保持旧编号；拓扑顺序作为计算结果，不等同于编号顺序 |
| 独占产出规则与改稿、整合共同修改稿件有落差 | [产出规则](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/tickets_template.md#L133)、[改稿模板](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/tickets_template.md#L654)、[整合模板](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/tickets_template.md#L733) | 明确串行与条目所有权，保留验收溯源，不自动并行写同文件 |
| 已确认方案仍可能过不了输入预检 | [评分及范围](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/spec_template.md#L188)、[实际值检查](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/ars_handoff_protocol.md#L25) | 不把“确认”翻译成“材料齐全”；缺少评分、范围时只问缺的内容 |

回环的跨会话处理目前写在入口里，而状态协议引用的盘问协议章节未包含同等细节，见 [wfh-grill:141](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-grill/SKILL.md#L141)、[状态协议:111](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/state_protocol.md#L111)。缩短入口时必须把这段完整迁入共享引用，不得丢掉。

## 4. 三个候选结构方案

| 方案 | 结构 | 优点 | 缺点 | 迁移成本 | 对协议的影响 |
|---|---|---|---|---|---|
| A：保留七入口，重写文案 | 原入口集合与职责不变；中文名称解释、短入口、错误翻译、折叠高级说明 | 改动较小；旧命令与只读行为容易保持 | 用户仍需在多个入口间切换；“继续”仍可能只拿到提示词；不能独立满足单入口和自动执行要求 | 低至中：描述、七入口、模板输出、README、索引 | 主要改展示；状态和执行授权边界仍沿旧规则 |
| B：一个默认入口 + 三动作 | 新增薄入口 `/wfh`；开始、推进、验收；旧七入口高级保留；共享规则仍唯一 | 满足研究者用人话推进；可统一进度、错误、ARS 选择；不复制七套实现 | 必须处理触发冲突、授权、恢复与宿主差异；仅做别名不能达标 | 中：默认入口、清单/索引、输出协议、限定写入权限、迁移说明与行为测试 | 保留事实源和文件结构；增加意图分派与展示边界；默认“继续”的执行路径需更新 |
| C：只做 ARS 融合层 | 保留原 wfh 流程，增加意图映射、内容准备与结果翻译 | 较快改善生产环节；不会要求用户背模式名 | 新用户仍需选 wfh 命令；不解决多个确认和提示词搬运；流程与生产间仍割裂 | 中：映射、交接、结果、诊断、索引 | ARS 来源与验证边界不变，wfh 七入口仍独立 |

A 或 C 可以作为 B 的实施组成部分，但各自作为终局都不能满足第一优先级。推荐 B，采用下述兼容实现，不删除现有研究能力。

## 5. 推荐方案 B 的具体边界

### 5.1 默认入口和高级入口

增加 `wfh/SKILL.md` 作为薄分派入口，控制在 60 行内；其描述使用研究语言，支持自然语言触发。已有七个执行技能保留原目录和命令，改为高级入口；按需读取选中技能及共享协议，不把七份内容复制进新入口。共享包继续不执行。

**数量变化明确列出**：发布清单将从八个技能目录变为九个，即一个默认入口、七个高级入口、一个共享包。用户需要记住的入口从七个变为一个，但没有声称物理入口也只剩一个。采用新增薄入口是为了保留旧命令、旧路径及只读查询语义，避免迁移中把 `wfh-ask` 直接改成会执行的命令。

高级入口的自然语言自动触发应收拢到默认入口；可考虑 `disable-model-invocation: true`，由 `/wfh` 读取对应实现说明执行，同时保留用户直接斜杠调用。该元数据的宿主实际效果须在实施时核实，不能只凭文档声称已隐藏或已解决触发冲突。不把“新建一个 command 包装文件”单独当作自然语言触发已实现。

默认分派遵循以下顺序：

1. 用户显式指定技能或生产模式时尊重用户；不强制先走完整规划。
2. 只有询问进度时只读；多个课题不猜选，问一次课题名称。
3. “继续”沿既有进度中的进行中或下一步执行；不重新收集已有背景。依赖、输入、研究确认或授权缺失时，仅请求所缺内容。
4. 新方向先澄清问题；已有研究问题则按轮收敛设计。未知事实由系统查询，科学贡献、机理、解释与价值评分仍由研究者决定。
5. “做完了”触发证据验收，不能只凭一句话把步骤标完成。
6. 收到审稿意见先组织改稿；结论站不住则解释受影响的研究决定并走回环确认，不自动更换结论。

### 5.2 三动作下保留必要的确认

| 用户动作 | 默认行为 | 何时停下来 |
|---|---|---|
| 开始 | 读已有材料，问剩余问题，整理研究方案和步骤草案 | 研究决定、用户评分、方案边界和步骤粒度需要确认；不让用户选内部命令 |
| 推进 | 读当前进度，验证依赖与输入，直接开展当前已授权步骤 | 需要用户做实验、补材料、裁决研究判断、允许新的会话或其他宿主授权时 |
| 验收 | 按原标准读取证据，同步进度；不通过则解释缺件或需重新讨论的决定 | 证伪或设计失效需要确认回环；不代填结果，不自动改上游 |

默认路径不把整段内部启动提示词作为每步必审材料。保留必要研究确认；技术提示词按需查看。长步骤需要新会话时，遵循宿主权限和用户授权；没有新会话工具则在可容纳的输入边界内在当前会话推进。若无法保持边界，明确需要新会话，并给一个可执行动作，不能假称自动接续成功。旧高级执行命令原有显式提示词确认可保留。

“帮我看看现在做到哪”不修改文件；“继续”才是当前一步的执行请求，完成后停下，不自动连跑。这是默认分派规则的变更，必须记录在 MIGRATION，而不是把现有只读入口悄悄改写。依据：[原只读边界](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-ask/SKILL.md#L43)、[原逐步停止](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-implement-spec/SKILL.md#L188)。

### 5.3 只看一个进度文件，同时保留原始结构

进度文件 FLOW.md 标题后增加一段派生中文摘要，例如：

> 现在已确认研究范围，正在核对两组材料的界面表征。下一步是补齐对照组的测试记录；拿到记录后，我会检查它是否支持当前解释。

这是设计示例，未实际运行。摘要不新增第二条持久命令，只用人话解释原状态和唯一的“下一步”；机器字段、章节名、五字段结构、编号、引用和完成记录保持兼容。事实源仍为步骤文件，决定来源仍为 `decisions/LEDGER.md`，不能把摘要变成另一套事实源。依据：[视图与事实源](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/flow_template.md#L107)、[下一步唯一位置](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/references/flow_template.md#L152)。

摘要由有写入授权的动作同步：初始化、确认方案、生成下一步或验收后。若允许下一步入口同步摘要，必须在共享写入权限中明确这项派生字段权限；现有“只写下一步”不够。只读查询发现不一致时，只报告重新计算的结果和需要修复的位置，不写回，也不依据过期摘要执行。

其余文件默认只在系统内部读写。用户需要时给自然语言摘要，提到文件时写“BRIEF.md（研究方案）”“TERMS.md（术语说明）”“decisions/（研究决定记录）”“tasks/（步骤记录）”。正文内的合同字段、已有文件名和机器状态不改名；内部完整表格不原样搬到默认进度报告。

### 5.4 按动作和条件读取

| 场景 | 初始读取 | 满足条件才追加 |
|---|---|---|
| 进度查询 | 默认入口 + 状态规则 + FLOW 与图验证所需步骤元数据 | 声明的完成证据；不加载 ARS 或全套盘问模板 |
| 新方向 | 默认入口 + 分流规则 | 模糊到没有研究问题时读探索契约；问题已定时读盘问核心和决策分类 |
| 方案合成 | 已确认决定 + 方案字段及确认规则 | 真正写术语、决定记录或交给 ARS 时读相应模板/交接分支 |
| 切步骤 | 通用图约束、相应步骤类型和进度更新规则 | 改稿才读改稿模板；全局机械改动才读对应分支 |
| 推进 | FLOW、目标步骤、明确声明输入、执行规则 | 只有 ARS 步骤读目标模式与适用交接规则 |
| 验收 | 图和证据验证、同步与失败分类规则 | 结论失败才读回环模板；ARS 步骤才检查实际调用记录 |

短 SKILL 不能只是把原文整体搬到一个新的长文件并仍要求每次通读。拆分时给每个引用写出读取条件；研究边界、图校验和证据规则不能延后到动作之后。历史 SPEC 保留原文，增加当前行为说明或归档指针，历史决策不删除。依据：[共享唯一来源](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/SPEC.md#L140)、[历史标记](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/SPEC.md#L7)。

### 5.5 索引与安装说明

索引生成改用两个逻辑来源标识，例如 `wfh/<相对路径>` 与 `ars/<相对路径>`，指纹只依赖这些稳定键和内容；生成文件记录 ARS 版本/来源身份，不渲染安装绝对路径。实际调用时动态解析用户或宿主提供的当前 ARS 根。

不取消 `--ars-root`，也不把本次下载目录硬编码为默认。入口集合应从实际发布清单核对，避免脚本 `WFH` 常量永久固定为七项；共享包与高级入口的角色要单独表达。依据：[硬编码集合](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/scripts/refresh_index.py#L11)、[命令解析](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/scripts/refresh_index.py#L151)、[只读检查](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/scripts/refresh_index.py#L210)。

README 的快速开始保持 ≤15 行，只说装什么、用 `/wfh` 加一句研究意图、卡住时仍对同一入口说“卡住了”。两个插件的详细安装步骤和高级入口折叠；日常使用者不执行索引维护。ARS 未安装只影响所需的生产动作，不妨碍本地研究整理。ARS 分支的额外工具依赖按实际动作再说明。

## 6. 用户可见术语替换表

替换作用于入口 description、默认报告、提问、确认、失败提示和面向研究者的说明；不全仓字面替换标识符、路径、证据或论文内容。

| 内部表达 | 用户可见表达 |
|---|---|
| task / 任务 / ticket | 步骤 |
| frontier | 现在能做的；提问场景为“现在需要你回答的” |
| claim | 要证明的说法；已在讨论结论时按上下文称“这个结论” |
| claim ledger | 要证明的说法和现有证据 |
| Brief | 研究方案 |
| MDR | 研究决定记录；需要展开时解释“为什么这样设计” |
| grill | 问清研究问题 / 确定研究设计 |
| spec | 整理研究方案 |
| close | 验收 |
| drift / NEXT_STEP_DRIFT | 进度对不上 |
| tracer bullet | 先做一小步，检查整条证据链能否走通 |
| expand–contract | 分批替换并核对一致性 |
| blocked by / blocker | 需要先完成…… |
| todo / doing / done / blocked / dropped | 待开始 / 正在做 / 已通过验收 / 等待材料或前一步 / 已取消 |
| startability / graph_valid | 现在能不能开始 / 步骤顺序是否一致 |
| Schema / Passport / 回执 | 依语义解释“必需研究信息 / 材料来源记录 / 实际接收或执行记录”，不展示内部标签 |
| ARS:<skill>:<mode> | 我会使用检索 / 写作 / 审稿 / 改稿 / 格式整理能力 |
| 错误码 / 内部 token | 不展示；保存在现有内部执行或验收记录中 |

失败展示固定为两句话：**发生了什么或缺什么；现在可以做的一件事。** 不把不同失败都翻成“重试”，不在折叠详情里继续向普通用户展示裸码。示例为设计稿：

| 内部情况 | 两句用户提示 |
|---|---|
| ARS 不可用 | 现在还没有装好负责检索和写作的扩展。请按安装说明添加 ARS，完成后对我说“继续”。 |
| 必需研究范围缺失 | 研究方案还没有说明材料范围，暂时不能开始写作。请告诉我这次包含哪些体系、排除哪些体系。 |
| 缺输入 | 这一步还缺对照组的测试记录。请把记录放到这里或告诉我文件位置。 |
| 进度不一致 | 进度里写的下一步已经完成，和步骤记录对不上。你可以让我先核对并修正进度。 |
| 结论被证伪 | 现有证据不支持原先的解释，这一步不能通过验收。请确认是否重新讨论“界面反应导致寿命差异”这一决定。 |
| 未知生产错误 | 写作没有完成，目前无法确认已有结果。请让我先检查本次失败记录。 |

未知错误不编造具体缺件，不自动吞掉未完成状态。ARS 原始响应只作为内部证据，研究者看到的是保留证据含义的摘要。宿主原始工具报错、扩展自有通知不全由 wfh 文本控制；必须单独记录实际可控范围，不宣称能隐藏宿主界面的一切文字。

## 7. “研究意图 → ARS 模式”映射草稿

此表为维护者和模型内部使用，用户只见研究动作。来源为下载版真实注册表，执行前仍需加载所选技能及该分支契约。用户显式指定优先；输入缺失只补所缺材料，不据此偷偷换模式。默认不调用整流程编排器。依据：[SPEC 边界](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/SPEC.md#L251)。

下表中的 `DR`、`AP`、`REV` 分别指注册表的 deep-research、academic-paper、academic-paper-reviewer，缩写只在此表使用。

| 意图 | 默认内部选择 | 分流与必要输入 | 注册表依据 |
|---|---|---|---|
| 检索：快速了解方向 | DR `quick` | 主题、范围；输出研究短报，不冒称系统综述 | [15–16 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:15) |
| 检索：深入研究具体问题 | DR `full` | 明确问题与研究范围；不是默认跑整篇论文 | [15 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:15) |
| 检索：核实一个说法 | DR `fact-check` | 待核对说法和来源；与作者决定是否更换结论分开 | [20 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:20) |
| 开始：研究问题尚不清楚 | DR `socratic` 或 wfh 盘问 | 前者探索研究问题；已有明确问题才用 wfh 收敛设计；两者不混为 ≤4 轮同一承诺 | [21 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:21)、[原分工](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-grill/SKILL.md#L20) |
| 综述：梳理已有证据 | DR `lit-review` | 问题、范围、文献；研究综述与发表型综述文章区分 | [18 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:18) |
| 综述：写综述论文 | AP `lit-review` | 已有文献材料与写作意图 | [34 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:34) |
| 综述：明确要求系统综述 | DR `systematic-review` | 具体研究问题、纳排标准等；不因“综述”二字一律选系统综述 | [22 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:22) |
| 写作：写提纲 | AP `outline-only` | 已有研究问题、证据和写作边界 | [30 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:30) |
| 写作：写引言等章节 | 已有稿件改引言用 AP `revision`；从零新写的映射暂不定案 | 没有独立章节模式，且 full 指南排除仅特定章节；受限写作是待验证的衔接候选，不能当作已支持默认路径 | [28 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:28) |
| 写作：写摘要 | AP `abstract-only` | 正文、研究结果与语言要求；不把摘要写作映射到整篇生产 | [33 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:33) |
| 审稿：投稿前全面自审 | REV `full` | 稿件与需要确认的审稿配置 | [44 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:44) |
| 审稿：快速看 / 只看方法 | REV `quick` / `methodology-focus` | 以用户限定范围分流，不都用五视角全面审稿 | [46–47 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:46) |
| 改稿：审稿意见回来了 | AP `revision-coach` → wfh 改稿步骤 | 先收原文、稿件，组织逐条回应与待确认策略，再切步骤；不自动决定更换科学主张 | [31–32 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:31) |
| 改稿：按已确认策略修改 | AP `revision` | 原稿、意见、已确认回应策略；逐步执行后验收 | [31 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:31) |
| 改稿：检查已有回复草稿 | AP `rebuttal-audit` | 审稿意见与已有回复；不把只收到意见的情况送去此分支 | [38 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:38) |
| 格式：转 Word、LaTeX、PDF / 引用格式 | AP `format-convert` | 可转换的稿件、目标格式及该格式所需工具；转换不等于科学验收 | [35 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:35) |
| 格式：核引用 / 使用声明 | AP `citation-check` / `disclosure` | 按需求分别选；使用声明需目标期刊或政策信息 | [36–37 行](../ars-audit-3.24.2-xijalnlx/academic-research-skills-3.24.2/MODE_REGISTRY.md:36) |

保留 ARS 自身的明确意图和多阶段歧义处理。一次给出原稿、意见和文献但没有明确要做什么时，只问一个研究目标问题，不把 35 个模式列给用户挑。筛选已有文献记录只有用户明确要求筛选时才转 `sr-screener`，不能因系统综述自动切过去。真实的内部交接材料继续遵守 ARS 原契约，不伪装 wfh 外部方案为已验证的内部材料。

## 8. 按三个提交实施的边界（等待确认）

| 提交 | 中文提交标题草案 | 范围与完成条件 | 单独回滚时的边界 |
|---|---|---|---|
| 1：入口与文案 | `refactor: 用研究语言重写入口与反馈` | 现有八份 SKILL 均 ≤60 行；长规则移入按条件读取的引用；改用户可见描述、提问、确认和错误反馈；保留原命令与行为，不先加入单入口执行；历史 SPEC 原文保留 | 还原本提交即可恢复旧文案与加载结构；不改已有课题文件结构 |
| 2：结构简化 | `refactor: 增加统一入口并简化进度展示` | 新增薄默认入口及清单；默认三动作、旧入口折叠；FLOW 中文派生摘要与写权限明确；处理默认执行必需的冲突；索引入口集合和稳定来源键一并修正；README、MIGRATION 记录当时可用行为 | 统一入口移除后旧七入口仍可使用；已有 FLOW 中新增摘要是可忽略附加内容，不需反向迁移 |
| 3：ARS 融合 | `refactor: 自动衔接研究意图与 ARS 能力` | 落实映射、真实入口解析、内容准备和结果/失败翻译；不复制 ARS；完成实际用户脚本、十段输出、十二条行为回归；更新最终 README、MIGRATION 和验证记录 | 恢复到前两步的默认 wfh 流程与旧 ARS 接法；课题原始文件仍保持兼容 |

每个提交均更新受其影响的生成索引并完成相应检查，不能留下靠后续提交才能加载的入口或断链引用。最终验收修正并入第三个提交，不另加一个“验证补丁”提交。实施时逐个提交汇报“改了什么、验证了什么、如何撤销”；提交后的默认撤销方式为对具体提交作逆向提交，保留课题数据。本文不预先生成不存在的提交号，也不在方案确认前提交。

## 9. 验收清单与实际测试记录设计

以下全部是实施后的验收要求；除索引基线外，本轮不标记“已通过”。

| 观察项 | 通过标准 | 证据 |
|---|---|---|
| 单入口 | 新会话仅输入 `/wfh` 加研究意图可进入正确动作；自然语言触发另测；不要求选择旧命令 | 保存真实触发、实际加载入口和第一段用户回复 |
| 零内部术语 | 十段真实用户回复及可见提示/报告没有禁词与裸诊断标记；内部文件名均附中文说明 | 静态扫描 + 人工核对；内部记录另存不进入用户报告 |
| 一屏 | 快速开始正文 ≤15 行；全部九份 SKILL ≤60 行，含 frontmatter；高级目录折叠 | 实际物理行数，不能只数主段落 |
| 自动 ARS | 用户没说模式名；记录系统选择、实际调用和结果；用户显式指定优先 | 真实调用记录与用户输出；下载源可读不等于实际可调用 |
| 可行动失败 | 已知失败均给“缺什么/发生什么 + 一个动作”两句；未知失败有诚实兜底 | 错误表覆盖及至少 ARS 缺失、输入缺失、进度冲突的真实样本 |
| 行为保持 | 下列十二条保留的研究行为全部验证 | 对照原 SPEC，不要求复现旧错误码和旧命令输出格式 |
| 索引一致 | 指定有效 ARS 根执行 `--check` 退出 0；两份清单与目录一致；移动同内容根后不产生仅因路径变化的差异 | 保存命令、退出码、实际输出与两根目录的对照 |
| 文件兼容 | 原路径、章节、字段、编号、引用、完成记录仍可读；旧课题无需批量迁移 | 用旧课题的隔离副本查询、续做和验收，比较更新范围 |
| 不改 ARS | 下载资料和安装目录无改动，wfh 发布包不包含 ARS 源文件 | 文件清单与写入范围检查 |

### 9.1 八条用户脚本如何实际运行

在隔离的合成科研工作区进行，不冒充真实实验。每条记录：给定状态、用户原话、实际读取、真实回复、实际动作/调用、文件差异、是否符合预期；失败保留原输出，不把预期文案填到“实际输出”栏。建议写入 `docs/UX-TEST-RESULTS.md`；它是维护验证资料，不是新增课题产物。

| # | 用户原话 | 前置材料 | 实际应观察到的行为 |
|---|---|---|---|
| 1 | 我想研究固态电池界面，但还没想清楚具体问题 | 无已有课题 | 进入探索或合适的盘问，问研究内容，不让用户选命令；不代定机理 |
| 2 | 帮我看看我现在做到哪了 | 唯一旧课题副本 | 只读进度，报告现在在哪、一个下一步；不启动研究、不改文件 |
| 3 | 继续 | 上一步已定位且有可开始步骤 | 直接进入当前步骤；不重问已有背景；实际执行不以“提示词已生成”充数 |
| 4 | 这一步做完了 | 有声明产出、原验收标准及证据 | 逐项验收并更新步骤与进度；缺证据不能标通过 |
| 5 | 帮我写引言 | 已确认问题、方案、证据及写作材料 | 系统选择真实写作路径并实际调用 ARS；用户不用报模式名；仅交付授权范围 |
| 6 | 审稿意见回来了 | 审稿原文及稿件 | 进入改稿组织，切出步骤，确认回应策略；意见要改结论时不静默修改 |
| 7 | 这个结论站不住 | 当前说法、反例证据及决定来源 | 解释影响哪个研究决定，按回环规则确认和记录；不把它当一般执行失败重跑 |
| 8 | ARS 没装 | 控制为生产入口不可用 | 两句人话说明及可操作安装指引；不崩溃、不冒称写作完成；本地整理仍可进行 |

十段真实输出取八条各一段，再加“缺少必要输入”和“进度指向已完成步骤”各一段。另测多个课题、需要人工实验、缺新会话工具、明确指定模式、多阶段输入无明确意图；这些是分派边界，不要求用户学习内部名称。

若实施验证时当前宿主仍未暴露 ARS Skill，必须记录实际不可用，不能以读取下载包或模拟文本声称“实际调用通过”。该项属于未完成验收，需在可加载插件的会话复测。

### 9.2 原 SPEC 十二条的保留关系

依据：[SPEC 测试用例](https://github.com/wanfuhao-art/wfh-science-skills/blob/4105918de626c0c7c118534b07cd60348f511763/wfh-research/SPEC.md#L278)。历史条文保留；对外命令、旧词和错误码的改动在迁移说明里解释。

| 原编号 | 必须保持的行为 | 新界面下如何观察 |
|---|---|---|
| 1 | 已有问题的默认规划盘问 ≤4 轮；实质性决定无建议；确认门；术语与重要决定记录 | 用完整合成输入实际分轮，核对没有代定贡献；探索过程不虚称同一轮次上限 |
| 2 | 合成方案不重访谈；四个必需字段；未决保留；评分来自用户 | 比较已有回答与新提问，检查内部文件及用户评分来源 |
| 3 | ≥6 个可验证步骤，依赖、执行方式、验收齐全，图无环 | 检查实际内部步骤文件与图；用户无需看图算法 |
| 4 | 查询—推进—验收闭环，输入范围受限、可做步骤正确推进 | 真实执行后读文件差异，不凭文字说“已更新” |
| 5 | 三类研究意图正确分流，事前读真实契约 | 改验正确动作及一条下一步；不再要求展示“一个命令+反模式” |
| 6 | 电池例的术语、设计理由、四个说法及人工 XPS/ICP-MS 步骤保留 | 合成证据明确标注；系统不冒充测量完成 |
| 7 | 外部方案真实接收；删 Scope 的负例与评分未决负例；内部门禁不绕过 | 分开记录 wfh 预检与 ARS 响应；用户只见缺项与动作 |
| 8 | 连续三次接受后不再给下一题建议；来源或待核验；不造引用 | 保存实际对话与来源检查，不只检查模板句子 |
| 9 | 说法失败触发回环并关联正确决定，旧行留痕 | 真实写入回环包并恢复正确分支；用户先确认 |
| 10 | ≥3 个改稿步骤与终端整合，意见原文/回应/改动对应，图无环 | 核对实际 R 编号文件与整合依赖 |
| 11 | 仅进度“下一步”与声明输入可接手；过期下一步能被发现；合法进行中可恢复 | 正负样本均跑；对外用“进度对不上”，不要求裸码 |
| 12 | 各说法只登记引用键，集中核验一次共享文献 | 检查引用核验产物和调用记录，避免每步重复核同一篇 |

## 10. 迁移范围与等待确认的事项

实施后的 MIGRATION.md 至少包含：旧七命令 → `/wfh` 加意图的对应关系；原只读查询仍只读；提示词生成与实际推进的差别；高级入口位置；默认隐藏的内部记录；FLOW 的派生摘要；索引维护变化；ARS 缺失时怎么办。旧 `wfh-status` 只作为历史迁移说明，不宣称仓库仍提供该命令。

| 旧入口意图 | 新默认用法 |
|---|---|
| wfh-ask 咨询 / 状态 | `/wfh 我现在该做什么` / `/wfh 帮我看看进度` |
| wfh-grill | `/wfh 我想研究……` |
| wfh-spec | `/wfh 把确认过的内容整理成研究方案` |
| wfh-tickets | `/wfh 帮我安排接下来的步骤` |
| wfh-next | `/wfh 继续`；只要提示词时明确说“生成接手说明，先不执行” |
| wfh-close | `/wfh 这一步做完了` |
| wfh-implement-spec | `/wfh 继续`；需要另开会话时由系统解释并遵守宿主授权 |

本方案不要求已有课题迁移文件；FLOW、BRIEF、TERMS、decisions、tasks 的路径与原结构保持兼容。没有旧摘要也能重新计算状态，不以“先升级所有文件”为继续工作的前提。

需要维护者确认的是**方案 B 整体及其明确的边界变化**：新增一个薄入口使物理技能数变为九个；旧七入口保留；默认“继续”执行已授权当前步骤而不是只给提示词；研究确认和回环确认仍保留。其余常规文案与拆分按上述约束实施。

尚需核实的技术问题不得当作已解决：章节写作的真实范围限定、当前宿主默认入口/高级入口触发与新会话行为、ARS 实际可调用性。实施时以真实契约与实际输出判断；如章节执行必须启动更大范围的写作，先把限制说明给维护者，不能虚构新模式或默默扩大范围。

其中有一个需要维护者给边界的未决项：若核实后 ARS 确实无法在现有正式契约内从零只写引言，是否允许 wfh 读取 ARS 写作指引后组织一次明确限定范围的写作调用，并以实际输出证明边界？若不允许，则不能在“不改 ARS、不假造模式”的同时宣称这条验收已通过；应保留未通过并协商目标。此项不影响先完成已明确的入口、文案和进度改造，但不能在最终交付时绕过。

本轮改动只有新增本文和用户要求的 ARS 下载目录；原有 `docs/UX-REFACTOR-PROMPT.md` 保留。没有修改技能、协议、索引、README 或发布清单，没有提交。若不采用方案，可移除本文；下载资料可以整目录移除，不影响已安装插件或旧课题。

## 附录：统计复核方法

本次使用 Python 标准库、`git ls-files` 和字面正则统计，解释器使用隔离模式。以下命令只读；下载目录和本文不会进入基线统计，因为它们未被跟踪。实施后需要按本文记录的基准提交重新取文件集合，不能把新增文档混入旧基线。

```bash
python3 -I - <<'PY'
from pathlib import Path
import re, subprocess
paths = [Path(p) for p in subprocess.check_output(['git', 'ls-files', '-z']).decode().split('\0') if p]
print('tracked files:', len(paths))
print('tracked lines:', sum(p.read_bytes().count(b'\n') for p in paths))
md = '\n'.join(p.read_text() for p in paths if p.suffix == '.md')
for term in ('frontier', 'claim', 'Brief', 'MDR', 'ticket', 'claim ledger', 'tracer bullet', 'expand–contract', 'Schema', 'Passport', '回执', 'blocked by'):
    print(term, len(re.findall(re.escape(term), md, re.I)))
for p in paths:
    if p.name == 'SKILL.md' or p.as_posix().startswith('wfh-research/references/'):
        print(p, p.read_bytes().count(b'\n'))
PY
```
