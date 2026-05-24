## 2026-05-07 - NumPy Scalar Fast-Paths
**Learning:** When introducing scalar fast-paths in scientific computing functions to avoid NumPy overhead (using `isinstance(M, (int, float, np.number))`), it is crucial to explicitly check for 0-dimensional NumPy arrays (`isinstance(M, np.ndarray) and M.ndim == 0`). If these fall through to array logic that performs boolean masking (`arr[valid] = ...`), they trigger an `IndexError: too many indices for array`.
**Action:** Always ensure 0-D array edge-cases are safely funneled into the scalar logic or handled by `np.atleast_1d` before array operations.

## 2026-05-15 - Fast-path Polymorphism via `try/except ValueError`
**Learning:** When creating math functions intended to support both standard scalars and NumPy arrays, you can use a `try...except ValueError:` block containing a boolean comparison (e.g., `if M < 1.0:`) as a highly efficient polymorphism technique. Scalars will evaluate normally, while NumPy arrays will raise the ambiguous truth value `ValueError`, safely falling through to vectorized logic without the overhead of `isinstance` or `np.asarray` checks.
**Action:** Use the `try/except ValueError` pattern around a simple comparison when implementing dual scalar/array mathematical functions to achieve a significant speedup for scalar inputs.

## 2024-05-19 - Numpy Array Fast Path Polymorphism
**Learning:** In highly mathematical Python functions relying on NumPy arrays (like `rankine` isentropic flow calculations), adding a simple `if M == 0` scalar fast path can throw a `ValueError` for array inputs. To cleanly handle both scalars and arrays without explicit `isinstance` checks (which are slow), you can use an EAFP pattern: wrap the fast scalar operations (`m_sq = M * M`) in a `try...except (ValueError, TypeError): pass` block. It handles array logic (`ValueError`) and Python list logic (`TypeError`) cleanly while bypassing the performance penalty of `pow(M, 2)` for scalars.
**Action:** Always wrap standard scalar math fast-paths using a `try...except (ValueError, TypeError): pass` block when poly-morphic math functions need to process both fast scalars and slower numpy arrays/lists.
## 2024-05-21 - Matplotlib Plot Layout Initialization
**Learning:** In Matplotlib (>= 3.6.0), calling `fig.tight_layout()` or `plt.tight_layout()` after plotting triggers a secondary layout computation and an expensive re-draw.
**Action:** To significantly speed up plot generation, pass the `layout='tight'` parameter directly during initialization (e.g., `plt.subplots(layout='tight')`) to calculate the optimal layout just-in-time during the primary draw pipeline.

## 2024-05-23 - NumPy Polymorphic Math Optimization
**Learning:** When attempting to optimize functions that handle both scalars and NumPy arrays, avoid brittle type-checking or hacky `try/except ValueError` blocks on mathematical operations. Instead, rely on universally faster math constructs like replacing `M**2` with `M * M` and replacing `(** -1.0)` with direct division `1.0 / (...)`. These mathematical identities execute faster across both data types without any branching logic.
**Action:** Always prefer direct division operations (`1.0 / M`) over negative exponentiation (`M ** -1.0`), and multiplication (`M * M`) over exponentiation (`M ** 2`), letting NumPy and Python natively handle the polymorphism.

## 2026-05-30 - EAFP Polymorphism over `isinstance` overhead
**Learning:** In highly mathematical Python functions serving both scalars and numpy arrays, explicitly checking types with `isinstance` and `np.asarray` adds significant overhead (often halving performance for scalars). The Pythonic "Easier to Ask for Forgiveness than Permission" (EAFP) pattern using `try/except ValueError` naturally bifurcates the execution path. For example, a scalar evaluates normally, while a NumPy array triggers a `ValueError` on ambiguous boolean logic (e.g., `M > 1.0`), safely falling through to the vectorized logic.
**Action:** Replace `isinstance` checks with a `try/except (ValueError, TypeError)` wrapper around a fast mathematical path for scalars.
