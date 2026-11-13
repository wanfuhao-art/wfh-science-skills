# wfh-science-skills

一个 Claude Code 插件：wfh 科研工作流。负责决策收敛、Brief、任务图、状态与验收；检索、写作、审稿、修订与格式转换由外部 **ARS** 插件完成。

## 包含什么

### wfh 工作流（8 个 skills）

| 目录 | 作用 |
|---|---|
| `wfh-ask/` | 科研入口咨询 + 课题状态：该用哪个技能，或课题现在做到哪 |
| `wfh-grill/` | 按轮盘问，收敛研究决策，产出 `TERMS.md` / MDR / 决策台账 |
| `wfh-spec/` | 把已确认台账压成 `BRIEF.md` |
| `wfh-tickets/` | 把 Brief 切成可验证任务图；`revision` 模式把审稿意见切成改稿任务 |
| `wfh-next/` | 为单条任务生成新会话启动 / 恢复提示词 |
| `wfh-close/` | 逐条证据验收，更新任务与 `FLOW.md`；claim 失败时输出回环包 |
| `wfh-research/` | 共享协议、模板、索引生成器（不是执行入口） |
| `wfh-implement-spec/` | 可选编排层：生成提示词 → 开新会话 → 自动验收 |

### 外部依赖：ARS

本仓库**不包含** ARS。使用前先安装：

```text
/plugin marketplace add https://github.com/Imbad0202/academic-research-skills.git
/plugin install academic-research-skills
```

- 测试版本：ARS 3.24.2。
- wfh 只负责“什么时候、拿什么输入、调哪个 ARS 模式”；ARS 的 35 个 mode 与 `/ars-*` 命令保持原样。
- ARS 缺失或版本不符时，`wfh-ask` 与 `wfh-next` 会报 `ARS_NOT_AVAILABLE`，不静默降级。

## 仓库结构

```text
wfh-science-skills/
├── .claude-plugin/        # plugin.json + marketplace.json
├── wfh-*/                 # 8 个 wfh skills
└── README.md
```

## 安装

```text
/plugin marketplace add <本仓库路径或 GitHub 仓库>
/plugin install wfh-science-skills
```

- 本地文件夹：`<本仓库路径或 GitHub 仓库>` 换成仓库绝对路径。
- GitHub：换成 `wanfuhao-art/wfh-science-skills`。

## 快速开始

```text
/wfh-ask 我该用哪个技能？
/wfh-grill 我想研究……
/wfh-spec
/wfh-tickets
/wfh-ask 这个课题现在做到哪了？
```

## 工作流

```text
/wfh-grill → /wfh-spec → /wfh-tickets
                              │
              ┌───────────────┴────────────────┐
              │  每条任务：                     │
              │  /wfh-ask 看 frontier 与下一步   │
              │  /wfh-next 生成启动提示词        │
              │  新会话执行（ARS / direct / human）│
              │  /wfh-close 验收并推进           │
              └───────────────┬────────────────┘
                              │
        终端 integrate 任务 → 阶段 6 审稿（ARS）
                              │
        /wfh-tickets revision → 阶段 7 改稿任务
                              │
        阶段 8 定稿（ARS format-convert / disclosure）
```

`FLOW.md` 的「下一步」节是唯一持久位置，记录 `命令 / 输入 / 产出 / 失败时`；每个技能收尾时更新它，`wfh-ask` 负责检查漂移。

## 前置依赖

- **Claude Code / Claude Desktop**：需要支持插件与 skills 的版本。
- **ARS 插件**：见上。
- **Python 3**：仅 `wfh-research/scripts/refresh_index.py` 需要，用于生成 / 校验路由索引。

## 许可

- 本插件：CC-BY-NC-4.0，© wanfuhao-art，见根目录 `LICENSE`。
- 不包含 ARS 代码或其它第三方代码。
- 盘问与任务图设计借鉴了 `mattpocock-skills` 的 grilling / to-spec / to-tickets 思路，未包含其代码。

## 说明

- `wfh-status` 已并入 `wfh-ask` 的 status 模式；当前有 7 个 wfh 执行入口。
- `wfh-research` 是共享包，不是执行入口。
- `wfh-implement-spec` 的自动开新会话依赖 Claude Desktop 的 session 工具；不可用时回退为手动复制提示词，再用 `/wfh-implement-spec --close <ID>` 验收。
- 本仓库不包含任何研究数据。
