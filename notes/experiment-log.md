# 实验日志

尚未执行。每个任务追加 Purpose / Observation / Hypothesis / Decision。
只记录合成数据观察，避免把工作流演示当作科研证据。

## 2026-09-27 — EXP-001 revision 1 / EXP-001-R01

- Purpose：比较窗口 1、3、7 的中心移动平均对合成含噪信号重建误差及峰值衰减的影响，验证实验交接流程。
- Observation：直接读取 `results/EXP-001/EXP-001-R01/metrics.csv` 和 `results/EXP-001/EXP-001-R01/summary.csv`，窗口 1、3、7 的平均 RMSE 分别为 0.346744、0.211492、0.260907，平均峰值衰减分别为 -0.013528、0.078721、0.288393。仅在本次三个固定 seed 中，窗口 3 的平均 RMSE 最低，窗口 7 的平均峰值衰减最大；负衰减表示超调。
- Hypothesis：本次任务未提出或检验新增假说，不将上述有限观察扩展为普适结论。
- Decision：独立命令 `python scripts/demo.py validate --run-id EXP-001-R01` 退出码为 0，原始信号、九个组合、指标、汇总及哈希校验通过。结果已提交为 `d7a09827ec833ef3aa23186402330fd0a1c55db0`；manifest 代码提交为 `afe1ee4c28f0f2826324f885b0441a7f83ab6050`、dirty 为 false。完成 EXP-001，交由网页 Chat 阅读真实证据后创建 REPORT-002，不重复运行本 run_id。
- 限制：合成数据工作流演示，n=3；样本标准差不是置信区间，未做显著性检验，不支持真实数据效果或真实科研发现。

## 2026-09-27 — REPORT-002 revision 1 / evidence EXP-001-R01

- Purpose：基于指定 evidence commit `d7a09827ec833ef3aa23186402330fd0a1c55db0` 的已有合成实验结果，讨论重建误差与峰值保持的权衡；TASK 与入口先提交为 `1bc99fe80eea2111153b9ffa4dc4ea5d3cfd6ac9`。
- Observation：EXP-001 revision 1 已完成。三个输入与上游 TASK 的 blob SHA 全部吻合；提交 LF 与本地 CRLF 导致严格字节比较失败，但确认仅换行差异，Git 规范化内容全部一致（core.autocrlf=true），未改写证据。窗口 3 平均 RMSE 最低但仍有平均峰值损失；窗口 1 平均峰值偏差接近零且轻微超调，同时 RMSE 最高；窗口 7 较窗口 3 有更大的峰值衰减和更高的 RMSE。
- Hypothesis：未提出或检验新假说，未做显著性检验；每窗 n=3，ddof=1 样本 SD 不是置信区间，结果只适用于固定设置的合成数据。
- Decision：实际执行 validate 和 report，退出码均为 0；validate 未改文件，report 只生成 `reports/REPORT-002.md`。仅补充报告文字完成七项 Required discussion，独立 CSV 汇总及报告数值核对通过。报告先单独提交为 `901fcea03e38062a3cac6500994e9c05b91848aa`，随后在 REPORT-002/HANDOFF.md 记录该 outputs_commit、完整命令输出及核验限制，并另行提交 HANDOFF 和本日志。未运行 EXP-001 run 命令，未修改任何输入证据。
