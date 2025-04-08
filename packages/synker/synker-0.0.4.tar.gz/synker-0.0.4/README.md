# 📦 synker

**synker** is a Python package for generating synthetic datasets based on real data using Kernel Density Estimation (KDE) methods.

It supports:
- Bandwidth selection (Scott's and Silverman's rules)
- 2D KDE
- Synthetic data generation
- Kullback–Leibler (KL) divergence evaluation
- Arbitrary probability interval selection for data filtering and analysis

---

## 🚀 Features

- **Bandwidth Estimation** using Scott's and Silverman's rules  
- **2D Kernel Density Estimation**
- **Synthetic Data Generation** based on KDE
- **KL Divergence Calculation** to compare real and synthetic data
- **Probability Interval Filtering (`pinkde`)**: Identify data points within specified probability ranges
- Modular and extensible design for ease of integration

---

## 🧠 Installation

Clone the repository and install the package locally:

```bash
git clone https://github.com/dhaselib/synker
cd synker
pip install .
```

---

## 🗂 Example Usage

```python
import numpy as np
import matplotlib.pyplot as plt
from synker.scott import Scott
from synker.silverman import Silverman
from synker.kl_div import KL_div
from synker.synthetic import Synthetic
from synker.kde import kde, Pinkde
import pandas as pd

# Generate sample data
np.random.seed(42)
data = np.random.weibull(a=10, size=(1000, 2))
X = np.random.weibull(a=5, size=1000)
Y = np.random.weibull(a=20, size=1000)

# Bandwidth estimation
hx = Scott(X)
hy = Scott(Y)
# Or using Silverman's rule
# hx = Silverman(X)
# hy = Silverman(Y)

# KDE
syn_X = np.linspace(min(X), max(X), 100)
syn_Y = np.linspace(min(Y), max(Y), 100)
pkde = kde(X, Y, syn_X, syn_Y, hx, hy)

# Alternatively:
pkde = kde(X, Y, hx=hx, hy=hy, res=100)

# Generate synthetic data
synth_data = Synthetic(X=X, Y=Y, hx=hx, hy=hy, res=100)
# Or use automatic bandwidth selection
synth_data = Synthetic(X, Y, bandwidth_method="Scott")

Synth_X = synth_data[:, 0]
Synth_Y = synth_data[:, 1]

# Calculate KL divergence
KL_divergence = KL_div(real_data=data, synthetic_data=synth_data, hx=hx, hy=hy)

# Use pinkde to filter based on probability interval
grid_x = np.linspace(min(X), max(X), 100)
grid_y = np.linspace(min(Y), max(Y), 100)
min_val, max_val = 0.2, 0.5
pinkde_result = pinkde(X, Y, hx, hy, "Scott", grid_x, grid_y, 100, min_val, max_val)

# Plotting
plt.figure(figsize=(8, 8))
plt.scatter(X, Y, label="Original Data")
plt.scatter(Synth_X, Synth_Y, label="Synthetic Data")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.title("Original vs. Synthetic Data")

plt.figure(figsize=(8, 8))
plt.scatter(X, Y, label="Original Data", alpha=0.3)
plt.scatter(
    pinkde_result["X"],
    pinkde_result["Y"],
    label=f"P {min_val * 100:.0f}–{max_val * 100:.0f}%",
    color='red',
    alpha=0.3
)
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.title("Pinkde Result")
plt.show()
```

---

## ✅ Testing

A test file `test_synker.py` is included to validate core functionalities like bandwidth estimation, KDE, synthetic generation, KL divergence, and the `pinkde` module.

### Run tests:
```bash
python -m unittest test_synker.py
```

### Tests cover:
- Scott and Silverman bandwidth estimation  
- 2D KDE result structure  
- Synthetic data shape and boundary validation  
- Non-negative KL divergence check  
- Probability interval selection with `pinkde`  

---

## 📁 Project Structure

```
synker/
├── __init__.py
├── scott.py
├── silverman.py
├── kde.py
├── sampling.py
├── kl_divergence.py
├── pinkde.py
├── tests/
│   └── test_synker.py
└── README.md
```

---

## 📜 License

This project is licensed under the **MIT License**:

```
MIT License

Copyright (c) 2025 Danial Haselibozchaloee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```