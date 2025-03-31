from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        """Custom header with title."""
        self.set_font("Arial", 'B', 16)
        self.set_text_color(30, 144, 255)  # DodgerBlue
        self.cell(0, 10, "Bitcoin DCA Backtest Report", ln=True, align='C')
        self.ln(10)

    def footer(self):
        """Custom footer with page numbers."""
        self.set_y(-15)
        self.set_font("Arial", 'I', 10)
        self.set_text_color(128)  # Grey color
        self.cell(0, 10, f"Page {self.page_no()}", align='C')

def generate_pdf_report(start_date, end_date, investment, frequency, total_invested, final_value, profit, plot_path):
    """
    Generates a detailed and well-structured PDF report summarizing the backtest results.
    """
    pdf = PDF()
    pdf.add_page()

    # Section: Summary
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)  # Black
    pdf.cell(0, 10, "Backtest Summary", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Backtest Period: {start_date} to {end_date}", ln=True)
    pdf.cell(0, 10, f"Daily Investment: ${investment:.2f}", ln=True)
    pdf.cell(0, 10, f"Investment Frequency: {frequency.capitalize()}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Financial Results", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Total Invested: ${total_invested:.2f}", ln=True)
    pdf.cell(0, 10, f"Final Portfolio Value: ${final_value:.2f}", ln=True)

    # ✅ **Set text color conditionally for profit**
    if profit >= 0:
        pdf.set_text_color(0, 128, 0)  # Green for positive profit
    else:
        pdf.set_text_color(255, 0, 0)  # Red for negative profit

    pdf.cell(0, 10, f"Total Profit: ${profit:.2f}", ln=True)

    # Reset text color to black
    pdf.set_text_color(0, 0, 0)
    
    pdf.ln(10)

    # Section: Investment Strategy
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Investment Strategy", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.multi_cell(0, 8, (
        "The Dollar-Cost Averaging (DCA) strategy involves investing a fixed amount "
        "of money into Bitcoin at regular intervals. This method aims to reduce the impact "
        "of volatility by spreading out purchases over time, potentially leading to a "
        "more stable average entry price."
    ))
    pdf.ln(10)

    # Section: Performance Chart
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Performance Chart", ln=True)
    pdf.ln(5)

    if os.path.exists(plot_path):
        pdf.image(plot_path, x=10, w=pdf.w - 20)
    else:
        pdf.cell(0, 10, "Performance chart not found.", ln=True)

    # Section: Conclusion
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Conclusion", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.multi_cell(0, 8, (
        "This backtest demonstrates the potential of DCA as a long-term investment "
        "strategy. While short-term fluctuations are inevitable, disciplined investing "
        "over time can provide stable growth in a volatile market."
    ))

    # Save the PDF
    output_path = "DCA_Backtest_Report.pdf"
    pdf.output(output_path)
    return output_path

if __name__ == '__main__':
    # Test PDF generation with sample values
    report = generate_pdf_report(
        start_date="2020-01-01",
        end_date="2024-12-31",
        investment=30,
        frequency="daily",
        total_invested=10000,
        final_value=12000,
        profit=2000,
        plot_path="performance.png"
    )
    print("PDF report generated at", report)


