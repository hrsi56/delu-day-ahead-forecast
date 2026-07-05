import sympy as sp


def four_subspaces(A):
    """
    מחשב בסיסים לארבעת תתי-המרחבים היסודיים של Strang עבור מטריצה A:
    - מרחב העמודות C(A)      (תת-מרחב של R^m)
    - מרחב האפס N(A)          (תת-מרחב של R^n)
    - מרחב השורות C(A^T)      (תת-מרחב של R^n)
    - מרחב האפס השמאלי N(A^T) (תת-מרחב של R^m)
    מחזיר dict עם הדרגה (rank), הממדים והבסיסים (כמטריצות sympy, אריתמטיקה מדויקת).
    """
    A = sp.Matrix(A)
    m, n = A.shape
    rank = A.rank()

    col_space = A.columnspace()
    null_space = A.nullspace()
    row_space = A.T.columnspace()
    left_null_space = A.T.nullspace()

    return {
        "shape": (m, n),
        "rank": rank,
        "dim_C(A)": rank,
        "dim_N(A)": n - rank,
        "dim_C(A^T)": rank,
        "dim_N(A^T)": m - rank,
        "C(A)_basis": col_space,
        "N(A)_basis": null_space,
        "C(A^T)_basis": row_space,
        "N(A^T)_basis": left_null_space,
    }


def print_subspaces(A):
    r = four_subspaces(A)
    m, n = r["shape"]
    print(f"מטריצה A בגודל {m}x{n}, rank(A) = {r['rank']}\n")

    print(f"C(A)  — מרחב העמודות (dim={r['dim_C(A)']}, תת-מרחב של R^{m}):")
    for v in r["C(A)_basis"]:
        print("   ", v.T.tolist()[0])

    print(f"\nN(A)  — מרחב האפס / הקרנל (dim={r['dim_N(A)']}, תת-מרחב של R^{n}):")
    if r["N(A)_basis"]:
        for v in r["N(A)_basis"]:
            print("   ", v.T.tolist()[0])
    else:
        print("    {0}  (עמודות בלתי-תלויות לינארית)")

    print(f"\nC(A^T) — מרחב השורות (dim={r['dim_C(A^T)']}, תת-מרחב של R^{n}):")
    for v in r["C(A^T)_basis"]:
        print("   ", v.T.tolist()[0])

    print(f"\nN(A^T) — מרחב האפס השמאלי / הקוקרנל (dim={r['dim_N(A^T)']}, תת-מרחב של R^{m}):")
    if r["N(A^T)_basis"]:
        for v in r["N(A^T)_basis"]:
            print("   ", v.T.tolist()[0])
    else:
        print("    {0}  (שורות בלתי-תלויות לינארית)")

    # בדיקת ניצבות בין הזוגות המשלימים (אימות משפט הממדים והאורתוגונליות)
    print("\n--- בדיקות ניצבות ---")
    for cv in r["C(A)_basis"]:
        for nv in r["N(A^T)_basis"]:
            print("C(A)·N(A^T) dot =", (cv.T * nv)[0], " (אמור=0)")
    for rv in r["C(A^T)_basis"]:
        for nv in r["N(A)_basis"]:
            print("C(A^T)·N(A) dot =", (rv.T * nv)[0], " (אמור=0)")


if __name__ == "__main__":
    # דוגמה עם דרגה חסרה (rank deficient): שורה 2 = 2*שורה 1
    A = [[1, 2, 3],
         [2, 4, 6],
         [3, 5, 7]]
    print_subspaces(A)
