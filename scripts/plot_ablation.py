"""Plot training curves of several experiment runs grouped by condition.

Usage:
    python scripts/plot_ablation.py --out Cap5/ablation_returns.pdf \
        --group "rho=0:path/to/runA path/to/runB" \
        --group "rho=0.25:path/to/runC path/to/runD"

Each run directory must contain metrics.jsonl as written by vsss-sim's train_jax.py
(fields used: env_steps, mean_episode_return, blue_goals, yellow_goals, episodes).
Runs in a group are aligned on generation and shown as mean line + min/max band.
"""
import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def load(run: Path):
    rows = [json.loads(line) for line in (run / "metrics.jsonl").read_text().splitlines() if line.strip()]
    rows.sort(key=lambda r: r["generation"])
    steps = np.array([r["env_steps"] for r in rows], dtype=float)
    ret = np.array([r["mean_episode_return"] for r in rows], dtype=float)
    # Goal rate per episode from per-generation counters (blue goals / completed episodes).
    eps = np.maximum(np.array([r.get("episodes", 0) for r in rows], dtype=float), 1.0)
    blue = np.array([r.get("blue_goals", 0) for r in rows], dtype=float) / eps
    return steps, ret, blue


def smooth(y, k):
    if k <= 1 or len(y) < k:
        return y
    kernel = np.ones(k) / k
    return np.convolve(np.pad(y, (k // 2, k - 1 - k // 2), mode="edge"), kernel, mode="valid")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", action="append", required=True, help="label:run1 run2 ...")
    parser.add_argument("--out", required=True)
    parser.add_argument("--smooth", type=int, default=5, help="moving-average window in generations")
    args = parser.parse_args()

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    for group in args.group:
        label, _, runs = group.partition(":")
        data = [load(Path(p)) for p in runs.split()]
        n = min(len(d[0]) for d in data)  # align on the shortest run
        steps = np.mean([d[0][:n] for d in data], axis=0)
        for ax, idx, name in ((axes[0], 1, "Mean episode return"), (axes[1], 2, "Blue goals per episode")):
            curves = np.stack([smooth(d[idx][:n], args.smooth) for d in data])
            line, = ax.plot(steps, curves.mean(axis=0), label=f"{label} (n={len(data)})")
            ax.fill_between(steps, curves.min(axis=0), curves.max(axis=0), alpha=0.2, color=line.get_color())
            ax.set_xlabel("Environment steps")
            ax.set_ylabel(name)
            ax.grid(alpha=0.3)
    axes[0].legend(frameon=False)
    fig.tight_layout()
    fig.savefig(args.out)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
