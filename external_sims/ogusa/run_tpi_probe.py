"""Reduced TPI probe: OG-USA defaults, T shortened to 50, SS-only=False.
Baseline only. Purpose: measure TPI viability/wall time in this sandbox."""
import json, os, time, importlib.resources
from ogcore.parameters import Specifications
from ogcore import execute

def main():
    from ogusa.calibrate import Calibration
    from distributed import Client, LocalCluster
    t0=time.time()
    out=os.path.abspath("OUTPUT_TPI_PROBE")
    p=Specifications(baseline=True, num_workers=1, baseline_dir=out, output_base=out)
    with importlib.resources.open_text("ogusa","ogusa_default_parameters.json") as f:
        defaults=json.load(f)
    p.update_specifications(defaults)
    p.update_specifications({"T": 50})
    c=Calibration(p); d=c.get_dict()
    p.update_specifications({k:v for k,v in d.items() if k in ("eta","zeta","e")})
    print("PROBE T=",p.T,"S=",p.S,"J=",p.J, flush=True)
    cluster=LocalCluster(n_workers=1, threads_per_worker=1, dashboard_address=None)
    client=Client(cluster)
    try:
        execute.runner(p, time_path=True, client=client)
    finally:
        client.close(); cluster.close()
    print("PROBE DONE wall", time.time()-t0, flush=True)

if __name__=="__main__":
    main()
