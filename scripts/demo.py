"""Small, dependency-free workflow fixture. Python 3.10+."""
import argparse
import csv
import hashlib
import json
import math
import platform
import random
import re
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'configs' / 'EXP-001.json'
METRICS = ['rmse', 'peak_attenuation']
FIELDS = ['window', 'seed'] + METRICS
SUMMARY = ['window', 'n', 'rmse_mean', 'rmse_sd', 'peak_attenuation_mean', 'peak_attenuation_sd']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identifier(value):
    require(bool(re.fullmatch(r'[A-Z0-9][A-Z0-9_-]{0,63}', value)), 'Invalid identifier')
    return value


def outdir(run_id):
    return ROOT / 'results' / 'EXP-001' / identifier(run_id)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def git_state():
    def git(*args):
        return subprocess.check_output(['git', '-C', str(ROOT), *args], stderr=subprocess.DEVNULL, text=True).strip()
    try:
        if Path(git('rev-parse', '--show-toplevel')).resolve() != ROOT:
            return {'commit': None, 'dirty': None, 'note': 'Demo root is not a Git repository root'}
        return {'commit': git('rev-parse', 'HEAD'), 'dirty': bool(git('status', '--porcelain'))}
    except (OSError, subprocess.CalledProcessError):
        return {'commit': None, 'dirty': None, 'note': 'No committed Git repository detected'}


def check_config(c):
    require(c['experiment_id'] == 'EXP-001', 'Unexpected experiment ID')
    require(c['seeds'] == [42, 123, 2026] and c['windows'] == [1, 3, 7], 'Unexpected experiment grid')
    require(c['n_points'] == 240 and c['noise_std'] == 0.35, 'Unexpected fixed settings')


def signal(c, seed):
    rng = random.Random(seed)
    clean = [math.sin(2 * math.pi * i / 40) + 0.5 * math.sin(2 * math.pi * i / 10)
             for i in range(c['n_points'])]
    noisy = [v + rng.gauss(0, c['noise_std']) for v in clean]
    return {'seed': seed, 'clean': clean, 'noisy': noisy}


def measure(record, window):
    clean, noisy = record['clean'], record['noisy']
    half = window // 2
    smooth = [statistics.mean(noisy[max(0, i-half):min(len(noisy), i+half+1)])
              for i in range(len(noisy))]
    rmse = math.sqrt(statistics.mean((a-b)**2 for a, b in zip(smooth, clean)))
    # Mean signed loss at the true signal's local positive maxima.
    peaks = [i for i in range(1, len(clean)-1) if clean[i] > clean[i-1] and clean[i] > clean[i+1]]
    attenuation = statistics.mean(clean[i] - smooth[i] for i in peaks)
    return {'window': window, 'seed': record['seed'], 'rmse': rmse, 'peak_attenuation': attenuation}


def summarize(rows):
    result = []
    for window in sorted({r['window'] for r in rows}):
        subset = [r for r in rows if r['window'] == window]
        row = {'window': window, 'n': len(subset)}
        for name in METRICS:
            vals = [r[name] for r in subset]
            row[name+'_mean'] = statistics.mean(vals)
            row[name+'_sd'] = statistics.stdev(vals)
        result.append(row)
    return result


def write_csv(path, fields, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def load_csv(path, fields):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        require(reader.fieldnames == fields, f'Wrong columns: {path.name}')
        result = []
        for row in reader:
            require(None not in row and all(v is not None for v in row.values()), 'Malformed CSV row')
            parsed = {k: int(v) if k in ('window', 'seed', 'n') else float(v) for k, v in row.items()}
            require(all(math.isfinite(v) for v in parsed.values()), 'Non-finite metric')
            result.append(parsed)
        return result


def near(a, b):
    return math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-12)


def run(run_id):
    c = json.loads(CONFIG.read_text(encoding='utf-8'))
    check_config(c)
    state = git_state()
    d = outdir(run_id)
    require(not d.exists(), f'Run already exists; choose a new run_id: {run_id}')
    d.mkdir(parents=True)
    raw = [signal(c, seed) for seed in c['seeds']]
    rows = [measure(record, w) for record in raw for w in c['windows']]
    write_json(d / 'signals.json', raw)
    write_csv(d / 'metrics.csv', FIELDS, rows)
    write_csv(d / 'summary.csv', SUMMARY, summarize(rows))
    manifest = {
        'experiment_id': 'EXP-001', 'run_id': run_id,
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(), 'config': c, 'git': state,
        'source_hashes': {p: digest(ROOT / p) for p in ['scripts/demo.py', 'configs/EXP-001.json']},
        'artifact_hashes': {p: digest(d / p) for p in ['signals.json', 'metrics.csv', 'summary.csv']},
        'definitions': {
            'data': 'Synthetic signal; no external dataset',
            'signal': 'sin(2*pi*i/40) + 0.5*sin(2*pi*i/10), i=0..239',
            'boundary': 'Centered moving average; clip window to available samples at edges',
            'rmse': 'sqrt(mean((smoothed-clean)^2)); lower is better',
            'peak_attenuation': 'mean(clean-smoothed) at true local maxima; zero means no mean loss; negative means overshoot',
            'sd': 'Sample standard deviation across three seeds (ddof=1); not a confidence interval'
        }
    }
    write_json(d / 'manifest.json', manifest)
    print(f'CREATED {d.relative_to(ROOT).as_posix()} (9 rows)')
    if state['commit'] is None or state['dirty']:
        print('NOTE: Code provenance is not a clean committed demo repository; inspect manifest before handoff.')


def validate(run_id):
    d = outdir(run_id)
    m = json.loads((d / 'manifest.json').read_text(encoding='utf-8'))
    require(m['experiment_id'] == 'EXP-001' and m['run_id'] == run_id, 'Manifest identity mismatch')
    c = m['config']
    check_config(c)
    require(set(m['artifact_hashes']) == {'signals.json', 'metrics.csv', 'summary.csv'}, 'Missing artifact hashes')
    for name, expected in m['artifact_hashes'].items():
        require(digest(d / name) == expected, f'Artifact hash mismatch: {name}')
    require(set(m['source_hashes']) == {'scripts/demo.py', 'configs/EXP-001.json'}, 'Missing source hashes')
    for name, expected in m['source_hashes'].items():
        require(digest(ROOT / name) == expected, f'Source changed since run: {name}')
    raw = json.loads((d / 'signals.json').read_text(encoding='utf-8'))
    require(len(raw) == len(c['seeds']) and {r['seed'] for r in raw} == set(c['seeds']), 'Raw seed mismatch')
    for record in raw:
        regenerated = signal(c, record['seed'])
        for key in ['clean', 'noisy']:
            require(len(record[key]) == c['n_points'], 'Wrong signal length')
            require(all(near(a, b) for a, b in zip(record[key], regenerated[key])), 'Raw signal mismatch')
    rows = load_csv(d / 'metrics.csv', FIELDS)
    expected_keys = {(w, seed) for w in c['windows'] for seed in c['seeds']}
    require(len(rows) == 9 and {(r['window'], r['seed']) for r in rows} == expected_keys,
            'Expected exactly nine unique window/seed combinations')
    by_seed = {r['seed']: r for r in raw}
    for row in rows:
        computed = measure(by_seed[row['seed']], row['window'])
        require(all(near(row[k], computed[k]) for k in METRICS), 'Metric does not match raw signal')
    summary = load_csv(d / 'summary.csv', SUMMARY)
    require(len(summary) == 3 and {r['window'] for r in summary} == set(c['windows']), 'Summary grid mismatch')
    expected = {r['window']: r for r in summarize(rows)}
    for row in summary:
        require(all(near(row[k], expected[row['window']][k]) for k in SUMMARY), 'Summary mismatch')
    print(f'PASS {run_id}: 9 unique combinations, finite metrics, raw data, aggregation and hashes verified')
    return summary


def report(run_id, task_id):
    identifier(task_id)
    rows = validate(run_id)
    p = ROOT / 'reports' / (task_id + '.md')
    require(not p.exists(), 'Report already exists; inspect before creating a replacement')
    best = min(rows, key=lambda r: r['rmse_mean'])
    lines = ['# 合成信号平滑实验报告', '', f'Task: {task_id}', f'Run: {run_id}', '',
             '本报告仅描述工作流演示中的合成信号。每个窗口使用相同的三个随机 seed。', '',
             '| Window | RMSE mean ± sample SD | Peak attenuation mean ± sample SD | n |',
             '|---|---|---|---|']
    for r in rows:
        lines.append(f"| {r['window']} | {r['rmse_mean']:.6f} ± {r['rmse_sd']:.6f} | {r['peak_attenuation_mean']:.6f} ± {r['peak_attenuation_sd']:.6f} | {r['n']} |")
    lines += ['', f"在本次三个 seed 的结果中，窗口 {best['window']} 的平均 RMSE 最低，为 {best['rmse_mean']:.6f}。",
              '', 'RMSE 越低越好。峰值衰减为真值局部峰处 clean − smoothed 的平均值；正值表示衰减，负值表示超调，不能简单按越小越好排序。',
              '', '± 表示三个 seed 之间的样本标准差，不是置信区间。未进行显著性检验；不得据此声称稳健提升或真实数据泛化能力。',
              '', '## 证据（路径均相对仓库根目录）', '',
              f'- results/EXP-001/{run_id}/metrics.csv',
              f'- results/EXP-001/{run_id}/summary.csv',
              f'- results/EXP-001/{run_id}/manifest.json', '']
    p.parent.mkdir(exist_ok=True)
    p.write_text('\n'.join(lines), encoding='utf-8')
    print(f'CREATED {p.relative_to(ROOT).as_posix()}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['run', 'validate', 'report'])
    parser.add_argument('--run-id', default='EXP-001-R01')
    parser.add_argument('--task-id', default='REPORT-002')
    args = parser.parse_args()
    try:
        if args.action == 'run':
            run(args.run_id)
        elif args.action == 'validate':
            validate(args.run_id)
        else:
            report(args.run_id, args.task_id)
    except (ValueError, OSError, KeyError, TypeError, csv.Error) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
