# Byzantium — Terminal Demo

_Byzantium_ is a terminal-based sandbox for exploring **salt, burn, ash, and defection** — a UI harness for a larger system that treats coordination, history, and authority very differently than traditional Byzantine-style models.

This repository contains **a runnable demo**, not the full cryptographic protocol.

---

![Title screen](Screenshots/SS1.png)

---

## What This Is

- A **single-file terminal demo**
- A **rules + interaction sandbox**
- A **UI lens** into a system built around overwrite, residue, and consequence

This demo intentionally favors:
- legibility
- determinism
- minimal input
- visible pressure

It does **not** implement cryptographic validation, networking, or persistence.  
Those live in the broader *ObliviousCompute* project and will be integrated later.

---

![Text feed](Screenshots/SS2.png)

---

## What This Is Not

- Not a finished protocol
- Not a multiplayer system
- Not cryptographically secure (yet)
- Not a consensus engine

Think of this as **wrapping paper**, not the gift.

---

![Clear feed and Monuments](Screenshots/SS3.png)

---

## Running the Demo

### Requirements

- Python **3.9+**
- A UNIX-like terminal environment

### Supported Platforms

- macOS ✅
- Linux ✅

### Not Supported

- Windows ❌  

(Sorry — not sorry. This demo relies on terminal behavior and ANSI handling that Windows does not provide cleanly.)

---

![In-game Lore page](Screenshots/SS4.png)

---

### Run

From the `Byzantium/` directory:

```bash
python3 ByzantiumDEMO.py
