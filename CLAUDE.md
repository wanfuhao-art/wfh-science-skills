# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目性质与权威来源

这是科研流程技能插件，主要实现是 Markdown 中的路由、执行协议和模板，不是常规 Python 应用。Python 脚本仅用于维护索引及离线验证，均使用标准库；日常使用插件不需要 Python。没有依赖安装、编译构建或独立 lint 配置。

本文件仅供源码仓库维护，不作为安装后插件的运行时上下文；`.gitattributes` 将其排除在 Git 导出归档之外。发布前对实际导出包执行清单严格校验与隔离安装；直接校验源码目录时，CLI 可能对根目录 `CLAUDE.md` 给出不会被插件加载的警告。

先读 `README.md` 了解产品边界。现行行为以各入口 `SKILL.md` 和 `wfh-research/references/` 共享协议为准；`MIGRATION.md` 说明兼容要求。`wfh-research/SPEC.md`、历史审计及发布记录用于理解设计背景，不能覆盖现行协议。

## 常用维护命令

以下命令均从仓库根目录运行。

协议、插件清单、技能调用边界及包内链接检查：

```bash
python3 -I wfh-research/evals/check_contracts.py
```

评估工具回归测试：

```bash
python3 -I wfh-research/evals/test_eval_tools.py
```

运行单个工具测试（此脚本接受 unittest 的类名或方法名）：

```bash
python3 -I wfh-research/evals/test_eval_tools.py OutputChecks.test_manifest_keeps_missing_replies_visible
```

### 能力索引

以下命令要求 `$ARS_ROOT` 已指向由宿主安装信息或其他可靠来源确认的 ARS 文档根，其中应有 `MODE_REGISTRY.md` 和 `.claude-plugin/plugin.json`。不能把历史审计路径或猜测的版本缓存目录当作当前安装。

只读检查索引是否与来源一致：

```bash
python3 -I wfh-research/scripts/refresh_index.py --ars-root "$ARS_ROOT" --check
```

重新生成 `wfh-research/references/skills_index.md`：

```bash
python3 -I wfh-research/scripts/refresh_index.py --ars-root "$ARS_ROOT"
```

索引工具回归，包括目录迁移、来源指纹、清单不一致与只读检查：

```bash
python3 -I wfh-research/scripts/verify_index.py --ars-root "$ARS_ROOT"
```

`refresh_index.py --check` 返回 0 表示一致，1 表示过期，2 表示来源或清单存在诊断问题。省略 `--check` 会写文件，即使缺少 ARS 也会写入带诊断的索引；不要用省略 `--ars-root` 的刷新覆盖现有完整索引。脚本使用 `Path.is_relative_to` 和 `str.removesuffix`，维护环境需 Python 3.9 或以上。

### 合成案例与回复检查

生成独立的合成科研工作区；输出目录必须尚不存在，`.scratch/` 已被 Git 忽略：

```bash
python3 -I wfh-research/evals/prepare_cases.py --output .scratch/ux-cases
```

在案例工作区完成宿主演练，并将实际回复保存到 `eval-NN/with_skill/outputs/response.md` 后检查：

```bash
python3 -I wfh-research/evals/check_outputs.py --results .scratch/ux-cases --cases .scratch/ux-cases/evals.json --output .scratch/ux-report.json
```

`prepare_cases.py` 只生成材料，不运行模型。`check_outputs.py` 只检查已保存回复的词汇、文件用途说明及缺失情况，不能判定科研行为正确。另一个文件 `wfh-research/evals/evals.json` 是带模拟 ARS 的协议演练案例集，不是已执行结果。离线检查、源码核对、宿主真实调用应分别报告；真实行为验证需重新加载插件后演练，重点见 `docs/RELEASE-3.2.2.md`。

## 核心架构

- **插件发现层**：`.claude-plugin/plugin.json` 与 `marketplace.json` 声明同一组九个技能目录，版本与技能列表必须同步。`check_contracts.py` 同时核对实际目录和调用角色；增减入口时需要相应更新检查。
- **默认入口与高级入口**：`wfh/SKILL.md` 是可被自然语言触发的统一入口。七个高级入口保留 `disable-model-invocation: true`，供用户手动调用；默认入口通过 Read 加载对应实现，不自动用 Skill 调用高级入口。`wfh-research/SKILL.md` 同时设置 `user-invocable: false` 和 `disable-model-invocation: true`，只是内部共享包；按当前动作加载所需分支，不把整个包当作启动必读。
- **共享协议层**：`dispatch_protocol.md` 管意图分派，`execution_protocol.md` 管执行与上下文隔离，`state_protocol.md` 管状态和验收，`ars_handoff_protocol.md` 管外部科研能力交接，`user_output_protocol.md` 管用户可见表达。入口、共享协议、模板和契约检查共同构成实现；改行为时一起核对，避免只改某个入口留下冲突规则。
- **研究工作区层**：`FLOW.md` 汇总阶段、任务图与下一步；`BRIEF.md` 保存研究方案及主张；`TERMS.md` 和 `decisions/` 保存术语与研究决定；`tasks/` 保存步骤、产物和证据。这些是用户课题运行时文件，不是初始化插件源码仓库时应创建的文件。
- **外部能力与索引层**：ARS 提供检索、写作、审稿和专业核验，本仓库不包含其生产代码。`refresh_index.py` 从本插件入口、共享文档以及显式提供的 ARS 文档生成导航与内容指纹；`skills_index.md` 是生成文件，不能手工维护，也不证明技能已被宿主加载。修改入口、共享协议、清单或索引生成器后均可能需要刷新索引。

## 修改行为时必须保留的边界

- 独立小请求直接处理，不强迫创建完整课题。默认 `/wfh` 只有在用户明确要求生成方案或授权的交付目标包含方案时才衔接方案整理；单独 `/wfh-grill` 确认讨论后停下，不生成或更新 `BRIEF.md`。
- 高级入口职责保持独立：`wfh-ask` 只读，`wfh-next` 只准备交接，`wfh-close` 只验收，`wfh-implement-spec` 确认接手摘要后只执行指定一步。单说“继续”只恢复当前步骤；明确授权的多步骤目标才接续推进。
- 已有任务图时，每个 AI 可执行步骤使用全新执行子代理，返工也不复用。交接传工作区、任务文件、声明输入、产出和验收要求等指针，不粘贴材料正文或上一步对话。执行子代理只写声明产物和执行证据；主会话读取实际产物后验收并同步任务状态及 `FLOW.md`。验收子代理与执行子代理使用不同上下文。
- 科研建议、研究者确认、证据支持是三个不同状态。交付完成与主张支持程度分开：否定结果也可以满足原定验收标准；改变研究解释或设计须走回环确认，不能静默修改上游决定。
- 步骤文件是状态、依赖、执行方式、产出声明和验收标准的事实源，`FLOW.md` 的任务表是视图。发现两者冲突先报告原值并停写，不据此静默修复。任务状态只有 `todo/doing/done/blocked/dropped`，`partial` 是验收结果；`done` 必须有实际完成证据，`dropped` 不解锁依赖。依赖满足不等于输入、资源和研究决定已允许启动。改状态行为时联查 `state_protocol.md`、`flow_template.md`、`flow_details.md`、`tickets_template.md` 和相关入口。
- 保留既有工作区路径、状态 token、任务编号和已确认验收标准；不要按 Dxx 编号猜研究决定含义，也不要强制 T01 为某种任务类型。兼容细节查 `MIGRATION.md` 和状态协议。
- ARS 的模式、输入要求、阈值与必要确认以实际版本原文为准，不在 wfh 中另建一套专业门槛。源码兼容基线是 3.24.2，不代表用户当前安装版本；不修改 ARS 安装目录，不把读取文档描述为实际调用。
- 面向科研用户时遵循 `user_output_protocol.md`：中文说明实际进度、缺件和下一步，文件路径附中文用途，内部状态与协议术语不直接倾倒给用户。
