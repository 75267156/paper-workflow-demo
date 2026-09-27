# 当前入口

active_task: REPORT-002
task_path: .ai/tasks/REPORT-002/TASK.md
handoff_path: .ai/tasks/REPORT-002/HANDOFF.md
depends_on: [EXP-001]

这里只维护入口和依赖，不重复保存执行状态。
REPORT-002 由网页 Chat 阅读 EXP-001 的实际合成实验结果后创建。
历史任务保留，但不在每轮启动时全部读取。
