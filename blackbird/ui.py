import json
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from .network import collect_snapshot, filter_tcp
from . import __version__

LABELS = {
    'name': 'Interface', 'ipv4': 'Endereço IPv4', 'ipv6': 'Endereço IPv6',
    'gateway': 'Gateway IPv4', 'dns': 'Servidores DNS',
    'local_address': 'Endereço local', 'local_port': 'Porta local',
    'remote_address': 'Endereço remoto', 'remote_port': 'Porta remota',
    'state': 'Estado', 'pid': 'PID', 'process': 'Programa',
}


class Workstation:
    def __init__(self, root):
        self.root = root
        self.results = queue.Queue()
        self.snapshot = None
        root.title(f'BLACKBIRD Workstation {__version__} • Network Inspector')
        root.geometry('1050x650')
        root.minsize(760, 450)
        frame = ttk.Frame(root, padding=16)
        frame.pack(fill='both', expand=True)
        ttk.Label(frame, text='BLACKBIRD / Network Inspector', font=('Segoe UI', 18, 'bold')).pack(anchor='w')
        ttk.Label(frame, text='Estudos de redes • consultas locais somente leitura').pack(anchor='w', pady=(2, 12))
        self.summary = tk.StringVar(value='Interfaces: —   |   Registros TCP: —   |   Portas em escuta: —')
        ttk.Label(frame, textvariable=self.summary, font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0, 12))
        bar = ttk.Frame(frame)
        bar.pack(fill='x')
        self.refresh = ttk.Button(bar, text='Consultar este computador', command=self.collect)
        self.refresh.pack(side='left')
        self.export = ttk.Button(bar, text='Exportar JSON', command=self.save, state='disabled')
        self.export.pack(side='left', padx=8)
        ttk.Label(bar, text='Filtro TCP:').pack(side='left', padx=(16, 4))
        self.query = tk.StringVar()
        ttk.Entry(bar, textvariable=self.query).pack(side='left', fill='x', expand=True)
        self.query.trace_add('write', lambda *_: self.render_tcp())
        self.visible = tk.StringVar(value='Nenhuma consulta realizada.')
        ttk.Label(frame, textvariable=self.visible).pack(anchor='w', pady=(8, 0))
        tabs = ttk.Notebook(frame)
        tabs.pack(fill='both', expand=True, pady=12)
        self.interfaces = self.table(tabs, 'Interfaces / IP / DNS', ('name', 'ipv4', 'ipv6', 'gateway', 'dns'))
        self.tcp = self.table(tabs, 'Conexões TCP', ('local_address', 'local_port', 'remote_address', 'remote_port', 'state', 'pid', 'process'))
        lessons = ttk.Frame(tabs, padding=16)
        tabs.add(lessons, text='Estudar')
        ttk.Label(lessons, justify='left', wraplength=700, text=(
            '1. Identifique seu IP, gateway e servidores DNS.\n\n'
            '2. Compare Listen (aguarda conexão) e Established (conexão estabelecida).\n\n'
            '3. Filtre por PID ou processo e compare com o Gerenciador de Tarefas.\n\n'
            '4. Em um laboratório próprio, abra um servidor em 127.0.0.1 e observe sua porta.\n\n'
            'Um endereço 0.0.0.0 ou :: em Listen indica todas as interfaces daquela família; '
            'a acessibilidade também depende do firewall. Uma porta aberta, isoladamente, não prova vulnerabilidade.\n\n'
            'Os relatórios contêm IPs e processos. Revise antes de compartilhar.'
        )).pack(anchor='w')
        self.status = tk.StringVar(value='Pronto. Clique em Consultar para criar um retrato da rede local.')
        ttk.Label(frame, textvariable=self.status, wraplength=950).pack(anchor='w')
        root.after(100, self.poll)

    def table(self, tabs, title, columns):
        frame = ttk.Frame(tabs)
        tabs.add(frame, text=title)
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=LABELS.get(col, col))
            tree.column(col, width=130, minwidth=70)
        vertical = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        horizontal = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        tree.grid(row=0, column=0, sticky='nsew')
        vertical.grid(row=0, column=1, sticky='ns')
        horizontal.grid(row=1, column=0, sticky='ew')
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        return tree

    def collect(self):
        self.refresh.configure(state='disabled')
        self.status.set('Consultando dados locais…')
        def worker():
            try:
                self.results.put((True, collect_snapshot()))
            except Exception as exc:
                self.results.put((False, str(exc)))
        threading.Thread(target=worker, daemon=True).start()

    def poll(self):
        try:
            ok, value = self.results.get_nowait()
        except queue.Empty:
            pass
        else:
            self.refresh.configure(state='normal')
            if ok:
                self.snapshot = value
                self.update_summary()
                self.fill(self.interfaces, value['interfaces'])
                self.render_tcp()
                self.export.configure(state='normal')
                self.status.set(f"Coleta UTC: {value['captured_at']} • {len(value['tcp'])} conexões TCP. Dados representam o momento da consulta.")
            else:
                self.status.set('A consulta falhou; os dados anteriores foram preservados.')
                messagebox.showerror('Network Inspector', value)
        self.root.after(100, self.poll)

    def fill(self, tree, rows):
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            values = [row.get(col, '') for col in tree['columns']]
            tree.insert('', 'end', values=[', '.join(map(str, v)) if isinstance(v, list) else v for v in values])

    def render_tcp(self):
        if self.snapshot:
            rows = filter_tcp(self.snapshot['tcp'], self.query.get())
            self.fill(self.tcp, rows)
            self.visible.set(f"Exibindo {len(rows)} de {len(self.snapshot['tcp'])} registros TCP. A exportação inclui todos os registros.")

    def update_summary(self):
        if self.snapshot:
            rows = self.snapshot['tcp']
            ports = {row.get('local_port') for row in rows if row.get('state') == 'Listen'}
            self.summary.set(f"Interfaces: {len(self.snapshot['interfaces'])}   |   Registros TCP: {len(rows)}   |   Portas em escuta: {len(ports)}")

    def save(self):
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON', '*.json')], initialfile='blackbird-network.json')
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as file:
                    json.dump(self.snapshot, file, ensure_ascii=False, indent=2)
            except OSError as exc:
                messagebox.showerror('Exportação', str(exc))
            else:
                self.status.set('Relatório exportado. Revise IPs e processos antes de compartilhar.')


def run():
    root = tk.Tk()
    Workstation(root)
    root.mainloop()
