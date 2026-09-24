from __future__ import annotations

import argparse
from pathlib import Path

from boid.applications.sleep import compute_sleep_boid


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--psg", required=True)
    p.add_argument("--hypnogram", required=True)
    p.add_argument("--record-id", required=True)
    p.add_argument("--embedding-lag", type=int, required=True)
    p.add_argument("--c-n", type=float, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    windows, epochs = compute_sleep_boid(
        psg_path=args.psg,
        hypnogram_path=args.hypnogram,
        record_id=args.record_id,
        embedding_lag=args.embedding_lag,
        finite_sample_correction=args.c_n,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    windows.to_csv(args.output, index=False)
    epoch_path = args.output.with_name(args.output.stem + "_30s.csv")
    epochs.to_csv(epoch_path, index=False)

    print("4-s BOID windows:", args.output)
    print("30-s sleep-stage table:", epoch_path)


if __name__ == "__main__":
    main()
