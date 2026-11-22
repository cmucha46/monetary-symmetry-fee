import numpy as np, json, sys
from copy import deepcopy
from HARK.ConsumptionSaving.ConsIndShockModel import IndShockConsumerType, init_idiosyncratic_shocks

rng_seed = 12345
# HARK defaults (init_idiosyncratic_shocks) except as noted
base = deepcopy(init_idiosyncratic_shocks)
base.update({
    'cycles': 0,               # infinite horizon
    'T_cycle': 1,
    'AgentCount': 2000,        # per beta type; 7 types -> 14,000 agents
    'aXtraMax': 30,
    'aXtraCount': 48,
    'seed': rng_seed,
})
# Sabelhaus-Song / HARK default income process is already in defaults:
# PermShkStd 0.1, TranShkStd 0.1, UnempPrb 0.05, IncUnemp 0.3 (documented in notes)
betas = [0.93,0.94,0.95,0.96,0.97,0.98,0.99]  # uniform grid, mean 0.96 (=HARK default DiscFac), spread +-0.03
print("betas", betas, flush=True)

all_m, all_a, all_p, all_c, all_mpc, all_beta = [], [], [], [], [], []
solutions = {}
eps = 1e-3
SIM_PERIODS = 300
for bi, beta in enumerate(betas):
    params = deepcopy(base)
    params['DiscFac'] = beta
    params['seed'] = rng_seed + 100*bi
    agent = IndShockConsumerType(**params)
    agent.T_sim = SIM_PERIODS
    agent.track_vars = ['mNrm','aLvl','pLvl','cNrm']
    agent.solve(verbose=False)
    solutions[beta] = agent.solution[0].cFunc
    agent.initialize_sim()
    agent.simulate(sim_periods=SIM_PERIODS)
    # final period cross-section
    m = np.asarray(agent.history['mNrm'][-1], dtype=float)
    a = np.asarray(agent.history['aLvl'][-1], dtype=float)
    p = np.asarray(agent.history['pLvl'][-1], dtype=float)
    cN = np.asarray(agent.history['cNrm'][-1], dtype=float)
    cfunc = agent.solution[0].cFunc
    mpc = (cfunc(m+eps) - cfunc(m-eps)) / (2*eps)  # normalized derivative = lvl derivative
    mpc = np.clip(mpc, 0, None)
    all_m.append(m); all_a.append(a); all_p.append(p); all_c.append(cN*p); all_mpc.append(mpc)
    all_beta.append(np.full_like(m, beta))
    print(f"beta={beta}: mean aLvl={a.mean():.3f} mean mNrm={m.mean():.3f} mean MPC={mpc.mean():.3f} share a~0={(a<1e-6).mean():.3f}", flush=True)

m = np.concatenate(all_m); a = np.concatenate(all_a); p = np.concatenate(all_p)
c = np.concatenate(all_c); mpc = np.concatenate(all_mpc); btype = np.concatenate(all_beta)
N = len(m)
print("N", N)

# MPC by wealth (aLvl) quintile
qs = np.quantile(a, [0,.2,.4,.6,.8,1.0])
rows=[]
for i in range(5):
    lo,hi = qs[i], qs[i+1]
    mask = (a>=lo)&(a<=hi) if i==4 else (a>=lo)&(a<hi)
    rows.append(dict(quintile=i+1, a_range=[float(lo),float(hi)], n=int(mask.sum()),
                     mean_aLvl=float(a[mask].mean()), wealth_share=float(a[mask].sum()/a.sum()),
                     mean_MPC=float(mpc[mask].mean()), median_MPC=float(np.median(mpc[mask])),
                     share_MPC_gt_0p9=float((mpc[mask]>0.9).mean())))
    print(rows[-1])

# Exact incidence contrast using each type's cFunc (nonlinear, not derivative-linearised)
# Total shock: uniform per-capita amount = 0.10 * mean permanent income
uniform_amt = 0.10 * p.mean()
total_shock = uniform_amt * N
# (b) uniform
dC_uniform = 0.0; dC_asset = 0.0
# need per-agent cfunc by type: recompute in blocks by beta value
for beta in betas:
    mask = btype==beta
    cf = solutions[beta]
    mm, pp, aa = m[mask], p[mask], a[mask]
    # uniform
    dm_u = uniform_amt/pp
    dC_uniform += float(np.sum((cf(mm+dm_u)-cf(mm))*pp))
    # pro-rata to assets: shock_i = total * a_i / sum(a_all)
    shock_i = total_shock * aa / a.sum()
    dm_a = shock_i/pp
    dC_asset += float(np.sum((cf(mm+dm_a)-cf(mm))*pp))

agg_mpc_uniform = dC_uniform/total_shock
agg_mpc_asset = dC_asset/total_shock
# derivative-based population aggregate MPC (uniform weighting)
agg_mpc_deriv = float(mpc.mean())

at_constraint = a < 1e-6
results = dict(
    N=int(N), sim_periods=SIM_PERIODS, betas=betas,
    mean_aLvl=float(a.mean()), mean_pLvl=float(p.mean()), mean_mNrm=float(m.mean()),
    wealth_quantile_edges=qs.tolist(),
    quintiles=rows,
    agg_MPC_derivative_uniform=float(agg_mpc_deriv),
    uniform_per_capita_amount=float(uniform_amt), total_shock=float(total_shock),
    agg_MPC_uniform_exact=float(agg_mpc_uniform), dC_uniform=float(dC_uniform),
    agg_MPC_asset_prorata_exact=float(agg_mpc_asset), dC_asset=float(dC_asset),
    ratio_asset_over_uniform=float(agg_mpc_asset/agg_mpc_uniform),
    diff_asset_minus_uniform=float(agg_mpc_asset-agg_mpc_uniform),
    share_at_borrowing_constraint_aLvl_lt_1e_6=float(at_constraint.mean()),
    share_MPC_gt_0p9=float((mpc>0.9).mean()),
    share_MPC_gt_0p5=float((mpc>0.5).mean()),
    mean_MPC_top_wealth_quintile=float(rows[-1]['mean_MPC']),
    mean_MPC_bottom_wealth_quintile=float(rows[0]['mean_MPC']),
    mpc_by_beta={str(beta): float(mpc[btype==beta].mean()) for beta in betas},
    mean_aLvl_by_beta={str(beta): float(a[btype==beta].mean()) for beta in betas},
)
with open('results.json','w') as f: json.dump(results,f,indent=2)
print(json.dumps(results,indent=2))
