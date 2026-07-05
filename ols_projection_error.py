import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def solve_normal_equations(A, b):
    """
    פותר את בעיית הריבועים הפחותים ע"י המשוואות הנורמליות:
    A^T A x = A^T b
    ומחזיר גם את ההיטל p=Ax̂ וגם את וקטור השגיאה e=b-p.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    AtA = A.T @ A
    Atb = A.T @ b
    x_hat = np.linalg.solve(AtA, Atb)
    p = A @ x_hat
    e = b - p
    return x_hat, p, e, AtA, Atb


if __name__ == "__main__":
    # A היא 3x2 (עמודות בת"ל, full column rank) ; b מחוץ ל-C(A)
    A = np.array([[1, 0],
                  [0, 1],
                  [1, 1]], dtype=float)
    b = np.array([1, 2, 4], dtype=float)

    x_hat, p, e, AtA, Atb = solve_normal_equations(A, b)

    print("A^T A =\n", AtA)
    print("A^T b =", Atb)
    print("x̂ (פתרון ריבועים פחותים) =", x_hat)
    print("p = A x̂  (ההיטל של b על C(A)) =", p)
    print("e = b - p  (וקטור השגיאה) =", e)

    orth_check = A.T @ e
    print("בדיקת ניצבות A^T e (צריך ≈0):", orth_check)

    x_lstsq, *_ = np.linalg.lstsq(A, b, rcond=None)
    print("בדיקה מול np.linalg.lstsq:", x_lstsq)
    print("||e||^2 (שארית ריבועית מינימלית) =", e @ e)

    # ---------------- ציור תלת-ממדי ----------------
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")
    origin = np.zeros(3)

    a1, a2 = A[:, 0], A[:, 1]
    ss = np.linspace(-1, 5, 10)
    tt = np.linspace(-1, 5, 10)
    S, T = np.meshgrid(ss, tt)
    plane = np.array([S.flatten() * a1[i] + T.flatten() * a2[i] for i in range(3)])
    ax.plot_trisurf(plane[0], plane[1], plane[2], alpha=0.15, color="gray")

    def draw_vec(v, color, label):
        ax.quiver(*origin, *v, color=color, linewidth=2, arrow_length_ratio=0.08)
        ax.text(*(v * 1.05), label, color=color, fontsize=12)

    draw_vec(b, "red", "b")
    draw_vec(p, "blue", "p = Ax̂")
    draw_vec(e, "green", "e = b-p")
    draw_vec(a1, "gray", "a1")
    draw_vec(a2, "gray", "a2")

    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax.set_title("Orthogonal projection of b onto C(A); error vector e is orthogonal to C(A)")
    plt.tight_layout()
    plt.savefig("ols_projection_error.png", dpi=150)
    print("\nהגרף נשמר בשם ols_projection_error.png")
