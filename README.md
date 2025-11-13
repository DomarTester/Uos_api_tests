# 🧪 UOS Server Integration API Test Suite

This repository contains a **pytest-based test suite** for validating the **UOS Server Integration API**.

It covers a complete workflow using `GET`, `POST`, and `DELETE` operations — focused on **Hotspot Vouchers** — with proper setup and cleanup to simulate realistic API behavior.

---

## 🧰 Tech Stack

- **Language:** Python 3.10+
- **Framework:** pytest
- **HTTP Client:** requests
- **Env Loader:** python-dotenv
- **Reports (optional):** allure-pytest

---

## 📋 Prerequisites

1. **Python 3.10+**
   - Verify installation:
     ```bash
     python3 --version   # Linux/macOS
     python --version    # Windows
     ```
   - If Python is missing, install it from [https://www.python.org/downloads/](https://www.python.org/downloads/).

2. **pip (Python package manager)**
   - Usually comes with Python.
   - Upgrade pip:
     ```bash
     python3 -m pip install --upgrade pip  # Linux/macOS
     python -m pip install --upgrade pip   # Windows
     ```
3. **UOS Server (UniFi OS) with an active API and a generated API key** 


## ⚙️ Setup

1. Clone the repository or extract the ZIP.
2. Navigate to the project directory.
3. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
.venv\Scripts\activate      # On Windows
```
or
```bash
python3 -m venv .venv
source .venv/bin/activate   # On macOS/Linux
```


4. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔧 Configuration
Create and edit the .env file with your UniFi (UOS) details. Use the '.env.sample' file as a template.

## ▶️ Run Tests
Basic Run
```bash
pytest -v
```
Generate Allure Report
```bash
pytest -v --alluredir=./reports
```
