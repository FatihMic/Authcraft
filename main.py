import customtkinter as ctk
from tkinter import messagebox
import string
import secrets
from core.storage import SQLiteStorage
from core.security import SecurityManager

ctk.set_appearance_mode("Dark")

class AuthCraftApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AuthCraft — Enterprise Password & Vault Manager")
        self.geometry("1150x720")
        self.resizable(False, False)

        # Gelişmiş Renk Paleti (Slate & Indigo)
        self.COLOR_BG = "#0f172a"
        self.COLOR_PANEL = "#1e293b"
        self.COLOR_CARD = "#182234"
        self.COLOR_INPUT = "#334155"
        self.COLOR_ACCENT = "#6366f1"
        self.COLOR_ACCENT_HOVER = "#4f46e5"
        self.COLOR_TEXT_MAIN = "#f8fafc"
        self.COLOR_TEXT_MUTED = "#94a3b8"

        self.configure(fg_color=self.COLOR_BG)

        self.storage = SQLiteStorage()
        self.current_user = None
        self.master_password = None
        self.selected_category = "Tümü"

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def generate_strong_password(self, length=16):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(chars) for _ in range(length))

    # --- EKRAN 1: SPLIT GİRİŞ EKRANI ---
    def show_login_screen(self):
        self.clear_screen()
        main_card = ctk.CTkFrame(self, width=950, height=580, corner_radius=24, fg_color=self.COLOR_CARD)
        main_card.place(relx=0.5, rely=0.5, anchor="center")

        left_panel = ctk.CTkFrame(main_card, width=440, height=580, corner_radius=24, fg_color=self.COLOR_PANEL)
        left_panel.pack(side="left", fill="both")
        left_panel.pack_propagate(False)

        ctk.CTkLabel(left_panel, text="🛡️", font=ctk.CTkFont(size=72)).pack(pady=(90, 10))
        ctk.CTkLabel(left_panel, text="AuthCraft Enterprise", font=ctk.CTkFont(size=28, weight="bold"), text_color=self.COLOR_TEXT_MAIN).pack(pady=(0, 10))
        ctk.CTkLabel(left_panel, text="AES-256 Askeri Düzey Şifreleme\nve Canlı Sızıntı Taraması Gücü.", 
                      font=ctk.CTkFont(size=13), text_color=self.COLOR_TEXT_MUTED, justify="center").pack(pady=(0, 30))

        right_panel = ctk.CTkFrame(main_card, width=510, height=580, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)

        form_box = ctk.CTkFrame(right_panel, fg_color="transparent")
        form_box.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.75)

        ctk.CTkLabel(form_box, text="Kasaya Erişim 🔓", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 20))

        self.username_entry = ctk.CTkEntry(form_box, placeholder_text="Kullanıcı Adı", height=44, corner_radius=10, fg_color=self.COLOR_INPUT)
        self.username_entry.pack(fill="x", pady=(0, 16))

        self.password_entry = ctk.CTkEntry(form_box, placeholder_text="Ana Şifre (Master Password)", show="•", height=44, corner_radius=10, fg_color=self.COLOR_INPUT)
        self.password_entry.pack(fill="x", pady=(0, 25))

        login_btn = ctk.CTkButton(form_box, text="Kasayı Aç ➔", height=46, corner_radius=10,
                                   fg_color=self.COLOR_ACCENT, hover_color=self.COLOR_ACCENT_HOVER,
                                   font=ctk.CTkFont(size=14, weight="bold"), command=self.handle_login)
        login_btn.pack(fill="x", pady=(0, 15))

        switch_btn = ctk.CTkButton(form_box, text="Hesabınız yok mu? Yeni Kasa Oluşturun", fg_color="transparent", 
                                    text_color=self.COLOR_ACCENT, hover=False, command=self.show_register_screen)
        switch_btn.pack()

    def show_register_screen(self):
        self.clear_screen()
        main_card = ctk.CTkFrame(self, width=950, height=580, corner_radius=24, fg_color=self.COLOR_CARD)
        main_card.place(relx=0.5, rely=0.5, anchor="center")

        left_panel = ctk.CTkFrame(main_card, width=440, height=580, corner_radius=24, fg_color=self.COLOR_PANEL)
        left_panel.pack(side="left", fill="both")
        left_panel.pack_propagate(False)

        ctk.CTkLabel(left_panel, text="✨", font=ctk.CTkFont(size=72)).pack(pady=(130, 10))
        ctk.CTkLabel(left_panel, text="Yeni Kasa Oluştur", font=ctk.CTkFont(size=26, weight="bold"), text_color=self.COLOR_TEXT_MAIN).pack(pady=(0, 10))

        right_panel = ctk.CTkFrame(main_card, width=510, height=580, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)

        form_box = ctk.CTkFrame(right_panel, fg_color="transparent")
        form_box.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.75)

        ctk.CTkLabel(form_box, text="Kayıt Ol", font=ctk.CTkFont(size=22, weight="bold"), text_color=self.COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 20))

        reg_user = ctk.CTkEntry(form_box, placeholder_text="Kullanıcı Adı", height=42, fg_color=self.COLOR_INPUT)
        reg_user.pack(fill="x", pady=8)

        reg_email = ctk.CTkEntry(form_box, placeholder_text="E-posta", height=42, fg_color=self.COLOR_INPUT)
        reg_email.pack(fill="x", pady=8)

        reg_pass = ctk.CTkEntry(form_box, placeholder_text="Ana Şifre (Master Password)", show="•", height=42, fg_color=self.COLOR_INPUT)
        reg_pass.pack(fill="x", pady=8)

        def do_register():
            u, e, p = reg_user.get().strip(), reg_email.get().strip(), reg_pass.get().strip()
            if u and e and p:
                try:
                    self.storage.save_user(u, p, e)
                    messagebox.showinfo("Başarılı", "Kasanız oluşturuldu!")
                    self.show_login_screen()
                except Exception:
                    messagebox.showerror("Hata", "Bu kullanıcı adı alınmış!")
            else:
                messagebox.showwarning("Eksik", "Lütfen tüm alanları doldurun.")

        reg_btn = ctk.CTkButton(form_box, text="Kasa Oluştur", height=46, fg_color="#10b981", hover_color="#059669",
                                font=ctk.CTkFont(weight="bold"), command=do_register)
        reg_btn.pack(fill="x", pady=(15, 10))

        back_btn = ctk.CTkButton(form_box, text="← Girişe Dön", fg_color="transparent", text_color=self.COLOR_TEXT_MUTED, command=self.show_login_screen)
        back_btn.pack()

    # --- EKRAN 2: GELİŞMİŞ DASHBOARD & KASA PANELİ ---
    def show_vault_screen(self):
        self.clear_screen()

        # SOL ZENGİN SIDEBAR
        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.COLOR_PANEL)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="🛡️ AuthCraft", font=ctk.CTkFont(size=22, weight="bold"), text_color=self.COLOR_TEXT_MAIN).pack(pady=(25, 5))
        ctk.CTkLabel(sidebar, text=f"👤 {self.current_user[0]}", font=ctk.CTkFont(size=13), text_color=self.COLOR_ACCENT).pack(pady=(0, 20))

        ctk.CTkLabel(sidebar, text="KATEGORİLER", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.COLOR_TEXT_MUTED).pack(anchor="w", padx=20, pady=(10, 5))

        categories = [
            ("🔑 Tüm Şifreler", "Tümü"),
            ("🌐 Web Şifreleri", "Web Şifresi"),
            ("💳 Banka / Kartlar", "Banka / Kart"),
            ("📶 Wi-Fi Ağları", "Wi-Fi"),
            ("📝 Gizli Notlar", "Gizli Not")
        ]

        def select_cat(cat_val):
            self.selected_category = cat_val
            refresh_vault()

        for label_text, cat_val in categories:
            btn = ctk.CTkButton(sidebar, text=label_text, fg_color="transparent", anchor="w", 
                                hover_color=self.COLOR_INPUT, text_color=self.COLOR_TEXT_MAIN,
                                command=lambda c=cat_val: select_cat(c))
            btn.pack(fill="x", padx=10, pady=2)

        logout_btn = ctk.CTkButton(sidebar, text="🔒 Kasayı Kilitle", height=40, fg_color="#ef4444", hover_color="#dc2626",
                                   font=ctk.CTkFont(weight="bold"), command=self.show_login_screen)
        logout_btn.pack(side="bottom", fill="x", padx=20, pady=25)

        # SAĞ İÇERİK ALANI
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=25, pady=20)

        # 1. METRİK İSTATİSTİK KARTLARI (DASHBOARD)
        metrics_frame = ctk.CTkFrame(content, fg_color="transparent")
        metrics_frame.pack(fill="x", pady=(0, 15))

        self.m_total = ctk.CTkLabel(metrics_frame, text="0", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.COLOR_TEXT_MAIN)
        self.m_web = ctk.CTkLabel(metrics_frame, text="0", font=ctk.CTkFont(size=20, weight="bold"), text_color="#38bdf8")
        self.m_bank = ctk.CTkLabel(metrics_frame, text="0", font=ctk.CTkFont(size=20, weight="bold"), text_color="#10b981")

        cards_data = [
            ("Toplam Kayıt", self.m_total, self.COLOR_CARD),
            ("Web Hesapları", self.m_web, self.COLOR_CARD),
            ("Banka / Kartlar", self.m_bank, self.COLOR_CARD)
        ]

        for title, val_lbl, bg in cards_data:
            c_box = ctk.CTkFrame(metrics_frame, fg_color=bg, corner_radius=12, height=65)
            c_box.pack(side="left", fill="x", expand=True, padx=5)
            c_box.pack_propagate(False)
            ctk.CTkLabel(c_box, text=title, font=ctk.CTkFont(size=11), text_color=self.COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(8, 0))
            val_lbl.master = c_box
            val_lbl.pack(anchor="w", padx=15)

        # 2. ÜST ARAMA VE EKLE BAR
        top_bar = ctk.CTkFrame(content, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 15))

        search_entry = ctk.CTkEntry(top_bar, placeholder_text="🔍 Arama yapın...", height=42, width=350, fg_color=self.COLOR_CARD)
        search_entry.pack(side="left")
        search_entry.bind("<KeyRelease>", lambda e: refresh_vault(search_entry.get()))

        add_modal_btn = ctk.CTkButton(top_bar, text="+ Yeni Şifre Ekle", height=42, fg_color="#10b981", hover_color="#059669",
                                      font=ctk.CTkFont(weight="bold"), command=lambda: self.open_add_item_modal(refresh_vault))
        add_modal_btn.pack(side="right")

        # 3. ŞİFRE LİSTESİ SCROLL AREA
        scroll_area = ctk.CTkScrollableFrame(content, fg_color="transparent")
        scroll_area.pack(fill="both", expand=True)

        def refresh_vault(query=""):
            for w in scroll_area.winfo_children():
                w.destroy()

            all_items = self.storage.get_vault_items(self.current_user[0], self.master_password, self.current_user[2], query)

            # İstatistikleri Güncelle
            self.m_total.configure(text=str(len(all_items)))
            self.m_web.configure(text=str(sum(1 for i in all_items if i[1] == "Web Şifresi")))
            self.m_bank.configure(text=str(sum(1 for i in all_items if i[1] == "Banka / Kart")))

            # Kategori Filtresi Uygula
            if self.selected_category != "Tümü":
                items = [i for i in all_items if i[1] == self.selected_category]
            else:
                items = all_items

            if not items:
                ctk.CTkLabel(scroll_area, text="📂 Seçili kategoride kayıt bulunamadı.", font=ctk.CTkFont(size=14), text_color=self.COLOR_TEXT_MUTED).pack(pady=40)

            for item_id, category, title, account_name, secret_val, url in items:
                card = ctk.CTkFrame(scroll_area, fg_color=self.COLOR_CARD, corner_radius=12, height=75)
                card.pack(fill="x", pady=6)
                card.pack_propagate(False)

                icon_map = {"Web Şifresi": "🌐", "Banka / Kart": "💳", "Wi-Fi": "📶", "Gizli Not": "📝"}
                icon = icon_map.get(category, "🔑")

                info_frame = ctk.CTkFrame(card, fg_color="transparent")
                info_frame.pack(side="left", padx=15)

                ctk.CTkLabel(info_frame, text=f"{icon} {title}", font=ctk.CTkFont(size=14, weight="bold"), text_color=self.COLOR_TEXT_MAIN).pack(anchor="w")
                ctk.CTkLabel(info_frame, text=f"{account_name} • {category}", font=ctk.CTkFont(size=11), text_color=self.COLOR_TEXT_MUTED).pack(anchor="w")

                btn_frame = ctk.CTkFrame(card, fg_color="transparent")
                btn_frame.pack(side="right", padx=15)

                pass_label = ctk.CTkLabel(btn_frame, text="••••••••••••", font=ctk.CTkFont(size=12), text_color="#a7f3d0")
                pass_label.pack(side="left", padx=10)

                def toggle_pass(lbl=pass_label, val=secret_val):
                    if lbl.cget("text") == "••••••••••••":
                        lbl.configure(text=val)
                    else:
                        lbl.configure(text="••••••••••••")

                toggle_btn = ctk.CTkButton(btn_frame, text="👁️", width=36, height=32, fg_color=self.COLOR_INPUT, command=toggle_pass)
                toggle_btn.pack(side="left", padx=4)

                def check_pwned(val=secret_val):
                    count = SecurityManager.check_pwned_password(val)
                    if count > 0:
                        messagebox.showerror("⚠️ TEHLİKE!", f"Bu şifre veri ihlallerinde {count:,} kez SIZDIRILMIŞ!")
                    else:
                        messagebox.showinfo("✅ GÜVENLİ", "Şifre bilinen sızıntılarda bulunamadı.")

                pwned_btn = ctk.CTkButton(btn_frame, text="🛡️ Tara", width=60, height=32, fg_color="#f59e0b", hover_color="#d97706",
                                          font=ctk.CTkFont(size=11, weight="bold"), command=check_pwned)
                pwned_btn.pack(side="left", padx=4)

                def copy_pass(val=secret_val):
                    self.clipboard_clear()
                    self.clipboard_append(val)
                    messagebox.showinfo("Kopyalandı", "Şifre panoya kopyalandı!")

                copy_btn = ctk.CTkButton(btn_frame, text="📋", width=36, height=32, fg_color=self.COLOR_INPUT, command=copy_pass)
                copy_btn.pack(side="left", padx=4)

                def make_del(i_id=item_id):
                    return lambda: (self.storage.delete_vault_item(i_id), refresh_vault())

                del_btn = ctk.CTkButton(btn_frame, text="🗑️", width=36, height=32, fg_color="#ef4444", hover_color="#b91c1c", command=make_del())
                del_btn.pack(side="left", padx=4)

        refresh_vault()

    def open_add_item_modal(self, callback_refresh):
        modal = ctk.CTkToplevel(self)
        modal.title("Yeni Şifre / Hesap Ekle")
        modal.geometry("450x550")
        modal.grab_set()

        modal.configure(fg_color=self.COLOR_BG)

        ctk.CTkLabel(modal, text="Yeni Şifre Kaydı 🔑", font=ctk.CTkFont(size=18, weight="bold"), text_color=self.COLOR_TEXT_MAIN).pack(pady=(20, 15))

        cat_dropdown = ctk.CTkOptionMenu(modal, values=["Web Şifresi", "Banka / Kart", "Wi-Fi", "Gizli Not"], height=38)
        cat_dropdown.pack(fill="x", padx=30, pady=8)

        title_in = ctk.CTkEntry(modal, placeholder_text="Başlık (Örn: Netflix)", height=38)
        title_in.pack(fill="x", padx=30, pady=8)

        acc_in = ctk.CTkEntry(modal, placeholder_text="Kullanıcı Adı / E-posta", height=38)
        acc_in.pack(fill="x", padx=30, pady=8)

        pass_frame = ctk.CTkFrame(modal, fg_color="transparent")
        pass_frame.pack(fill="x", padx=30, pady=8)

        pass_in = ctk.CTkEntry(pass_frame, placeholder_text="Şifre", height=38)
        pass_in.pack(side="left", fill="x", expand=True, padx=(0, 5))

        def fill_gen_pass():
            pass_in.delete(0, 'end')
            pass_in.insert(0, self.generate_strong_password())

        gen_btn = ctk.CTkButton(pass_frame, text="⚡ Üret", width=70, height=38, fg_color=self.COLOR_ACCENT, command=fill_gen_pass)
        gen_btn.pack(side="right")

        url_in = ctk.CTkEntry(modal, placeholder_text="Web Sitesi URL (İsteğe Bağlı)", height=38)
        url_in.pack(fill="x", padx=30, pady=8)

        def save_item():
            cat = cat_dropdown.get()
            t = title_in.get().strip()
            a = acc_in.get().strip()
            p = pass_in.get().strip()
            u = url_in.get().strip()

            if t and p:
                self.storage.add_vault_item(self.current_user[0], self.master_password, self.current_user[2], cat, t, a, p, u)
                modal.destroy()
                callback_refresh()
            else:
                messagebox.showwarning("Eksik", "Lütfen Başlık ve Şifre alanlarını doldurun.")

        save_btn = ctk.CTkButton(modal, text="Kaydet", height=42, fg_color="#10b981", hover_color="#059669",
                                 font=ctk.CTkFont(weight="bold"), command=save_item)
        save_btn.pack(fill="x", padx=30, pady=(20, 0))

    def handle_login(self):
        u, p = self.username_entry.get().strip(), self.password_entry.get().strip()
        user = self.storage.get_user(u)

        if user:
            hashed_input = SecurityManager.hash_password(p, user[2])
            if hashed_input == user[1]:
                self.current_user = user
                self.master_password = p
                self.show_vault_screen()
                return

        messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")


if __name__ == "__main__":
    app = AuthCraftApp()
    app.mainloop()