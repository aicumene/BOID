from pathlib import Path


def test_boid_does_not_vendor_mssa_core():
    package_dir = Path(__file__).resolve().parents[1] / "src" / "boid"
    forbidden = {"hankel.py", "mssa.py", "rank.py"}
    assert not (forbidden & {p.name for p in package_dir.iterdir()})
