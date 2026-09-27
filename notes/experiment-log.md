# 实验日志

尚未执行。每个任务追加 Purpose / Observation / Hypothesis / Decision。
只记录合成数据观察，避免把工作流演示当作科研证据。

## 2026-09-27 — EXP-001 revision 1 / EXP-001-R01

- Purpose：比较窗口 1、3、7 的中心移动平均对合成含噪信号重建误差及峰值衰减的影响，验证实验交接流程。
- Observation：直接读取 `results/EXP-001/EXP-001-R01/metrics.csv` 和 `results/EXP-001/EXP-001-R01/summary.csv`，窗口 1、3、7 的平均 RMSE 分别为 0.346744、0.211492、0.260907，平均峰值衰减分别为 -0.013528、0.078721、0.288393。仅在本次三个固定 seed 中，窗口 3 的平均 RMSE 最低，窗口 7 的平均峰值衰减最大；负衰减表示超调。
- Hypothesis：本次任务未提出或检验新增假说，不将上述有限观察扩展为普适结论。
- Decision：独立命令 `python scripts/demo.py validate --run-id EXP-001-R01` 退出码为 0，原始信号、九个组合、指标、汇总及哈希校验通过。结果已提交为 `d7a09827ec833ef3aa23186402330fd0a1c55db0`；manifest 代码提交为 `afe1ee4c28f0f2826324f885b0441a7f83ab6050`、dirty 为 false。完成 EXP-001，交由网页 Chat 阅读真实证据后创建 REPORT-002，不重复运行本 run_id。
- 限制：合成数据工作流演示，n=3；样本标准差不是置信区间，未做显著性检验，不支持真实数据效果或真实科研发现。
