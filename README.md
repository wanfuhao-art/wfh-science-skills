# wfh-science-skills

一个 Claude Code 插件：把 wfh 科研工作流和 ARS 学术研究技能打包在一起，装一次即可使用。

## 包含什么

### wfh 工作流（8 个 skills）

| 目录 | 作用 |
|---|---|
| `wfh-ask/` | 科研入口咨询 + 课题状态：该用哪个技能，或课题现在做到哪 |
| `wfh-grill/` | 按轮盘问，收敛研究决策，产出 `TERMS.md` / MDR / 决策台账 |
| `wfh-spec/` | 把已确认台账压成 `BRIEF.md` |
| `wfh-tickets/` | 把 Brief 切成可验证任务图，写 `tasks/` 与 `FLOW.md` |
| `wfh-next/` | 为单条任务生成新会话启动 / 恢复提示词 |
| `wfh-close/` | 逐条证据验收，更新任务与 `FLOW.md` |
| `wfh-research/` | 共享协议、模板、索引生成器（不是执行入口） |
| `wfh-implement-spec/` | 可选编排层：生成提示词 → 开新会话 → 自动验收 |

### ARS 学术研究（5 个 skills，已内置）

| 目录 | 作用 |
|---|---|
| `academic-paper/` | 论文写作：plan / full / outline / revision / abstract / citation-check / disclosure / format-convert 等 |
| `academic-paper-reviewer/` | 模拟审稿：多份审稿报告 + 编辑决定 + 改稿路线图 |
| `academic-pipeline/` | 10 阶段全流程编排 |
| `deep-research/` | 深度检索、文献综述、事实核查、系统综述 |
| `sr-screener/` | 系统综述筛选：协议、标题/摘要、全文、PRISMA |

ARS 运行时（`shared/`、`scripts/`、`commands/`、`agents/`、`hooks/`、`docs/`）也在插件根目录，`/ars-*` 命令随插件一起提供。

## 仓库结构

```text
wfh-science-skills/
├── .claude-plugin/               # plugin.json + marketplace.json
├── wfh-*/                        # 8 个 wfh skills
├── academic-*/ deep-research/ sr-screener/  # 5 个 ARS skills
├── shared/ scripts/ commands/ agents/ hooks/ docs/  # ARS 运行时
├── MODE_REGISTRY.md
└── third_party/academic-research-skills/  # ARS 原始许可证与 NOTICE
```

## 安装

### 作为插件安装（推荐）

在 Claude Code 中运行：

```text
/plugin marketplace add <仓库路径或 GitHub 仓库>
/plugin install wfh-science-skills
```

**装一次即可**，ARS 已内置，不需要再装 `academic-research-skills`。

- 本地 zip / 文件夹：`<仓库路径或 GitHub 仓库>` 换成解压后的仓库绝对路径。
- GitHub：换成 `wanfuhao-art/wfh-science-skills`（Private 仓库需要先把对方加为 collaborator，或改成 Public）。

## 快速开始

```text
/wfh-ask 我该用哪个技能？
/wfh-grill 我想研究……
/wfh-spec
/wfh-tickets
/wfh-ask 这个课题现在做到哪了？
/ars-reviewer
/ars-revision
```

## 工作流

```text
/wfh-grill → /wfh-spec → /wfh-tickets
                              │
              ┌───────────────┴────────────────┐
              │  每条任务：                     │
              │  /wfh-ask 看 frontier           │
              │  /wfh-next 生成启动提示词        │
              │  新会话执行（ARS / direct / human）│
              │  /wfh-close 验收并推进           │
              └───────────────┬────────────────┘
                              │
              阶段 5–8：ARS 审稿 → 改稿 → 格式 → 定稿
```

## 前置依赖

- **Claude Code / Claude Desktop**：需要支持插件与 skills 的版本。
- **Python 3**：仅 `wfh-research/scripts/refresh_index.py` 需要，用于生成 / 校验路由索引。

## 许可

- 本插件整体：CC-BY-NC-4.0，© wanfuhao-art，见根目录 `LICENSE`。
- 内置 ARS：CC-BY-NC-4.0，© 2026 Cheng-I Wu，原仓库 https://github.com/Imbad0202/academic-research-skills；原始许可证、NOTICE 与 README 见 `third_party/academic-research-skills/`。
- ARS 文件按原样内置，仅调整了目录位置以便打包；非商业使用，请遵守原仓库条款。

## 说明

- `wfh-status` 已并入 `wfh-ask` 的 status 模式；当前有 6 个 wfh 执行入口。
- `wfh-research` 是共享包，不是执行入口。
- `wfh-implement-spec` 的自动开新会话依赖 Claude Desktop 的 session 工具；不可用时回退为手动复制提示词，再用 `/wfh-implement-spec --close <ID>` 验收。
- 本仓库不包含任何研究数据。
