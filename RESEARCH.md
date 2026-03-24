# ⚛️ Quantum Threats — Research Notes

> **Topic:** Shor's Algorithm and the RSA-2048 Problem
> **Date:** March 2026

---

## 📌 What Is RSA and Why Do We Care?

Right now, almost everything you do online is protected by RSA encryption.
When you log into your bank, send an email, or open any HTTPS website — RSA is working quietly in the background.

RSA works because of one simple fact:

> Multiplying two large prime numbers together is **easy**.
> But if someone gives you the result and asks you to find the original two numbers — that is **incredibly hard**.

**Small example:**

```
17 × 19 = 323              → easy to compute
Given 323, find 17 and 19  → takes effort, but doable for small numbers
```

Now imagine instead of 17 and 19, you are using numbers that are **hundreds of digits long**.
That is RSA-2048. The "2048" means the key is 2048 bits long.
Even the fastest classical computer on Earth would need **millions of years** to crack it.

That is why we trust it.

---

## 💥 The Problem — Quantum Computers

In **1994**, a mathematician named **Peter Shor** published an algorithm
that can break RSA dramatically faster — but only on a quantum computer.

The difference in speed is not just "a little faster."
It is so extreme that the comparison barely makes sense.

| Approach | Method | Operations Needed | Time Estimate |
|---|---|---|---|
| Classical Computer | GNFS Algorithm | ~10²⁷ | Millions of years |
| Quantum Computer | Shor's Algorithm | ~10¹⁰ | Hours |
| **Speedup** | | **~10¹⁷ ×** | |

That gap — **10¹⁷** — is not an upgrade. That is a completely different world.

---

## 🧠 How Shor's Algorithm Works (In Simple Words)

Forget the math for a second. Here is the intuition.

**Step 1 — Pick a random number and look for a pattern**

Say you want to factor `N = 15`. You pick `a = 7` and start computing:

```
7^1 mod 15 = 7
7^2 mod 15 = 4
7^3 mod 15 = 13
7^4 mod 15 = 1   ← back to 1
7^5 mod 15 = 7   ← repeats!
```

The sequence repeats every **4 steps**. The period is `r = 4`.

**Step 2 — Use the period to find the factors**

```python
from math import gcd

gcd(7**2 - 1, 15)  # → gcd(48, 15) = 3  ✓
gcd(7**2 + 1, 15)  # → gcd(50, 15) = 5  ✓

# Result: 15 = 3 × 5
```

**Step 3 — The key question: how do you find the period?**

- **Classical computer** → checks one step at a time. Slow. For large numbers the period can be astronomically long.
- **Quantum computer** → checks all steps *at the same time* using superposition, then uses the **Quantum Fourier Transform** to read the period in one shot.

It is like the difference between:
- Reading every page of a book one by one to find a name
- Reading all pages simultaneously and the answer just appears

That is genuinely what quantum computers do here.

---

## 🔬 The Quantum Steps (Still Simple)

```
1. Create superposition     →  quantum register holds ALL values of x at once
2. Apply the oracle         →  compute a^x mod N for all x simultaneously  
3. Quantum Fourier Transform→  interference reveals the period as bright peaks
4. Measure                  →  read off the period r
5. Classical math           →  gcd(a^(r/2) ± 1, N) gives the prime factors
```

The expensive part classically (finding the period) becomes cheap quantumly.
Everything else is just regular math.

---

## 🛡️ Why We Are Not Panicking Yet

Shor's Algorithm needs a **large, stable quantum computer** to run on.
Today's machines are noisy and error-prone.

```
Current state (2026):
  IBM / Google hardware  →  ~1,000 physical qubits
  Needed to break RSA-2048  →  ~4,000 stable logical qubits
  Logical qubit cost    →  ~1,000 physical qubits each (error correction)
  Physical qubits needed in total  →  millions
```

We are not there yet. But the field is moving fast.
Most experts say it is a question of **when**, not **if**.

---

## 🔐 What Is Being Done About It

The world is already preparing.

In **2024**, NIST finalized new encryption standards designed to be safe
even against quantum computers. These are called **post-quantum cryptography**.

| Algorithm | Purpose | Safe From Quantum? |
|---|---|---|
| RSA-2048 | Key exchange + signatures | ❌ Broken by Shor's |
| CRYSTALS-Kyber | Key exchange | ✅ Yes |
| CRYSTALS-Dilithium | Digital signatures | ✅ Yes |

These new algorithms use different math problems that Shor's Algorithm cannot touch.
Governments and companies are quietly migrating to them right now —
the same way HTTPS replaced HTTP a decade ago.

---

## 📋 Quick Summary

- **RSA** keeps the internet secure by using hard-to-factor large numbers
- **Shor's Algorithm** on a quantum computer can factor them exponentially faster
- Classical computers need **~10²⁷ operations** for RSA-2048
- Quantum computers need only **~10¹⁰ operations** for RSA-2048
- The speedup is **~10¹⁷ times** — an almost incomprehensible gap
- We do not have powerful enough quantum computers **yet**, but the timeline is shrinking
- **Post-quantum encryption standards** are already being deployed as a precaution

> **The bottom line:**
> Quantum computing does not break *all* encryption.
> But it breaks the most widely used kind.
> And that is a very big deal.
