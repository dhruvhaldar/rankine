## 2026-05-07 - NumPy Scalar Fast-Paths
**Learning:** When introducing scalar fast-paths in scientific computing functions to avoid NumPy overhead (using `isinstance(M, (int, float, np.number))`), it is crucial to explicitly check for 0-dimensional NumPy arrays (`isinstance(M, np.ndarray) and M.ndim == 0`). If these fall through to array logic that performs boolean masking (`arr[valid] = ...`), they trigger an `IndexError: too many indices for array`.
**Action:** Always ensure 0-D array edge-cases are safely funneled into the scalar logic or handled by `np.atleast_1d` before array operations.
## 2024-05-16 - Numpy scalar/array polymorphism and power operations
**Learning:**
1) In mathematical functions designed to accept both scalars and NumPy arrays seamlessly, wrapping a simple scalar condition like `if M == 0:` in a `try...except ValueError: pass` block is a highly efficient way to fast-path scalars while gracefully falling through to array logic (where the condition raises an ambiguous truth value ValueError).
2) While replacing `M**2` with `M * M` is famously faster for standard Python scalars (yielding ~30% speedups), it actually performs *worse* on NumPy arrays, as `**2` is highly optimized in NumPy's underlying C implementation.

**Action:** When optimizing math utilities like `calc_area_mach` that handle mixed inputs, use `try/except ValueError` for fast scalar checks. Additionally, if an operation heavily favors arrays, stick to `M**2` rather than `M * M`, or implement distinct logic branches if scalar performance is critical.
