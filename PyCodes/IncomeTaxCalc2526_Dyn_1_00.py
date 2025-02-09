import tkinter as tk
from tkinter import ttk

class TaxCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Tax Calculator")
        self.root.geometry("1000x1200")
        self.root.resizable(True, True)

        # Create sections
        self.create_income_section()
        self.create_deductions_section()
        self.create_capital_gains_section()
        self.create_summary_section()
        self.create_tax_info_section()

    def create_income_section(self):
        frame = ttk.LabelFrame(self.root, text="Income Details")
        frame.pack(fill="both", padx=10, pady=5)

        ttk.Label(frame, text="Salary Income (₹):").grid(row=0, column=0, padx=5, pady=2)
        self.salary = ttk.Entry(frame)
        self.salary.grid(row=0, column=1, padx=5, pady=2)
        self.salary.bind("<KeyRelease>", self.update_total_income)

        ttk.Label(frame, text="Interest from Savings (₹):").grid(row=1, column=0, padx=5, pady=2)
        self.interest = ttk.Entry(frame)
        self.interest.grid(row=1, column=1, padx=5, pady=2)
        self.interest.bind("<KeyRelease>", self.update_total_income)

        ttk.Label(frame, text="Other Income (₹):").grid(row=2, column=0, padx=5, pady=2)
        self.other_income = ttk.Entry(frame)
        self.other_income.grid(row=2, column=1, padx=5, pady=2)
        self.other_income.bind("<KeyRelease>", self.update_total_income)

    def create_deductions_section(self):
        frame = ttk.LabelFrame(self.root, text="Deductions")
        frame.pack(fill="both", padx=10, pady=5)

        ttk.Label(frame, text="HRA Exemption (₹):").grid(row=0, column=0, padx=5, pady=2)
        self.hra = ttk.Entry(frame)
        self.hra.grid(row=0, column=1, padx=5, pady=2)
        self.hra.bind("<KeyRelease>", self.update_total_income)

        self.salaried_var = tk.BooleanVar()
        self.salaried_check = ttk.Checkbutton(frame, text="Salaried Person (₹75,000 deduction)", variable=self.salaried_var, command=self.update_total_income)
        self.salaried_check.grid(row=1, columnspan=2, padx=5, pady=2)

    def create_capital_gains_section(self):
        frame = ttk.LabelFrame(self.root, text="Capital Gains")
        frame.pack(fill="both", padx=10, pady=5)

        ttk.Label(frame, text="STCG (₹):").grid(row=0, column=0, padx=5, pady=2)
        self.stcg = ttk.Entry(frame)
        self.stcg.grid(row=0, column=1, padx=5, pady=2)
        self.stcg.bind("<KeyRelease>", self.update_total_income)

        ttk.Label(frame, text="LTCG (₹):").grid(row=1, column=0, padx=5, pady=2)
        self.ltcg = ttk.Entry(frame)
        self.ltcg.grid(row=1, column=1, padx=5, pady=2)
        self.ltcg.bind("<KeyRelease>", self.update_total_income)

    def create_summary_section(self):
        self.summary_frame = ttk.LabelFrame(self.root, text="Total Taxable Income (Excluding LTCG & STCG)")
        self.summary_frame.pack(fill="both", padx=10, pady=5)

        self.total_income_label = ttk.Label(self.summary_frame, text="Total Income: ₹0", font=("Arial", 12, "bold"))
        self.total_income_label.pack(pady=5)

    def create_tax_info_section(self):
        self.tax_info_frame = ttk.LabelFrame(self.root, text="Tax Calculation Details (Dynamic)")
        self.tax_info_frame.pack(fill="both", padx=10, pady=5)

        self.tax_info_label = ttk.Label(self.tax_info_frame, text="Tax details will update dynamically...", justify="left")
        self.tax_info_label.pack(pady=5, padx=5)

    def update_total_income(self, event=None):
        try:
            salary = float(self.salary.get() or 0)
            interest = float(self.interest.get() or 0)
            other_income = float(self.other_income.get() or 0)
            hra = float(self.hra.get() or 0)
            is_salaried = self.salaried_var.get()

            standard_deduction = 75000 if is_salaried else 0
            total_income = salary - hra - standard_deduction + interest + other_income

            self.total_income_label.config(text=f"Total Income: ₹{total_income:,.2f}")
            self.update_tax_breakdown(total_income)

        except ValueError:
            self.total_income_label.config(text="Invalid Input")
            self.tax_info_label.config(text="Enter valid numbers.")

    def update_tax_breakdown(self, net_income):
        try:
            tax = 0
            slabs = [(400000, 0.00), (800000, 0.05), (1200000, 0.10),
                     (1600000, 0.15), (2000000, 0.20), (2400000, 0.25), (float('inf'), 0.30)]
            prev_limit = 0
            breakdown = ""

            if net_income > 1200000:
                breakdown += "Income Tax Breakdown:\n"
                for limit, rate in slabs:
                    if net_income > limit:
                        tax_amount = (limit - prev_limit) * rate
                        tax += tax_amount
                        breakdown += f"• ₹{prev_limit:,} - ₹{limit:,}: {rate*100:.0f}% → ₹{tax_amount:,.2f}\n"
                        prev_limit = limit
                    else:
                        tax_amount = (net_income - prev_limit) * rate
                        tax += tax_amount
                        breakdown += f"• ₹{prev_limit:,} - ₹{net_income:,}: {rate*100:.0f}% → ₹{tax_amount:,.2f}\n"
                        break
            else:
                breakdown += "Income tax on salary, savings, and other sources: ₹0 (Below ₹12,00,000)\n"

            # Capital Gains Calculation
            stcg = float(self.stcg.get() or 0)
            ltcg = float(self.ltcg.get() or 0)
            taxable_ltcg = max(ltcg - 125000, 0)

            stcg_tax = stcg * 0.20
            ltcg_tax = taxable_ltcg * 0.125
            total_tax = tax + stcg_tax + ltcg_tax

            breakdown += f"\nSTCG Tax (20%): ₹{stcg_tax:,.2f}\n"
            breakdown += f"LTCG Tax (12.5% after ₹1,25,000 deduction): ₹{ltcg_tax:,.2f}\n"
            breakdown += f"\nTotal Tax Payable: ₹{total_tax:,.2f}"

            self.tax_info_label.config(text=breakdown)

        except ValueError:
            self.tax_info_label.config(text="Enter valid numbers.")

# Initialize App
root = tk.Tk()
app = TaxCalculatorApp(root)
root.mainloop()
