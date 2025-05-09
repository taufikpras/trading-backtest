from fpdf import FPDF
from fpdf.enums import XPos, YPos
import pandas as pd
from prettytable import PrettyTable

def format_rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")

def format_percent(x):
    return f"{x * 100:.2f}%"

FONT = 'helvetica'

class PDFReport(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.section_title = ""

    def header(self):
        if self.page_no() == 1:
            self.set_font(FONT, 'B', 16)
            self.cell(0, 10, 'Backtest Summary Report', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
            self.ln(5)
        else:
            self.set_font(FONT, 'B', 12)
            self.cell(0, 10, self.section_title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(5)

    def chapter_title(self, title):
        self.set_font(FONT, 'B', 12)
        self.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

    def chapter_body(self, body):
        self.set_font(FONT, '', 11)
        self.multi_cell(0, 8, body)
        self.ln()

    def create_table(self, dataframe, col_widths=None):
        self.set_font(FONT, '', 10)
        if col_widths is None:
            col_widths = [self.epw / len(dataframe.columns)] * len(dataframe.columns)

        # Header
        for i, column in enumerate(dataframe.columns):
            self.cell(col_widths[i], 8, str(column), border=1, align='C')
        self.ln()

        # Rows
        for idx, row in dataframe.iterrows():
            for i, item in enumerate(row):
                self.cell(col_widths[i], 8, str(item), border=1)
            self.ln()
        self.ln(5)

def save_multiple_backtests_to_pdf(backtest_results:pd.DataFrame, filename="full_backtest_report.pdf", stg_name:str=""):
    pdf = PDFReport(orientation = 'L')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf_link = {}
    summary_link = pdf.add_link()
    pdf.set_link(summary_link)
    # ======= Buat Link untuk Setiap Saham =======
    links = {}
    for idx,row in backtest_results.iterrows():
        links[row["Ticker"]] = pdf.add_link()

    # ======= Halaman 1: Summary Table =======
    summary_text = (
        f'Number of Stocks: {backtest_results.shape[0]}\n'
        f'Total Profit: {format_rupiah(backtest_results["total_profit"].sum())}\n'
        f'Number of Trades: {backtest_results["number_of_trades"].sum()}\n'
        f'Precision: {format_percent(backtest_results["precision"].mean())}\n'
        f'Largest Profit: {format_rupiah(backtest_results["largest_profit"].max())}\n'
        f'Largest Loss: {format_rupiah(backtest_results["largest_loss"].min())}\n'
        f'Max Drawdown: {format_rupiah(backtest_results["max_drawdown"].min())}\n'
        f'Avg CAGR Percent: {format_percent(backtest_results["yearly_cagr"].mean())}\n'
        f'Avg CAGR Value: {format_rupiah(backtest_results["yearly_cagr_value"].mean())}\n'
    )

    backtest_results_1 = backtest_results.sort_values(by='total_profit', ascending=False)
    backtest_results_1['total_profit'] = backtest_results['total_profit'].apply(format_rupiah)
    backtest_results_1['precision'] = backtest_results['precision'].apply(format_percent)
    backtest_results_1['yearly_cagr'] = backtest_results['yearly_cagr'].apply(format_percent)
    backtest_results_1['yearly_cagr_value'] = backtest_results['yearly_cagr_value'].apply(format_rupiah)
    backtest_results_1['max_drawdown'] = backtest_results['max_drawdown'].apply(format_rupiah)
    backtest_results_1['largest_profit'] = backtest_results['largest_profit'].apply(format_rupiah)
    backtest_results_1['largest_loss'] = backtest_results['largest_loss'].apply(format_rupiah)

    pdf.chapter_title("Summary Table")
    pdf.chapter_body(summary_text)
    summary_data = []
    for idx, row in backtest_results_1.iterrows():
        summary_data.append({
            'Ticker': row['Ticker'],
            'Total Profit': row['total_profit'],
            'Number of Trades': row['number_of_trades'],
            'Precision': row['precision'],
            'Largest Profit': row['largest_profit'],
            'Largest Loss': row['largest_loss'],
            'Max Drawdown': row['max_drawdown'],
            'CAGR Percent': row['yearly_cagr'],
            'CAGR Value': row['yearly_cagr_value']
        })

    summary_df = pd.DataFrame(summary_data)
    col_widths = [25, 30, 30, 25, 30, 30, 30, 30, 30]

    pdf.set_font(FONT, '', 10)
    # Header
    for i, column in enumerate(summary_df.columns):
        pdf.cell(col_widths[i], 8, str(column), border=1, align='C')
    pdf.ln()

    # Rows + Add hyperlink for ticker
    for idx, row in summary_df.iterrows():
        for i, item in enumerate(row):
            if i == 0:  # kolom pertama = ticker
                pdf.set_text_color(0, 0, 255)  # Biru
                pdf.cell(col_widths[i], 8, str(item), border=1, align='C', link=links[item])
                pdf.set_text_color(0, 0, 0)  # Balik ke hitam
            else:
                pdf.cell(col_widths[i], 8, str(item), border=1)
        pdf.ln()
    pdf.ln(5)

    # ====== Halaman Berikutnya: Detail per Saham ======
    for idx, row in backtest_results_1.iterrows():
        pdf.add_page()
        pdf.section_title = f"Detail Report - {row['Ticker']}"
        pdf.set_link(links[row["Ticker"]])

        # <<< Tambahkan Back to Summary link
        pdf.set_font(FONT, 'I', 10)
        pdf.set_text_color(0, 0, 255)
        pdf.cell(0, 10, 'Back to Summary', new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=summary_link)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

        # Detail Statistics
        pdf.chapter_title(f"Summary Statistics {row['Ticker']}")
        stats = row
        summary_text = (
            f"Total Profit: {stats['total_profit']}\n"
            f"Number of Trades: {stats['number_of_trades']}\n"
            f"Precision: {stats['precision']}\n"
            f"Largest Profit: {stats['largest_profit']}\n"
            f"Largest Loss: {stats['largest_loss']}\n"
            f"Max Drawdown: {stats['max_drawdown']}\n"
        )
        pdf.chapter_body(summary_text)

        # Yearly Profit Table
        pdf.chapter_title(f"Yearly Profit - {row['Ticker']}")
        yearly_profit_df = row['yearly_profit']
        # yearly_profit_df.index.name = 'Year'
        # yearly_profit_df.reset_index(inplace=True)
        if not yearly_profit_df.empty:
            yearly_profit_df['start_balance'] = yearly_profit_df['start_balance'].apply(format_rupiah)
            yearly_profit_df['end_balance'] = yearly_profit_df['end_balance'].apply(format_rupiah)
            yearly_profit_df['profit_money'] = yearly_profit_df['profit_money'].apply(format_rupiah)
            yearly_profit_df['profit_percent'] = yearly_profit_df['profit_percent'].apply(format_percent)
        pdf.create_table(yearly_profit_df, col_widths=[30, 40, 40, 40, 40])

        # Trade History Table
        pdf.chapter_title(f"Trade History - {row['Ticker']}")
        trades_df = row['trades']
        if not trades_df.empty:
            trades_df['entry_date'] = trades_df['entry_date'].dt.strftime('%Y-%m-%d')
            trades_df['exit_date'] = trades_df['exit_date'].dt.strftime('%Y-%m-%d')
            trades_df['entry_price'] = trades_df['entry_price'].apply(format_rupiah)
            trades_df['entry_cost'] = trades_df['entry_cost'].apply(format_rupiah)
            trades_df['initial_sl'] = trades_df['initial_sl'].apply(format_rupiah)
            trades_df['exit_price'] = trades_df['exit_price'].apply(format_rupiah)
            trades_df['profit'] = trades_df['profit'].apply(format_rupiah)
            trades_df['account_balance'] = trades_df['account_balance'].apply(format_rupiah)
            display_cols = ['entry_date', 'exit_date', 'entry_price', 'exit_price', 'initial_sl','lot', 'entry_cost', 'profit', 'account_balance']
            trades_to_display = trades_df[display_cols].copy()
            col_widths = [25, 25, 20, 20, 20, 20, 35, 35, 35]
            pdf.create_table(trades_to_display, col_widths=col_widths)
        else:
            pdf.chapter_body("No trades available.")

    # Save file
    pdf.output(f'./data/output/{filename}')
    print(f"PDF saved to {filename}")

def print_table(df:pd.DataFrame):
    table = PrettyTable()
    df.reset_index(drop=True, inplace=True)
    values = df.to_dict(orient='records')
    table.field_names = values[0].keys()
    
    for row in values:
        table.add_row(row.values())
    print(table)
