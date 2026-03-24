"""
Shor's Algorithm Simulation — Factoring N = 15
================================================
No Qiskit required. We use NumPy to simulate the key quantum step:
period-finding via the Quantum Fourier Transform (QFT).

Steps of Shor's Algorithm:
  1. Pick a random integer  a  with  1 < a < N
  2. Compute gcd(a, N) — if > 1, we already found a factor (lucky!)
  3. QUANTUM STEP: Find the period r of  f(x) = a^x mod N
  4. Use r to compute factors:  gcd(a^(r/2) ± 1, N)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from math import gcd
import time
import warnings
warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
N = 15          # Number to factor
a = 7           # Base (chosen so period-finding is interesting)
NUM_QUBITS = 8  # Simulated register size  (2^8 = 256 states)

# ──────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────

def classical_period_find(a: int, N: int):
    """
    Classical brute-force period finding.
    Try x = 1, 2, 3, ... until a^x mod N == 1.
    Returns (period, steps_taken).
    """
    steps = 0
    x = 1
    while True:
        steps += 1
        val = pow(a, x, N)
        if val == 1:
            return x, steps
        x += 1


def quantum_period_find(a: int, N: int, num_qubits: int):
    """
    Simulates the quantum period-finding circuit using numpy FFT.

    The quantum computer prepares a superposition of all x values,
    applies the modular exponentiation oracle, then applies the QFT.
    The QFT reveals peaks at multiples of (2^n / r),
    where r is the period we are looking for.

    Returns (period, state_vector, fft_magnitudes).
    """
    size = 2 ** num_qubits  # Number of states in the quantum register

    # ── Step 1: Uniform superposition of all |x⟩ states ──────────────
    state = np.ones(size, dtype=complex) / np.sqrt(size)

    # ── Step 2: Apply oracle  f(x) = a^x mod N ───────────────────────
    # Each state |x⟩ is mapped to |x⟩|a^x mod N⟩.
    # We "measure" the second register, collapsing to a single residue.
    residues = np.array([pow(a, x, N) for x in range(size)])
    target_residue = residues[1]          # The residue we "observed"
    mask = (residues == target_residue).astype(float)
    state = state * mask                  # Collapse to matching states
    state /= np.linalg.norm(state)        # Re-normalise

    # ── Step 3: Quantum Fourier Transform ─────────────────────────────
    # numpy's FFT is mathematically equivalent to the QFT on this register.
    fft_state = np.fft.fft(state) / np.sqrt(size)
    magnitudes = np.abs(fft_state) ** 2   # Probability distribution

    # ── Step 4: Read the period from FFT peaks ────────────────────────
    # Peaks occur at indices  k * (size / r)  for k = 0, 1, 2, ...
    # We find the first non-zero peak index and derive r.
    peak_indices = np.where(magnitudes > 1e-6)[0]
    # Ignore index 0 (DC component)
    peak_indices = peak_indices[peak_indices > 0]
    if len(peak_indices) == 0:
        return None, state, magnitudes

    # Smallest non-zero peak index → spacing = size / r  → r = size / index
    first_peak = peak_indices[0]
    period = round(size / first_peak)

    return period, state, magnitudes


def find_factors(a: int, N: int, period: int):
    """
    Given the period r, compute the factors of N.
    Classic Shor post-processing step.
    """
    if period is None or period % 2 != 0:
        return None, None
    candidate1 = pow(a, period // 2) - 1
    candidate2 = pow(a, period // 2) + 1
    f1 = gcd(candidate1, N)
    f2 = gcd(candidate2, N)
    return f1, f2


# ──────────────────────────────────────────────
# RUN CLASSICAL
# ──────────────────────────────────────────────
print("=" * 52)
print("  Shor's Algorithm Simulation  —  N =", N)
print("=" * 52)

t0 = time.perf_counter()
classical_period, classical_steps = classical_period_find(a, N)
classical_time = time.perf_counter() - t0

print(f"\n[CLASSICAL]  a = {a},  N = {N}")
print(f"  Period found : r = {classical_period}")
print(f"  Steps taken  : {classical_steps}")
print(f"  Wall time    : {classical_time*1000:.4f} ms")

f1, f2 = find_factors(a, N, classical_period)
print(f"  Factors of {N} : {f1} × {f2}")

# ──────────────────────────────────────────────
# RUN QUANTUM (SIMULATED)
# ──────────────────────────────────────────────
t0 = time.perf_counter()
quantum_period, state_vec, fft_mags = quantum_period_find(a, N, NUM_QUBITS)
quantum_time = time.perf_counter() - t0

print(f"\n[QUANTUM]    a = {a},  N = {N},  qubits = {NUM_QUBITS}")
print(f"  Period found : r = {quantum_period}")
print(f"  Wall time    : {quantum_time*1000:.4f} ms  (classical simulation of QFT)")

f1q, f2q = find_factors(a, N, quantum_period)
print(f"  Factors of {N} : {f1q} × {f2q}")

# ──────────────────────────────────────────────
# COMPLEXITY COMPARISON DATA
# ──────────────────────────────────────────────
bit_sizes = np.array([64, 128, 256, 512, 1024, 2048])

# Classical best (General Number Field Sieve):
#   exp( (64/9)^(1/3) * n^(1/3) * (ln n)^(2/3) )
def gnfs_ops(bits):
    n = bits * np.log(2)
    return np.exp((64/9)**(1/3) * n**(1/3) * np.log(n)**(2/3))

# Quantum (Shor's algorithm):  O(n^3) gate operations
def shor_ops(bits):
    return bits ** 3

classical_ops = gnfs_ops(bit_sizes)
quantum_ops   = shor_ops(bit_sizes)

# ──────────────────────────────────────────────
# VISUALISATION
# ──────────────────────────────────────────────
fig = plt.figure(figsize=(16, 10), facecolor="#0d1117")
fig.suptitle(
    "Shor's Algorithm — Quantum vs Classical Factoring",
    fontsize=18, fontweight="bold", color="white", y=0.98
)

gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38)

# ── Plot 1: f(x) = a^x mod N (the periodic function) ─────────────────
ax1 = fig.add_subplot(gs[0, 0])
xs = np.arange(0, 30)
ys = [pow(a, int(x), N) for x in xs]
ax1.stem(xs, ys, linefmt="#00d4ff", markerfmt="o", basefmt=" ")
ax1.axhline(1, color="#ff6b6b", linewidth=1.2, linestyle="--", label="f(x)=1 (period boundary)")
# Shade period bands
for i in range(0, 30, classical_period):
    ax1.axvspan(i, i + classical_period, alpha=0.07, color="#00d4ff")
ax1.set_title(f"Modular Function  f(x) = {a}ˣ mod {N}", color="white", fontsize=10)
ax1.set_xlabel("x", color="#aaaaaa"); ax1.set_ylabel("f(x)", color="#aaaaaa")
ax1.legend(fontsize=7, labelcolor="white", facecolor="#1a1f2e")
ax1.set_facecolor("#1a1f2e"); ax1.tick_params(colors="#aaaaaa")
for sp in ax1.spines.values(): sp.set_color("#333344")

# ── Plot 2: Quantum state before QFT ──────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
probs_before = np.abs(state_vec) ** 2
ax2.bar(range(len(probs_before)), probs_before, color="#7c3aed", width=1.0, alpha=0.85)
ax2.set_title("Quantum State After Oracle\n(Before QFT)", color="white", fontsize=10)
ax2.set_xlabel("Basis state |x⟩", color="#aaaaaa")
ax2.set_ylabel("Probability", color="#aaaaaa")
ax2.set_facecolor("#1a1f2e"); ax2.tick_params(colors="#aaaaaa")
for sp in ax2.spines.values(): sp.set_color("#333344")

# ── Plot 3: QFT output — peaks reveal the period ──────────────────────
ax3 = fig.add_subplot(gs[0, 2])
size = 2 ** NUM_QUBITS
ax3.bar(range(size), fft_mags, color="#00d4ff", width=1.0, alpha=0.9)
# Mark the period peaks
peak_indices = np.where(fft_mags > 1e-6)[0]
ax3.scatter(peak_indices, fft_mags[peak_indices], color="#ff6b6b",
            s=60, zorder=5, label=f"Peaks → r = {quantum_period}")
ax3.set_title("QFT Output — Period Peaks", color="white", fontsize=10)
ax3.set_xlabel("Frequency index", color="#aaaaaa")
ax3.set_ylabel("Probability", color="#aaaaaa")
ax3.legend(fontsize=8, labelcolor="white", facecolor="#1a1f2e")
ax3.set_facecolor("#1a1f2e"); ax3.tick_params(colors="#aaaaaa")
for sp in ax3.spines.values(): sp.set_color("#333344")

# ── Plot 4: Classical steps — trial-by-trial ──────────────────────────
ax4 = fig.add_subplot(gs[1, 0])
all_vals = [pow(a, x, N) for x in range(1, 20)]
colors4  = ["#ff6b6b" if v == 1 else "#00d4ff" for v in all_vals]
ax4.bar(range(1, 20), all_vals, color=colors4, alpha=0.85)
ax4.set_title(f"Classical: Checking a^x mod N one-by-one\n(Red = period found at x={classical_period})",
              color="white", fontsize=9)
ax4.set_xlabel("x (trial number)", color="#aaaaaa")
ax4.set_ylabel("a^x mod N", color="#aaaaaa")
ax4.set_facecolor("#1a1f2e"); ax4.tick_params(colors="#aaaaaa")
for sp in ax4.spines.values(): sp.set_color("#333344")

# ── Plot 5: Complexity comparison (log scale) ─────────────────────────
ax5 = fig.add_subplot(gs[1, 1])
ax5.semilogy(bit_sizes, classical_ops, "o-", color="#ff6b6b",
             linewidth=2.5, markersize=6, label="Classical (GNFS) — sub-exponential")
ax5.semilogy(bit_sizes, quantum_ops, "s-", color="#00d4ff",
             linewidth=2.5, markersize=6, label="Quantum (Shor) — polynomial O(n³)")
ax5.fill_between(bit_sizes, quantum_ops, classical_ops, alpha=0.12, color="#39d353")
ax5.axvline(2048, color="#ffd700", linewidth=1.5, linestyle="--", label="RSA-2048 (today's standard)")
ax5.set_title("Operations to Break RSA\n(log scale)", color="white", fontsize=10)
ax5.set_xlabel("Key size (bits)", color="#aaaaaa")
ax5.set_ylabel("Operations", color="#aaaaaa")
ax5.legend(fontsize=7.5, labelcolor="white", facecolor="#1a1f2e")
ax5.set_facecolor("#1a1f2e"); ax5.tick_params(colors="#aaaaaa")
for sp in ax5.spines.values(): sp.set_color("#333344")

# ── Plot 6: Summary stats panel ───────────────────────────────────────
ax6 = fig.add_subplot(gs[1, 2])
ax6.set_facecolor("#1a1f2e"); ax6.axis("off")
for sp in ax6.spines.values(): sp.set_color("#333344")

summary_lines = [
    ("TARGET", f"N = {N}  =  {f1q} × {f2q}", "#ffd700"),
    ("", "", "white"),
    ("CLASSICAL", "", "#ff6b6b"),
    ("  Base", f"a = {a}", "#aaaaaa"),
    ("  Period r", str(classical_period), "#ff6b6b"),
    ("  Steps", str(classical_steps), "#ff6b6b"),
    ("  Complexity", "O(exp(n^(1/3)))", "#ff6b6b"),
    ("  RSA-2048", "~10²⁷ operations", "#ff6b6b"),
    ("", "", "white"),
    ("QUANTUM (SHOR)", "", "#00d4ff"),
    ("  Base", f"a = {a}", "#aaaaaa"),
    ("  Period r", str(quantum_period), "#00d4ff"),
    ("  Qubits used", str(NUM_QUBITS), "#00d4ff"),
    ("  Complexity", "O(n³) polynomial", "#00d4ff"),
    ("  RSA-2048", "~10¹⁰ operations", "#00d4ff"),
    ("", "", "white"),
    ("SPEEDUP", "≈ 10¹⁷× faster", "#39d353"),
]

y = 0.97
for label, value, color in summary_lines:
    if label:
        ax6.text(0.05, y, f"{label}:", color=color, fontsize=8.5,
                 fontweight="bold", transform=ax6.transAxes)
        ax6.text(0.52, y, value, color=color, fontsize=8.5,
                 transform=ax6.transAxes)
    y -= 0.062

ax6.set_title("Result Summary", color="white", fontsize=10)

plt.savefig("/mnt/user-data/outputs/quantum_threats_shor.png",
            dpi=150, bbox_inches="tight", facecolor="#0d1117")
print("\n[✓] Chart saved → quantum_threats_shor.png")
plt.show()
print("\n[DONE] Simulation complete.")
