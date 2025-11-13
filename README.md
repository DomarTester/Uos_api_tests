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

## ⚙️ Setup

1. Clone the repository or extract the ZIP.
2. Navigate to the project directory.
3. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate   # On macOS/Linux
.venv\Scripts\activate      # On Windows
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔧 Configuration
Edit the .env file with your UniFi (UOS) details. Use the '.env.sample' file as a template.

## ▶️ Run Tests
Basic Run
```bash
pytest -v
```
Generate Allure Report
```bash
pytest -v --alluredir=./reports
```
