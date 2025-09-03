#!/usr/bin/env python3
"""
Momentum — Fully Centered Habit Tracker CLI
"""

from __future__ import annotations
import os
import sqlite3
from datetime import date
from dataclasses import dataclass
from typing import List
import platform

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import box

DB_FILE = "momentum.db"
console = Console()

# ───────────────────────────────
# Terminal Helper
# ───────────────────────────────
def clear_terminal():
    os.system("cls" if platform.system() == "Windows" else "clear")

# ───────────────────────────────
# Data Models
# ───────────────────────────────
@dataclass
class Habit:
    id: int
    name: str

# ───────────────────────────────
# Database
# ───────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER,
                    log_date TEXT,
                    done INTEGER,
                    FOREIGN KEY (habit_id) REFERENCES habits (id)
                )""")
    conn.commit()
    conn.close()

def add_habit(name: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO habits (name) VALUES (?)", (name,))
        conn.commit()
        console.print(Align.center(Panel(f"[green]Habit added:[/green] {name}", border_style="green", expand=False)))
    except sqlite3.IntegrityError:
        console.print(Align.center(Panel(f"[red]Habit already exists:[/red] {name}", border_style="red", expand=False)))
    conn.close()

def remove_habit(name: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM habits WHERE name=?", (name,))
    conn.commit()
    conn.close()
    console.print(Align.center(Panel(f"[red]Habit removed:[/red] {name}", border_style="red", expand=False)))

def list_habits() -> List[Habit]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name FROM habits")
    habits = [Habit(id=row[0], name=row[1]) for row in c.fetchall()]
    conn.close()
    return habits

def log_habit(name: str, done: bool = True):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id FROM habits WHERE name=?", (name,))
    row = c.fetchone()
    if row:
        habit_id = row[0]
        today = str(date.today())
        c.execute("SELECT id FROM logs WHERE habit_id=? AND log_date=?", (habit_id, today))
        if c.fetchone():
            c.execute("UPDATE logs SET done=? WHERE habit_id=? AND log_date=?", (int(done), habit_id, today))
        else:
            c.execute("INSERT INTO logs (habit_id, log_date, done) VALUES (?,?,?)", (habit_id, today, int(done)))
        conn.commit()
        console.print(Align.center(Panel(f"[cyan]Logged:[/cyan] {name} → {'✅' if done else '❌'}", border_style="cyan", expand=False)))
    else:
        console.print(Align.center(Panel(f"[red]Habit not found:[/red] {name}", border_style="red", expand=False)))
    conn.close()

def show_history(habit_name: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id FROM habits WHERE name=?", (habit_name,))
    row = c.fetchone()
    if not row:
        console.print(Align.center(Panel(f"[red]No habit found:[/red] {habit_name}", border_style="red", expand=False)))
        return
    habit_id = row[0]
    c.execute("SELECT log_date, done FROM logs WHERE habit_id=? ORDER BY log_date", (habit_id,))
    logs = c.fetchall()
    conn.close()

    table = Table(title=f"History — {habit_name}", box=box.SIMPLE_HEAVY, expand=False)
    table.add_column("Date", style="dim", justify="center")
    table.add_column("Done", style="bold", justify="center")
    if not logs:
        table.add_row("-", "-")
    else:
        for log_date, done in logs:
            table.add_row(log_date, "✅" if done else "❌")
    console.print(Align.center(table))

# ───────────────────────────────
# Menu
# ───────────────────────────────
def show_menu():
    menu_text = """
[bold magenta]Momentum — Habit Tracker[/bold magenta]

[green][1][/green] Add Habit
[green][2][/green] View History
[green][3][/green] Log Habit
[green][4][/green] Remove Habit
[green][5][/green] List Habits
[green][6][/green] Quit
"""
    console.print(Align.center(Panel(Align.center(Text.from_markup(menu_text)), border_style="magenta", padding=(1,3), expand=False)))

# ───────────────────────────────
# Centered input
# ───────────────────────────────
def centered_input(prompt: str) -> str:
    width = console.size.width
    plain_prompt = Text.from_markup(f"[bold yellow]{prompt}[/bold yellow] ").plain
    pad = max((width - len(plain_prompt)) // 2, 0)
    return console.input(" " * pad + f"[bold yellow]{prompt}[/bold yellow] ").strip()

# ───────────────────────────────
# Main Loop
# ───────────────────────────────
def main():
    init_db()
    while True:
        clear_terminal()
        show_menu()
        choice = centered_input("Choose an option [1/2/3/4/5/6]:")
        if choice == "1":
            name = centered_input("Habit name:")
            if name: add_habit(name)
        elif choice == "2":
            name = centered_input("Which habit?")
            if name: show_history(name)
        elif choice == "3":
            name = centered_input("Habit name:")
            if name: log_habit(name, True)
        elif choice == "4":
            name = centered_input("Habit name:")
            if name: remove_habit(name)
        elif choice == "5":
            habits = list_habits()
            if habits:
                table = Table(title="Habits", box=box.SIMPLE_HEAVY, expand=False)
                table.add_column("ID", style="dim", justify="center")
                table.add_column("Name", style="bold cyan", justify="center")
                for h in habits:
                    table.add_row(str(h.id), h.name)
                console.print(Align.center(table))
            else:
                console.print(Align.center(Panel("[yellow]No habits yet.[/yellow]", expand=False)))
        elif choice == "6" or choice.lower() == "q":
            console.print(Align.center(Panel("[bold red]Exited - Keep tracking your habits![/bold red]", expand=False)))
            break
        else:
            console.print(Align.center(Panel("[red]Invalid choice. Please select a number from the menu.[/red]", border_style="red", expand=False)))

        console.input(Align.center("\nPress [bold cyan]Enter[/bold cyan] to continue..."))

if __name__ == "__main__":
    main()
