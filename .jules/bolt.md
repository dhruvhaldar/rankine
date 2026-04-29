## 2026-04-29 - [SciPy Root-Finding Inlining]
**Learning:** When using numerical root-finders (like `scipy.optimize.brentq`) that pass scalar values to a residual function, using `numpy` functions (e.g., `np.sqrt`, `np.sin`) inside the closure introduces severe scalar dispatch overhead, drastically slowing down evaluation.
**Action:** Replace `numpy` mathematical functions with their standard Python `math` library equivalents (`math.sqrt`, `math.sin`) inside high-frequency root-finding closures to often yield a ~20-30% speedup in solver loops.
