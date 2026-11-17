# wfh + ARS 配套安装指南

[返回首页](../README.md)

完整科研流程使用两个独立插件：**wfh-science-skills 负责研究设计、步骤与进度；academic-research-skills（ARS）负责检索、写作、审稿与核验。请分别安装并启用。** 安装 wfh 不会自动安装 ARS，也不需要安装作为设计参考的 Matt skills。

| 插件 | 官方仓库 | 插件标识 |
|---|---|---|
| wfh | [wanfuhao-art/wfh-science-skills](https://github.com/wanfuhao-art/wfh-science-skills) | `wfh-science-skills@wfh-science-skills` |
| ARS | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | `academic-research-skills@academic-research-skills` |

## 1. 选择使用环境

推荐在最新版 Claude Code（终端或 IDE 集成），或 Claude Desktop 的 **Code 标签页**中使用配套流程。先确认宿主本身可以正常对话、本机已安装 Git 且能够访问 GitHub；网络依赖代理时先开启代理。

wfh 日常使用无需安装 Python，也没有 pip 或 npm 依赖安装步骤。ARS 的 Word、PDF 导出等功能可能需要 Pandoc、排版编译器或其他可选工具，按其 [官方安装指南](https://github.com/Imbad0202/academic-research-skills/blob/main/docs/SETUP.md) 配置，不必为了开始使用而先装齐全部工具。

Claude Desktop 的普通聊天、claude.ai 与 Code 标签页是不同运行环境。ARS 官方另提供账户市场等安装方式，但普通聊天中的 hooks、插件代理和工具支持不同；本项目的任务执行隔离与配套流程尚未在这些渠道完成验证。不要把在一个渠道安装完成视为其他渠道也已加载。

## 2. 安装两个插件

### 方法 A：在会话中安装（推荐）

在 Claude Code 或 Desktop Code 标签页的**会话输入框**中，按 [首页四条安装命令](../README.md#安装先装两个插件再从-wfh-开始) 逐条发送。它们是 `/plugin` 命令，不是系统终端命令。

### 方法 B：在系统终端安装

如果已经安装 Claude Code CLI，也可以在系统终端逐条运行以下等价命令。默认使用用户范围，供该用户的项目使用。

```bash
claude plugin marketplace add wanfuhao-art/wfh-science-skills
```

```bash
claude plugin install wfh-science-skills@wfh-science-skills
```

```bash
claude plugin marketplace add Imbad0202/academic-research-skills
```

```bash
claude plugin install academic-research-skills@academic-research-skills
```

支持 `--marketplace` 的较新 CLI 还可以将每个插件的添加市场、安装合并为一条命令。这是上面方法的替代方式，无需重复执行：

```bash
claude plugin install wfh-science-skills --marketplace wanfuhao-art/wfh-science-skills
```

```bash
claude plugin install academic-research-skills --marketplace Imbad0202/academic-research-skills
```

### 私有仓库与源码下载

如果 wfh 仓库为私有，安装者必须先获得访问权限，并让本机 Git 使用自己的 GitHub 认证。未经授权的人无法通过安装命令、Release 或仓库链接获取私有内容。仓库公开后，这项私有访问授权不再需要。

下载 ZIP 或克隆源码只取得了文件，不代表宿主已安装、启用或注册技能。本地安装时可以把添加市场命令中的 GitHub 仓库名换成解压后仓库的绝对路径；ARS 仍需单独安装。

## 3. 重新打开会话并检查入口

安装后重新打开会话。通过 `/plugin` 管理界面确认两个插件已安装并启用，再输入 `/` 查看入口列表，检查是否有 `wfh-science-skills:wfh` 以及 ARS 的入口（例如 `ars-plan`；名称以实际版本为准）。

可以用完整入口做一次只读检查：

```text
/wfh-science-skills:wfh 请检查 wfh 和 ARS 是否已安装、启用并在当前会话中可调用，说明各自用途；先不要创建文件或执行研究。无法确认的项目请明确说明。
```

检查插件列表、查看源码和读取技能文档都不等于实际科研调用成功。真正的检索、写作和核验需要在具体任务中检查调用与交付结果。

本文安装标识已与两方插件清单核对。wfh 的既有源码兼容核查基线为 **ARS 3.24.2**；2026-11-17 查看 ARS 官方仓库时，其清单版本为 **3.24.3**。默认安装跟随各仓库市场配置，不固定在上述版本；此处不表示已对 3.24.3 完成真实配套运行验证。模式、输入要求和必要确认以实际加载版本的原文为准。既有验证范围见 [3.2.2 发布说明](RELEASE-3.2.2.md)。

## 4. 从 wfh 开始使用

安装好后，日常从 wfh 描述研究目标，无需先学习所有高级入口和 ARS 模式。简写 `/wfh` 无法解析时，使用 `/wfh-science-skills:wfh`。

讨论研究方向：

```text
/wfh-science-skills:wfh 我想研究固态电池界面，请比较几个有依据的研究方向，先讨论，不生成方案。
```

讨论后整理研究方案：

```text
/wfh-science-skills:wfh 帮我问清研究设计，确认后生成研究方案。
```

配合 ARS 完成具体研究工作：

```text
/wfh-science-skills:wfh 请配合 ARS 检索这个研究问题的文献，比较主要解释及各自的证据，交付一份带来源的综述。
```

长期课题：

```text
/wfh-science-skills:wfh 带我把这个研究想法推进到论文初稿，先确认研究设计，再安排步骤；缺材料或需要我作研究决定时告诉我。
```

独立小请求无需先建立完整课题。只安装 wfh 仍可做设计讨论、方案整理和进度管理；需要检索、写作、审稿与引用核验时，补装并启用 ARS。科研决定、原始数据与必要确认仍由研究者提供。

## 5. 更新与卸载

在系统终端先刷新各自市场，再更新插件；完成后重新打开会话：

```bash
claude plugin marketplace update wfh-science-skills
```

```bash
claude plugin update wfh-science-skills@wfh-science-skills
```

```bash
claude plugin marketplace update academic-research-skills
```

```bash
claude plugin update academic-research-skills@academic-research-skills
```

不再使用时，可在 `/plugin` 管理界面分别禁用、卸载两个插件，或在系统终端运行：

```bash
claude plugin uninstall wfh-science-skills@wfh-science-skills
```

```bash
claude plugin uninstall academic-research-skills@academic-research-skills
```

插件卸载与研究资料清理是两件事；如需清理课题，请先自行备份研究方案、进度、研究决定、步骤记录及实际产物。

## 常见问题

| 现象 | 处理方式 |
|---|---|
| `Repository not found`、403 或认证失败 | 先用自己的 GitHub 账号确认能否访问仓库；私有仓库联系维护者授权，并检查本机 Git 认证。组织策略也可能限制访问。 |
| 无法连接 GitHub，或代理端口连接失败 | 检查网络；本机 Git 配了代理时，确认对应代理软件已启动。 |
| 没有 `/plugin` 或命令不识别 | 确认使用的是 Claude Code / Desktop Code 标签页，并更新宿主；普通聊天请对照相应平台的安装文档。 |
| 已安装但找不到 `/wfh` | 确认插件已启用，重新打开会话，并尝试完整入口 `/wfh-science-skills:wfh`。 |
| wfh 可以用，但检索或写作提示缺少 ARS | 单独安装、启用 `academic-research-skills`，重新打开会话，确认 ARS 入口已注册。 |
| 安装了 ARS，导出 Word / PDF 失败 | 按 ARS 实际输出分支检查 Pandoc、排版编译器等可选工具；Markdown 输出不要求这些导出工具。 |
| 更新后仍是旧版本 | 确认刷新了正确市场、更新了正确范围的插件，并重新打开会话；不同宿主、用户或安装范围可能各自保留安装。 |
