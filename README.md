# Quantum Threats — Shor's Algorithm vs RSA

A clean, minimal simulation showing **why quantum computers threaten RSA encryption** — using only Python + NumPy. No Qiskit required.

---

## 🔍 What This Project Does

1. **Research**: Compares classical vs quantum time-complexity to break RSA-2048  
2. **Simulation**: Runs Shor's algorithm to factor N = 15 (both classically and with a simulated QFT)  
3. **Visualization**: 6-panel chart showing the period-finding process and the massive speedup

---

## 📊 The Core Idea

RSA encryption is secure because **factoring large numbers is hard** for classical computers.

Shor's Algorithm changes that completely:

| Approach | Algorithm | Complexity | Operations for RSA-2048 |
|---|---|---|---|
| Classical | GNFS (best known) | sub-exponential `exp(n^1/3)` | ~10²⁷ operations |
| Quantum | Shor's Algorithm | polynomial `O(n³)` | ~10¹⁰ operations |
| **Speedup** | | | **≈ 10¹⁷ × faster** |

---

## 🧠 How Shor's Algorithm Works

```
Given N = p × q (RSA public key), pick a random base  a < N

Step 1 ─ Sanity check:   gcd(a, N) > 1  →  already found a factor!
Step 2 ─ QUANTUM STEP:   Find the period r  of  f(x) = a^x mod N
           The QFT creates a superposition over all x values at once,
           then reveals the period through interference peaks.
Step 3 ─ Math magic:     gcd(a^(r/2) ± 1, N)  gives the prime factors
```

**Example with N = 15, a = 7:**
```
f(x) = 7^x mod 15:  7, 4, 13, 1, 7, 4, 13, 1, ...
                                    ↑
                              period r = 4

gcd(7² - 1, 15) = gcd(48, 15) = 3   ✓
gcd(7² + 1, 15) = gcd(50, 15) = 5   ✓

15 = 3 × 5
```

---

## 📈 Output Charts

The script generates a 6-panel figure:

| Panel | What it shows |
|---|---|
| Top-left | The periodic function f(x) = a^x mod N |
| Top-middle | Quantum state vector **after** the oracle (before QFT) |
| Top-right | QFT output — bright peaks reveal the period |
| Bottom-left | Classical brute-force — checking one x at a time |
| Bottom-middle | Complexity comparison on a log scale across key sizes |
| Bottom-right | Result summary (factors found, steps, speedup) |

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/your-username/quantum-threats-shor
cd quantum-threats-shor

# 2. Install dependencies  (only 2!)
pip install numpy matplotlib

# 3. Run
python shor_simulation.py
```

That's it. The chart saves automatically as `quantum_threats_shor.png`.

---

## 📁 File Structure

```
quantum-threats-shor/
├── shor_simulation.py   ← main simulation + visualization
├── quantum_threats_shor.png  ← output chart (auto-generated)
└── README.md
```

---

## 🔧 Customization

Open `shor_simulation.py` and change the top config block:

```python
N = 15          # Try 21 (= 3 × 7) for a different example
a = 7           # Base integer — must satisfy gcd(a, N) == 1
NUM_QUBITS = 8  # Simulated register size (2^8 = 256 states)
```

**Try N = 21:**
- Valid bases: 2, 4, 5, 8, 10, 11, 13, 16, 17, 19, 20
- Example: `N = 21, a = 2`  →  period = 6  →  factors: 3 × 7

---

## ⚠️ Why This Matters for Cybersecurity

- **RSA-2048** is used to secure HTTPS, SSH, email, banking, and more
- A quantum computer with ~4,000 stable logical qubits could break it in **hours**
- Today's best quantum hardware has ~1,000 noisy physical qubits — not there yet
- NIST finalized **post-quantum cryptography standards** in 2024 (CRYSTALS-Kyber, CRYSTALS-Dilithium) to prepare

---

## 📚 Key Concepts

- **Quantum superposition** — a qubit can be 0 and 1 simultaneously
- **Quantum interference** — wrong answers cancel out, right answers amplify
- **Quantum Fourier Transform (QFT)** — the quantum equivalent of FFT; reveals periodicity in O(n²) gates vs O(n·2ⁿ) classically
- **Period finding** → integer factoring (Shor's reduction, 1994)

---

## 🛠️ Dependencies

```
python >= 3.8
numpy
matplotlib
```

No Qiskit. No quantum hardware. Just the math.

---

## 📄 License

MIT — free to use, modify, and share.
