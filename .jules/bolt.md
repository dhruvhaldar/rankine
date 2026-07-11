## 2024-05-18 - Brentq Exact Bounds
**Learning:** When replacing `newton` with `brentq` for bounded physical equations (e.g., Mach number >= 1.0), use the exact mathematical boundary (e.g., `1.0`) as the bracket limit if the residual function evaluates cleanly at that boundary. Using an artificially restricted bound (e.g., `1.000001`) to avoid perceived divide-by-zero risks can introduce `ValueError` regressions for valid edge cases (e.g., near-zero inputs) whose roots fall within the artificially excluded gap.
**Action:** Use exact bounds (like `1.0`) instead of epsilon-offset bounds (`1.000001`) for solvers when mathematically safe.

## 2024-05-18 - Avoid Trigonometric Inverse in Root Finding Objectives
**Learning:** In the `rankine/shocks.py` module, the `ObliqueShock.solve_beta` numerical solver originally calculated `math.atan(tan_theta) - theta == 0`. This evaluated an expensive `math.atan` inside the high-frequency `brentq` iteration loop. Transforming the objective function to evaluate `tan_theta - math.tan(theta) == 0` allowed the target tangent to be precomputed outside the loop, avoiding the expensive inverse trig function inside the loop altogether.
**Action:** Always attempt to transform root-finding objectives mathematically to move expensive evaluations (like inverse trig functions) outside the numerical solver iteration loop.
