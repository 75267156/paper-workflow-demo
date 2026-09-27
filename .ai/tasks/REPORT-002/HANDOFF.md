# REPORT-002 工作交接

task_id: REPORT-002
revision: 1
executed_revision: 1
status: COMPLETED
generation_status: COMPLETED
repository: 75267156/paper-workflow-demo
branch: main
depends_on: [EXP-001]
evidence_commit: d7a09827ec833ef3aa23186402330fd0a1c55db0
evidence_task_revision: 1
run_id: EXP-001-R01
task_commit: 1bc99fe80eea2111153b9ffa4dc4ea5d3cfd6ac9
outputs_commit: 901fcea03e38062a3cac6500994e9c05b91848aa
report_path: reports/REPORT-002.md
path_base: repository_root
executed_date: 2026-09-27
python_version: 3.12.7

## 入口、依赖与授权范围

初始 HEAD 为 `b31a2f4585f521195f016e26f96b4e56eefca8b9`，工作树干净，当前分支为 main，origin 为 `https://github.com/75267156/paper-workflow-demo.git`。沙箱账户首次 Git 检查因仓库所有权限制失败；随后在获准的正常账户环境下完成 Git 操作，未修改全局 Git 配置。

已保存用户粘贴的 TASK，只还原网页转义的下划线和元数据换行，不改变任务含义。逐项检查元数据并扫描 TODO/TBD/FIXME、模板标记和待填项，未发现未填占位符。TASK 和 INDEX 在执行 validate/report 前提交为上述 task_commit。

直接读取 EXP-001/TASK.md 和 HANDOFF.md，确认 revision / executed_revision 均为 1、run_id 为 EXP-001-R01、状态为 COMPLETED、results_commit 与 evidence_commit 一致。没有重复执行 EXP-001。

用户本轮直接指令另外授权保存 TASK、更新 INDEX，并在报告提交后提交 HANDOFF 和日志；因此任务管理文件及 `notes/experiment-log.md` 的本任务追加记录属于本轮显式授权。report 命令本身仍严格只写 Allowed outputs 中的报告。未修改源代码、配置、上游 TASK/HANDOFF、其他任务或原始实验结果。

## 输入证据校验

通过 `git show <evidence_commit>:<path>` 实际读取指定提交中的三个输入文件及 EXP-001/TASK.md，核对 blob SHA，并直接读取本地 CSV/JSON 内容。以下提交 blob 与 `git hash-object --path=<path> <path>` 得到的工作树规范化 blob 全部一致：

| 输入路径 | 提交与工作树规范化 blob SHA |
|---|---|
| results/EXP-001/EXP-001-R01/metrics.csv | 230c7742d68daaa9c4d44a4d805970d8b02f690f |
| results/EXP-001/EXP-001-R01/summary.csv | 602f3539943bc64834b117cbd3854ce1de3301cd |
| results/EXP-001/EXP-001-R01/manifest.json | 02dbf4f5602fe03c5f46a96d8358b6e25930b32f |
| .ai/tasks/EXP-001/TASK.md | bab905acdb336b66349eff2fed3153bccd4b5914 |

最初严格逐字节断言在 metrics.csv 上失败（检查进程退出码 1）。后续对全部四个文件定位差异：提交使用 LF，本地使用 CRLF；仅将 CRLF 归一化为 LF 后，所有字节均一致。系统 Git 配置 `C:/Program Files/Git/etc/gitconfig` 中 `core.autocrlf=true`，未发现其他内容差异；按 Git 内容规范化判定证据内容一致，不能声称原始字节完全相同。本次未改写任何证据或换行。具体核对记录如下：

| 文件 | 提交字节数 | 本地字节数 | 提交 CRLF 数 | 本地 CRLF 数 |
|---|---:|---:|---:|---:|
| metrics.csv | 445 | 455 | 0 | 10 |
| summary.csv | 324 | 328 | 0 | 4 |
| manifest.json | 1429 | 1471 | 0 | 42 |
| EXP-001/TASK.md | 1610 | 1651 | 0 | 41 |

本地 metrics.csv SHA-256 为 `73147c1402bf148bb32de7268bea23ff86cfdb7424b9ac112279dedac1cfb5ad`，summary.csv 为 `585727cc6a18814faf1f6469e19d49be639a33989c76460c29022e3131dccafc`，均与 manifest 的运行时文件哈希一致；本地 manifest.json SHA-256 为 `96491ba69db2fec215c2b22dae17342d210decc958e30fbfe4e37cf50c2b2ae7`。

manifest 记录代码 commit 为 `afe1ee4c28f0f2826324f885b0441a7f83ab6050`、dirty 为 false。运行时源码与配置的实际哈希由下述 validate 校验；没有从 HANDOFF 摘要代取数值。

## 实际执行与输出

从仓库根目录执行以下两个命令，顺序如下。

### 1. 只读校验

命令：`python scripts/demo.py validate --run-id EXP-001-R01`

退出码：0。stdout：

```text
PASS EXP-001-R01: 9 unique combinations, finite metrics, raw data, aggregation and hashes verified
```

stderr 为空。命令前后对仓库内全部非 .git 文件做 SHA-256 快照比较，改变路径集合为空。

### 2. 报告生成

命令：`python scripts/demo.py report --run-id EXP-001-R01 --task-id REPORT-002`

退出码：0。stdout：

```text
PASS EXP-001-R01: 9 unique combinations, finite metrics, raw data, aggregation and hashes verified
CREATED reports/REPORT-002.md
```

stderr 为空。report 内部再次调用 validate。前后文件快照唯一变化为 `reports/REPORT-002.md`，未越过 Allowed outputs。

validate 覆盖九个唯一窗口/seed 组合、有限指标、原始信号一致性、指标重算、均值和样本标准差汇总、源码/配置及产物哈希。它调用同一脚本的信号和指标函数，在内存中复算用于校验，不是另一套独立算法验证，也没有生成或覆盖实验产物。未执行 `run` 命令。

## 报告复核

生成稿的讨论不完整，随后仅修改报告文字，保留生成的 CSV 指标表。使用标准库 csv/statistics/math 另行读取 metrics.csv 与 summary.csv，确认九个唯一组合齐全，各窗口 n=3；重新汇总均值与 ddof=1 样本标准差，按 rel_tol=1e-12、abs_tol=1e-15 与 CSV 比较，全部一致。该检查进程退出码为 0，输出：

```text
PASS independent CSV aggregation: 9 unique combinations; means and sample SD agree
PASS all 12 report table metrics and six-decimal narrative values match CSV rounding
PASS report fixed settings and code provenance match manifest; required definition and limitation terms present
```

人工逐项复核 Required discussion：

1. 明确窗口 3 的平均 RMSE 为 0.211492，低于窗口 1 的 0.346744 和窗口 7 的 0.260907，仅限本次固定 seed。
2. 明确窗口 3 的平均峰值衰减为 0.078721，存在平均峰值损失。
3. 明确窗口 1 的 -0.013528 为接近零的轻微平均超调，且其 RMSE 最高，不按负衰减更好排序。
4. 明确窗口 7 的衰减 0.288393 大于窗口 3，RMSE 也更高，说明较强平滑带来的峰值损失。
5. 表格包含三个窗口全部样本 SD；明确每窗 n=3、ddof=1，SD 不是置信区间或标准误。
6. 区分低重建误差与平均峰值偏差接近零，不推导普适总体优劣。
7. 列明固定信号公式、240 点、噪声标准差 0.35、边界截取及固定 seed 42/123/2026，限制为已有合成数据。

报告给出两项指标定义及方向，明确未进行显著性检验，不声称真实科研发现、真实数据效果或普适性。报告提交前再次核对四份输入的 Git 规范化哈希均未变化；当时唯一未跟踪文件为报告，未发现额外修改。报告单独提交为 outputs_commit，然后才创建本 HANDOFF 并追加日志。

## 状态与限制

报告生成与验证完成，无未解决内容阻塞。Git 换行规范化差异已如实披露。所有结果来自既有合成实验，每个窗口仅三个固定 seed，样本 SD 不能作为显著性证据。本 HANDOFF 记录的是本次实际执行结果；推送是否成功由随后实际 `git push` 和远端分支核对结果确认。
