# wfh-science-skills

科研工作流 skills for Claude Code：用 wfh 整理研究决策、Brief 与任务状态，用 ARS 做检索、写作、审稿与改稿。

## 包含什么

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
| `vendor/academic-research-skills/` | ARS 3.24.2 快照，方便一次安装（CC-BY-NC-4.0） |

## 仓库结构

```text
wfh-science-skills/
├── wfh-*/                         # 六个 wfh 入口 + wfh-research + wfh-implement-spec
└── vendor/
    └── academic-research-skills/  # ARS 3.24.2 快照（CC-BY-NC-4.0）
```

## 安装

### 1. 安装 ARS（生产层）

wfh 负责决策、Brief、任务图和验收；检索、写作、审稿、修订、格式转换由 ARS 完成。ARS 已随仓库放在 `vendor/academic-research-skills/`，可以一次安装；也可以从官方仓库安装最新版。

**方式 A：用仓库内置的 ARS（一次安装）**

在仓库根目录运行：

```text
/plugin marketplace add ./vendor/academic-research-skills
/plugin install academic-research-skills
```

**方式 B：从官方仓库安装（推荐，便于更新）**

```text
/plugin marketplace add Imbad0202/academic-research-skills
/plugin install academic-research-skills
```

官方仓库：https://github.com/Imbad0202/academic-research-skills

`vendor/` 里是 ARS 3.24.2 的快照；官方仓库更新后，建议用方式 B 或重新拉取本仓库。

### 2. 安装 wfh skills（本仓库）

把这些目录复制到项目的 `.claude/skills/`：

```bash
mkdir -p .claude/skills
cp -R wfh-* .claude/skills/
```

也可以复制到用户级 `~/.claude/skills/`，让所有项目可用。

## 快速开始

```text
/wfh-ask 我该用哪个技能？
/wfh-grill 我想研究……
/wfh-spec
/wfh-tickets
/wfh-ask 这个课题现在做到哪了？
/wfh-next T01
/wfh-close T01
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

- **Claude Code / Claude Desktop**：需要支持 skills 的版本。
- **ARS（可选，但强烈建议）**：`academic-research-skills` 插件，提供检索、写作、审稿、修订、格式转换。安装方式见上。
- **Python 3**：仅 `wfh-research/scripts/refresh_index.py` 需要，用于生成 / 校验路由索引。

## 没有 ARS 时能用什么

| 能力 | 没有 ARS | 有 ARS |
|---|---|---|
| `wfh-grill` / `wfh-spec` / `wfh-tickets` / `wfh-ask` / `wfh-next` / `wfh-close` | ✅ | ✅ |
| `direct` 任务（你自己分析） | ✅ | ✅ |
| `human` 任务（实验 / 仪器 / 作者裁决） | ✅ | ✅ |
| `ARS:` 任务（检索 / 写作 / 审稿 / 改稿 / 格式） | ❌ 保持 blocked | ✅ |

## 第三方依赖与许可

- **wfh skills**（本仓库作者原创）：MIT，见根目录 `LICENSE`。
- **ARS**（`vendor/academic-research-skills/`）：CC-BY-NC-4.0，作者 Cheng-I Wu，原仓库 https://github.com/Imbad0202/academic-research-skills。非商业使用；请遵守原仓库条款。
- 两层许可分开：根目录 MIT 只覆盖 wfh skills，不覆盖 `vendor/` 里的 ARS。
- 本仓库不包含任何研究数据。

## 说明

- `wfh-status` 已并入 `wfh-ask` 的 status 模式；当前有 6 个 wfh 执行入口。
- `wfh-research` 是共享包，不是第八个执行入口。
- `wfh-implement-spec` 的自动开新会话依赖 Claude Desktop 的 session 工具；不可用时回退为手动复制提示词，再用 `/wfh-implement-spec --close <ID>` 验收。
- 本仓库包含 wfh skills 和 ARS 快照，不包含任何研究数据。
