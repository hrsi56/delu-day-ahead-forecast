import numpy as np


def gaussian_elimination_solve(A, b, verbose=True):
    """
    פותר Ax = b בשיטת אלימינציית גאוס עם pivoting חלקי (partial pivoting),
    ולאחר מכן back substitution. מדפיס כל שלב אם verbose=True.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).reshape(-1, 1)
    n = A.shape[0]
    Aug = np.hstack([A, b])

    if verbose:
        print("מטריצה מורחבת התחלתית [A | b]:")
        print(Aug)
        print()

    # Forward elimination עם partial pivoting
    for k in range(n):
        pivot_row = np.argmax(np.abs(Aug[k:, k])) + k
        if pivot_row != k:
            Aug[[k, pivot_row]] = Aug[[pivot_row, k]]
            if verbose:
                print(f"Pivoting: החלפת שורה {k} עם שורה {pivot_row}")

        pivot = Aug[k, k]
        if abs(pivot) < 1e-12:
            raise ValueError("המטריצה סינגולרית (או קרובה לכך) — אין פתרון יחיד")

        for i in range(k + 1, n):
            factor = Aug[i, k] / pivot
            Aug[i, k:] -= factor * Aug[k, k:]
            if verbose:
                print(f"R{i} <- R{i} - ({factor:.4f}) * R{k}")

        if verbose:
            print(Aug)
            print()

    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Aug[i, -1] - Aug[i, i + 1:n] @ x[i + 1:n]) / Aug[i, i]

    return x


if __name__ == "__main__":
    # מערכת קלאסית עם פתרון ידוע: x = (2, 3, -1)
    A = [[2, 1, -1],
         [-3, -1, 2],
         [-2, 1, 2]]
    b = [8, -11, -3]

    x = gaussian_elimination_solve(A, b)
    print("פתרון x̂ =", x)

    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)
    residual = A_np @ x - b_np
    print("בדיקה: A x̂ - b (אמור להיות ~0) =", residual)

    print("\nהשוואה מול np.linalg.solve:", np.linalg.solve(A_np, b_np))
