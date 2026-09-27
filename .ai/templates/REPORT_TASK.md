# REPORT-002：基于 EXP-001 的短报告

task_id: REPORT-002
revision: 1
depends_on: [EXP-001]
evidence_commit: <网页 Chat 实际读取的结果提交号>
run_id: <已完成的 EXP-001 run_id>

## Goal
根据真实结果生成短报告，比较误差和峰值保持情况。

## Evidence
- results/EXP-001/<run_id>/metrics.csv
- results/EXP-001/<run_id>/summary.csv
- results/EXP-001/<run_id>/manifest.json
- .ai/tasks/EXP-001/HANDOFF.md（工作报告，不代替数值证据）

## Allowed outputs
- reports/REPORT-002.md
- .ai/tasks/REPORT-002/HANDOFF.md
- notes/experiment-log.md

## Execution
先确认本地证据文件与 evidence_commit 中相同路径内容一致；再运行：
python scripts/demo.py validate --run-id <run_id>
python scripts/demo.py report --run-id <run_id> --task-id REPORT-002

## Required discussion
<网页 Chat 根据实际结果写出希望报告讨论的具体问题；不要提前编造胜者或数字>

## Forbidden claims
- 不声称统计显著、真实科研有效或适用于所有信号。
- 不把样本标准差写成置信区间。
- 不修改输入结果；不重新执行 EXP。

## Completion
报告数值与证据一致；说明指标方向、样本数与限制；更新本任务 HANDOFF。
