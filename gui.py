import tkinter as tk
from tkinter import ttk, messagebox
from engine import CalculationEngine
import feedback_db

class StrategyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        feedback_db.init_db()
        self.title("Assistente de Estratégia Lotto365 - V3.2 Final")
        self.geometry("850x950")
        self.style = ttk.Style(self); self.style.configure('TButton',font=('Helvetica',10),padding=5); self.style.configure('Hot.TButton',background='orange',foreground='black'); self.style.configure('Cold.TButton',background='lightblue',foreground='black'); self.style.configure('TLabelFrame.Label',font=('Helvetica',11,'bold')); self.style.configure('Big.TButton',font=('Helvetica',12,'bold'))
        self.hot_numbers, self.cold_numbers = set(), set(); self.hot_buttons, self.cold_buttons = {}, {}; self.positional_vars, self.first_num_hot_entries = {}, {}; self.filter_vars = {}
        canvas = tk.Canvas(self); scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview); scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all"))); canvas.create_window((0,0),window=scrollable_frame,anchor="nw"); canvas.configure(yscrollcommand=scrollbar.set); canvas.pack(side="left",fill="both",expand=True); scrollbar.pack(side="right",fill="y")
        self._create_number_selection_section(scrollable_frame); self._create_first_number_section(scrollable_frame); self._create_positional_stats_section(scrollable_frame); self._create_filters_section(scrollable_frame)
        self.generate_button=ttk.Button(scrollable_frame,text="Gerar Sugestões",style='Big.TButton',command=self.run_engine); self.generate_button.pack(pady=20,padx=10,fill='x')
        self.last_engine = None

    def _create_number_selection_section(self, p):
        f = ttk.LabelFrame(p, text="Estatísticas Gerais: Seleção de Números Populares e Frios", padding="10"); f.pack(fill="x", pady=5, padx=10)
        ttk.Label(f, text="Populares:").pack(); hf = ttk.Frame(f); hf.pack(); self._create_number_grid(hf, self.hot_buttons, self.on_hot_number_click)
        ttk.Label(f, text="Frios:").pack(pady=(10,0)); cf = ttk.Frame(f); cf.pack(); self._create_number_grid(cf, self.cold_buttons, self.on_cold_number_click)

    def _create_first_number_section(self, p):
        f = ttk.LabelFrame(p, text="Estatísticas Específicas do 1º Número", padding="10"); f.pack(fill="x", pady=5, padx=10)
        ttk.Label(f, text="Digite os 9 números mais populares para a 1ª posição e suas contagens:").pack(); grid_frame = ttk.Frame(f); grid_frame.pack(pady=5)
        for i in range(9):
            ttk.Label(grid_frame, text=f"{i+1}º: Num:").grid(row=i, column=0); num_entry = ttk.Entry(grid_frame, width=5); num_entry.grid(row=i, column=1)
            ttk.Label(grid_frame, text="Contagem:").grid(row=i, column=2, padx=(10,0)); count_entry = ttk.Entry(grid_frame, width=5); count_entry.grid(row=i, column=3)
            self.first_num_hot_entries[i] = (num_entry, count_entry)

    def _create_positional_stats_section(self, p):
        f = ttk.LabelFrame(p, text="Estatísticas Percentuais por Posição", padding="10"); f.pack(fill="x", expand=True, pady=10, padx=10)
        for i in range(1, 6): self._create_positional_row(f, i)

    def _create_positional_row(self, p, pos):
        rf = ttk.Frame(p, padding=5); rf.pack(fill='x', expand=True); ttk.Label(rf, text=f"{pos}ª Posição:", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, padx=5, sticky='w'); self.positional_vars[pos] = {}
        ttk.Label(rf, text="Ímpar:").grid(row=0, column=1); odd_var = tk.StringVar(); self.positional_vars[pos]['odd'] = odd_var; odd_entry = ttk.Entry(rf, width=5, textvariable=odd_var); odd_entry.grid(row=0, column=2); ttk.Label(rf, text="% / Par:").grid(row=0, column=3); par_var = tk.StringVar(); self.positional_vars[pos]['par'] = par_var; par_entry = ttk.Entry(rf, width=5, textvariable=par_var); par_entry.grid(row=0, column=4, padx=(0,15)); odd_entry.bind("<FocusOut>", lambda e, v1=odd_var, v2=par_var: self._update_complement(v1, v2)); par_entry.bind("<FocusOut>", lambda e, v1=par_var, v2=odd_var: self._update_complement(v1, v2))
        ttk.Label(rf, text="Hi:").grid(row=0, column=5); hi_var = tk.StringVar(); self.positional_vars[pos]['hi'] = hi_var; hi_entry = ttk.Entry(rf, width=5, textvariable=hi_var); hi_entry.grid(row=0, column=6); ttk.Label(rf, text="% / Lo:").grid(row=0, column=7); lo_var = tk.StringVar(); self.positional_vars[pos]['lo'] = lo_var; lo_entry = ttk.Entry(rf, width=5, textvariable=lo_var); lo_entry.grid(row=0, column=8, padx=(0,15)); hi_entry.bind("<FocusOut>", lambda e, v1=hi_var, v2=lo_var: self._update_complement(v1, v2)); lo_entry.bind("<FocusOut>", lambda e, v1=lo_var, v2=hi_var: self._update_complement(v1, v2))
        cf = ttk.Frame(rf); cf.grid(row=0, column=9, padx=10); self.positional_vars[pos]['colors'] = {}
        for idx, color in enumerate(['Amarela','Verde','Branca']): ttk.Label(cf, text=f"{color}:").grid(row=0, column=idx*2); entry = ttk.Entry(cf, width=4); entry.grid(row=0, column=idx*2+1, padx=(0,5)); self.positional_vars[pos]['colors'][color] = entry

    def _create_filters_section(self, p):
        f = ttk.LabelFrame(p, text="Filtros Matemáticos Adicionais", padding="10"); f.pack(fill="x", pady=10, padx=10); self.filter_vars = {}
        filters = {'use_fibonacci':"Usar Bônus para Números Fibonacci",'use_primes':"Usar Bônus para Números Primos",'use_squares':"Usar Bônus para Quadrados Perfeitos",'use_sum':"Usar Filtro de Soma Ideal (75-115)"}
        for key, text in filters.items(): var = tk.BooleanVar(value=True); cb = ttk.Checkbutton(f, text=text, variable=var); cb.pack(anchor='w'); self.filter_vars[key] = var

    def _create_number_grid(self, p, btn_dict, cmd):
        for i in range(36): n=i+1; r,c=divmod(i,12); b=ttk.Button(p,text=str(n),width=4,command=lambda n=n:cmd(n)); b.grid(row=r,column=c,padx=2,pady=2); btn_dict[n]=b

    def _update_complement(self, var1, var2):
        try: val1 = int(var1.get())
        except (ValueError, tk.TclError): return
        if 0 <= val1 <= 100: var2.set(str(100 - val1))

    def on_hot_number_click(self, n):
        if n in self.hot_numbers: self.hot_numbers.remove(n); self.hot_buttons[n].configure(style='TButton'); self.cold_buttons[n].config(state="normal")
        else: self.hot_numbers.add(n); self.hot_buttons[n].configure(style='Hot.TButton'); self.cold_buttons[n].config(state="disabled")

    def on_cold_number_click(self, n):
        if n in self.cold_numbers: self.cold_numbers.remove(n); self.cold_buttons[n].configure(style='TButton'); self.hot_buttons[n].config(state="normal")
        else: self.cold_numbers.add(n); self.cold_buttons[n].configure(style='Cold.TButton'); self.hot_buttons[n].config(state="disabled")

    def run_engine(self):
        try:
            user_inputs = self.collect_inputs()
            active_filters = {key: var.get() for key, var in self.filter_vars.items()}
            self.last_engine = CalculationEngine(user_inputs, active_filters)
            combo_suggs = self.last_engine.generate_5_number_suggestions()
            first_num_suggs = self.last_engine.generate_1st_number_suggestions()
            self.display_results(combo_suggs, first_num_suggs)
        except Exception as e:
            messagebox.showerror("Erro de Cálculo", f"Ocorreu um erro ao gerar as sugestões.\nVerifique se todos os campos foram preenchidos corretamente.\n\nDetalhe do Erro: {e}")

    def handle_feedback(self, liked_combo):
        if not self.last_engine:
            messagebox.showwarning("Aviso", "Motor de cálculo não inicializado.")
            return
        properties_to_save = self.last_engine.get_combo_properties_for_feedback(liked_combo)
        feedback_db.record_feedback(properties_to_save)
        messagebox.showinfo("Feedback Registrado", f"Obrigado! Sua preferência pela combinação {liked_combo} foi salva e irá influenciar futuras sugestões.")

    def collect_inputs(self):
        i={'positional_stats':{},'first_number_stats':{'hot_frequencies':{}}}; i['general_hot']=self.hot_numbers; i['general_cold']=self.cold_numbers
        for j in range(9):
            num_e, count_e = self.first_num_hot_entries[j]
            if num_e.get() and count_e.get():
                i['first_number_stats']['hot_frequencies'][int(num_e.get())] = int(count_e.get())
        for j in range(1, 6):
            i['positional_stats'][j]={'odd_even':{'Ímpar':int(self.positional_vars[j]['odd'].get() or 50),'Par':int(self.positional_vars[j]['par'].get() or 50)},'hi_lo':{'Hi':int(self.positional_vars[j]['hi'].get() or 50),'Lo':int(self.positional_vars[j]['lo'].get() or 50)},'colors':{c:float(e.get() or 33.3) for c, e in self.positional_vars[j]['colors'].items()}}
        return i

    def display_results(self, combo_suggs, first_num_suggs):
        res_win = tk.Toplevel(self); res_win.title("Sugestões Geradas"); res_win.geometry("500x400")
        ttk.Label(res_win, text="Sugestões de Apostas", font=("Helvetica", 16, "bold")).pack(pady=10)
        ttk.Label(res_win, text="Para Sorteio de 5 Números:", font=("Helvetica", 12, "underline")).pack(anchor='w', padx=10)
        for i, combo in enumerate(combo_suggs):
            combo_frame = ttk.Frame(res_win); combo_frame.pack(anchor='w', padx=20, fill='x')
            ttk.Label(combo_frame, text=f"Sugestão {i+1}: {combo}", font=("Courier", 11)).pack(side='left')
            feedback_button = ttk.Button(combo_frame, text="[ 👍 Gostei ]", command=lambda c=combo: self.handle_feedback(c)); feedback_button.pack(side='right', padx=10)
        ttk.Label(res_win, text="\nPara Aposta no 1º Número:", font=("Helvetica", 12, "underline")).pack(anchor='w', padx=10)
        for i, (num, score) in enumerate(first_num_suggs):
            ttk.Label(res_win, text=f"  {i+1}º Lugar: Número {num} (Pontuação: {score})", font=("Courier", 11)).pack(anchor='w', padx=20)