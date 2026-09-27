# EXP-001 工作报告

task_id: EXP-001
executed_revision: 1
run_id: EXP-001-R01
status: COMPLETED
repository: 75267156/paper-workflow-demo
branch: main
results_commit: d7a09827ec833ef3aa23186402330fd0a1c55db0
path_base: repository_root

## 工作报告
2026-09-27 完成 TASK revision 1。运行前工作树干净，`git pull --ff-only` 返回已是最新版本；代码和配置均已提交，未修改实验定义。使用 Python 3.12.7 执行 `python scripts/demo.py run --run-id EXP-001-R01`，退出码为 0，生成 3 个窗口 × 3 个 seed 的 9 个组合。

直接读取 metrics.csv 和 summary.csv：窗口 1、3、7 的平均 RMSE 分别为 0.346744、0.211492、0.260907；平均峰值衰减分别为 -0.013528、0.078721、0.288393。在本次三个 seed 的合成信号中，窗口 3 的平均 RMSE 最低；窗口 7 的平均峰值衰减最大。峰值衰减为真值局部峰处 clean − smoothed 的均值，负值表示超调，不能简单按越小越好排序。

## Evidence
以下路径均相对仓库根目录，结果版本为 `d7a09827ec833ef3aa23186402330fd0a1c55db0`：

- `results/EXP-001/EXP-001-R01/signals.json`：三个 seed 的原始合成信号与含噪信号。
- `results/EXP-001/EXP-001-R01/metrics.csv`：九个窗口/seed 组合的指标。
- `results/EXP-001/EXP-001-R01/summary.csv`：每个窗口跨三个 seed 的均值及样本标准差。
- `results/EXP-001/EXP-001-R01/manifest.json`：实际配置、Python 版本、代码版本、源文件及产物 SHA-256、指标定义。

manifest 的代码 commit 为 `afe1ee4c28f0f2826324f885b0441a7f83ab6050`，与运行前 HEAD 一致；`dirty: false`，代码来源无异常。代码提交与结果提交不同，符合先提交代码、运行后提交结果的顺序。

## Verification
独立执行：`python scripts/demo.py validate --run-id EXP-001-R01`。

退出码：0。输出：`PASS EXP-001-R01: 9 unique combinations, finite metrics, raw data, aggregation and hashes verified`。

验证覆盖九个组合完整且唯一、指标有限、原始信号重新生成一致、指标由原始信号重算一致、汇总均值与样本标准差一致，以及源文件与产物哈希一致。另行检查 manifest 的代码 commit 和 dirty 状态，结果如上。validate 使用同一脚本中的生成及计算函数，不构成第二套独立算法验证。

限制：全部数据为人工生成的信号，仅三个固定 seed；样本标准差不是置信区间。未进行显著性检验，不支持真实科研发现、普适性或真实数据效果的结论。

## Open issues / Next action
无已知执行或校验阻塞。后续由网页 Chat 读取上述真实证据后创建 REPORT-002；不预写假说或后续报告结论。
