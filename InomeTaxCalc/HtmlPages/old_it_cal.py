import tkinter as tk
from tkinter import messagebox

def calculate_tax():
    try:
        gross_income = float(entry_gross_income.get())
        deduction_80C = float(entry_deduction_80C.get())
        deduction_24b = float(entry_deduction_24b.get())

        # Calculate net taxable income
        net_income = gross_income - deduction_80C - deduction_24b

        # Calculate tax based on old regime slabs
        if net_income <= 250000:
            tax = 0
        elif net_income <= 500000:
            tax = (net_income - 250000) * 0.05
        elif net_income <= 1000000:
            tax = 12500 + (net_income - 500000) * 0.20
        else:
            tax = 12500 + 100000 + (net_income - 1000000) * 0.30
        
        messagebox.showinfo("Tax Calculation", f"Net Taxable Income: ₹{net_income:.2f}\nTax Payable: ₹{tax:.2f}")
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers")

# Create the main window
root = tk.Tk()
root.title("Income Tax Calculator (Old Regime)")

# Create and place labels and entry boxes for inputs
tk.Label(root, text="Gross Income:").grid(row=0, column=0, padx=10, pady=10)
entry_gross_income = tk.Entry(root)
entry_gross_income.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Deduction under 80C:").grid(row=1, column=0, padx=10, pady=10)
entry_deduction_80C = tk.Entry(root)
entry_deduction_80C.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Interest on Housing Loan (24b):").grid(row=2, column=0, padx=10, pady=10)
entry_deduction_24b = tk.Entry(root)
entry_deduction_24b.grid(row=2, column=1, padx=10, pady=10)

# Create and place the calculate button
calculate_button = tk.Button(root, text="Calculate Tax", command=calculate_tax)
calculate_button.grid(row=3, columnspan=2, pady=20)

# Run the main loop
root.mainloop()
