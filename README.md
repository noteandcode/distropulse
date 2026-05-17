# distropulse
Most developers build great products but struggle with distribution. `DistroPulse` is a lightweight Streamlit application designed for indie hackers, software engineers, and founders to diagnose their product's growth pattern using their first 30 days of data—and get an immediate engineering-focused tactical to-do list.
## 📊 How It Works

Instead of vague marketing advice, `DistroPulse` uses raw hard metrics (`Retention %`, `Signups`, `Spend`, and `Referrals`) to calculate your **CAC** (Customer Acquisition Cost) and **K-factor** (Viral Coefficient). 

Based on these data points, it instantly categorizes your project into one of three growth states:
*   🔴 **The Leaky Bucket** (Good initial hype, bad retention — product fixes needed)
*   🟡 **The Bicycle** (Great product retention, weak manual distribution — loops needed)
*   🟢 **The Rocket** (Exponential growth, organic network effects — infrastructure scaling needed)

---

## 🛠️ Features

*   **No-Login Input:** Simple sliders and numeric inputs for your first 30 days of metrics.
*   **Mathematical Curve Projection:** Visualizes the next 30 days of your projected growth trajectory based on your viral coefficient.
*   **Actionable Next Steps:** Generates an interactive, practical To-Do list customized to your product's specific bottleneck.

---

## 🚀 Quick Start & Installation

To run this application locally, ensure you have Python installed, then follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com
cd distropulse
```

### 2. Install dependencies
```bash
pip install streamlit numpy pandas
```

### 3. Run the application
```bash
streamlit run app.py
```

Your browser should automatically open the app at `http://localhost:8501`.

---

## 🌐 Deploy to Production (Free)

This app is fully compatible with **Streamlit Community Cloud**. To deploy it globally for free:
1. Push this code to a public GitHub repository.
2. Go to [share.streamlit.io](https://streamlit.io) and log in with your GitHub account.
3. Click **"New app"**, select your repository, branch, and `app.py` file.
4. Click **"Deploy!"** – Your app will be live in seconds.

---

## 🧮 The Core Logic Behind the Code

The application categorizes growth utilizing standard SaaS unit economics:
*   **CAC:** $\text{Marketing Spend} / \text{Total Signups}$
*   **K-Factor:** $\text{Users from Referrals} / \text{Total Signups}$

### Classification Rules:
*   **Retention < 20%:** `The Leaky Bucket` $\rightarrow$ Focus heavily on onboarding before spending a dime on marketing.
*   **Retention $\ge$ 20% & K-Factor < 0.2:** `The Bicycle` $\rightarrow$ The product is sticky, but you need programmatic growth loops or developer SEO.
*   **Retention $\ge$ 20% & K-Factor $\ge$ 0.2:** `The Rocket` $\rightarrow$ Organic network effects are live. Load-test infrastructure immediately.

---

## 📝 License

This project is licensed under the MIT License - feel
