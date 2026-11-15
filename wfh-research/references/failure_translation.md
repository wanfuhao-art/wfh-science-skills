# 失败翻译表

只在失败时读取；默认回复仍按 [研究者界面](user_output_protocol.md) 说明缺口与当前动作，研究裁决所需依据不受固定句数限制。内部标记只作记录，用户回复不出现标记、错误码或原始技术提示词。

| 内部分类或标记 | 用户说明与一个动作 |
|---|---|
| ARS_NOT_AVAILABLE（安装根未确认） | 还无法确认本次研究扩展的位置，尚未读取它的实际要求。请提供宿主显示的插件根或技能基目录。 |
| ARS_NOT_AVAILABLE（已确认未安装） | 负责检索和写作的扩展尚未安装。请按安装说明装好后对我说“继续”。 |
| ARS_NOT_AVAILABLE（原因未明） | 本次无法使用负责检索和写作的扩展，尚不能确认原因。请让我核对宿主显示的扩展状态。 |
| SKILL_NOT_LOADED | 本会话没有提供所需扩展入口，读取源码不能启动它。请在已启用该扩展的会话继续。 |
| HANDOFF_INCOMPLETE, BRIEF_INCOMPLETE | 研究材料还缺少{中文必需信息}。请补充{一个当前缺项}。 |
| BRIEF_NOT_FOUND | 还没有找到这个课题的研究方案。请让我先整理已确认的研究内容。 |
| BRIEF_NOT_CONFIRMED, GRILL_NOT_CONFIRMED | 研究方案／研究决定还没有得到你的确认。请确认{中文摘要中的待确认内容}。 |
| FLOW_NOT_FOUND | 这里还没有找到课题的进度记录。请告诉我课题名称或已有记录的位置。 |
| TASK_NOT_FOUND, TASK_ID_INVALID, TASK_INDEX_INVALID | 步骤记录缺失或编号对不上，暂时不能继续。请让我核对{具体中文标题}对应的记录。 |
| TASK_DEPENDENCY_INVALID, TASK_GRAPH_CYCLE | 有些步骤的先后顺序无法成立。请让我列出需要调整的顺序供你确认。 |
| FLOW_TASK_CONFLICT, FLOW_CACHE_STALE, NEXT_STEP_DRIFT | 进度文件和步骤记录对不上。请让我先核对差异并在你确认后同步进度。 |
| INPUT_DECLARATION_INCOMPLETE | 这一步还没有列全需要核对的前序证据。请让我先补齐步骤安排中的证据位置供你确认。 |
| INPUT_MISSING, EVIDENCE_GAP | 这一步还缺{具体材料或外部返回物}。请提供{一个明确返回物或位置}。 |
| TASK_DONE_UNVERIFIED | 已记为完成的步骤缺少足够的验收证据。请让我列出缺口供你确认重新核对的范围。 |
| TASK_BLOCKED | 这一步还需要先完成{中文步骤或条件}。请先完成{一个实际前置动作}。 |
| TASK_HUMAN | 这一步需要你完成{实验或人工判断}。请完成后提供{具体返回物}。 |
| TASK_CLOSED | 这一步已通过验收或已取消。请确认是否要重新开展这一步。 |
| TASK_TOO_BIG | 这一步包含的工作太多，难以一次核对清楚。请确认我提出的拆分安排。 |
| CLAIM_UNTRACEABLE | 这条说法还找不到来源。请提供它依据的研究决定或材料。 |
| CLAIM_UNVERIFIABLE | 这条说法还没有可操作的验证方法。请说明什么观察结果能够检验它。 |
| SUBQ_UNMAPPED, UNRESOLVED_UNMAPPED | 还有研究问题或未决信息没有对应的处理步骤。请确认我列出的对应关系。 |
| NO_TRACER_BULLET | 目前还没有材料齐全、能先走通证据链的小步骤。请先补齐{具体前置材料}。 |
| REVIEW_NOT_FOUND | 还没有收到审稿意见原文。请提供审稿信或告诉我它的位置。 |
| REVIEW_NOT_READY | 审稿阶段的材料或状态还没有确认。请让我先核对已有审稿意见的来源和范围。 |
| CLAIM_REFUTED, DESIGN_INVALID, REOPEN_REQUIRED | 先按原验收标准判断交付：若检验本身已完成，说“本次检验已完成，但证据不支持{原说法或设计}”；若交付仍有缺口，说“原交付标准尚未满足，缺少{具体内容}”。需要改变研究决定时另请作者确认重新讨论{受影响决定}；不能把否定结果直接翻译成验收失败。 |
| EXECUTION_FAILURE, SESSION_INCOMPLETE | 本次工作没有完成或结果仍需纠正。请让我检查{具体未完成部分}后重新开展这一步。 |
| SESSION_START_FAILED | 没能开启独立会话。可以改用新的执行子代理完成这一步，或留在当前会话的输入范围内继续；不会假称已经在独立会话中运行。 |
| STATE_CHANGED, STATE_SYNC_INCOMPLETE | 记录刚被其他操作改动，或只更新了一部分。请让我重新核对记录后再请你确认同步范围。 |
| INDEX_STALE, INDEX_INVALID | 能力目录已过期或有不一致的信息。请让我核对实际可用的入口。 |

未知失败：第一句说“本次{研究动作}没有完成，目前无法确认结果”，第二句说“请让我先检查本次失败记录”。保留原始失败来源与状态，不假称重试或换入口已经解决。
