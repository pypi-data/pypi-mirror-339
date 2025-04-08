# 🐢 Slowpoke
<h1 align="center" style="font-size: 4rem;">🐢 SLOWPOKE</h1>

**Slowpoke** is a lightweight Python package that helps you monitor and log **slow API routes** in your Flask application. If you're wondering _"Which endpoints are dragging me down?"_, Slowpoke has your back.

---

## 🚀 Installation

Until we publish on PyPI, install directly from GitHub:

```bash
pip install git+https://github.com/vedangit/slowpoke.git
```

---

## ⚙️ Usage

### 1. Add `slowpoke` to your Flask app

```python
from slowpoke import monitor

app = Flask(__name__)
monitor(app)

```

> The `threshold_ms` parameter sets the time (in milliseconds) after which a request is considered slow.

---

### 2. Run your app normally

Make requests as usual. Slowpoke will track how long each endpoint takes.

---

### 3. View the report

Once you've made some requests, generate a report from the command line:

```bash
slowpoke report
```

This will print a table of all routes that exceeded the threshold, including method, endpoint, duration, and timestamp.

---

## 🧪 Example App

You can test out `slowpoke` quickly by running the example Flask app:

```bash
cd examples
python app.py
```

Then hit some routes and run:

```bash
slowpoke report
```

---

## 🛣️ Roadmap

### ✅ Version 0 (Current):
- Log all Flask routes that exceed a threshold.
- CLI tool to view slow route report.

### 🔜 Version 1 (Coming soon):
- Middleware-based integration.
- Save reports to file.
- Optional integration with logging tools.
- FastAPI + Django support.

---

## 🧠 Why Slowpoke?

- 🚀 Fast to integrate  
- 🔍 Focused on performance bottlenecks  
- 🧼 Clean CLI reporting  
- 💻 Perfect for side projects or production  

---

## 👩‍💻 Author

Made with ❤️ by [Vedangi](https://github.com/vedangit)

---

## 📄 License

MIT License
 
