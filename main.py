import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


filepaths = glob.glob("./invoices/*.xlsx")

for filepath in filepaths:
    df = pd.read_excel(filepath, sheet_name="Sheet 1", dtype=str)

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    filename = Path(filepath).stem
    invoice_nr, date = filename.split("-")

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Invoice nr. {invoice_nr}", ln=1)

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

    # Add a header
    columns = [x.replace("_", " ").title() for x in df.columns]
    pdf.set_font(family="Times", size=10, style="B")
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt=columns[0], border=1)
    pdf.cell(w=70, h=8, txt=columns[1], border=1)
    pdf.cell(w=40, h=8, txt=columns[2], border=1)
    pdf.cell(w=25, h=8, txt=columns[3], border=1)
    pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

    # Add the columns
    for index, row in df.iterrows():
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=row["product_id"], border=1)
        pdf.cell(w=70, h=8, txt=row["product_name"], border=1)
        pdf.cell(w=40, h=8, txt=row["amount_purchased"], border=1)
        pdf.cell(w=25, h=8, txt=row["price_per_unit"], border=1)
        pdf.cell(w=30, h=8, txt=row["total_price"], border=1, ln=1)

    # Add the total price
    total_sum = str(df["total_price"].astype(float).sum())
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=70, h=8, txt="", border=1)
    pdf.cell(w=40, h=8, txt="", border=1)
    pdf.cell(w=25, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt=total_sum, border=1, ln=1)

    # Add total sum sentences
    pdf.set_font(family="Times", size=14, style="B")
    pdf.cell(w=30, h=8, txt=f"The total price is: {total_sum}.", ln=1)

    # Add company name and logo
    pdf.set_font(family="Times", size=14, style="B")
    pdf.cell(w=30, h=8, txt="Pythonhow")
    pdf.image("pythonhow.png", w=10)

    pdf.output(f"pdfs/{filename}.pdf")
