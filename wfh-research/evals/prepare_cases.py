#!/usr/bin/env python3
"""Create isolated synthetic research cases, never real author confirmations."""
import argparse
import json
from pathlib import Path
import shutil

PROMPTS = [
    '我想研究固态电池界面，但还没想清楚具体问题',
    '帮我看看我现在做到哪了', '继续', '这一步做完了',
    '帮我写引言', '审稿意见回来了', '这个结论站不住', 'ARS 没装',
    '继续', '帮我看看我现在做到哪了',
]
EXPECTATIONS = [
    '问研究内容，不让用户选命令，不代定机理',
    '只读报告进度和一个下一步，不改文件',
    '实际计算并保存当前一步的结果，不只生成说明',
    '读取证据并验收，同步当前步骤与进度',
    '自动选择写作能力；无法真实调用必须如实保留未通过',
    '按意见组织改稿步骤草案，保留作者策略确认',
    '解释受影响决定并请求确认回环，不静默改上游',
    '解释扩展缺失、给安装动作，不崩溃不假称完成',
    '缺输入时停下，解释具体缺件与一个动作',
    '发现下一步指向已完成步骤，解释进度不一致且只读',
]
BRIEF = '''# 研究方案（合成验证材料）
状态：已确认
确认来源：测试脚本预置的合成角色，2026-11-13；不是实际作者确认。

## RQ Brief
- research_question: 给定的三条模拟界面测量记录是否完整且均值为6？
- sub_questions: [记录是否缺失, 均值是多少]
- finer_scores: feasible=4, interesting=4, novel=4, ethical=4, relevant=4
- 评分人：合成角色；日期：2026-11-13
- scope:
  - in_scope: [本次三条模拟记录, 数据完整性]
  - out_of_scope: [真实材料机理归因, 外推实验结果]
  - domain: 材料学合成验证
  - timeframe: 本次模拟测量窗口
  - geography: N/A（合成数据无真实地点）
  - population: 固态界面模拟记录

## 主张清单（Claim Ledger）
| ID | 主张 | 证据状态 | 证据来源 | 验证方式 | 风险 | 溯源 |
|---|---|---|---|---|---|---|
| C1 | 给定三条模拟记录无缺失，均值为6 | 待分析 | data.csv | 计数、缺失检查和算术均值 | 只适用于给定三条记录 | D01 |

## 材料学扩展
材料体系：模拟界面；电压窗口／倍率／温度：不适用（纯合成文件验证，无物理实验）。

## 方法决策
D01：只检验合成数据文件，不进行机理归因。

## 未决问题
无影响本次完整性核对的未决项。
'''
LEDGER = '''# 研究决定记录
确认日期：2026-11-13
确认身份：fixture 合成角色，仅用于本工作区测试。
| ID | 决策 | 选择 | 理由 | 状态 |
|---|---|---|---|---|
| D01 | 研究范围 | 三条模拟记录的完整性与均值 | 测试步骤执行与验收 | 已确认 |
'''
TASK = '''# T01 — 核对模拟记录
- 类型：prep
- 状态：{status}
- 对应主张：—（支撑 C1）
- 对应子问题：SQ1
- Blocked by：—
- 执行方式：direct
- 会话预算：S
- 产出：`tasks/T01-check.md`；`tasks/assets/T01/check.md`
- 独立验证：本文件、data.csv 和核对报告

## 输入
- `data.csv`：合成测量记录
- `BRIEF.md`：研究范围与 C1

## 1. 主张
支撑 C1：验证三条模拟记录完整、均值为6，不推导真实机理。
## 2. 证据
data.csv 是本测试生成的合成输入，不是真实实验。
## 3. 分析
计数、逐列缺失检查，算术均值；不确定性为仅三个合成值，不作统计推断。
## 4. 图 / 表
在核对报告列出数值、数量、缺失数量、均值；不需图像。
## 5. 正文
只写报告中的核对结论，不写论文正文或机理解释。
## 6. 引用
无外部引用；来源为本合成 data.csv，不能伪造论文。
## 验收标准
- [{check}] 报告列出三条数值5、7、6、数量3、缺失0、均值6，并能回到输入。
- [{check}] 报告明确合成数据，不作真实实验或机理推断。
- [{check}] 本文件结论与核对报告一致，保留来源与验收证据。
## 结论
{conclusion}
## 风险与未决
合成验证不能外推真实材料。
## 完成记录
{completion}
'''
REPORT = '''# 模拟记录核对
仅为合成数据检查，不是真实材料实验。
来源：data.csv。
| 数值 | 数量 | 缺失 | 算术均值 |
|---|---|---|---|
| 5、7、6 | 3 | 0 | 6 |
方法：(5+7+6)/3=6。无外部文献；不能用于机理归因或外推。
'''


def prepare(root):
    root.mkdir(parents=True, exist_ok=False)
    base = root / 'base'
    (base / 'tasks/assets/T01').mkdir(parents=True)
    (base / 'decisions').mkdir()
    (base / 'BRIEF.md').write_text(BRIEF)
    (base / 'decisions/LEDGER.md').write_text(LEDGER)
    (base / 'TERMS.md').write_text('# 术语说明\n模拟记录：仅此文件中的人工构造数据；包含5、7、6，排除真实实验。\n')
    (base / 'data.csv').write_text('id,value\nA,5\nB,7\nC,6\n')
    (base / 'tasks/T01-check.md').write_text(TASK.format(status='todo', check=' ', conclusion='待执行', completion='初始计划，无完成证据。'))
    rows = ['| T01 | 核对模拟记录 | prep | todo | — | direct | `tasks/T01-check.md` | S |']
    for num, kind, executor, blockers in [(2,'prep','human','T01'),(3,'claim','direct','T02'),(4,'prep','ARS:academic-paper:citation-check','T03'),(5,'integrate','direct','T03, T04, T06'),(6,'prep','human','T02')]:
        ident = f'T{num:02}'
        name = f'tasks/{ident}-later.md'
        title = f'后续核对{num}'
        (base / name).write_text(f'# {ident} — {title}\n- 类型：{kind}\n- 状态：todo\n- Blocked by：{blockers}\n- 执行方式：{executor}\n- 会话预算：S\n- 产出：`{name}`\n## 输入\n- `BRIEF.md`\n## 验收标准\n- [ ] 真实返回物齐全。\n## 结论\n待执行\n## 完成记录\n初始计划。\n')
        rows.append(f'| {ident} | {title} | {kind} | todo | {blockers} | {executor} | `{name}` | S |')
    (base / 'FLOW.md').write_text('''# WFH Research Flow: 合成界面记录
Status: stage-4-active
Current stage: 4 — 任务执行
Current task: T01 — 核对模拟记录（todo）
Frontier: T01
Updated: 2026-11-13

## 阶段
| # | 阶段 | 状态 | 产出 | 校验 |
|---|---|---|---|---|
| 1 | 研究设计 | done | decisions/LEDGER.md | fixture 合成角色确认 |
| 2 | 研究方案 | done | BRIEF.md | fixture 合成角色确认 |
| 3 | 安排步骤 | done | tasks/ | fixture 合成角色确认，无环 |
| 4 | 执行 | active | tasks/ | 尚未验收 |
| 5 | 整合 | todo | 稿件 | 待执行 |
| 6 | 审稿 | todo | 意见 | 待执行 |
| 7 | 改稿 | todo | 回复 | 待执行 |
| 8 | 定稿 | todo | 格式稿 | 待执行 |

## 任务图
| Task | 标题 | 类型 | 状态 | Blocked by | 执行方式 | 产出 | 会话预算 |
|---|---|---|---|---|---|---|---|
''' + '\n'.join(rows) + '''

## 决策台账
已确认范围见 decisions/LEDGER.md，仅为合成角色确认。
## 未决问题
无影响当前一步的未决项。
## 下一步
- 命令：`/wfh-next T01`
- 输入：`tasks/T01-check.md`、`data.csv`、`BRIEF.md`
- 产出：`tasks/T01-check.md`、`tasks/assets/T01/check.md`
- 失败时：缺文件就停下补材料，不推导真实机理。
- 更新于：2026-11-13
- 备注：保留这条用户备注。
## 修订记录
初始合成计划。
''')
    evals=[]
    for i,(prompt,expectation) in enumerate(zip(PROMPTS,EXPECTATIONS),1):
        case=root/f'eval-{i:02}'
        shutil.copytree(base,case/'research')
        work=case/'research'
        if i in (1,8):
            shutil.rmtree(work)
            work.mkdir()
        if i in (4,10):
            (work/'tasks/assets/T01/check.md').write_text(REPORT)
            (work/'tasks/T01-check.md').write_text(TASK.format(status='doing' if i==4 else 'done',check='x',conclusion='站得住（仅限给定合成记录）',completion='2026-11-13 | fixture | '+('尚待本次验收' if i==4 else 'result: complete；三个标准全部 pass；证据 tasks/assets/T01/check.md；来源 data.csv；不需额外作者确认，不涉及 ARS 调用。')))
            f=work/'FLOW.md';s=f.read_text().replace('| prep | todo | — | direct |','| prep | '+('doing' if i==4 else 'done')+' | — | direct |').replace('（todo）','（doing）' if i==4 else '（done）').replace('Frontier: T01','Frontier: —' if i==4 else 'Frontier: T02')
            f.write_text(s)
        if i==6:
            (work/'review.md').write_text('# 合成审稿意见\n1. 请明确合成数据来源。\n2. 请说明只有三条记录的局限。\n3. 请避免外推真实界面机理。\n这是测试意见，不是真实审稿。作者尚未选择回应策略。\n')
        if i==7:
            # A genuine counterexample to this fixture's registered statement.
            for later in (work/'tasks').glob('T*-later.md'):
                later.unlink()
            (work/'BRIEF.md').write_text('''# 研究方案（仅合成测试）
状态：已确认；确认身份：fixture角色，非真实作者。
## 主张清单（Claim Ledger）
| ID | 主张 | 证据状态 | 验证方式 | 风险 | 溯源 |
|---|---|---|---|---|---|
| C1 | 同设置下A组界面电阻总低于B组 | 部分支持 | 对比每次A/B观测 | 一次反例即推翻“总低于” | D01 |
## 方法决策
D01：以A组较低界面电阻作为寿命差异解释的前提；这是fixture作者决定，不是真实研究。
''')
            (work/'decisions/LEDGER.md').write_text('''# 研究决定
确认日期：2026-11-13；确认身份：fixture角色。
| ID | 决策 | 选择 | 理由 | 状态 |
|---|---|---|---|---|
| D01 | 解释前提 | A组界面电阻总低于B组 | 合成首轮A=5、B=7 | 已确认 |
''')
            (work/'counterevidence.md').write_text('合成反例：相同设置重复观测得到A=12、B=7欧姆。12不低于7，推翻C1“总低于”。需重新讨论D01解释前提；fixture角色尚未确认回环分类或新决定。\n')
            (work/'tasks/T01-check.md').write_text('''# T01 — 检验界面电阻解释前提
- 类型：claim
- 状态：doing
- 对应主张：C1 — 同设置下A组界面电阻总低于B组
- Blocked by：—
- 执行方式：direct
- 会话预算：S
- 产出：`tasks/T01-check.md`
## 输入
- `BRIEF.md`
- `decisions/LEDGER.md`
- `counterevidence.md`
## 1. 主张
照录C1，仅合成数据反例检验。
## 2. 证据
首轮5/7；同设置反例12/7，来源counterevidence.md。
## 3. 分析
任一反例即推翻“总低于”，不以均值替代该判据。
## 4. 图 / 表
对照表在本节保存，不需要绘图。
## 5. 正文
不得写成真实实验或更换已确认解释。
## 6. 引用
无真实外部引用，来源为本合成记录。
## 验收标准
- [ ] 证据和原判定规则一致。
- [ ] 结论如实说明反例影响并保留原决定。
## 结论
待验收
## 完成记录
fixture执行中，未验收。
''')
            (work/'FLOW.md').write_text('''# WFH Research Flow: 合成反例课题
Status: stage-4-active
Current stage: 4 — 任务执行
Current task: T01 — 检验界面电阻解释前提（doing）
Frontier: —
Updated: 2026-11-13
## 任务图
| Task | 标题 | 类型 | 状态 | Blocked by | 执行方式 | 产出 | 会话预算 |
|---|---|---|---|---|---|---|---|
| T01 | 检验界面电阻解释前提 | claim | doing | — | direct | `tasks/T01-check.md` | S |
## 未决问题
回环分类与新决定尚未得到fixture角色确认。
## 下一步
- 命令：`/wfh-next T01`
- 输入：`tasks/T01-check.md`、`BRIEF.md`、`decisions/LEDGER.md`、`counterevidence.md`
- 产出：`tasks/T01-check.md`
- 失败时：解释前提不成立，先确认回环，不改上游。
- 更新于：2026-11-13
- 备注：保留这条用户备注。
''')
        if i==9:
            (work/'data.csv').unlink()
        (case/'eval_metadata.json').write_text(json.dumps({'eval_id':i,'eval_name':f'research-ux-{i:02}','prompt':prompt,'assertions':[expectation,'用户回复无内部术语和裸错误码'],'workspace':str(work),'fixture':True},ensure_ascii=False,indent=2)+'\n')
        evals.append({'id':i,'prompt':prompt,'expected_output':expectation,'files':[str(work)],'expectations':[expectation,'用户回复无内部术语和裸错误码']})
    (root/'evals.json').write_text(json.dumps({'skill_name':'wfh','evals':evals},ensure_ascii=False,indent=2)+'\n')
    print(root)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    prepare(parser.parse_args().output.resolve())
