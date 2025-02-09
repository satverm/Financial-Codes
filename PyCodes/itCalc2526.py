import tkinter as tk
from tkinter import ttk, messagebox

class TaxCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comprehensive Tax Calculator")
        self.root.geometry("500x600")

        # Create sections
        self.create_income_section()
        self.create_deductions_section()
        self.create_capital_gains_section()
        self.create_buttons()

    def create_income_section(self):
        frame = ttk.LabelFrame(self.root, text="Income Details")
        frame.pack(fill="both", padx=10, pady=5)

        ttk.Label(frame, text="Salary Income (₹):").grid(row=0, column=0, padx=5, pady=2)
        self.salary = ttk.Entry(frame)
        self.salary.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Interest from Savings (₹):").grid(row=1, column=0, padx=5, pady=2)
        self.interest = ttk.Entry(frame)
        self.interest.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Other Income (₹):").grid(row=2, column=0, padx=5, pady=2)
        self.other_income = ttk.Entry(frame)
        self.other_income.grid(row=2, column=1, padx=5, pady=2)

    def create_deductions_section(self):
        frame = ttk.LabelFrame(self.root, text="Deductions")
        frame.pack(fill="both", padx=10, pady=5)

        ttk.Label(frame, text="HRA Exemption (₹):").grid(row=0, column=0, padx=5, pady=2)
        self.hra = ttk.Entry(frame)
        self.hra.grid(row=0, column=1, padx=5, pady=2)

        self.salaried_var = tk.BooleanVar()
        self.salaried_check = ttk.Checkbutton(frame, text="Salaried Person (₹75,000 deduction)", variable=self.salaried_var)
        self.salaried_check.grid(row=1, columnspan=2, padx=5, pady=2)

    def create_capital_gains_section(self):
        frame = ttk.LabelFrame(self.root, text="Capital Gains")
        frame.pack(fill="both", padx=10, pady=5)

        ttk.Label(frame, text="STCG (₹):").grid(row=0, column=0, padx=5, pady=2)
        self.stcg = ttk.Entry(frame)
        self.stcg.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame, text="LTCG (₹):").grid(row=1, column=0, padx=5, pady=2)
        self.ltcg = ttk.Entry(frame)
        self.ltcg.grid(row=1, column=1, padx=5, pady=2)

    def create_buttons(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Button(frame, text="Calculate Tax", command=self.calculate_tax).pack()

    def calculate_tax(self):
        try:
            salary = float(self.salary.get() or 0)
            hra = float(self.hra.get() or 0)
            interest = float(self.interest.get() or 0)
            other_income = float(self.other_income.get() or 0)
            stcg = float(self.stcg.get() or 0)
            ltcg = float(self.ltcg.get() or 0)
            is_salaried = self.salaried_var.get()

            standard_deduction = 75000 if is_salaried else 0
            taxable_ltcg = max(ltcg - 125000, 0)

            net_income = (salary - hra - standard_deduction) + interest + other_income
            total_tax = 0
            breakdown = ""

            if net_income <= 1200000:
                breakdown += "Income tax on salary, interest, and other sources: ₹0 (Below ₹12,00,000)\n\n"
            else:
                tax = 0
                slabs = [
                    (400000, 0.00), (800000, 0.05), (1200000, 0.10),
                    (1600000, 0.15), (2000000, 0.20), (2400000, 0.25),
                    (float('inf'), 0.30)
                ]
                prev_limit = 0

                for limit, rate in slabs:
                    if net_income > limit:
                        tax += (limit - prev_limit) * rate
                        breakdown += f"{int(rate * 100)}% on ₹{limit - prev_limit} = ₹{(limit - prev_limit) * rate:.2f}\n"
                        prev_limit = limit
                    else:
                        tax += (net_income - prev_limit) * rate
                        breakdown += f"{int(rate * 100)}% on ₹{net_income - prev_limit} = ₹{(net_income - prev_limit) * rate:.2f}\n"
                        break

                total_tax += tax
                breakdown += f"\nIncome Tax Total: ₹{tax:.2f}\n\n"

            stcg_tax = stcg * 0.20
            total_tax += stcg_tax
            breakdown += f"Short-Term Capital Gains Tax (20%): ₹{stcg_tax:.2f}\n\n"

            ltcg_tax = taxable_ltcg * 0.125
            total_tax += ltcg_tax
            breakdown += f"Long-Term Capital Gains Tax (12.5% after ₹1,25,000 deduction): ₹{ltcg_tax:.2f}\n\n"

            breakdown += f"Total Tax Liability: ₹{total_tax:.2f}"

            self.show_tax_breakdown(breakdown)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers!")

    def show_tax_breakdown(self, breakdown):
        new_window = tk.Toplevel(self.root)
        new_window.title("Tax Breakdown")
        new_window.geometry("400x400")

        text = tk.Text(new_window, wrap="word", padx=10, pady=10)
        text.insert("1.0", breakdown)
        text.config(state="disabled")
        text.pack(expand=True, fill="both")

        ttk.Button(new_window, text="Close", command=new_window.destroy).pack(pady=5)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TaxCalculatorApp(root)
    root.mainloop()
