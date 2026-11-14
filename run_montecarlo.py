"""Convenience runner:  python3 run_montecarlo.py  (writes results/montecarlo_*.csv)

Monte Carlo v2 (Lane I): parameter uncertainty over the deterministic
fiscal module. Fixed seed 20261114, 10,000 draws by default.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from monetary_symmetry.montecarlo import main

if __name__ == "__main__":
    main()
