"""FCFS CPU Scheduling Simulator — Python 3, standard-library Tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox


def schedule_fcfs(processes):
    """Return (scheduled rows, timeline, averages). All times are integers."""
    if not processes:
        raise ValueError("Add at least one process.")
    seen = set()
    for p in processes:
        if not isinstance(p['arrival'], int) or p['arrival'] < 0:
            raise ValueError("Arrival time must be a non-negative integer.")
        if not isinstance(p['burst'], int) or p['burst'] <= 0:
            raise ValueError("Burst time must be a positive integer.")
        if p['id'] in seen:
            raise ValueError("Process IDs must be unique.")
        seen.add(p['id'])
    ordered = sorted(enumerate(processes), key=lambda pair: (pair[1]['arrival'], pair[0]))
    current = 0
    rows = []
    timeline = []
    for _, p in ordered:
        if current < p['arrival']:
            timeline.append({'label': 'IDLE', 'start': current, 'end': p['arrival']})
            current = p['arrival']
        start = current
        current += p['burst']
        rows.append({**p, 'start': start, 'completion': current,
                     'turnaround': current - p['arrival'], 'waiting': start - p['arrival']})
        timeline.append({'label': p['id'], 'start': start, 'end': current})
    averages = {'waiting': sum(r['waiting'] for r in rows) / len(rows),
                'turnaround': sum(r['turnaround'] for r in rows) / len(rows)}
    return rows, timeline, averages


class FCFSApp(tk.Tk):
    COLORS = ['#2563eb', '#059669', '#7c3aed', '#ea580c', '#0891b2', '#be185d', '#4f46e5']

    def __init__(self):
        super().__init__()
        self.title('FCFS CPU Scheduling Simulator')
        self.geometry('1180x820')
        self.minsize(900, 650)
        self.configure(bg='#f3f6fb')
        self.processes = []
        self.next_id = 1
        self.timeline = []
        self._style()
        self._build()
        self.load_sample()

    def _style(self):
        style = ttk.Style(self)
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure('TFrame', background='#f3f6fb')
        style.configure('TLabel', background='#f3f6fb', foreground='#475569', font=('Segoe UI', 10))
        style.configure('TEntry', padding=7)
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=(13, 9),
                        background='#e2e8f0', foreground='#0f172a', borderwidth=0)
        style.map('TButton', background=[('active', '#cbd5e1')])
        style.configure('Primary.TButton', background='#2563eb', foreground='#ffffff')
        style.map('Primary.TButton', background=[('active', '#1d4ed8')])
        style.configure('Treeview', font=('Segoe UI', 10), rowheight=32,
                        background='#ffffff', fieldbackground='#ffffff', foreground='#334155',
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#dbeafe')], foreground=[('selected', '#1e3a8a')])
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'),
                        background='#eaf0f8', foreground='#334155', padding=9, relief='flat')

    def _build(self):
        # A vertically scrollable dashboard keeps the summary visible on smaller screens.
        shell = tk.Canvas(self, bg='#f3f6fb', highlightthickness=0)
        vbar = ttk.Scrollbar(self, orient='vertical', command=shell.yview)
        shell.configure(yscrollcommand=vbar.set)
        vbar.pack(side='right', fill='y')
        shell.pack(side='left', fill='both', expand=True)
        root = tk.Frame(shell, bg='#f3f6fb', padx=24, pady=18)
        window = shell.create_window((0, 0), window=root, anchor='nw')
        root.bind('<Configure>', lambda e: shell.configure(scrollregion=shell.bbox('all')))
        shell.bind('<Configure>', lambda e: shell.itemconfigure(window, width=e.width))
        def wheel(e):
            if e.delta:
                shell.yview_scroll(int(-e.delta / 120), 'units')
        shell.bind_all('<MouseWheel>', wheel)

        header = tk.Frame(root, bg='#f3f6fb')
        header.pack(fill='x', pady=(0, 16))
        tk.Label(header, text='FCFS  /  CPU SCHEDULING', bg='#f3f6fb', fg='#2563eb',
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        tk.Label(header, text='Scheduling Dashboard', bg='#f3f6fb', fg='#0f172a',
                 font=('Segoe UI', 25, 'bold')).pack(anchor='w')
        tk.Label(header, text='First Come, First Served  •  Non-preemptive  •  Arrival-order execution',
                 bg='#f3f6fb', fg='#64748b', font=('Segoe UI', 10)).pack(anchor='w', pady=(4, 0))

        def panel(title, subtitle=None):
            outer = tk.Frame(root, bg='white', highlightbackground='#dbe3ef', highlightthickness=1)
            outer.pack(fill='x', pady=(0, 13))
            head = tk.Frame(outer, bg='white', padx=16, pady=12)
            head.pack(fill='x')
            tk.Label(head, text=title, bg='white', fg='#0f172a',
                     font=('Segoe UI', 12, 'bold')).pack(anchor='w')
            if subtitle:
                tk.Label(head, text=subtitle, bg='white', fg='#64748b',
                         font=('Segoe UI', 9)).pack(anchor='w', pady=(3, 0))
            content = tk.Frame(outer, bg='white', padx=16, pady=8)
            content.pack(fill='x', pady=(0, 10))
            return content

        form = panel('01   Process input', 'Enter nonnegative arrival times and positive burst times.')
        self.id_var = tk.StringVar()
        self.arrival_var = tk.StringVar()
        self.burst_var = tk.StringVar()
        for i, (label, var) in enumerate((('Process ID', self.id_var),
                                           ('Arrival Time (AT)', self.arrival_var),
                                           ('Burst Time (BT)', self.burst_var))):
            field = tk.Frame(form, bg='white')
            field.grid(row=0, column=i, sticky='ew', padx=(0, 12))
            tk.Label(field, text=label, bg='white', fg='#475569',
                     font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(0, 5))
            ttk.Entry(field, textvariable=var).pack(fill='x')
            form.columnconfigure(i, weight=1)
        buttons = tk.Frame(form, bg='white')
        buttons.grid(row=0, column=3, sticky='s')
        ttk.Button(buttons, text='+ Add', command=self.add_process,
                   style='Primary.TButton').pack(side='left', padx=3)
        ttk.Button(buttons, text='Update', command=self.update_selected).pack(side='left', padx=3)
        ttk.Button(buttons, text='Delete', command=self.delete_selected).pack(side='left', padx=3)

        toolbar = tk.Frame(root, bg='#f3f6fb')
        toolbar.pack(fill='x', pady=(0, 14))
        ttk.Button(toolbar, text='▶  Run FCFS', command=self.run_schedule,
                   style='Primary.TButton').pack(side='left', padx=(0, 9))
        ttk.Button(toolbar, text='Load sample', command=self.load_sample).pack(side='left', padx=(0, 9))
        ttk.Button(toolbar, text='Clear all', command=self.clear_all).pack(side='left')
        self.status = tk.StringVar(value='Ready.')
        tk.Label(toolbar, textvariable=self.status, bg='#f3f6fb', fg='#475569',
                 font=('Segoe UI', 9)).pack(side='right')

        input_panel = panel('02   Process queue', 'Select a row to edit or delete it.')
        self.input_tree = ttk.Treeview(input_panel, columns=('pid', 'arrival', 'burst'),
                                       show='headings', height=4, selectmode='browse')
        for col, heading in [('pid', 'Process'), ('arrival', 'Arrival Time'), ('burst', 'Burst Time')]:
            self.input_tree.heading(col, text=heading)
            self.input_tree.column(col, anchor='center', width=130)
        self.input_tree.pack(fill='x')
        self.input_tree.bind('<<TreeviewSelect>>', self.select_process)

        chart_panel = panel('03   Gantt chart', 'Execution timeline; gray blocks indicate idle CPU time.')
        self.canvas = tk.Canvas(chart_panel, height=122, bg='white', highlightthickness=0)
        scroll = ttk.Scrollbar(chart_panel, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=scroll.set)
        self.canvas.pack(fill='x')
        scroll.pack(fill='x')
        self.canvas.bind('<Configure>', lambda event: self.draw_gantt())

        result_panel = panel('04   Scheduling results', 'CT = completion time  •  TAT = CT − AT  •  WT = TAT − BT')
        columns = ('pid', 'arrival', 'burst', 'start', 'completion', 'turnaround', 'waiting')
        headings = ('Process', 'AT', 'BT', 'Start', 'CT', 'TAT', 'WT')
        self.result_tree = ttk.Treeview(result_panel, columns=columns, show='headings', height=5)
        for col, heading in zip(columns, headings):
            self.result_tree.heading(col, text=heading)
            self.result_tree.column(col, anchor='center', minwidth=70, width=110)
        self.result_tree.pack(fill='x')
        self.result_tree.tag_configure('alternate', background='#f8fafc')

        metrics = tk.Frame(root, bg='#f3f6fb')
        metrics.pack(fill='x', pady=(0, 18))
        self.avg_wait = tk.StringVar(value='Average Waiting Time: —')
        self.avg_turn = tk.StringVar(value='Average Turnaround Time: —')
        for i, (name, variable) in enumerate((('WAITING TIME', self.avg_wait),
                                              ('TURNAROUND TIME', self.avg_turn))):
            card = tk.Frame(metrics, bg='white', highlightbackground='#dbe3ef', highlightthickness=1,
                            padx=18, pady=14)
            card.grid(row=0, column=i, sticky='ew', padx=(0 if i == 0 else 7, 7 if i == 0 else 0))
            metrics.columnconfigure(i, weight=1)
            tk.Label(card, text=name, bg='white', fg='#64748b',
                     font=('Segoe UI', 9, 'bold')).pack(anchor='w')
            tk.Label(card, textvariable=variable, bg='white', fg='#1d4ed8',
                     font=('Segoe UI', 15, 'bold')).pack(anchor='w', pady=(7, 0))

    def _get_input(self):
        pid = self.id_var.get().strip()
        if not pid:
            raise ValueError('Process ID cannot be empty.')
        try:
            arrival = int(self.arrival_var.get().strip())
            burst = int(self.burst_var.get().strip())
        except ValueError:
            raise ValueError('Arrival and burst times must be whole numbers.') from None
        if arrival < 0:
            raise ValueError('Arrival time must be 0 or greater.')
        if burst <= 0:
            raise ValueError('Burst time must be greater than 0.')
        return {'id': pid, 'arrival': arrival, 'burst': burst}

    def _unique(self, pid, skip=None):
        return all(p['id'].casefold() != pid.casefold() for i, p in enumerate(self.processes) if i != skip)

    def _clear_inputs(self):
        self.id_var.set(f'P{self.next_id}')
        self.arrival_var.set('')
        self.burst_var.set('')

    def _refresh_input(self):
        self.input_tree.delete(*self.input_tree.get_children())
        for i, p in enumerate(self.processes):
            self.input_tree.insert('', 'end', iid=str(i), values=(p['id'], p['arrival'], p['burst']))
        self._clear_results()

    def _clear_results(self):
        self.result_tree.delete(*self.result_tree.get_children())
        self.timeline = []
        self.avg_wait.set('Average Waiting Time: —')
        self.avg_turn.set('Average Turnaround Time: —')
        self.draw_gantt()

    def add_process(self):
        try:
            p = self._get_input()
            if not self._unique(p['id']):
                raise ValueError('Process ID already exists.')
        except ValueError as exc:
            messagebox.showerror('Invalid input', str(exc))
            return
        self.processes.append(p)
        self.next_id += 1
        self._refresh_input()
        self.status.set(f'{len(self.processes)} process(es) added. Run FCFS to calculate.')

    def select_process(self, _event=None):
        selected = self.input_tree.selection()
        if selected:
            p = self.processes[int(selected[0])]
            self.id_var.set(p['id'])
            self.arrival_var.set(str(p['arrival']))
            self.burst_var.set(str(p['burst']))

    def update_selected(self):
        selected = self.input_tree.selection()
        if not selected:
            messagebox.showwarning('No selection', 'Select a process to update.')
            return
        index = int(selected[0])
        try:
            p = self._get_input()
            if not self._unique(p['id'], skip=index):
                raise ValueError('Process ID already exists.')
        except ValueError as exc:
            messagebox.showerror('Invalid input', str(exc))
            return
        self.processes[index] = p
        self._refresh_input()
        self.status.set('Process updated. Run FCFS again.')

    def delete_selected(self):
        selected = self.input_tree.selection()
        if not selected:
            messagebox.showwarning('No selection', 'Select a process to delete.')
            return
        del self.processes[int(selected[0])]
        self._refresh_input()
        self.status.set('Process deleted. Run FCFS again.')

    def clear_all(self):
        self.processes.clear()
        self.next_id = 1
        self._refresh_input()
        self.status.set('All processes cleared.')

    def load_sample(self):
        self.processes = [
            {'id': 'P1', 'arrival': 0, 'burst': 5},
            {'id': 'P2', 'arrival': 1, 'burst': 3},
            {'id': 'P3', 'arrival': 2, 'burst': 8},
            {'id': 'P4', 'arrival': 3, 'burst': 2},
        ]
        self.next_id = 5
        self._refresh_input()
        self.run_schedule()

    def run_schedule(self):
        try:
            rows, self.timeline, averages = schedule_fcfs(self.processes)
        except ValueError as exc:
            messagebox.showerror('Cannot schedule', str(exc))
            return
        self.result_tree.delete(*self.result_tree.get_children())
        for i, p in enumerate(rows):
            self.result_tree.insert('', 'end', tags=('alternate',) if i % 2 else (), values=(p['id'], p['arrival'], p['burst'], p['start'],
                                                       p['completion'], p['turnaround'], p['waiting']))
        self.avg_wait.set(f"Average Waiting Time: {averages['waiting']:.2f}")
        self.avg_turn.set(f"Average Turnaround Time: {averages['turnaround']:.2f}")
        self.status.set(f'Scheduled {len(rows)} process(es) successfully.')
        self.draw_gantt()

    def draw_gantt(self):
        c = self.canvas
        c.delete('all')
        if not self.timeline:
            c.create_text(18, 48, text='Run FCFS to display the Gantt chart.', anchor='w', fill='#64748b')
            c.configure(scrollregion=(0, 0, 500, 122))
            return
        x = 24
        color_idx = 0
        for segment in self.timeline:
            duration = segment['end'] - segment['start']
            width = max(70, duration * 32)
            idle = segment['label'] == 'IDLE'
            color = '#cbd5e1' if idle else self.COLORS[color_idx % len(self.COLORS)]
            if not idle:
                color_idx += 1
            c.create_rectangle(x, 22, x + width, 77, fill=color, outline='white', width=2)
            c.create_text(x + width / 2, 49, text=segment['label'], fill='#0f172a' if idle else 'white', font=('Segoe UI', 10, 'bold'))
            c.create_text(x, 91, text=str(segment['start']), anchor='n', font=('Segoe UI', 9), fill='#334155')
            x += width
        c.create_text(x, 91, text=str(self.timeline[-1]['end']), anchor='n', font=('Segoe UI', 9), fill='#334155')
        c.configure(scrollregion=(0, 0, x + 40, 122))


if __name__ == '__main__':
    app = FCFSApp()
    app.mainloop()
