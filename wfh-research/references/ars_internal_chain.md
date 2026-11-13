# ARS 内部链：Passport、回执与额外门禁

> 只在来源为 ars-internal 时读取；外部作者材料走 [交接协议](ars_handoff_protocol.md) §1–§3。
> 保留收到的原始 Passport、回执及 companion 的身份和字节；按当前 ARS 原文重放。

---

## 1. 身份与边界

- 不把 wfh 改称 deep-research，不把没有验证的状态写成 VERIFIED。
- 来源为 deep-research 生成或明确恢复 ARS 内部跨阶段 handoff 时，保留 Schema 9 Material Passport、current #672 链的 builder 回执；provided 时保留 companion。
- 来源不清、混有既有 Passport/回执/阶段记录时，先查明来源与用途；不把内部链改名为外部材料以逃避校验。

## 2. 指定工具

```text
python -B <ARS_ROOT>/scripts/build_cross_document_consistency_advisory.py build-preregistration-artifact
  --status <provided|not_provided|access_failed|retrieval_failed>
  --artifact-id <显式标识>
  --declared-at <调用方显式提供的 RFC3339 时间>
  --output <任务允许的输出路径>
```

运行前读当前工具 `--help` 与协议。`provided` 还需 `--companion`、`--relative-path`；真实来源使用 `author_provided_completed_preregistration`。builder 校验 UTF-8、拒绝空白指导模板并计算字节/内容绑定。不可用状态禁止 companion/path，provenance 为 `not_provided`；缺少文件本身不授权选择该状态。`synthetic_fixture` 在 ARS 原文中保留给仓库测试，不擅自作为真实交接来源。

## 3. 责任

- wfh-spec 本身只写 Brief，不运行 builder、不创建 Passport。
- 后续执行方仅在合法的内部链/作者明确声明且任务授权时调用指定 builder；作者状态或声明时间未提供时保留未决并停下。
- builder 的成功只证明契约构造成功，不证明研究有效、已预注册、已获作者确认或已通过完整 ARS 门禁。

## 4. 被 ARS 拒绝时

明确外部入口仍被 ARS 拒绝时，记录实际缺项与 `rejected_by: ars-intake`，保留 `ars_invoked: true`，停止当前任务。可报告来源条件存在歧义；不静默转入口、生成缺失声明或要求忽略校验。
