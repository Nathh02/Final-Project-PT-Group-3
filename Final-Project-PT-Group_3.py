import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class DiskSchedulingApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Disk Scheduling Simulator (FCFS, SSTF, SCAN)")
        self.root.geometry("1180x760")
        self.root.minsize(980, 650)
        self.root.configure(bg="#e9edf2")

        self.history_records: list[str] = []
        self.last_results: dict | None = None

        self._configure_styles()
        self._build_layout()
        self._load_sample_defaults()
        self._show_page("home")

    def _configure_styles(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Sim.Treeview",
            background="#ffffff",
            foreground="#1e293b",
            rowheight=26,
            fieldbackground="#ffffff",
            bordercolor="#cbd5e1",
            borderwidth=1,
            font=("Segoe UI", 9),
        )
        style.configure(
            "Sim.Treeview.Heading",
            background="#1e3a8a",
            foreground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
        )
        style.map("Sim.Treeview.Heading", background=[("active", "#1d4ed8")])

    def _build_layout(self) -> None:
        # Left Sidebar
        self.sidebar = tk.Frame(self.root, bg="#172554", width=210)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        brand_box = tk.Frame(self.sidebar, bg="#0f172a", padx=16, pady=18)
        brand_box.pack(fill=tk.X)

        tk.Label(
            brand_box,
            text="DISK\nSCHEDULING",
            bg="#0f172a",
            fg="#ffffff",
            font=("Segoe UI", 14, "bold"),
            justify=tk.LEFT,
        ).pack(anchor="w")

        tk.Label(
            brand_box,
            text="SIMULATOR",
            bg="#0f172a",
            fg="#93c5fd",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(2, 0))

        self.nav_home_btn = tk.Button(
            self.sidebar,
            text="   Home",
            bg="#1e40af",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            padx=14,
            pady=12,
            cursor="hand2",
            command=lambda: self._show_page("home"),
        )
        self.nav_home_btn.pack(fill=tk.X, pady=(10, 2))

        self.nav_about_btn = tk.Button(
            self.sidebar,
            text="   Comparison & About",
            bg="#172554",
            fg="#cbd5e1",
            activebackground="#1e3a8a",
            activeforeground="#ffffff",
            bd=0,
            font=("Segoe UI", 10),
            anchor="w",
            padx=14,
            pady=12,
            cursor="hand2",
            command=lambda: self._show_page("about"),
        )
        self.nav_about_btn.pack(fill=tk.X, pady=2)

        # Main Content Area
        self.main_area = tk.Frame(self.root, bg="#e9edf2")
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Top Header Bar
        header_bar = tk.Frame(self.main_area, bg="#ffffff", padx=22, pady=12)
        header_bar.pack(fill=tk.X)
        tk.Frame(self.main_area, bg="#cbd5e1", height=1).pack(fill=tk.X)

        self.header_title = tk.Label(
            header_bar,
            text="DISK SCHEDULING SIMULATOR",
            bg="#ffffff",
            fg="#0f172a",
            font=("Segoe UI", 16, "bold"),
        )
        self.header_title.pack(side=tk.LEFT)

        self.header_sub = tk.Label(
            header_bar,
            text="FCFS  |  SSTF  |  SCAN (Elevator)",
            bg="#ffffff",
            fg="#475569",
            font=("Segoe UI", 10),
        )
        self.header_sub.pack(side=tk.RIGHT)

        # Pages Container
        self.pages_container = tk.Frame(self.main_area, bg="#e9edf2")
        self.pages_container.pack(fill=tk.BOTH, expand=True, padx=16, pady=14)

        self.home_page = tk.Frame(self.pages_container, bg="#e9edf2")
        self.about_page = tk.Frame(self.pages_container, bg="#e9edf2")

        self._build_home_page()
        self._build_about_page()

    def _build_home_page(self) -> None:
        upper_row = tk.Frame(self.home_page, bg="#e9edf2")
        upper_row.pack(fill=tk.BOTH, expand=True)

        # --- LEFT INPUT PANEL ---
        input_card = tk.Frame(
            upper_row,
            bg="#ffffff",
            bd=1,
            relief=tk.SOLID,
            width=310,
            padx=16,
            pady=14,
        )
        input_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        input_card.pack_propagate(False)

        tk.Label(
            input_card,
            text="Input",
            bg="#ffffff",
            fg="#0f172a",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        tk.Label(
            input_card,
            text="Select Algorithm",
            bg="#ffffff",
            fg="#334155",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        self.algo_var = tk.StringVar(value="FCFS")
        algo_combo = ttk.Combobox(
            input_card,
            textvariable=self.algo_var,
            values=["FCFS", "SSTF", "SCAN (Elevator)"],
            state="readonly",
            font=("Segoe UI", 9),
        )
        algo_combo.pack(fill=tk.X, pady=(3, 10))
        algo_combo.bind("<<ComboboxSelected>>", lambda _e: self._refresh_selected_algo_view())

        range_row = tk.Frame(input_card, bg="#ffffff")
        range_row.pack(fill=tk.X, pady=(0, 10))

        min_col = tk.Frame(range_row, bg="#ffffff")
        min_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        tk.Label(
            min_col,
            text="Disk Min",
            bg="#ffffff",
            fg="#334155",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        self.min_entry = tk.Entry(min_col, font=("Segoe UI", 9), bg="#f8fafc", relief=tk.SOLID, bd=1)
        self.min_entry.pack(fill=tk.X, pady=(3, 0), ipady=3)

        max_col = tk.Frame(range_row, bg="#ffffff")
        max_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))
        tk.Label(
            max_col,
            text="Disk Max",
            bg="#ffffff",
            fg="#334155",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        self.max_entry = tk.Entry(max_col, font=("Segoe UI", 9), bg="#f8fafc", relief=tk.SOLID, bd=1)
        self.max_entry.pack(fill=tk.X, pady=(3, 0), ipady=3)

        head_dir_row = tk.Frame(input_card, bg="#ffffff")
        head_dir_row.pack(fill=tk.X, pady=(0, 10))

        head_col = tk.Frame(head_dir_row, bg="#ffffff")
        head_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        tk.Label(
            head_col,
            text="Initial Head",
            bg="#ffffff",
            fg="#334155",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        self.head_entry = tk.Entry(head_col, font=("Segoe UI", 9), bg="#f8fafc", relief=tk.SOLID, bd=1)
        self.head_entry.pack(fill=tk.X, pady=(3, 0), ipady=3)

        dir_col = tk.Frame(head_dir_row, bg="#ffffff")
        dir_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))
        tk.Label(
            dir_col,
            text="SCAN Direction",
            bg="#ffffff",
            fg="#334155",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        self.dir_var = tk.StringVar(value="right")
        dir_combo = ttk.Combobox(
            dir_col,
            textvariable=self.dir_var,
            values=["right", "left"],
            state="readonly",
            font=("Segoe UI", 9),
        )
        dir_combo.pack(fill=tk.X, pady=(3, 0))

        tk.Label(
            input_card,
            text="Request Queue (Cylinders)",
            bg="#ffffff",
            fg="#334155",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        self.queue_entry = tk.Entry(input_card, font=("Segoe UI", 9), bg="#f8fafc", relief=tk.SOLID, bd=1)
        self.queue_entry.pack(fill=tk.X, pady=(3, 14), ipady=4)

        run_btn = tk.Button(
            input_card,
            text="Run Simulation",
            bg="#f59e0b",
            fg="#0f172a",
            activebackground="#d97706",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            pady=8,
            cursor="hand2",
            command=self.run_simulation,
        )
        run_btn.pack(fill=tk.X)

        reset_btn = tk.Button(
            input_card,
            text="Reset Sample",
            bg="#e2e8f0",
            fg="#1e293b",
            activebackground="#cbd5e1",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            pady=5,
            cursor="hand2",
            command=self._load_sample_defaults,
        )
        reset_btn.pack(fill=tk.X, pady=(8, 0))

        # --- RIGHT RESULTS PANEL ---
        results_card = tk.Frame(
            upper_row,
            bg="#ffffff",
            bd=1,
            relief=tk.SOLID,
            padx=16,
            pady=14,
        )
        results_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        top_res_header = tk.Frame(results_card, bg="#ffffff")
        top_res_header.pack(fill=tk.X, pady=(0, 8))

        tk.Label(
            top_res_header,
            text="Results",
            bg="#ffffff",
            fg="#0f172a",
            font=("Segoe UI", 13, "bold"),
        ).pack(side=tk.LEFT)

        self.active_algo_banner = tk.Label(
            top_res_header,
            text="FCFS Algorithm",
            bg="#ffffff",
            fg="#1e3a8a",
            font=("Segoe UI", 11, "bold"),
        )
        self.active_algo_banner.pack(side=tk.RIGHT)

        # Info Strip
        info_strip = tk.Frame(results_card, bg="#f8fafc", bd=1, relief=tk.SOLID, padx=10, pady=6)
        info_strip.pack(fill=tk.X, pady=(0, 10))

        self.lbl_meta = tk.Label(
            info_strip,
            text="Initial Head: -  |  Request Queue: -",
            bg="#f8fafc",
            fg="#334155",
            font=("Segoe UI", 9, "bold"),
            anchor="w",
        )
        self.lbl_meta.pack(fill=tk.X)

        self.lbl_sequence = tk.Label(
            info_strip,
            text="Service Sequence: -",
            bg="#f8fafc",
            fg="#0f172a",
            font=("Consolas", 9, "bold"),
            anchor="w",
            wraplength=760,
            justify=tk.LEFT,
        )
        self.lbl_sequence.pack(fill=tk.X, pady=(2, 0))

        # Step by step Table
        table_frame = tk.Frame(results_card, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("step", "from_cyl", "to_cyl", "calc", "movement")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Sim.Treeview",
            height=8,
        )
        self.tree.heading("step", text="Step")
        self.tree.heading("from_cyl", text="From Cylinder")
        self.tree.heading("to_cyl", text="To Cylinder")
        self.tree.heading("calc", text="Calculation")
        self.tree.heading("movement", text="Movement (Cylinders)")

        self.tree.column("step", width=65, anchor=tk.CENTER)
        self.tree.column("from_cyl", width=110, anchor=tk.CENTER)
        self.tree.column("to_cyl", width=155, anchor=tk.CENTER)
        self.tree.column("calc", width=140, anchor=tk.CENTER)
        self.tree.column("movement", width=140, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Summary Metric Cards
        stats_grid = tk.Frame(results_card, bg="#ffffff")
        stats_grid.pack(fill=tk.X, pady=(10, 0))
        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)

        self.card_total_val = self._make_stat_box(stats_grid, 0, 0, "Total Head Movement", "0 cylinders")
        self.card_avg_val = self._make_stat_box(stats_grid, 0, 1, "Average Seek Length", "0.00")
        self.card_fcfs_val = self._make_stat_box(stats_grid, 1, 0, "FCFS Total", "-")
        self.card_sstf_scan_val = self._make_stat_box(stats_grid, 1, 1, "SSTF / SCAN Total", "-")

        # --- BOTTOM HISTORY PANEL ---
        history_card = tk.Frame(
            self.home_page,
            bg="#ffffff",
            bd=1,
            relief=tk.SOLID,
            padx=16,
            pady=10,
            height=135,
        )
        history_card.pack(fill=tk.X, pady=(12, 0))
        history_card.pack_propagate(False)

        hist_top = tk.Frame(history_card, bg="#ffffff")
        hist_top.pack(fill=tk.X, pady=(0, 4))

        tk.Label(
            hist_top,
            text="History",
            bg="#ffffff",
            fg="#0f172a",
            font=("Segoe UI", 11, "bold"),
        ).pack(side=tk.LEFT)

        tk.Button(
            hist_top,
            text="Clear History",
            bg="#f59e0b",
            fg="#0f172a",
            font=("Segoe UI", 8, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=2,
            cursor="hand2",
            command=self._clear_history,
        ).pack(side=tk.RIGHT)

        self.history_list = tk.Listbox(
            history_card,
            font=("Consolas", 9),
            bg="#f8fafc",
            fg="#1e293b",
            bd=1,
            relief=tk.SOLID,
            height=4,
        )
        self.history_list.pack(fill=tk.BOTH, expand=True)

    def _make_stat_box(
        self, parent: tk.Frame, row: int, col: int, title: str, initial_val: str
    ) -> tk.Label:
        box = tk.Frame(
            parent,
            bg="#f8fafc",
            bd=1,
            relief=tk.SOLID,
            padx=12,
            pady=6,
        )
        padx_val = (0, 6) if col == 0 else (6, 0)
        pady_val = (0, 6) if row == 0 else (0, 0)
        box.grid(row=row, column=col, sticky="nsew", padx=padx_val, pady=pady_val)

        tk.Label(
            box,
            text=title,
            bg="#f8fafc",
            fg="#64748b",
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w")

        val_lbl = tk.Label(
            box,
            text=initial_val,
            bg="#f8fafc",
            fg="#0f172a",
            font=("Segoe UI", 11, "bold"),
        )
        val_lbl.pack(anchor="w")
        return val_lbl

    def _build_about_page(self) -> None:
        comp_card = tk.Frame(self.about_page, bg="#ffffff", bd=1, relief=tk.SOLID, padx=18, pady=16)
        comp_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            comp_card,
            text="Algorithm Comparison & Overview",
            bg="#ffffff",
            fg="#0f172a",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        self.comp_summary_lbl = tk.Label(
            comp_card,
            text="Run a simulation on the Home tab to view full side-by-side comparison metrics.",
            bg="#ffffff",
            fg="#475569",
            font=("Segoe UI", 9),
        )
        self.comp_summary_lbl.pack(anchor="w", pady=(0, 10))

        comp_cols = ("algo", "total", "avg", "sequence")
        self.comp_tree = ttk.Treeview(
            comp_card,
            columns=comp_cols,
            show="headings",
            style="Sim.Treeview",
            height=5,
        )
        self.comp_tree.heading("algo", text="Algorithm")
        self.comp_tree.heading("total", text="Total Head Movement")
        self.comp_tree.heading("avg", text="Average Seek")
        self.comp_tree.heading("sequence", text="Service Sequence")

        self.comp_tree.column("algo", width=140, anchor=tk.CENTER)
        self.comp_tree.column("total", width=160, anchor=tk.CENTER)
        self.comp_tree.column("avg", width=120, anchor=tk.CENTER)
        self.comp_tree.column("sequence", width=460, anchor=tk.W)
        self.comp_tree.pack(fill=tk.X, pady=(0, 16))

        desc_text = (
            "• FCFS (First-Come, First-Served): Services cylinder requests strictly in arrival order.\n"
            "• SSTF (Shortest Seek Time First): Picks the pending request closest to the current head position.\n"
            "• SCAN (Elevator): Moves in the chosen initial direction up to the disk boundary before reversing."
        )
        tk.Label(
            comp_card,
            text=desc_text,
            bg="#f8fafc",
            fg="#334155",
            font=("Segoe UI", 9),
            justify=tk.LEFT,
            padx=12,
            pady=10,
        ).pack(fill=tk.X)

    def _show_page(self, page_name: str) -> None:
        self.home_page.pack_forget()
        self.about_page.pack_forget()

        if page_name == "home":
            self.home_page.pack(fill=tk.BOTH, expand=True)
            self.nav_home_btn.configure(bg="#1e40af", fg="#ffffff", font=("Segoe UI", 10, "bold"))
            self.nav_about_btn.configure(bg="#172554", fg="#cbd5e1", font=("Segoe UI", 10))
        else:
            self.about_page.pack(fill=tk.BOTH, expand=True)
            self.nav_about_btn.configure(bg="#1e40af", fg="#ffffff", font=("Segoe UI", 10, "bold"))
            self.nav_home_btn.configure(bg="#172554", fg="#cbd5e1", font=("Segoe UI", 10))

    def _load_sample_defaults(self) -> None:
        self.min_entry.delete(0, tk.END)
        self.min_entry.insert(0, "0")

        self.max_entry.delete(0, tk.END)
        self.max_entry.insert(0, "199")

        self.head_entry.delete(0, tk.END)
        self.head_entry.insert(0, "53")

        self.dir_var.set("right")

        self.queue_entry.delete(0, tk.END)
        self.queue_entry.insert(0, "98, 183, 37, 122, 14, 124, 65, 67")

    def _clear_history(self) -> None:
        self.history_records.clear()
        self.history_list.delete(0, tk.END)

    def _parse_and_validate(self) -> tuple[int, int, int, list[int], str] | None:
        try:
            disk_min = int(self.min_entry.get().strip())
            disk_max = int(self.max_entry.get().strip())
            head = int(self.head_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Disk min, disk max, and initial head must be integers.")
            return None

        if disk_min < 0 or disk_min >= disk_max:
            messagebox.showerror(
                "Invalid Disk Range",
                "Disk minimum must be >= 0 and strictly less than disk maximum.",
            )
            return None

        if not (disk_min <= head <= disk_max):
            messagebox.showerror(
                "Invalid Head Position",
                f"Initial head position must be within [{disk_min}, {disk_max}].",
            )
            return None

        tokens = self.queue_entry.get().replace(",", " ").split()
        if not tokens:
            messagebox.showerror("Empty Queue", "Please enter at least one cylinder request.")
            return None

        try:
            queue = [int(t) for t in tokens]
        except ValueError:
            messagebox.showerror("Invalid Queue", "Request queue must contain only integer cylinder numbers.")
            return None

        bad = [c for c in queue if not (disk_min <= c <= disk_max)]
        if bad:
            messagebox.showerror(
                "Out of Range Cylinders",
                f"Cylinders {bad} are outside the valid disk range [{disk_min}, {disk_max}].",
            )
            return None

        direction = self.dir_var.get().strip().lower()
        return disk_min, disk_max, head, queue, direction

    @staticmethod
    def _calc_fcfs(head: int, queue: list[int]) -> dict:
        seq = [head] + list(queue)
        return DiskSchedulingApp._build_algo_result("FCFS", seq, set(queue))

    @staticmethod
    def _calc_sstf(head: int, queue: list[int]) -> dict:
        remaining = list(queue)
        current = head
        seq = [head]
        while remaining:
            nxt = min(remaining, key=lambda c: (abs(c - current), c))
            seq.append(nxt)
            remaining.remove(nxt)
            current = nxt
        return DiskSchedulingApp._build_algo_result("SSTF", seq, set(queue))

    @staticmethod
    def _calc_scan(head: int, queue: list[int], disk_min: int, disk_max: int, direction: str) -> dict:
        left = sorted([c for c in queue if c < head], reverse=True)
        right = sorted([c for c in queue if c >= head])
        seq = [head]

        if direction == "right":
            seq.extend(right)
            if left:
                if seq[-1] != disk_max:
                    seq.append(disk_max)
                seq.extend(left)
        else:
            seq.extend(left)
            if right:
                if seq[-1] != disk_min:
                    seq.append(disk_min)
                seq.extend(right)

        return DiskSchedulingApp._build_algo_result("SCAN (Elevator)", seq, set(queue))

    @staticmethod
    def _build_algo_result(name: str, seq: list[int], queue_set: set[int]) -> dict:
        steps = []
        total = 0
        for i in range(len(seq) - 1):
            a, b = seq[i], seq[i + 1]
            diff = abs(b - a)
            total += diff
            to_str = f"{b} (boundary)" if (b not in queue_set and b != seq[0]) else str(b)
            steps.append((i + 1, a, to_str, f"|{b} - {a}|", diff))
        return {
            "name": name,
            "sequence": seq,
            "steps": steps,
            "total": total,
        }

    def run_simulation(self) -> None:
        parsed = self._parse_and_validate()
        if not parsed:
            return

        disk_min, disk_max, head, queue, direction = parsed

        fcfs_res = self._calc_fcfs(head, queue)
        sstf_res = self._calc_sstf(head, queue)
        scan_res = self._calc_scan(head, queue, disk_min, disk_max, direction)

        self.last_results = {
            "disk_min": disk_min,
            "disk_max": disk_max,
            "head": head,
            "queue": queue,
            "direction": direction,
            "algos": {
                "FCFS": fcfs_res,
                "SSTF": sstf_res,
                "SCAN (Elevator)": scan_res,
            },
        }

        self._refresh_selected_algo_view()
        self._refresh_comparison_table()

        stamp = datetime.now().strftime("%H:%M:%S")
        entry = (
            f"[{stamp}] Head={head} | Queue={queue} | "
            f"FCFS={fcfs_res['total']} | SSTF={sstf_res['total']} | SCAN({direction})={scan_res['total']}"
        )
        self.history_records.insert(0, entry)
        self.history_list.insert(0, entry)

    def _refresh_selected_algo_view(self) -> None:
        if not self.last_results:
            return

        selected_name = self.algo_var.get()
        res = self.last_results["algos"][selected_name]
        queue = self.last_results["queue"]
        head = self.last_results["head"]

        self.active_algo_banner.configure(text=f"{res['name']} Algorithm")
        self.lbl_meta.configure(
            text=f"Initial Head: {head}   |   Request Queue: {queue}   |   Total Movement: {res['total']}"
        )
        self.lbl_sequence.configure(
            text=f"Service Sequence: {' -> '.join(str(x) for x in res['sequence'])}"
        )

        for row in self.tree.get_children():
            self.tree.delete(row)

        for step_num, frm, to_lbl, calc_str, mv in res["steps"]:
            self.tree.insert("", tk.END, values=(step_num, frm, to_lbl, calc_str, mv))

        avg_seek = res["total"] / len(queue)
        fcfs_tot = self.last_results["algos"]["FCFS"]["total"]
        sstf_tot = self.last_results["algos"]["SSTF"]["total"]
        scan_tot = self.last_results["algos"]["SCAN (Elevator)"]["total"]

        self.card_total_val.configure(text=f"{res['total']} cylinders")
        self.card_avg_val.configure(text=f"{avg_seek:.2f} cyl/req")
        self.card_fcfs_val.configure(text=f"{fcfs_tot} cylinders")
        self.card_sstf_scan_val.configure(text=f"SSTF: {sstf_tot}  |  SCAN: {scan_tot}")

    def _refresh_comparison_table(self) -> None:
        if not self.last_results:
            return

        for row in self.comp_tree.get_children():
            self.comp_tree.delete(row)

        queue = self.last_results["queue"]
        algos = self.last_results["algos"]
        best_val = min(item["total"] for item in algos.values())

        for algo_name, item in algos.items():
            avg_val = item["total"] / len(queue)
            tag_note = " (Best)" if item["total"] == best_val else ""
            seq_str = " -> ".join(str(x) for x in item["sequence"])
            self.comp_tree.insert(
                "",
                tk.END,
                values=(
                    algo_name,
                    f"{item['total']} cylinders{tag_note}",
                    f"{avg_val:.2f}",
                    seq_str,
                ),
            )

        self.comp_summary_lbl.configure(
            text=(
                f"Range: [{self.last_results['disk_min']} - {self.last_results['disk_max']}]  |  "
                f"Initial Head: {self.last_results['head']}  |  "
                f"SCAN Direction: {self.last_results['direction'].upper()}  |  "
                f"Queue: {queue}"
            )
        )


def main() -> None:
    root = tk.Tk()
    DiskSchedulingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
