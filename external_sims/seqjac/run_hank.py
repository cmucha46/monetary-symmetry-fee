"""
One-asset HANK (shade-econ/sequence-jacobian v1.0.0, notebooks/hank.ipynb)
replicated in code, plus the sec.IX fiscal-incidence adaptation.

BASELINE (verbatim from hank.ipynb):
  fiscal(r, B): Tax = r * B          # interest burden charged to households
  transfers hetinput: Div and Tax both allocated proportional to skill e;
                      households hold bonds and receive (1+r)*a(-1), i.e.
                      interest income is allocated proportional to ASSETS a.
  Calibration: nE=7, nA=500 (grid arg), rstar=0.005, phi=1.5, B=5.6, Y=1.

ADAPTATION (NOT a shipped experiment):
  Variant model adds two exogenous sequences to the fiscal block:
    GTR  = aggregate government transfer paid FLAT (equal per household,
           T_add(e) = GTR for every skill state; aggregate = GTR since
           population weights pi_e sum to 1)
    GTAX = aggregate lump-sum tax financing, charged through the shipped
           tax rule (proportional to skill e)
    fiscal2: Tax = r*B + GTAX
    transfers2: T = div(e) - tax(e) + GTR   (flat payout added)

  Run A (interest-financed): baseline model, rstar shock. Households pay
    Tax = r*B (proportional to skill) and receive the interest (1+r)*a(-1)
    (proportional to assets -> concentrated on wealthy, low-MPC holders).
    The rstar path is scaled ex post (linear model: scaling is exact) so
    the REALIZED present value of the interest flow, sum_t dr_t*B/(1+r)^t,
    equals the target PV of runs B/C.
  Run B (transfer-recycled, tax-financed): GTR = GTAX = X_t.
    Same gross PV, same tax rule (proportional to skill) as A; only the
    recipient incidence differs (flat per household instead of per asset).
    Net aggregate household transfer = 0, exactly as in A.
    => B - A is the PURE REDISTRIBUTION contrast.
  Run C (pure recycling, auxiliary decomposition): GTR = X_t, GTAX = 0.
    Same flat payout as B, but financed OUTSIDE the household sector
    (the fee-on-the-financial-sector case of the actual proposal; this
    textbook model has no bank sector, so the charge has no household
    counterpart). => C - B is the RECYCLING (aggregate-injection) term.

  Common gross flow: X_t = X0 * rho^t, X0 = 0.01 (1% of steady-state Y per
  quarter initially), rho = 0.8, horizon T = 300 quarters.
  PV target = sum_t X_t / (1+r_ss)^t.
"""
import sys, json, time
import numpy as np
from sequence_jacobian import simple, create_model, hetblocks, grids

hh = hetblocks.hh_labor.hh
T_HORIZON = 300
X0, RHO = 0.01, 0.8
NA = int(sys.argv[1]) if len(sys.argv) > 1 else 500
OUT = {}

# ---------------- notebook blocks (verbatim) ----------------
def make_grid(rho_e, sd_e, nE, amin, amax, nA):
    e_grid, pi_e, Pi = grids.markov_rouwenhorst(rho=rho_e, sigma=sd_e, N=nE)
    a_grid = grids.agrid(amin=amin, amax=amax, n=nA)
    return e_grid, pi_e, Pi, a_grid

def transfers(pi_e, Div, Tax, e_grid):
    tax_rule, div_rule = e_grid, e_grid
    div = Div / np.sum(pi_e * div_rule) * div_rule
    tax = Tax / np.sum(pi_e * tax_rule) * tax_rule
    T = div - tax
    return T

def wages(w, e_grid):
    we = w * e_grid
    return we

def labor_supply(n, e_grid):
    ne = e_grid[:, np.newaxis] * n
    return ne

@simple
def firm(Y, w, Z, pi, mu, kappa):
    L = Y / Z
    Div = Y - w * L - mu/(mu-1)/(2*kappa) * (1+pi).apply(np.log)**2 * Y
    return L, Div

@simple
def monetary(pi, rstar, phi):
    r = (1 + rstar(-1) + phi * pi(-1)) / (1 + pi) - 1
    return r

@simple
def fiscal(r, B):
    Tax = r * B
    return Tax

@simple
def mkt_clearing(A, NE, C, L, Y, B, pi, mu, kappa):
    asset_mkt = A - B
    labor_mkt = NE - L
    goods_mkt = Y - C - mu/(mu-1)/(2*kappa) * (1+pi).apply(np.log)**2 * Y
    return asset_mkt, labor_mkt, goods_mkt

@simple
def nkpc_ss(Z, mu):
    w = Z / mu
    return w

@simple
def nkpc(pi, w, Z, Y, r, mu, kappa):
    nkpc_res = kappa * (w / Z - 1 / mu) + Y(+1) / Y * (1 + pi(+1)).apply(np.log) / (1 + r(+1)) \
               - (1 + pi).apply(np.log)
    return nkpc_res

# ---------------- variant (adaptation) blocks ----------------
def transfers2(pi_e, Div, Tax, GTR, e_grid):
    tax_rule, div_rule = e_grid, e_grid
    div = Div / np.sum(pi_e * div_rule) * div_rule
    tax = Tax / np.sum(pi_e * tax_rule) * tax_rule
    flat = GTR * np.ones_like(e_grid)   # equal per household; aggregate = GTR
    T = div - tax + flat
    return T

@simple
def fiscal2(r, B, GTAX):
    Tax = r * B + GTAX
    return Tax

# ---------------- build ----------------
hh_ext = hh.add_hetinputs([make_grid, transfers, wages]).add_hetoutputs([labor_supply])
# NOTE: variant household block is built only AFTER the baseline steady state
# is solved below; building two add_hetinputs blocks from the same base `hh`
# up front corrupts the first (KeyError: 'we' in steady_state).

calibration = {'eis': 0.5, 'frisch': 0.5, 'rho_e': 0.966, 'sd_e': 0.5, 'nE': 7,
               'amin': 0.0, 'amax': 150, 'nA': NA, 'Y': 1.0, 'Z': 1.0, 'pi': 0.0,
               'mu': 1.2, 'kappa': 0.1, 'rstar': 0.005, 'phi': 1.5, 'B': 5.6}
unknowns_ss = {'beta': 0.986, 'vphi': 0.8}
targets_ss = {'asset_mkt': 0, 'labor_mkt': 0}

hank_ss = create_model([hh_ext, firm, monetary, fiscal, mkt_clearing, nkpc_ss], name="HANK SS")
t0 = time.time()
ss0 = hank_ss.solve_steady_state(calibration, unknowns_ss, targets_ss, solver="hybr")
print(f"[ss] solved in {time.time()-t0:.1f}s  beta={ss0['beta']:.6f} vphi={ss0['vphi']:.6f}", flush=True)

hank = create_model([hh_ext, firm, monetary, fiscal, mkt_clearing, nkpc], name="HANK")
ss = hank.steady_state(ss0)

hh_ext2 = hh.add_hetinputs([make_grid, transfers2, wages]).add_hetoutputs([labor_supply])
cal2 = dict(calibration); cal2.update({'GTR': 0.0, 'GTAX': 0.0})
hank2_ss = create_model([hh_ext2, firm, monetary, fiscal2, mkt_clearing, nkpc_ss], name="HANK2 SS")
ss02 = hank2_ss.solve_steady_state(cal2, unknowns_ss, targets_ss, solver="hybr")
hank2 = create_model([hh_ext2, firm, monetary, fiscal2, mkt_clearing, nkpc], name="HANK2")
ss2 = hank2.steady_state(ss02)
assert np.isclose(ss['C'], ss2['C']) and np.isclose(ss['beta'], ss2['beta']), "variant ss must equal baseline ss (GTR=GTAX=0)"

ss_summary = {k: float(ss[k]) for k in ['beta', 'vphi', 'r', 'rstar', 'C', 'Y', 'A', 'B', 'w', 'pi',
                                        'Tax', 'Div', 'L', 'NE', 'asset_mkt', 'labor_mkt', 'goods_mkt']}
OUT['steady_state'] = ss_summary
print("[ss]", json.dumps(ss_summary, indent=1), flush=True)

# ---------------- MPC distribution ----------------
intern = ss.internals['hh']
D = np.asarray(intern['D']); cpol = np.asarray(intern['c']); apol = np.asarray(intern['a'])
a_grid = np.asarray(intern['a_grid']); e_grid = np.asarray(intern['e_grid'])
r_ss = float(ss['r'])
coh_grid = (1 + r_ss) * a_grid                      # c policy is over lagged assets a(-1); a transfer shifts coh 1:1
mpc = np.gradient(cpol, coh_grid, axis=1)           # dC/d(transfer) at each (e, a(-1)) state
mpc = np.clip(mpc, -0.05, 1.05)
Dmass = D / D.sum()
agg_mpc = float(np.sum(Dmass * mpc))
# population asset quintiles (by D mass over a, marginal over e)
marg_a = Dmass.sum(axis=0)
cum = np.cumsum(marg_a)
edges = [0]
for q in [0.2, 0.4, 0.6, 0.8]:
    edges.append(int(np.searchsorted(cum, q)))
edges.append(len(a_grid))
quint = []
for i in range(5):
    sl = slice(edges[i], edges[i+1] if i < 4 else len(a_grid))
    mass = marg_a[sl].sum()
    qmpc = float(np.sum(Dmass[:, sl] * mpc[:, sl]) / mass) if mass > 0 else float('nan')
    wealth_share = float(np.sum(Dmass[:, sl] * a_grid[sl][None, :]) / np.sum(Dmass * a_grid[None, :]))
    quint.append({'quintile': i+1, 'a_max': float(a_grid[min(edges[i+1]-1, len(a_grid)-1)]) if i < 4 else float(a_grid[-1]),
                  'pop_mass': float(mass), 'mean_MPC': qmpc, 'wealth_share': wealth_share})
htm_share = float(marg_a[0])                        # mass at a(-1) = amin = 0
OUT['mpc'] = {'aggregate_MPC_Dweighted': agg_mpc, 'hand_to_mouth_share_at_a0': htm_share,
              'by_asset_quintile_population': quint,
              'MPC_by_skill_row_Dweighted': [float(np.sum(Dmass[i]*mpc[i])/np.sum(Dmass[i])) for i in range(D.shape[0])],
              'e_grid': e_grid.tolist()}
print("[mpc] agg", agg_mpc, "htm", htm_share, flush=True)
print("[mpc] quintiles", json.dumps(quint), flush=True)
np.savez('ss_arrays.npz', D=D, c=cpol, a=apol, a_grid=a_grid, e_grid=e_grid, mpc=mpc)

# ---------------- Jacobians / experiment ----------------
unknowns = ['pi', 'w', 'Y']
targets = ['nkpc_res', 'asset_mkt', 'labor_mkt']
tvec = np.arange(T_HORIZON)
X = X0 * RHO ** tvec
disc = (1 + r_ss) ** (-tvec)
PV_target = float(np.sum(X * disc))
OUT['experiment_setup'] = {'X0': X0, 'rho': RHO, 'T': T_HORIZON, 'nA': NA, 'PV_target': PV_target}

t0 = time.time()
G = hank.solve_jacobian(ss, unknowns, targets, ['rstar', 'Z'], T=T_HORIZON)
print(f"[jac] baseline in {time.time()-t0:.1f}s", flush=True)

# Run A: unit-ish rstar path, then exact PV scaling (linear model)
drstar_unit = 0.001 * RHO ** tvec
dr_unit = np.asarray(G['r']['rstar']) @ drstar_unit
PV_flow_unit = float(np.sum(dr_unit * float(ss['B']) * disc))
scale_A = PV_target / PV_flow_unit
def scaled(Gcol, path):
    return np.asarray(Gcol) @ path
resA = {v: scaled(G[v]['rstar'], drstar_unit) * scale_A for v in ['C', 'Y', 'pi', 'r', 'w']}
OUT['runA_realized_PV_interest_flow'] = PV_flow_unit * scale_A
OUT['runA_drstar_amplitude_scaled'] = 0.001 * scale_A
print(f"[A] PV_flow_unit={PV_flow_unit:.6e} scale={scale_A:.3f} realizedPV={PV_flow_unit*scale_A:.6f} target={PV_target:.6f}", flush=True)

t0 = time.time()
G2 = hank2.solve_jacobian(ss2, unknowns, targets, ['GTR', 'GTAX', 'rstar', 'Z'], T=T_HORIZON)
print(f"[jac] variant in {time.time()-t0:.1f}s", flush=True)
resB = {v: scaled(G2[v]['GTR'], X) + scaled(G2[v]['GTAX'], X) for v in ['C', 'Y', 'pi', 'r', 'w']}
resC = {v: scaled(G2[v]['GTR'], X) for v in ['C', 'Y', 'pi', 'r', 'w']}

def stats(x):
    x = np.asarray(x, dtype=float)
    return {'peak': float(x.max()), 'trough': float(x.min()), 'argmax': int(x.argmax()),
            'cum_sum_T300': float(x.sum()), 'cum_sum_first20q': float(x[:20].sum()),
            'cum_disc_T300': float(np.sum(x * disc))}
OUT['results'] = {}
for name, res in [('A_interest_asset_incidence', resA), ('B_transfer_flat_taxfinanced', resB), ('C_transfer_flat_unfinanced_recycling', resC)]:
    OUT['results'][name] = {'dC': stats(res['C']), 'dY': stats(res['Y']),
                            'dpi_peak_bp': float(10000*np.max(np.abs(res['pi']))),
                            'dr_peak_bp': float(10000*np.max(np.abs(res['r'])))}
    np.savez(f'irf_{name}.npz', **{k: res[k] for k in res})
redist_C = OUT['results']['B_transfer_flat_taxfinanced']['dC']['cum_sum_T300'] - OUT['results']['A_interest_asset_incidence']['dC']['cum_sum_T300']
recyc_C = OUT['results']['C_transfer_flat_unfinanced_recycling']['dC']['cum_sum_T300'] - OUT['results']['B_transfer_flat_taxfinanced']['dC']['cum_sum_T300']
redist_Y = OUT['results']['B_transfer_flat_taxfinanced']['dY']['cum_sum_T300'] - OUT['results']['A_interest_asset_incidence']['dY']['cum_sum_T300']
recyc_Y = OUT['results']['C_transfer_flat_unfinanced_recycling']['dY']['cum_sum_T300'] - OUT['results']['B_transfer_flat_taxfinanced']['dY']['cum_sum_T300']
OUT['decomposition'] = {'redistribution_BminusA_cum_dC': redist_C, 'recycling_CminusB_cum_dC': recyc_C,
                        'ratio_recycling_to_abs_redistribution_C': float(recyc_C/abs(redist_C)) if redist_C != 0 else None,
                        'redistribution_BminusA_cum_dY': redist_Y, 'recycling_CminusB_cum_dY': recyc_Y,
                        'ratio_recycling_to_abs_redistribution_Y': float(recyc_Y/abs(redist_Y)) if redist_Y != 0 else None}
print(json.dumps(OUT['results'], indent=1), flush=True)
print(json.dumps(OUT['decomposition'], indent=1), flush=True)
json.dump(OUT, open('results.json', 'w'), indent=1)
print("DONE", flush=True)
