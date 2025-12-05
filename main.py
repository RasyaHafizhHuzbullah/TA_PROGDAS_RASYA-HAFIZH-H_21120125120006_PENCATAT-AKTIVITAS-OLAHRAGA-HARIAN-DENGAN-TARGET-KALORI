# MODUL 8: GUI Programming (Menggunakan Library Tkinter)
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime, date
import os

# MODUL 5: Object Oriented Programming I (Class)
class AppOlahraga:
    
    # MODUL 5: Constructor (__init__) - Method untuk inisialisasi Object
    def __init__(self): 
        # MODUL 8: Inisialisasi Window Utama (GUI)
        self.root = tk.Tk()
        self.root.title("Pencatat Olahraga Harian")
        self.root.geometry("950x750")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(True, True)

        # MODUL 1: Variabel & Tipe Data (Integer)
        self.target = 600
        
        # MODUL 1: Array (Dictionary) - Menyimpan data aktivitas & kalori per menit
        self.daftar = {
            "Lari": 10, "Jalan Cepat": 6, "Push-up": 8, "Sit-up": 8,
            "Sepeda": 8, "Renang": 13, "Lompat Tali": 12, "Yoga": 4, "Plank": 7,
            "Bulu Tangkis": 9, "Senam": 6
        }

        # MODUL 1: Variabel (String)
        self.data_file = "data_olahraga.json"
        # MODUL 1: Array (List) - Log aktivitas hari ini
        self.log_hari_ini = []
        # MODUL 1: Array (Dictionary) - Log aktivitas semua hari
        self.semua_log = {}

        # MODUL 1: Variabel untuk Animasi
        self.new_total_kcal = 0
        self.animation_step = 2.0 

        # Variabel untuk History Window (untuk menahan referensi widget)
        self.history_cb = None
        self.history_listbox = None

        # MODUL 4: Memanggil Method
        self.load_data()
        self.gui()
        self.update_tanggal_dan_ui() 
        self.root.mainloop()

    # MODUL 4: Method untuk membangun GUI (Tampilan)
    def gui(self):
        # MODUL 8: Komponen Label
        tk.Label(self.root, text="PENCATAT OLAHRAGA", font=("Arial", 28, "bold"),
                 bg="#2c3e50", fg="#ffffff").pack(pady=15)

        # MODUL 8: Komponen Label
        self.lbl_tanggal = tk.Label(self.root, text="", font=("Arial", 14, "italic"),
                                     bg="#2c3e50", fg="#ffffff")
        self.lbl_tanggal.pack(pady=(0,10))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Horizontal.TProgressbar", thickness=40, background="#e74c3c") 

        # MODUL 8: Komponen Progressbar
        self.pb = ttk.Progressbar(self.root, length=700, mode="determinate",
                                     maximum=self.target, style="Custom.Horizontal.TProgressbar")
        self.pb.pack(pady=20)
        
        # MODUL 8: Komponen Label
        self.lbl_kcal = tk.Label(self.root, text=f"0 / {self.target} kcal",
                                     font=("Arial", 20, "bold"),
                                     bg="#2c3e50", fg="#ecf0f1")
        self.lbl_kcal.pack(pady=(0, 10))

        btn_action_frame = tk.Frame(self.root, bg="#2c3e50")
        btn_action_frame.pack(pady=10)
        
        # MODUL 8: Komponen Button & Event Handling (command=self.reset_hari_ini)
        tk.Button(btn_action_frame, text="RESET HARI INI", font=("Arial", 14, "bold"), bg="#e74c3c", fg="white",
                  width=15, height=1, command=self.reset_hari_ini).pack(side="left", padx=10) 
                  
        # MODUL 8: Komponen Button & Event Handling (command=self.hapus_terpilih)
        tk.Button(btn_action_frame, text="HAPUS YANG DIPILIH", font=("Arial", 14, "bold"), bg="#f39c12", fg="white",
                  width=20, height=1, command=self.hapus_terpilih).pack(side="left", padx=10)
        
        # MODUL 8: Komponen Button BARU (Fitur Riwayat)
        tk.Button(btn_action_frame, text="LIHAT RIWAYAT", font=("Arial", 14, "bold"), bg="#3498db", fg="white",
                  width=15, height=1, command=self.show_history_window).pack(side="left", padx=10)


        # MODIFIKASI DIMULAI DI SINI UNTUK LABEL DAN CENTER ALIGNMENT
        frame = tk.Frame(self.root, bg="#34495e", relief="ridge", bd=8)
        frame.pack(pady=25, padx=80) 

        # MODUL 8: Komponen Label BARU - Jenis Olahraga
        tk.Label(frame, text="Jenis Olahraga:", font=("Arial", 14), bg="#34495e", fg="#ecf0f1")\
            .grid(row=0, column=0, pady=15, padx=10, sticky="e") # sticky="e" (East) agar label rata kanan
            
        # MODUL 8: Komponen Combobox
        self.cb = ttk.Combobox(frame, values=sorted(self.daftar.keys()), state="readonly",
                                 font=("Arial", 14), width=18)
        self.cb.set("Lari")
        self.cb.grid(row=0, column=1, pady=15, padx=10, sticky="w") # sticky="w" (West) agar input rata kiri

        # MODUL 8: Komponen Label BARU - Durasi
        tk.Label(frame, text="Durasi (Menit):", font=("Arial", 14), bg="#34495e", fg="#ecf0f1")\
            .grid(row=1, column=0, pady=15, padx=10, sticky="e")
            
        # MODUL 8: Komponen Entry (Textbox)
        self.entry = tk.Entry(frame, font=("Arial",16), width=10, justify="center")
        self.entry.grid(row=1, column=1, pady=15, padx=10, sticky="w")
        self.entry.focus()
        # MODUL 8: Event Handling (Bind tombol Enter)
        self.entry.bind("<Return>", lambda e: self.tambah())

        # MODUL 8: Komponen Button (Menggunakan columnspan=2 agar rata tengah)
        tk.Button(frame, text="TAMBAH", font=("Arial",16,"bold"), bg="#27ae60", fg="white",
                  width=18, height=2, command=self.tambah)\
            .grid(row=2, column=0, columnspan=2, pady=20)
        # MODIFIKASI BERAKHIR DI SINI

            
        lb_frame = tk.Frame(self.root, bg="#2c3e50") 
        lb_frame.pack(pady=20, padx=80, fill="both", expand=True)
        
        # MODUL 8: Komponen Listbox
        self.listbox = tk.Listbox(lb_frame, font=("Consolas", 12), height=14,
                                     bg="#2c3e50", fg="#ecf0f1", selectbackground="#3498db",
                                     selectmode=tk.SINGLE)
        scrollbar = tk.Scrollbar(lb_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # MODUL 8: Event Handling (Double klik untuk hapus)
        self.listbox.bind("<Double-1>", lambda e: self.hapus_terpilih())

    # MODUL 4 & 8: Method BARU untuk menampilkan jendela riwayat
    def show_history_window(self):
        """Method untuk membuat dan menampilkan jendela riwayat aktivitas."""
        
        # MODUL 8: Membuat TopLevel Window
        history_root = tk.Toplevel(self.root)
        history_root.title("Riwayat Aktivitas Harian")
        history_root.geometry("600x550")
        history_root.configure(bg="#2c3e50")
        history_root.resizable(False, False)
        
        # MODUL 8: Komponen Label
        tk.Label(history_root, text="RIWAYAT OLAHRAGA", font=("Arial", 20, "bold"),
                 bg="#2c3e50", fg="#ffffff").pack(pady=15)

        # MODUL 1: Ambil semua tanggal yang memiliki log, urutkan dari terbaru
        dates = sorted(self.semua_log.keys(), reverse=True)
        
        # MODUL 2: Pengkondisian IF (Cek jika tidak ada riwayat)
        if not dates:
            tk.Label(history_root, text="Belum ada riwayat tersimpan.", font=("Arial", 12),
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=50)
            return

        date_frame = tk.Frame(history_root, bg="#2c3e50")
        date_frame.pack(pady=10)
        
        tk.Label(date_frame, text="Pilih Tanggal:", font=("Arial", 12),
                 bg="#2c3e50", fg="#ecf0f1").pack(side="left", padx=10)

        # MODUL 8: Komponen Combobox untuk memilih tanggal
        self.history_cb = ttk.Combobox(date_frame, values=dates, state="readonly",
                                       font=("Arial", 12), width=15)
        self.history_cb.set(dates[0]) 
        self.history_cb.pack(side="left", padx=10)
        
        # MODUL 8: Event Handling (Bind Combobox saat tanggal dipilih)
        self.history_cb.bind("<<ComboboxSelected>>", self.update_history_list)

        lb_frame = tk.Frame(history_root, bg="#2c3e50") 
        lb_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # MODUL 8: Komponen Listbox untuk menampilkan log riwayat
        self.history_listbox = tk.Listbox(lb_frame, font=("Consolas", 12), height=14,
                                          bg="#2c3e50", fg="#ecf0f1", selectbackground="#3498db",
                                          selectmode=tk.SINGLE)
        scrollbar = tk.Scrollbar(lb_frame, orient="vertical", command=self.history_listbox.yview)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        self.history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # MODUL 4: Memanggil method untuk memuat data awal
        self.update_history_list() 


    # MODUL 4 & 1 & 3: Method BARU untuk memperbarui Listbox riwayat
    def update_history_list(self, event=None):
        """Memperbarui Listbox riwayat berdasarkan tanggal yang dipilih."""
        if not self.history_cb: # MODUL 2: Pengkondisian (Safety check)
            return
            
        selected_date = self.history_cb.get()
        # MODUL 1: Operasi pada Array (Dictionary)
        log = self.semua_log.get(selected_date, [])

        self.history_listbox.delete(0, tk.END)
        
        header = f" {'WAKTU':<5} │ {'JENIS OLAHRAGA':<12} │ {'DURASI':>6} │ {'KALORI':>6}"
        self.history_listbox.insert(tk.END, header)
        self.history_listbox.itemconfig(tk.END, {'fg': '#3498db'}) 
        self.history_listbox.insert(tk.END, "──────────────────────────────────────────────────────")
        
        # MODUL 2: Pengkondisian IF (Jika list kosong)
        if not log:
            self.history_listbox.insert(tk.END, f"   Tidak ada aktivitas pada {selected_date}...")
            return
            
        total_kcal = 0
        # MODUL 3: Perulangan FOR (Menampilkan setiap item dari log)
        for item in log:
            total_kcal += item.get("kcal", 0) 
            # MODUL 8: Menambahkan item ke Listbox
            self.history_listbox.insert(tk.END,
                f" {item.get('waktu',''): <5} │ {item.get('jenis',''): <12} │ {item.get('durasi',0):>6} menit → {item.get('kcal',0):>4} kcal") 
            
        self.history_listbox.insert(tk.END, "──────────────────────────────────────────────────────")
        self.history_listbox.insert(tk.END, f" TOTAL PADA {selected_date}: {total_kcal} kcal")
        self.history_listbox.itemconfig(tk.END, {'fg': '#2ecc71'}) 

    # MODUL 4: Method untuk meriset data hari ini
    def reset_hari_ini(self):
        """Meriset (menghapus) semua aktivitas yang tercatat hari ini."""
        # MODUL 2: Pengkondisian IF (Cek apakah ada data)
        if not self.log_hari_ini:
            messagebox.showinfo("Info", "Belum ada data hari ini.")
            return
            
        if messagebox.askyesno("Reset", "Yakin reset semua aktivitas hari ini?"):
            # MODUL 1: Operasi pada Array (List)
            self.log_hari_ini.clear()
            self.semua_log.pop(date.today().isoformat(), None) 
            # MODUL 4: Memanggil Method
            self.save_data()
            self.update_tanggal_dan_ui()

    # MODUL 4: Method untuk animasi progress bar
    def animate_progress(self):
        """Method untuk membuat animasi progress bar bergerak mulus."""
        current_value = self.pb['value']
        target_value = self.new_total_kcal
        
        # MODUL 2: Pengkondisian IF (Kondisi Berhenti)
        if current_value == target_value:
            return

        difference = target_value - current_value
        step = self.animation_step

        # MODUL 2: Pengkondisian IF-ELSE IF (Arah Animasi)
        if abs(difference) < step:
            self.pb['value'] = target_value
        else:
            if difference > 0:
                self.pb['value'] = current_value + step
            else:
                self.pb['value'] = current_value - step

            # MODUL 3: Perulangan Waktu (Recursive Call)
            self.root.after(10, self.animate_progress)

    # MODUL 4: Method untuk memperbarui tampilan UI utama
    def update_tanggal_dan_ui(self):
        """Method untuk memperbarui tampilan utama."""
        self.lbl_tanggal.config(text=datetime.now().strftime("%A, %d %B %Y"))

        # MODUL 1 & 3: Perhitungan Total Kalori (Implicit Looping)
        total = sum(item.get("kcal", 0) for item in self.log_hari_ini) 
        
        self.new_total_kcal = total 
        self.animate_progress() 
        
        persen = total / self.target if self.target else 0
        # MODUL 2: Pengkondisian IF-ELIF-ELSE (Mengubah warna progress bar)
        if persen < 0.5:
            color = "#e74c3c"
        elif persen < 1.0:
            color = "#f39c12"
        else:
            color = "#27ae60"
            
        ttk.Style().configure("Custom.Horizontal.TProgressbar", background=color)

        self.lbl_kcal.config(text=f"{total} / {self.target} kcal")

        # MODUL 4: Memanggil Method
        self.update_list()
        
    # MODUL 4: Method untuk menambah aktivitas
    def tambah(self):
        """Menambahkan aktivitas baru ke log hari ini."""
        # MODUL 2: Pengkondisian & Error Handling (try-except) untuk validasi input
        try:
            # MODUL 1: Variabel (Integer)
            durasi = int(self.entry.get().strip())
            # MODUL 2: Pengkondisian IF (Validasi nilai positif)
            if durasi <= 0: raise ValueError
        except:
            messagebox.showerror("Error", "Masukkan **angka bulat positif** untuk durasi!")
            self.entry.delete(0, tk.END)
            return

        # MODUL 1: Variabel
        jenis = self.cb.get()
        # MODUL 1: Variabel (Hasil perhitungan)
        kcal = durasi * self.daftar.get(jenis, 0) 
        waktu = datetime.now().strftime("%H:%M")

        # MODUL 1: Data Structure (Dictionary)
        entry = {"waktu": waktu, "jenis": jenis, "durasi": durasi, "kcal": kcal} 
        # MODUL 1: Operasi pada Array (List)
        self.log_hari_ini.append(entry)
        
        # --- Simpan Data ke semua_log ---
        self.semua_log.setdefault(date.today().isoformat(), []).append(entry)

        # MODUL 4: Memanggil Method
        self.save_data()
        self.entry.delete(0, tk.END)
        self.update_tanggal_dan_ui()

    # MODUL 4: Method untuk menampilkan log ke Listbox
    def update_list(self):
        """Method untuk menampilkan data log ke Listbox."""
        if not hasattr(self, "listbox"):
            return

        self.listbox.delete(0, tk.END)
        
        header = f" {'WAKTU':<5} │ {'JENIS OLAHRAGA':<12} │ {'DURASI':>6} │ {'KALORI':>6}"
        self.listbox.insert(tk.END, header)
        self.listbox.itemconfig(tk.END, {'fg': '#3498db'}) 
        self.listbox.insert(tk.END, "──────────────────────────────────────────────────────")

        # MODUL 2: Pengkondisian IF (Jika list kosong)
        if not self.log_hari_ini:
            self.listbox.insert(tk.END, "   Belum ada aktivitas hari ini...")
            return
            
        total = 0
        # MODUL 3: Perulangan FOR (Menampilkan setiap item dari list)
        for item in self.log_hari_ini:
            total += item.get("kcal", 0) 
            # MODUL 8: Menambahkan item ke Listbox
            self.listbox.insert(tk.END,
                f" {item.get('waktu',''): <5} │ {item.get('jenis',''): <12} │ {item.get('durasi',0):>6} menit → {item.get('kcal',0):>4} kcal") 
            
        self.listbox.insert(tk.END, "──────────────────────────────────────────────────────")
        self.listbox.insert(tk.END, f" TOTAL HARI INI: {total} kcal")
        self.listbox.itemconfig(tk.END, {'fg': '#2ecc71', 'selectbackground': '#2ecc71'}) 

    # MODUL 4: Method untuk menghapus log
    def hapus_terpilih(self):
        """Method untuk menghapus log tertentu."""
        sel = self.listbox.curselection()
        # MODUL 2: Pengkondisian IF
        if not sel: return
        
        log_index = sel[0] - 2 
        
        # MODUL 2: Pengkondisian IF
        if log_index < 0 or log_index >= len(self.log_hari_ini): 
            return
            
        if messagebox.askyesno("Hapus", "Yakin hapus aktivitas ini?"):
            # MODUL 1: Operasi pada Array (List)
            del self.log_hari_ini[log_index]
            self.semua_log[date.today().isoformat()] = self.log_hari_ini
            # MODUL 4: Memanggil Method
            self.save_data()
            self.update_tanggal_dan_ui()
            
    # MODUL 4: Method untuk menyimpan data
    def save_data(self):
        """Method untuk menyimpan semua log ke file JSON (Data Persistence)."""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.semua_log, f, indent=2) 
        # MODUL 2: Pengkondisian (Error Handling)
        except Exception as e: 
            print(f"Gagal menyimpan data: {e}") 
            pass

    # MODUL 4: Method untuk memuat data
    def load_data(self):
        """Method untuk memuat data dari file JSON, dan memuat log hari ini."""
        # MODUL 2: Pengkondisian IF (Cek keberadaan file)
        if os.path.exists(self.data_file):
            # MODUL 2: Pengkondisian (Error Handling)
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.semua_log = json.load(f)
                
                today_log = self.semua_log.get(date.today().isoformat(), [])
                cleaned_log = []
                
                # MODUL 3: Perulangan FOR (Memproses setiap item log yang dimuat)
                for item in today_log:
                    # Logika pembersihan dan konversi tipe data (menggunakan Modul 2 IF/try-except)
                    kcal_value = item.get('kcal')
                    kalori_value = item.get('kalori')
                    durasi_value = item.get('durasi', 0)
                    
                    final_kcal = 0
                    if kcal_value is not None:
                        try: final_kcal = int(kcal_value)
                        except: pass
                    elif kalori_value is not None:
                        try: final_kcal = int(kalori_value)
                        except: pass
                        
                    final_durasi = 0
                    try: final_durasi = int(durasi_value)
                    except: pass

                    # MODUL 1: Membuat Data Structure Baru
                    cleaned_entry = {
                        "waktu": item.get("waktu", "??:??"), 
                        "jenis": item.get("jenis", "Aktivitas Tidak Dikenal"), 
                        "durasi": final_durasi, 
                        "kcal": final_kcal 
                    }
                    # MODUL 1: Operasi pada Array (List)
                    cleaned_log.append(cleaned_entry)
                        
                # MODUL 1: Variabel (List)
                self.log_hari_ini = cleaned_log 
                
            # MODUL 2: Pengkondisian (Catching specific error)
            except json.JSONDecodeError:
                self.log_hari_ini = []
                self.semua_log = {}
                messagebox.showwarning("Peringatan Data", "File data_olahraga.json korup. Data direset.")
            except Exception:
                self.log_hari_ini = []
                self.semua_log = {}
        # MODUL 2: Pengkondisian ELSE
        else:
            self.semua_log = {}
            self.log_hari_ini = [] 

# Blok utama yang memastikan AppOlahraga() dijalankan pertama kali.
# MODUL 5: Instansiasi Objek AppOlahraga
if __name__ == "__main__":
    AppOlahraga()