import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation
from calcolo import calcola, scorpora

root = tk.Tk()
root.title('InFattura per Windows')
root.geometry('780x760')
root.minsize(680, 650)
root.configure(bg='#34444d')
style = ttk.Style(root)
style.theme_use('clam')
style.configure('TFrame', background='#34444d')
style.configure('TLabel', background='#34444d', foreground='white', font=('Segoe UI', 11))
style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'))
style.configure('TCheckbutton', background='#34444d', foreground='white', font=('Segoe UI', 10))
style.configure('TRadiobutton', background='#34444d', foreground='white', font=('Segoe UI', 10))
style.configure('TButton', font=('Segoe UI', 11, 'bold'), padding=8)
main = ttk.Frame(root, padding=24); main.pack(fill='both', expand=True)
ttk.Label(main, text='Calcolo parcella', style='Title.TLabel').pack(anchor='w')
ttk.Label(main, text='Calcolo diretto e scorporo dal netto', foreground='#c9d6d8').pack(anchor='w', pady=(0,12))
mode=tk.StringVar(value='diretto')
bar=ttk.Frame(main); bar.pack(fill='x')
ttk.Radiobutton(bar,text='Da diritti e onorari',variable=mode,value='diretto').pack(side='left',padx=(0,25))
ttk.Radiobutton(bar,text='Dal netto a pagare',variable=mode,value='inverso').pack(side='left')
form=ttk.Frame(main); form.pack(fill='x',pady=12)
for col in (0,1): form.columnconfigure(col,weight=1,uniform='c')
values={}; enabled={}
def field(key,label,row,col,default='',optional=False):
    frame=ttk.Frame(form); frame.grid(row=row,column=col,sticky='ew',padx=(0,16),pady=6)
    ttk.Label(frame,text=label).pack(anchor='w')
    line=ttk.Frame(frame); line.pack(fill='x',pady=(3,0))
    v=tk.StringVar(value=default); values[key]=v
    if optional:
        enabled[key]=tk.BooleanVar(value=key in ('cassa','iva'))
        ttk.Checkbutton(line,variable=enabled[key]).pack(side='left')
    tk.Entry(line,textvariable=v,font=('Segoe UI',14),bg='#3e765a',fg='white',insertbackground='white',relief='flat').pack(side='left',fill='x',expand=True,ipady=5)
field('importo','Importo (€)',0,0)
field('esenti','Spese esenti (€)',1,0,'0')
field('spese','Spese non esenti (€)',1,1,'0')
field('cassa','Cassa professionale (%)',2,0,'4',True)
field('iva','IVA (%)',2,1,'22',True)
field('ritenuta','Ritenuta d’acconto (%)',3,0,'20',True)
field('forfait','Maggiorazione forfettaria (%)',3,1,'15',True)
def number(key):
    s=values[key].get().strip().replace(' ','')
    if not s: s='0'
    if ',' in s: s=s.replace('.','').replace(',','.')
    try: n=Decimal(s)
    except InvalidOperation: raise ValueError('Controlla il valore: '+key)
    if not n.is_finite() or n < 0: raise ValueError('Inserisci valori numerici non negativi.')
    if key in enabled and not enabled[key].get(): return Decimal(0)
    if key in enabled and n > 100: raise ValueError('Le percentuali non possono superare 100%.')
    if key not in enabled and n.as_tuple().exponent < -2: raise ValueError('Gli importi possono avere al massimo due decimali.')
    return n
result=tk.Text(main,height=11,font=('Consolas',11),bg='#ecf1ee',fg='#20302a',relief='flat',state='disabled')
def go():
    try:
        v={k:number(k) for k in values}
        args=[v[k] for k in ('esenti','spese','cassa','iva','ritenuta','forfait')]
        if v['ritenuta'] >= 100: raise ValueError('La ritenuta deve essere inferiore al 100%.')
        r=calcola(v['importo'],*args) if mode.get()=='diretto' else scorpora(v['importo'],*args)
        labels=[('Diritti e onorari','onorario'),('Maggiorazione forfettaria','generali'),('Spese non esenti','spese'),('Cassa professionale','cassa'),('IVA','iva'),('Spese esenti','esenti'),('Ritenuta d’acconto (da sottrarre)','ritenuta'),('NETTO A PAGARE','netto')]
        txt='\n'.join(f'{label:<36} {r[key]:>12.2f} €' for label,key in labels)
        if mode.get()=='inverso' and r['netto'] != v['importo']:
            txt+='\n\nScarto per arrotondamento: '+str(r['netto']-v['importo'])+' €'
        result.config(state='normal'); result.delete('1.0','end'); result.insert('1.0',txt); result.config(state='disabled')
    except (ValueError,InvalidOperation) as e: messagebox.showerror('Controlla i dati',str(e))
def clear():
    for k,v in values.items(): v.set({'esenti':'0','spese':'0','cassa':'4','iva':'22','ritenuta':'20','forfait':'15'}.get(k,''))
    for k,v in enabled.items(): v.set(k in ('cassa','iva'))
    result.config(state='normal'); result.delete('1.0','end'); result.config(state='disabled')
buttons=ttk.Frame(main); buttons.pack(fill='x',pady=(4,12))
ttk.Button(buttons,text='Calcola',command=go).pack(side='left',padx=(0,10))
ttk.Button(buttons,text='Pulisci',command=clear).pack(side='left')
result.pack(fill='both',expand=True)
ttk.Label(main,text='Le spese non esenti concorrono a cassa, IVA e ritenuta. Verifica il trattamento del caso concreto.',wraplength=700,foreground='#c9d6d8',font=('Segoe UI',9)).pack(anchor='w',pady=(10,0))
root.mainloop()
