import streamlit as st
import numpy as np
import pandas as pd

# Page configuration
st.set_page_config(page_title="DistroPulse - Growth Diagnosis for Devs", page_icon="🚀", layout="centered")

st.title("🚀 DistroPulse")
st.subheader("Growth & Distribution Diagnostics for Developers")
st.write("Analyze your first 30 days of data to find where your growth bottlenecks are and get actionable next steps.")

st.info(
    "⚠️ **Disclaimer:** The results, diagnoses, and recommendations provided by DistroPulse are purely illustrative "
    "and based on simplified models. They do not constitute professional business, financial, or technical advice. "
    "All outputs are approximate estimates and may not reflect real-world outcomes. "
    "By using this tool, you acknowledge that the creators accept no liability whatsoever for any decisions made "
    "or actions taken based on the information displayed here."
)

st.divider()

# 1. Columns for input data
col1, col2 = st.columns(2)

with col1:
    n_users = st.number_input("Total signups in month 1 (N)", min_value=1, value=150, step=10)
    marketing_cost = st.number_input("Marketing spend ($)", min_value=0, value=50, step=10)

with col2:
    retention = st.slider("Weekly retention rate (Retention %)", min_value=0, max_value=100, value=25, help="What percentage of users are still active by week 4?")
    referrals = st.number_input("Users from invites/referrals (V)", min_value=0, value=15, step=5)

st.divider()

# 2. Behind-the-scenes calculations (CAC and K-factor)
cac = marketing_cost / n_users if n_users > 0 else 0
k_factor = referrals / n_users if n_users > 0 else 0

# Simulated timeline for the chart (30 days)
days = np.arange(1, 31)

# 3. Logic engine and categorization
if retention < 20:
    category = "🔴 The Leaky Bucket"
    # Declining/flattening curve simulation
    users_curve = n_users * (1 - np.exp(-days/5)) * (retention/100 + np.exp(-days/10))
    diagnostics = (
        "**Diagnosis:** Your marketing worked (you got people's attention), but your product fails to retain them. "
        "You do not have Product-Market Fit yet. Spending money on ads right now is just burning cash."
    )
    todo = [
        "**Fix the Onboarding:** Implement a guided tour or a setup wizard for the first-time user experience.",
        "**Automated Churn Interviews:** Trigger an automated email to users who became inactive after 3 days and ask *why* they left.",
        "**Feature Reduction:** Your app might be too complex. Strip away 80% of the features and double down on the core value proposition."
    ]

elif retention >= 20 and k_factor < 0.2:
    category = "🟡 The Bicycle (Linear Manual Growth)"
    # Linear growth simulation
    users_curve = (n_users / 2) + (days * (n_users / 60))
    diagnostics = (
        "**Diagnosis:** You built an excellent product because the people who use it, love it (great retention). "
        "However, your distribution channels are weak. New users only come when you manually hustle for them."
    )
    todo = [
        "**Programmatic Growth:** Build a referral loop into the product (e.g., *Invite a friend, get 10 extra credits*).",
        "**Public Output / Social Proof:** Make your product's usage visible to the world (e.g., add a 'Powered by [App]' badge or watermark).",
        "**Developer SEO:** Write StackOverflow-style blog posts targeting the exact technical errors or pain points your software solves."
    ]

else:
    category = "🟢 The Rocket (Exponential Loop)"
    # Exponential/S-curve growth simulation
    users_curve = (n_users / 10) * np.exp(days * (k_factor / 5))
    diagnostics = (
        "**Diagnosis:** You hit the jackpot. Your product spreads on its own (K-factor > 0.2), "
        "users love it, and they are actively inviting their peers. You are experiencing an organic network effect."
    )
    todo = [
        "**Infrastructure Load Test:** Will your servers survive a 10x traffic spike next week? Optimize your database queries now!",
        "**Optimize Pricing:** Tighten your free tier limits or consider raising prices. Users are highly motivated to pay right now.",
        "**Lookalike Ads:** Now it is actually worth running paid ads (Meta, Google), because every paid user will bring 1+ more users for free."
    ]

# 4. Displaying the results
st.header(f"Category: {category}")
st.write(diagnostics)

# Metrics UI
st.write("### 📊 Your Core Metrics")
m1, m2 = st.columns(2)
m1.metric("Customer Acquisition Cost (CAC)", f"${cac:.2f}")
m2.metric("Viral Coefficient (K-factor)", f"{k_factor:.2f}", help="If this is above 1.0, your product is growing virally on its own.")

# Rendering the chart
st.write("### 📈 Projected Growth Curve (Next 30 Days)")
chart_data = pd.DataFrame({'Day': days, 'Acquired Users': users_curve})
st.line_chart(chart_data.set_index('Day'))

# Displaying Action Items as Checkboxes
st.write("### 🛠️ Next Tactical Moves (Your To-Do List)")
for item in todo:
    st.checkbox(item, value=False)
    import streamlit as st
import streamlit.components.v1 as components
analytics_id = st.secrets["ANALYTICS_ID"]




