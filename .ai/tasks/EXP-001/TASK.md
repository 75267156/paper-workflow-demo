# EXP-001：合成信号平滑实验

task_id: EXP-001
revision: 1
depends_on: []
run_id: EXP-001-R01

## 目标
比较窗口 1、3、7 的中心移动平均，对合成含噪信号的重建误差和峰值衰减。
这是工作流测试，不用于支持真实世界的科学结论。

## 输入与固定设置
- 配置：configs/EXP-001.json
- 执行工具：scripts/demo.py
- 三个 seed，每个 seed 在各窗口之间使用同一条含噪信号。
- 每个序列 240 点；固定信号公式、噪声标准差与边界处理。
- 总计 3 个窗口 × 3 个 seed = 9 个组合。

## 修改范围
- 默认无需修改代码或配置；若程序失败，先报告具体故障，不自行更改实验定义。
- 允许生成 results/EXP-001/EXP-001-R01/ 下的产物。
- 允许更新本任务 HANDOFF.md 及 notes/experiment-log.md。
- 不修改其他任务、论文或既有实验结果。

## 执行
从仓库根目录运行：
```text
python scripts/demo.py run --run-id EXP-001-R01
python scripts/demo.py validate --run-id EXP-001-R01
```

## 验收
- 命令成功；9 个组合完整且唯一。
- 全部指标有限；CSV 与原始信号重新计算结果一致。
- summary.csv 与 metrics.csv 的均值、样本标准差一致。
- manifest 保存真实配置、代码版本、文件哈希及指标定义。
- 结果可提交并推送后，填写 HANDOFF 中的 evidence 路径和 results_commit。
- 使用 Markdown 报告执行结果；不要声称显著性、普适性或真实数据效果。

## 下一步
网页 Chat 阅读真实结果后创建 REPORT-002，而非直接沿用预写结论。
