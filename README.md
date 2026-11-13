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

## 安装

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

## 依赖

- **ARS（可选）**：`academic-research-skills` 插件，用于检索、写作、审稿、修订、格式转换。没有 ARS 时，wfh 的决策与任务管理仍可用，但 `ARS:` 任务会保持 blocked。
- **Python 3**：仅 `wfh-research/scripts/refresh_index.py` 需要，用于生成 / 校验路由索引。

## 说明

- `wfh-status` 已并入 `wfh-ask` 的 status 模式；当前有 6 个 wfh 执行入口。
- `wfh-research` 是共享包，不是第八个执行入口。
- `wfh-implement-spec` 的自动开新会话依赖 Claude Desktop 的 session 工具；不可用时回退为手动复制提示词，再用 `/wfh-implement-spec --close <ID>` 验收。
- 本仓库只包含 skills，不包含任何研究数据。
