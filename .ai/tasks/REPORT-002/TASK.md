# REPORT-002：基于 EXP-001 的短报告

task_id: REPORT-002
revision: 1
depends_on: [EXP-001]
repository: 75267156/paper-workflow-demo
branch: main
evidence_commit: d7a09827ec833ef3aa23186402330fd0a1c55db0
run_id: EXP-001-R01
evidence_task_revision: 1

## Goal

根据 EXP-001 的真实实验结果生成短报告，比较中心移动平均窗口 1、3、7 的重建误差与峰值保持情况，重点讨论实际 RMSE 与峰值衰减之间的权衡。

本报告只解释已有合成实验结果，不重新执行 EXP-001，不修改实验定义或原始结果，也不把合成数据结果外推为真实科研结论。

## Evidence

数值证据以 `evidence_commit` 中的下列仓库根目录相对路径为准：

- `results/EXP-001/EXP-001-R01/metrics.csv`
- `results/EXP-001/EXP-001-R01/summary.csv`
- `results/EXP-001/EXP-001-R01/manifest.json`
- `.ai/tasks/EXP-001/TASK.md`

工作交接元数据：

- `.ai/tasks/EXP-001/HANDOFF.md`

`HANDOFF.md` 用于确认 `run_id`、执行 revision、状态和 `results_commit`，不能代替上述 CSV 和 manifest 的数值证据。

网页 Chat 已直接使用 GitHub commit ref `d7a09827ec833ef3aa23186402330fd0a1c55db0` 读取前三个结果文件及 EXP-001/TASK.md。读取到的 GitHub blob SHA 为：

- `metrics.csv`: `230c7742d68daaa9c4d44a4d805970d8b02f690f`
- `summary.csv`: `602f3539943bc64834b117cbd3854ce1de3301cd`
- `manifest.json`: `02dbf4f5602fe03c5f46a96d8358b6e25930b32f`
- `.ai/tasks/EXP-001/TASK.md`: `bab905acdb336b66349eff2fed3153bccd4b5914`

## Evidence facts already checked in Chat

这些核对基于实际读取的 CSV/JSON 内容；不表示本轮已经执行仓库中的 Python `validate` 命令。

`metrics.csv` 包含且仅包含以下 9 个唯一 `(window, seed)` 组合：

- windows: `1, 3, 7`
- seeds: `42, 123, 2026`
- 每个 window 有 3 个 seed，总计 9 个组合，无重复、无缺失。

根据 `metrics.csv` 数值重新计算后，均值及样本标准差与 `summary.csv` 一致：

| window |  n |           RMSE mean |       RMSE sample SD | peak attenuation mean | peak attenuation sample SD |
| -----: | -: | ------------------: | -------------------: | --------------------: | -------------------------: |
|      1 |  3 |   0.346743765170684 | 0.013568713940637392 | -0.013527892694134295 |        0.05207291151786817 |
|      3 |  3 | 0.21149150621549398 | 0.004774516319313129 |   0.07872114363785279 |       0.025132972363549572 |
|      7 |  3 |  0.2609065975226672 |  0.01600983565479524 |   0.28839329361081456 |       0.013658055853025092 |

`manifest.json` 明确定义：

- RMSE：`sqrt(mean((smoothed-clean)^2))`，越低表示重建误差越小。
- peak attenuation：在真实局部峰位置计算 `mean(clean-smoothed)`；`0` 表示平均无峰值损失，正值表示衰减，负值表示超调。
- SD：三个 seed 间的样本标准差，`ddof=1`；不是置信区间。
- 数据为合成信号，无外部真实数据。
- 运行时记录的代码 commit 为 `afe1ee4c28f0f2826324f885b0441a7f83ab6050`，`dirty: false`。

## Allowed outputs

本任务只允许生成或更新：

- `reports/REPORT-002.md`
- `.ai/tasks/REPORT-002/HANDOFF.md`

不得修改 `results/EXP-001/EXP-001-R01/` 中任何文件，不得修改 EXP-001 的 TASK/HANDOFF、配置、源代码、其他任务、论文或既有实验结果。

## Execution

从仓库根目录执行。

首先确认本地证据文件与 `evidence_commit=d7a09827ec833ef3aa23186402330fd0a1c55db0` 中相同路径的内容一致。若无法确认，或发现证据文件已变化、缺失或与该提交不符，停止报告生成并在 REPORT-002/HANDOFF.md 中记录 `BLOCKED` 及具体差异；不得通过修改或重新生成 EXP-001 结果来消除差异。

不得运行 EXP-001 的实验生成命令：
```text
python scripts/demo.py run --run-id EXP-001-R01
```

可按项目既有流程执行只读校验：
```text
python scripts/demo.py validate --run-id EXP-001-R01
```

只有实际执行该命令后，才可在 REPORT-002/HANDOFF.md 中声称 Python validation 通过，并应记录真实退出码和输出。网页 Chat 本轮的 CSV 统计核对不能写成已经运行该命令。

证据确认后生成报告：
```text
python scripts/demo.py report --run-id EXP-001-R01 --task-id REPORT-002
```

若该命令试图修改 Allowed outputs 之外的文件，停止并报告，不接受额外修改。

## Required discussion

`reports/REPORT-002.md` 必须基于上述真实数值讨论误差与峰值衰减的权衡，而不是只给出单一“最佳窗口”。

至少说明：

1. 窗口 3 的平均 RMSE 为 `0.211492`，低于窗口 1 的 `0.346744` 和窗口 7 的 `0.260907`；在本次三个固定 seed 中，它的平均重建误差最低。
2. 窗口 3 的平均峰值衰减为 `0.078721`，说明降低总体重建误差的同时存在一定平均峰值损失。
3. 窗口 1 的平均峰值衰减为 `-0.013528`，接近零但略为负值；根据指标定义，这表示平均上轻微超调，而不是简单意义上的“衰减更小就是更好”。同时它的平均 RMSE 在三个窗口中最高。
4. 窗口 7 的平均峰值衰减为 `0.288393`，明显大于窗口 3；其平均 RMSE `0.260907` 也高于窗口 3。因此应具体说明较强平滑在本实验中带来的峰值损失，而不能笼统宣称更大窗口更优。
5. 对三个窗口同时报告或明确引用跨三个 seed 的样本标准差，并注明每个窗口只有 `n=3`。
6. 区分“重建误差低”和“峰值幅度保持接近零”这两个目标；不要把其中任一指标单独扩展为普适的总体优劣结论。
7. 说明这些结论只适用于 EXP-001 中固定信号公式、噪声水平、边界处理和三个固定 seed 的合成数据。

可酌情讨论各窗口跨 seed 的变异，但不得把三个 seed 的样本标准差解释为置信区间或显著性证据。

## Forbidden claims

- 不声称任何差异具有统计显著性。
- 不声称结果构成真实科研发现、真实数据效果或适用于所有信号。
- 不把样本标准差写成置信区间、标准误或显著性区间。
- 不把负的 peak attenuation 解释为“负衰减一定更好”；必须按 manifest 的“负值表示超调”定义解释。
- 不修改、重算生成或覆盖 EXP-001 的输入和结果文件。
- 不重新运行 EXP-001 实验。
- 不根据 HANDOFF 摘要替代实际 CSV/manifest 中的证据。
- 不虚构 Python validation、退出码、文件哈希、提交号或未实际执行的验证步骤。

## Completion

任务完成时应满足：

- `reports/REPORT-002.md` 中所有数值均可追溯到 `evidence_commit=d7a09827ec833ef3aa23186402330fd0a1c55db0` 的实际证据文件。
- 报告明确说明 RMSE 和 peak attenuation 的定义与方向。
- 报告明确说明每个窗口 `n=3`，SD 为 `ddof=1` 样本标准差且不是置信区间。
- 报告实际讨论窗口 1、3、7 在重建误差和峰值保持之间的权衡。
- 报告包含合成数据、固定 seed、无显著性检验等限制。
- 原始 EXP-001 结果未被修改或重新生成。
- 除 `reports/REPORT-002.md` 和 `.ai/tasks/REPORT-002/HANDOFF.md` 外无其他任务产物修改。
- REPORT-002/HANDOFF.md 记录实际使用的 `evidence_commit`、`run_id`、REPORT-002 revision、生成状态、报告路径以及任何实际执行的验证步骤。
