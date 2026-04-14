from fpdf import FPDF

def generate_pdf(data):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    # ================= TITLE =================
    pdf.cell(200, 10, txt="FinSight AI - Financial Report", ln=True, align='C')

    pdf.ln(10)

    # ================= KPIs =================
    pdf.cell(200, 10, txt=f"Total Income: Rs. {data['income']:.0f}", ln=True)
    pdf.cell(200, 10, txt=f"Total Expense: Rs. {data['expense']:.0f}", ln=True)
    pdf.cell(200, 10, txt=f"Savings: Rs. {data['savings']:.0f}", ln=True)
    pdf.cell(200, 10, txt=f"Savings Rate: {data['savings_rate']:.1f}%", ln=True)

    pdf.ln(10)

    # ================= INSIGHTS =================
    pdf.cell(200, 10, txt="Key Insights:", ln=True)

    for insight in data["insights"]:
        pdf.multi_cell(0, 8, f"- {insight}")

    pdf.ln(5)

    # ================= RECOMMENDATIONS =================
    pdf.cell(200, 10, txt="Recommendations:", ln=True)

    for rec in data["recommendations"]:
        pdf.multi_cell(0, 8, f"- {rec}")

    # ================= SAVE =================
    file_path = "financial_report.pdf"
    pdf.output(file_path)

    return file_path