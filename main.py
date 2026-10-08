"""Тестовое приложение для Toolbox ARM.

Проверяет весь путь запуска через батник:
  * батник нашёл Python, создал venv и поставил pandas и openpyxl из requirements.txt
    (видно в окне запуска: этапы и полоса «Библиотеки»);
  * вывод программы, в том числе русский текст, приходит в консоль окна запуска;
  * открывается обычное окно программы (tkinter) с таблицей;
  * закрыли окно — программа завершилась, этап «Приложение» стал «завершено».
"""
import sys
import time

print("Тест pandas: старт")
print(f"Python {sys.version.split()[0]}: {sys.executable}")

import pandas as pd  # noqa: E402

print(f"pandas {pd.__version__} импортирован")

for step in range(1, 4):
    print(f"Подготовка данных: шаг {step} из 3…")
    time.sleep(0.5)

df = pd.DataFrame({
    "Отдел": ["Продажи", "Финансы", "ИТ", "Продажи", "ИТ", "Финансы"],
    "Сотрудник": ["Иванов", "Петрова", "Сидоров", "Козлова", "Смирнов", "Орлова"],
    "Сумма": [120_000, 95_500, 143_250, 88_000, 101_700, 76_300],
})
summary = df.groupby("Отдел", as_index=False)["Сумма"].sum().sort_values("Сумма", ascending=False)
print("\nИтог по отделам:")
print(summary.to_string(index=False))

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    print("\ntkinter недоступен — окно не показываю, программа завершена.")
    sys.exit(0)

try:
    root = tk.Tk()
except tk.TclError as error:  # нет рабочего стола (например, запуск по SSH)
    print(f"\nОкно открыть нельзя ({error}) — программа завершена.")
    sys.exit(0)
root.title("Тест pandas — Toolbox ARM")
root.geometry("460x300")
ttk.Label(root, text="Итог по отделам (pandas groupby)", font=("Segoe UI", 12, "bold")).pack(pady=(14, 8))
tree = ttk.Treeview(root, columns=("dept", "sum"), show="headings", height=5)
tree.heading("dept", text="Отдел")
tree.heading("sum", text="Сумма, ₽")
tree.column("sum", anchor="e")
for _, row in summary.iterrows():
    tree.insert("", "end", values=(row["Отдел"], f"{row['Сумма']:,}".replace(",", " ")))
tree.pack(fill="both", expand=True, padx=14)
ttk.Button(root, text="Закрыть", command=root.destroy).pack(pady=12)

print("\nОкно открыто. Закройте его — программа завершится.")
root.mainloop()
print("Окно закрыто, программа завершена.")
