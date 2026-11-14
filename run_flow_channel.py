"""Convenience runner:  python3 run_flow_channel.py  (writes results/flow_channel_v1.csv)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from monetary_symmetry.flow_channel import main

if __name__ == "__main__":
    main()
