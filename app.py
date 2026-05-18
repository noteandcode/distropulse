import streamlit as st
import numpy as np
import pandas as pd
import io
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    HRFlowable, Table, TableStyle
)
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DistroPulse - Growth Diagnosis for Devs",
    page_icon="🚀",
    layout="centered",
)

st.title("🚀 DistroPulse")
st.subheader("Growth & Distribution Diagnostics for Developers")
st.write(
    "Analyze your first 30 days of data to find where your growth "
    "bottlenecks are and get actionable next steps."
)

st.info(
    "⚠️ **Disclaimer:** The results, diagnoses, and recommendations provided by DistroPulse are purely illustrative "
    "and based on simplified models. They do not constitute professional business, financial, or technical advice. "
    "All outputs are approximate estimates and may not reflect real-world outcomes. "
    "By using this tool, you acknowledge that the creators accept no liability whatsoever for any decisions made "
    "or actions taken based on the information displayed here."
)

st.divider()

# ── Input section ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    n_users = st.number_input("Total signups in month 1 (N)", min_value=1, value=150, step=10)
    marketing_cost = st.number_input("Marketing spend ($)", min_value=0, value=50, step=10)

with col2:
    retention = st.slider(
        "Weekly retention rate (Retention %)",
        min_value=0, max_value=100, value=25,
        help="What percentage of users are still active by week 4?",
    )
    referrals = st.number_input("Users from invites/referrals (V)", min_value=0, value=15, step=5)

st.divider()

# ── Calculations ──────────────────────────────────────────────────────────────
cac = marketing_cost / n_users if n_users > 0 else 0
k_factor = referrals / n_users if n_users > 0 else 0
days = np.arange(1, 31)

# ── Logic engine ──────────────────────────────────────────────────────────────
if retention < 20:
    category = "🔴 The Leaky Bucket"
    category_plain = "The Leaky Bucket"
    users_curve = n_users * (1 - np.exp(-days / 5)) * (retention / 100 + np.exp(-days / 10))
    diagnostics = (
        "**Diagnosis:** Your marketing worked (you got people's attention), but your product fails to retain them. "
        "You do not have Product-Market Fit yet. Spending money on ads right now is just burning cash."
    )
    diagnostics_plain = (
        "Your marketing worked (you got people's attention), but your product fails to retain them. "
        "You do not have Product-Market Fit yet. Spending money on ads right now is just burning cash."
    )
    todo = [
        (
            "Fix the Onboarding",
            "Implement a guided tour or a setup wizard for the first-time user experience.",
        ),
        (
            "Automated Churn Interviews",
            "Trigger an automated email to users who became inactive after 3 days and ask why they left.",
        ),
        (
            "Feature Reduction",
            "Your app might be too complex. Strip away 80% of the features and double down on the core value proposition.",
        ),
    ]

elif retention >= 20 and k_factor < 0.2:
    category = "🟡 The Bicycle (Linear Manual Growth)"
    category_plain = "The Bicycle (Linear Manual Growth)"
    users_curve = (n_users / 2) + (days * (n_users / 60))
    diagnostics = (
        "**Diagnosis:** You built an excellent product because the people who use it, love it (great retention). "
        "However, your distribution channels are weak. New users only come when you manually hustle for them."
    )
    diagnostics_plain = (
        "You built an excellent product because the people who use it, love it (great retention). "
        "However, your distribution channels are weak. New users only come when you manually hustle for them."
    )
    todo = [
        (
            "Programmatic Growth",
            "Build a referral loop into the product (e.g., Invite a friend, get 10 extra credits).",
        ),
        (
            "Public Output / Social Proof",
            "Make your product's usage visible to the world (e.g., add a 'Powered by [App]' badge or watermark).",
        ),
        (
            "Developer SEO",
            "Write StackOverflow-style blog posts targeting the exact technical errors or pain points your software solves.",
        ),
    ]

else:
    category = "🟢 The Rocket (Exponential Loop)"
    category_plain = "The Rocket (Exponential Loop)"
    users_curve = (n_users / 10) * np.exp(days * (k_factor / 5))
    diagnostics = (
        "**Diagnosis:** You hit the jackpot. Your product spreads on its own (K-factor > 0.2), "
        "users love it, and they are actively inviting their peers. You are experiencing an organic network effect."
    )
    diagnostics_plain = (
        "You hit the jackpot. Your product spreads on its own (K-factor > 0.2), "
        "users love it, and they are actively inviting their peers. You are experiencing an organic network effect."
    )
    todo = [
        (
            "Infrastructure Load Test",
            "Will your servers survive a 10x traffic spike next week? Optimize your database queries now!",
        ),
        (
            "Optimize Pricing",
            "Tighten your free tier limits or consider raising prices. Users are highly motivated to pay right now.",
        ),
        (
            "Lookalike Ads",
            "Now it is actually worth running paid ads (Meta, Google), because every paid user will bring 1+ more users for free.",
        ),
    ]

# ── Streamlit results UI ──────────────────────────────────────────────────────
st.header(f"Category: {category}")
st.write(diagnostics)

st.write("### 📊 Your Core Metrics")
m1, m2 = st.columns(2)
m1.metric("Customer Acquisition Cost (CAC)", f"${cac:.2f}")
m2.metric(
    "Viral Coefficient (K-factor)",
    f"{k_factor:.2f}",
    help="If this is above 1.0, your product is growing virally on its own.",
)

st.write("### 📈 Projected Growth Curve (Next 30 Days)")
chart_data = pd.DataFrame({"Day": days, "Acquired Users": users_curve})
st.line_chart(chart_data.set_index("Day"))

st.write("### 🛠️ Next Tactical Moves (Your To-Do List)")
for title, desc in todo:
    st.checkbox(f"**{title}:** {desc}", value=False)


# ── PDF generation helpers ────────────────────────────────────────────────────

ACCENT_COLOR   = colors.HexColor("#4F46E5")   # indigo
LIGHT_BG       = colors.HexColor("#F5F5FF")
TEXT_DARK      = colors.HexColor("#1E1B4B")
MUTED          = colors.HexColor("#6B7280")
FOOTER_TEXT    = colors.HexColor("#3A3D41")
PAGE_W, PAGE_H = A4
MARGIN         = float(20 * mm)


def make_chart_image(days_arr, curve, category_label):
    """Render the growth curve with matplotlib and return a BytesIO PNG."""
    fig, ax = plt.subplots(figsize=(7, 3), dpi=150)
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    ax.plot(days_arr, curve, color="#4F46E5", linewidth=2.5, solid_capstyle="round")
    ax.fill_between(days_arr, curve, alpha=0.12, color="#4F46E5")

    ax.set_xlabel("Day", fontsize=9, color="#6B7280")
    ax.set_ylabel("Acquired Users", fontsize=9, color="#6B7280")
    ax.set_title(f"Projected Growth Curve — {category_label}", fontsize=10, color="#1E1B4B", pad=8)
    ax.tick_params(colors="#6B7280", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#E5E7EB")

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf


def build_pdf(
    n_users_val, marketing_cost_val, retention_val, referrals_val,
    cac_val, k_factor_val,
    category_label, diagnosis_text, action_items,
    days_arr, curve,
):
    buf = io.BytesIO()

    FOOTER_NOTE = (
        "Interested in a version of DistroPulse connected to your own tool analytics? "
        "Reach out at hello@essayty.com"
    )

    def on_page(canvas, doc):
        """Draw header bar and footer on every page."""
        canvas.saveState()

        # ── Header bar ──────────────────────────────────────────────────────
        canvas.setFillColor(ACCENT_COLOR)
        canvas.rect(0, PAGE_H - 18 * mm, PAGE_W, 18 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawString(MARGIN, PAGE_H - 11 * mm, "DistroPulse  |  Growth & Distribution Report")
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(
            PAGE_W - MARGIN,
            PAGE_H - 11 * mm,
            datetime.now().strftime("%B %d, %Y"),
        )

        # ── Footer ───────────────────────────────────────────────────────────
        canvas.setStrokeColor(colors.HexColor("#E5E7EB"))
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, 14 * mm, PAGE_W - MARGIN, 14 * mm)

        canvas.setFillColor(FOOTER_TEXT)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(MARGIN, 9 * mm, FOOTER_NOTE)
        canvas.drawRightString(
            PAGE_W - MARGIN, 9 * mm,
            f"Page {doc.page}",
        )

        # ── Disclaimer ───────────────────────────────────────────────────────
        canvas.setFont("Helvetica-Oblique", 6)
        canvas.setFillColor(FOOTER_TEXT)
        canvas.drawString(
            MARGIN, 5 * mm,
            "Results are illustrative estimates only and do not constitute professional advice.",
        )

        canvas.restoreState()

    # ── Styles ────────────────────────────────────────────────────────────────
    styles = getSampleStyleSheet()

    s_section = ParagraphStyle(
        "SectionHead",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=ACCENT_COLOR,
        spaceAfter=4,
        spaceBefore=14,
    )
    s_body = ParagraphStyle(
        "Body",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=TEXT_DARK,
        leading=15,
        spaceAfter=6,
    )
    s_label = ParagraphStyle(
        "Label",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=TEXT_DARK,
    )
    s_desc = ParagraphStyle(
        "Desc",
        fontName="Helvetica",
        fontSize=9,
        textColor=MUTED,
        leading=14,
    )
    s_category = ParagraphStyle(
        "Category",
        fontName="Helvetica-Bold",
        fontSize=15,
        textColor=TEXT_DARK,
        spaceAfter=8,
        spaceBefore=6,
    )

    # ── Document ──────────────────────────────────────────────────────────────
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=24 * mm,
        bottomMargin=20 * mm,
    )

    story = []

    # ── Input summary table ───────────────────────────────────────────────────
    story.append(Paragraph("Input Summary", s_section))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E7EB")))
    story.append(Spacer(1, 4))

    input_data = [
        ["Total Signups (Month 1)", f"{int(n_users_val):,}",
         "Marketing Spend", f"${marketing_cost_val:,.0f}"],
        ["Weekly Retention Rate", f"{retention_val}%",
         "Referral Users", f"{int(referrals_val):,}"],
    ]
    tbl = Table(input_data, colWidths=[(PAGE_W - 2 * MARGIN) / 4] * 4)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("FONTNAME",   (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE",   (0, 0), (-1, -1), 9),
        ("TEXTCOLOR",  (0, 0), (-1, -1), TEXT_DARK),
        ("FONTNAME",   (0, 0), (0,  0),  "Helvetica-Bold"),
        ("FONTNAME",   (2, 0), (2,  0),  "Helvetica-Bold"),
        ("FONTNAME",   (0, 1), (0,  1),  "Helvetica-Bold"),
        ("FONTNAME",   (2, 1), (2,  1),  "Helvetica-Bold"),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.white),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT_BG, colors.HexColor("#EDEDFF")]),
        ("TOPPADDING",  (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(tbl)

    # ── Key metrics ───────────────────────────────────────────────────────────
    story.append(Spacer(1, 6))
    metrics_data = [
        [Paragraph("<b>Customer Acquisition Cost (CAC)</b>", s_desc),
         Paragraph(f"<b>${cac_val:.2f}</b>", s_category),
         Paragraph("<b>Viral Coefficient (K-factor)</b>", s_desc),
         Paragraph(f"<b>{k_factor_val:.2f}</b>", s_category)],
    ]
    m_tbl = Table(metrics_data, colWidths=[(PAGE_W - 2 * MARGIN) / 4] * 4)
    m_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX",        (0, 0), (1, 0),   1, ACCENT_COLOR),
        ("BOX",        (2, 0), (3, 0),   1, ACCENT_COLOR),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(m_tbl)

    # ── Diagnosis ─────────────────────────────────────────────────────────────
    story.append(Paragraph("Growth Stage Diagnosis", s_section))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E7EB")))
    story.append(Spacer(1, 4))
    story.append(Paragraph(category_label, s_category))
    story.append(Paragraph(diagnosis_text, s_body))

    # ── Chart ─────────────────────────────────────────────────────────────────
    story.append(Paragraph("Projected Growth Curve (Next 30 Days)", s_section))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E7EB")))
    story.append(Spacer(1, 4))

    chart_buf = make_chart_image(days_arr, curve, category_label)
    chart_img = RLImage(chart_buf, width=PAGE_W - 2 * MARGIN, height=(PAGE_W - 2 * MARGIN) * 3 / 7)
    story.append(chart_img)

    # ── Action items ──────────────────────────────────────────────────────────
    story.append(Paragraph("Next Tactical Moves", s_section))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E7EB")))
    story.append(Spacer(1, 4))

    for idx, (action_title, action_desc) in enumerate(action_items, start=1):
        num_col = Paragraph(f"<b>{idx}</b>", ParagraphStyle(
            "Num", fontName="Helvetica-Bold", fontSize=12,
            textColor=colors.white, alignment=TA_CENTER,
        ))
        num_bg = Table([[num_col]], colWidths=[8 * mm], rowHeights=[8 * mm])
        num_bg.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), ACCENT_COLOR),
            ("TOPPADDING",    (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ]))

        text_col = [
            Paragraph(action_title, s_label),
            Paragraph(action_desc,  s_desc),
        ]
        row = Table(
            [[num_bg, text_col]],
            colWidths=[10 * mm, PAGE_W - 2 * MARGIN - 10 * mm],
        )
        row.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_BG),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(row)
        story.append(Spacer(1, 5))

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    buf.seek(0)
    return buf


# ── Download button ───────────────────────────────────────────────────────────
st.divider()
st.write("### 📄 Export Your Report")

if st.button("Generate PDF Report", type="primary"):
    with st.spinner("Building your PDF…"):
        pdf_bytes = build_pdf(
            n_users_val=n_users,
            marketing_cost_val=marketing_cost,
            retention_val=retention,
            referrals_val=referrals,
            cac_val=cac,
            k_factor_val=k_factor,
            category_label=category_plain,
            diagnosis_text=diagnostics_plain,
            action_items=todo,
            days_arr=days,
            curve=users_curve,
        )

    st.download_button(
        label="⬇️ Download PDF",
        data=pdf_bytes,
        file_name="distropulse_report.pdf",
        mime="application/pdf",
    )


