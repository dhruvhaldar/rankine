## 2026-05-07 - NumPy Scalar Fast-Paths
**Learning:** When introducing scalar fast-paths in scientific computing functions to avoid NumPy overhead (using `isinstance(M, (int, float, np.number))`), it is crucial to explicitly check for 0-dimensional NumPy arrays (`isinstance(M, np.ndarray) and M.ndim == 0`). If these fall through to array logic that performs boolean masking (`arr[valid] = ...`), they trigger an `IndexError: too many indices for array`.
**Action:** Always ensure 0-D array edge-cases are safely funneled into the scalar logic or handled by `np.atleast_1d` before array operations.

## 2026-05-15 - Fast-path Polymorphism via `try/except ValueError`
**Learning:** When creating math functions intended to support both standard scalars and NumPy arrays, you can use a `try...except ValueError:` block containing a boolean comparison (e.g., `if M < 1.0:`) as a highly efficient polymorphism technique. Scalars will evaluate normally, while NumPy arrays will raise the ambiguous truth value `ValueError`, safely falling through to vectorized logic without the overhead of `isinstance` or `np.asarray` checks.
**Action:** Use the `try/except ValueError` pattern around a simple comparison when implementing dual scalar/array mathematical functions to achieve a significant speedup for scalar inputs.

## 2024-05-19 - Numpy Array Fast Path Polymorphism
**Learning:** In highly mathematical Python functions relying on NumPy arrays (like `rankine` isentropic flow calculations), adding a simple `if M == 0` scalar fast path can throw a `ValueError` for array inputs. To cleanly handle both scalars and arrays without explicit `isinstance` checks (which are slow), you can use an EAFP pattern: wrap the fast scalar operations (`m_sq = M * M`) in a `try...except (ValueError, TypeError): pass` block. It handles array logic (`ValueError`) and Python list logic (`TypeError`) cleanly while bypassing the performance penalty of `pow(M, 2)` for scalars.
**Action:** Always wrap standard scalar math fast-paths using a `try...except (ValueError, TypeError): pass` block when poly-morphic math functions need to process both fast scalars and slower numpy arrays/lists.
