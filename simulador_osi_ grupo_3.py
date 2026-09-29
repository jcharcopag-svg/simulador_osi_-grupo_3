import tkinter as tk
from tkinter import messagebox
import time
import random
import base64

class SimuladorOSI_Alineado:
    def __init__(self, root):
        self.root = root
        self.root.title("SISTEMA DE COMUNICACIÓN DE DATOS - UNEMI 2026")
        self.root.geometry("1200x850")
        self.root.configure(bg="#002147")

        # --- ENCABEZADO ---
        tk.Label(root, text="UNIVERSIDAD ESTATAL DE MILAGRO", font=("Helvetica", 18, "bold"), bg="#002147", fg="white").pack(pady=5)
        
        # --- NOTA TÉCNICA (ROSADO BAJITO) ---
        self.info_frame = tk.Frame(root, bg="#ffe6ea", bd=1, relief=tk.SOLID)
        self.info_frame.pack(fill=tk.X, padx=40, pady=5)
        info_text = ("NOTA TÉCNICA: El modelo OSI se lee del 7 al 1 (Emisor) porque describe el proceso de envío "
                    "desde la aplicación hasta el medio físico. En el Receptor se lee del 1 al 7 para reconstruir los datos.")
        tk.Label(self.info_frame, text=info_text, wraplength=1000, font=("Arial", 9, "italic"), bg="#ffe6ea").pack(pady=5)

        # --- PANEL DE CONTROL ---
        self.panel = tk.Frame(root, bg="#002147")
        self.panel.pack(pady=10)
        self.entrada = tk.Entry(self.panel, width=40, font=("Arial", 11))
        self.entrada.insert(0, "Datos de Evaluación UNEMI")
        self.entrada.pack(side=tk.LEFT, padx=10)

        tk.Button(self.panel, text="🚀 ENVIAR", command=self.transmitir, bg="#28a745", fg="white", width=12, font=("bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.panel, text="🔄 RESET", command=self.resetear, bg="#dc3545", fg="white", width=12, font=("bold")).pack(side=tk.LEFT, padx=5)

        # --- CONTENEDOR PRINCIPAL DE SIMULACIÓN ---
        self.main_container = tk.Frame(root, bg="#002147")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20)

        self.main_container.columnconfigure(0, weight=1) 
        self.main_container.columnconfigure(1, weight=0) 
        self.main_container.columnconfigure(2, weight=1) 

        # --- COLUMNA IZQUIERDA: PC-A ---
        self.frame_pca = tk.Frame(self.main_container, bg="#102a45")
        self.frame_pca.grid(row=0, column=0, sticky="nsew")
        
        self.canvas_a = tk.Canvas(self.frame_pca, width=480, height=120, bg="#ffe6ea", highlightthickness=1)
        self.canvas_a.pack(pady=5)
        tk.Label(self.frame_pca, text="TERMINAL EMISOR (ENCAPSULAMIENTO)", bg="#102a45", fg="#FFCC00", font=("bold", 9)).pack()
        
        # CONSOLA EMISOR CON FONDO GRIS AZULADO ELEGANTE (#1e293b)
        self.consola_a = tk.Text(self.frame_pca, width=60, height=22, bg="#1e293b", fg="#00ff00", font=("Consolas", 9, "bold"), bd=1, relief=tk.SOLID)
        self.consola_a.pack(pady=5)

        # --- COLUMNA CENTRAL: CANAL ---
        self.frame_canal = tk.Frame(self.main_container, bg="#002147")
        self.frame_canal.grid(row=0, column=1, padx=10)
        self.canvas_canal = tk.Canvas(self.frame_canal, width=110, height=120, bg="#002147", highlightthickness=0)
        self.canvas_canal.pack()
        
        # FLECHA MÁS GRUESA Y VISIBLE (width=7 y punta estilizada)
        self.flecha = self.canvas_canal.create_line(10, 60, 100, 60, arrow=tk.LAST, width=7, fill="#dee2e6", arrowshape=(16, 20, 6))
        tk.Label(self.frame_canal, text="CANAL\nM/M/1", bg="#002147", fg="white", font=("Arial", 8, "italic")).pack()

        # --- COLUMNA DERECHA: PC-B ---
        self.frame_pcb = tk.Frame(self.main_container, bg="#102a45")
        self.frame_pcb.grid(row=0, column=2, sticky="nsew")
        
        self.canvas_b = tk.Canvas(self.frame_pcb, width=480, height=120, bg="#ffe6ea", highlightthickness=1)
        self.canvas_b.pack(pady=5)
        tk.Label(self.frame_pcb, text="TERMINAL RECEPTOR (DESENCAPSULAMIENTO)", bg="#102a45", fg="#FFCC00", font=("bold", 9)).pack()
        
        # CONSOLA RECEPTOR CON FONDO GRIS AZULADO ELEGANTE (#1e293b)
        self.consola_b = tk.Text(self.frame_pcb, width=60, height=22, bg="#1e293b", fg="#33ccff", font=("Consolas", 9, "bold"), bd=1, relief=tk.SOLID)
        self.consola_b.pack(pady=5)

        self.nombres = ["APL", "PRE", "SES", "TRA", "RED", "ENL", "FIS"]
        self.rects_a = []
        self.rects_b = []
        self._dibujar_nodos()

    def _dibujar_nodos(self):
        for i in range(7):
            x = 15 + (i * 65)
            r = self.canvas_a.create_rectangle(x, 30, x+55, 90, outline="#002147", fill="#f8f9fa")
            self.canvas_a.create_text(x+27, 60, text=self.nombres[i], font=("Arial", 7, "bold"))
            self.rects_a.append(r)
        
        for i in range(7):
            x = 15 + (i * 65)
            r = self.canvas_b.create_rectangle(x, 30, x+55, 90, outline="#002147", fill="#f8f9fa")
            self.canvas_b.create_text(x+27, 60, text=self.nombres[6-i], font=("Arial", 7, "bold"))
            self.rects_b.append(r)

    def log_a(self, msg):
        self.consola_a.insert(tk.END, msg + "\n")
        self.consola_a.see(tk.END)
        self.root.update()

    def log_b(self, msg):
        self.consola_b.insert(tk.END, msg + "\n")
        self.consola_b.see(tk.END)
        self.root.update()

    def resetear(self):
        self.consola_a.delete(1.0, tk.END)
        self.consola_b.delete(1.0, tk.END)
        self.canvas_canal.itemconfig(self.flecha, fill="#dee2e6")
        for r in self.rects_a + self.rects_b:
            self.canvas_a.itemconfig(r, fill="#f8f9fa")
            self.canvas_b.itemconfig(r, fill="#f8f9fa")

    def transmitir(self):
        msg = self.entrada.get()
        if not msg: return
        self.resetear()
        
        # --- FASE 1: PC-A ---
        data_pdu = msg
        for i in range(7):
            self.canvas_a.itemconfig(self.rects_a[i], fill="#FFCC00")
            wq = random.expovariate(3.0)
            self.log_a(f"[PC-A] Encapsulando Capa {7-i}: Header (Wq: {wq:.4f}s)")
            if i == 1: data_pdu = base64.b64encode(data_pdu.encode()).decode()
            time.sleep(0.3)
            self.canvas_a.itemconfig(self.rects_a[i], fill="#28a745")

        # --- FASE 2: CANAL ---
        self.canvas_canal.itemconfig(self.flecha, fill="#FFCC00")
        self.log_a("\n>>> [CANAL] Propagación física en curso...")
        time.sleep(1)
        self.canvas_canal.itemconfig(self.flecha, fill="#28a745")
        self.log_b(">>> [CANAL] Trama de bits recibida.")

        # --- FASE 3: PC-B ---
        for i in range(7):
            idx = 6 - i
            self.canvas_b.itemconfig(self.rects_b[idx], fill="#FFCC00")
            self.log_b(f"[PC-B] Desencapsulando Capa {i+1}: Trailer (Wq: {random.uniform(0.01, 0.1):.4f}s)")
            if i == 5: data_pdu = base64.b64decode(data_pdu.encode()).decode()
            time.sleep(0.3)
            self.canvas_b.itemconfig(self.rects_b[idx], fill="#33ccff")

        self.log_b(f"\n{'='*45}\nÉXITO: Mensaje Final: {data_pdu}\n{'='*45}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorOSI_Alineado(root)
    root.mainloop()