import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

data_file = "expenses.json"

def load_data():
    if not os.path.exists(data_file):
        return []
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

expenses = load_data()

def add_expenses():
    amount = ent_amount.get()
    category = cb_category.get()
    date = ent_date.get()

    try:
        amount_float = float(amount)
        if amount_float <= 0: raise ValueError
        datetime.strptime(date, "%Y-%m-%d")

    except ValueError:
        messagebox.showerror("Ошибка", "Сумма должна быть > 0, дата: ГГГГ-ММ-ДД")
        return

    new_item = {"amount": amount_float, "category": category, "date": date}
    expenses.append(new_item)
    save_data(expenses)
    update_expenses()
    ent_amount.delete(0, tk.END)

def update_expenses():
    for row in table.get_children():
        table.delete(row)

    selected_cat = filter_category.get()
    total = 0

    for exp in expenses:
        if selected_cat == "Все" or exp["category"] == selected_cat:
            table.insert("", "end", values=(exp["amount"], exp["category"], exp["date"]))
            total += exp["amount"]

    label_total.config(text=f"Итого: {total:.2f}")

window = tk.Tk()
window.title("Expense Tracker (Трекер расходов)")
window.geometry("800x500")

frame_form = ttk.LabelFrame(window, text="Добавить расход")
frame_form.pack(pady=10, padx=10, fill="x")

sum_label = tk.Label(frame_form, text="Сумма:")
sum_label.grid(row=0, column=0, padx=5, pady=5)
ent_amount = tk.Entry(frame_form)
ent_amount.grid(row=0, column=1, padx=5, pady=5)

category_label = tk.Label(frame_form, text="Категория:")
category_label.grid(row=0, column=2, padx=5, pady=5)
cb_category = ttk.Combobox(frame_form, values=["Еда", "Транспорт", "Развлечения", "Дом"], state="readonly")
cb_category.grid(row=0, column=3, padx=5, pady=5)
cb_category.current(0)

data_label = tk.Label(frame_form, text="Дата: ")
data_label.grid(row=0, column=4, padx=5, pady=5)
ent_date = ttk.Entry(frame_form)
ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
ent_date.grid(row=0, column=5, padx=5, pady=5)

add_button = tk.Button(frame_form, text="Добавить", command=add_expenses)
add_button.grid(row=0, column=6, padx=5, pady=5)

filter_frame = tk.LabelFrame(window, text="Фильтр")
filter_frame.pack(pady=5, padx=10)

filter_category = ttk.Combobox(filter_frame, values=["Все", "Еда", "Транспорт", "Развлечения", "Дом"], state="readonly")
filter_category.current(0)
filter_category.pack(side="left", padx=5, pady=5)

ttk.Label(filter_frame, text="С:").pack(side="left", padx=2)
filter_start = ttk.Entry(filter_frame, width=10)
filter_start.insert(0, "2024-01-01")
filter_start.pack(side="left", padx=2)
ttk.Label(filter_frame, text="По:").pack(side="left", padx=2)
filter_end = ttk.Entry(filter_frame, width=10)
filter_end.insert(0, datetime.now().strftime("%Y-%m-%d"))
filter_end.pack(side="left", padx=2)

filter_button = tk.Button(filter_frame, text="Применить", command=update_expenses)
filter_button.pack(side="left", padx=5)

label_total = ttk.Label(filter_frame, text="Итого: 0", font="Arial 10")
label_total.pack(side="right", padx=10)

table = ttk.Treeview(window, columns=("Amount", "Category", "Date"), show="headings")
table.heading("Amount", text="Сумма")
table.heading("Category", text="Категория")
table.heading("Date", text="Дата")
table.pack(pady=10, padx=10, fill="both", expand=True)

update_expenses()

window.mainloop()