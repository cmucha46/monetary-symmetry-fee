"""Convenience runner:  python3 run_score.py  (writes results/*.csv)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from monetary_symmetry.score import main

if __name__ == "__main__":
    main()
