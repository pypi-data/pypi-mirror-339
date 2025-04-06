# Nexios – The Future of Python Frameworks!

<p align="center">
  <img src="https://raw.githubusercontent.com/nexios-labs/Nexios/90122b22fdd3a57fc1146f472087d483324df0e5/docs/_media/icon.svg" width="100" alt="Nexios Logo"/>
</p>

**The lightweight, blazing-fast Python framework you've been waiting for!**

[![GitHub stars](https://img.shields.io/github/stars/nexios-labs/Nexios?style=for-the-badge&logo=github)](https://github.com/nexios-labs/nexios)  
[![PyPI Downloads](https://img.shields.io/pypi/dm/nexios?style=for-the-badge)](https://pypi.org/project/nexios/)  
[![Documentation](https://img.shields.io/badge/Docs-Read%20Now-blue?style=for-the-badge)](https://nexios-labs.gitbook.io/)

## What is Nexios?

Think **FastAPI meets Express.js** but with its own **swagger**! Nexios is a modern Python framework designed to help you **build, deploy, and scale** applications **effortlessly**.

✅ **Super lightweight** – No unnecessary bloat!  
✅ **Crazy fast** 🚀 – Like, seriously!  
✅ **Insanely flexible** – Works with any ORM.  
✅ **Multiple authentication types** – Because security matters!

## 🛠 Installation

```bash
pip install nexios
```

## 🚀 Quick Start

### 1️⃣ Create a Simple Nexios Application

```python
from nexios import get_application

app = get_application()

@app.get("/")
async def home(request, response):
    return response.json({"message": "Welcome to Nexios!"})

@app.get("/users")
async def get_users(request, response):
    return response.json({"users": ["Alice", "Bob"]})
```

### 2️⃣ Run Your App with Uvicorn

```bash
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/` in your browser to see your app in action!

### 3️⃣ Expand

Nexios is designed to grow with your needs. Add more routes, integrate with your favorite ORM, and scale effortlessly!

---

## 🤯 Nexios vs. The World

| Feature              | Nexios 🚀        | FastAPI ⚡ | Django 🏗                     | Flask 🍶   |
| -------------------- | ---------------- | ---------- | ---------------------------- | ---------- |
| Speed                | ⚡⚡⚡⚡⚡       | ⚡⚡⚡⚡   | ⚡⚡                         | ⚡⚡⚡     |
| Ease of Use          | ✅✅✅✅✅       | ✅✅✅✅   | ✅✅✅                       | ✅✅✅✅   |
| ORM Support          | Any!             | SQLAlchemy | Django ORM                   | SQLAlchemy |
| Async Support        | ✅               | ✅         | ❌ (Django 4.1+ has partial) | ❌         |
| Authentication       | ✅               | ✅         | ✅                           | ❌         |
| Built-in Admin Panel | Coming Soon      | ❌         | ✅                           | ❌         |
| Best For             | APIs & Full Apps | APIs       | Full-stack Web Apps          | Small Apps |

---

## 📖 Read the Full Documentation

👉 <a href="https://nexios-labs.gitbook.io/nexios">https://nexios-labs.gitbook.io/nexios</a>

---

## ⭐ Star Nexios on GitHub!

If you love **Nexios**, show some ❤️ by **starring** the repo!

🔗 [**GitHub Repo**](https://github.com/nexios-labs/Nexios)

---
