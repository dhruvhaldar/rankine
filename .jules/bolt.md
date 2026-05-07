## 2026-05-07 - NumPy Scalar Fast-Paths
**Learning:** When introducing scalar fast-paths in scientific computing functions to avoid NumPy overhead (using `isinstance(M, (int, float, np.number))`), it is crucial to explicitly check for 0-dimensional NumPy arrays (`isinstance(M, np.ndarray) and M.ndim == 0`). If these fall through to array logic that performs boolean masking (`arr[valid] = ...`), they trigger an `IndexError: too many indices for array`.
**Action:** Always ensure 0-D array edge-cases are safely funneled into the scalar logic or handled by `np.atleast_1d` before array operations.
