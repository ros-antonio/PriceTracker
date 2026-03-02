import customtkinter as ctk
import json
import os
import sys

# Determinăm calea corectă către data.json
if getattr(sys, 'frozen', False):
    # Rulează ca .exe (PyInstaller) — din client/dist/ urcăm 2 nivele
    BASE_DIR = os.path.dirname(sys.executable)
    JSON_PATH = os.path.join(BASE_DIR, '..', '..', 'data.json')
else:
    # Rulează ca script Python — din client/ urcăm 1 nivel
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    JSON_PATH = os.path.join(BASE_DIR, '..', 'data.json')

# ── Paletă de culori (cool tones) ─────────────────────────────
BG_DARK        = "#080c14"
BG_CARD        = "#0f172a"
BG_CARD_ALT    = "#131c31"
BG_INPUT       = "#1e293b"
ACCENT         = "#06b6d4"   # cyan
ACCENT_HOVER   = "#22d3ee"
GREEN          = "#10b981"   # emerald
GREEN_HOVER    = "#34d399"
YELLOW         = "#38bdf8"   # sky blue (info/reload)
YELLOW_HOVER   = "#7dd3fc"
RED            = "#ef4444"   # red (destructive)
RED_HOVER      = "#f87171"
TEXT_PRIMARY   = "#e2e8f0"
TEXT_SECONDARY = "#64748b"
BORDER_COLOR   = "#1e3a5f"
LIST_SELECT    = "#164e63"   # dark cyan
LIST_BG        = "#0c1322"
LIST_HOVER     = "#172554"   # dark blue


class DarkDialog(ctk.CTkToplevel):
    """Dialog custom care respectă tema dark a aplicației."""

    def __init__(self, parent, title="", message="", dialog_type="info", on_confirm=None):
        super().__init__(parent)
        self.result = False
        self._on_confirm = on_confirm

        # Configurare fereastră
        self.title(title)
        self.configure(fg_color=BG_DARK)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Centare pe fereastra părinte
        self.update_idletasks()
        w, h = 420, 200
        px = parent.winfo_x() + (parent.winfo_width() - w) // 2
        py = parent.winfo_y() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{px}+{py}")

        # Iconiță + culoare în funcție de tip
        icons = {"info": "✅", "warning": "⚠️", "error": "❌", "confirm": "❓"}
        colors = {"info": GREEN, "warning": YELLOW, "error": RED, "confirm": ACCENT}
        icon = icons.get(dialog_type, "ℹ️")
        color = colors.get(dialog_type, ACCENT)

        # Conținut
        frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Header cu iconiță
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=16, pady=(16, 4))

        ctk.CTkLabel(
            header_frame, text=f"{icon}  {title}",
            font=("Segoe UI Bold", 16), text_color=color,
        ).pack(anchor="w")

        # Mesaj
        ctk.CTkLabel(
            frame, text=message,
            font=("Segoe UI", 13), text_color=TEXT_PRIMARY,
            wraplength=360, justify="left",
        ).pack(fill="x", padx=20, pady=(8, 16))

        # Butoane
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=(0, 14))

        if dialog_type == "confirm":
            ctk.CTkButton(
                btn_frame, text="Da", width=90, height=34,
                fg_color=RED, hover_color=RED_HOVER, text_color="#fff",
                font=("Segoe UI Semibold", 12), corner_radius=8,
                command=self._on_yes,
            ).pack(side="left", padx=(0, 8))
            ctk.CTkButton(
                btn_frame, text="Nu", width=90, height=34,
                fg_color=BORDER_COLOR, hover_color=LIST_HOVER, text_color=TEXT_PRIMARY,
                font=("Segoe UI Semibold", 12), corner_radius=8,
                command=self._on_no,
            ).pack(side="left")
        else:
            ctk.CTkButton(
                btn_frame, text="OK", width=90, height=34,
                fg_color=color, hover_color=ACCENT_HOVER, text_color="#fff" if color not in (GREEN, YELLOW) else "#111",
                font=("Segoe UI Semibold", 12), corner_radius=8,
                command=self._on_no,
            ).pack(side="left")

        # Escape pentru închidere
        self.bind("<Escape>", lambda _: self._on_no())
        self.protocol("WM_DELETE_WINDOW", self._on_no)

    def _on_yes(self):
        self.result = True
        self.grab_release()
        self.destroy()
        if self._on_confirm:
            self._on_confirm()

    def _on_no(self):
        self.result = False
        self.grab_release()
        self.destroy()


def show_dialog(parent, title, message, dialog_type="info", on_confirm=None):
    """Helper pentru a afișa un dialog dark-theme."""
    DarkDialog(parent, title, message, dialog_type, on_confirm)


class AnimatedButton(ctk.CTkButton):
    """Buton cu efect de pulsare la hover."""

    def __init__(self, master, pulse_color=None, **kwargs):
        super().__init__(master, **kwargs)
        self._pulse_color = pulse_color or ACCENT
        self._original_fg = kwargs.get("fg_color", ACCENT)
        self._hover_fg = kwargs.get("hover_color", ACCENT_HOVER)
        self._pulse_id = None
        self._pulse_step = 0
        self.bind("<Enter>", self._start_pulse)
        self.bind("<Leave>", self._stop_pulse)

    def _start_pulse(self, _e=None):
        self._pulse_step = 0
        self._animate_pulse_in()

    def _stop_pulse(self, _e=None):
        if self._pulse_id:
            self.after_cancel(self._pulse_id)
            self._pulse_id = None
        self.configure(fg_color=self._original_fg)

    def _animate_pulse_in(self):
        steps = 6
        if self._pulse_step <= steps:
            ratio = self._pulse_step / steps
            color = self._lerp_color(self._original_fg, self._hover_fg, ratio)
            self.configure(fg_color=color)
            self._pulse_step += 1
            self._pulse_id = self.after(25, self._animate_pulse_in)

    @staticmethod
    def _lerp_color(c1, c2, t):
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"


class ProductCard(ctk.CTkFrame):
    """Card vizual pentru un produs din listă."""

    def __init__(self, master, index, produs, selected=False, on_click=None, **kwargs):
        super().__init__(
            master,
            fg_color=BG_CARD if not selected else LIST_SELECT,
            corner_radius=10,
            border_width=1,
            border_color=ACCENT if selected else BORDER_COLOR,
            **kwargs,
        )
        self._index = index
        self._on_click = on_click
        self._selected = selected

        self.columnconfigure(1, weight=1)

        # Număr index
        idx_label = ctk.CTkLabel(
            self, text=f"#{index + 1}", font=("Segoe UI", 13, "bold"),
            text_color=ACCENT if not selected else "#fff", width=36,
        )
        idx_label.grid(row=0, column=0, rowspan=2, padx=(10, 6), pady=8)

        # Tag
        tag = produs.get("tag", "(fără tag)")
        tag_label = ctk.CTkLabel(
            self, text=tag, font=("Segoe UI Semibold", 13),
            text_color=TEXT_PRIMARY, anchor="w",
        )
        tag_label.grid(row=0, column=1, sticky="w", padx=4, pady=(8, 0))

        # Info secundar
        pret = produs.get("target_price", 0)
        link = produs.get("link", "")
        site = self._extrage_site(link)
        info = f"{site}   •   țintă: {pret} RON" if site else f"țintă: {pret} RON"
        info_label = ctk.CTkLabel(
            self, text=info, font=("Segoe UI", 11),
            text_color=TEXT_SECONDARY if not selected else "#dfe6e9", anchor="w",
        )
        info_label.grid(row=1, column=1, sticky="w", padx=4, pady=(0, 8))

        # Click pe orice element din card
        for widget in [self, idx_label, tag_label, info_label]:
            widget.bind("<Button-1>", self._handle_click)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def _handle_click(self, _e=None):
        if self._on_click:
            self._on_click(self._index)

    def _on_enter(self, _e=None):
        if not self._selected:
            self.configure(fg_color=LIST_HOVER, border_color=ACCENT)

    def _on_leave(self, _e=None):
        if not self._selected:
            self.configure(fg_color=BG_CARD, border_color=BORDER_COLOR)

    @staticmethod
    def _extrage_site(link):
        if "altex.ro" in link: return "Altex"
        if "emag.ro" in link: return "eMAG"
        if "pcgarage.ro" in link: return "PC Garage"
        if "amazon.com" in link: return "Amazon"
        return ""


class PriceTrackerApp:
    def __init__(self):
        # ── Configurare temă ──────────────────────────────────────
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("⚡ Price Tracker")
        self.root.geometry("820x700")
        self.root.resizable(True, True)
        self.root.configure(fg_color=BG_DARK)

        self.produse = []
        self.index_selectat = None
        self._card_widgets = []

        self._creaza_interfata()
        self._incarca_date()
        self._fade_in()

    # ── Fade-in la pornire ─────────────────────────────────────────

    def _fade_in(self):
        self.root.attributes("-alpha", 0.0)
        self._fade_step(0)

    def _fade_step(self, step):
        alpha = min(step / 12, 1.0)
        self.root.attributes("-alpha", alpha)
        if step < 12:
            self.root.after(30, self._fade_step, step + 1)

    # ── Citire / Scriere JSON ──────────────────────────────────────

    def _incarca_date(self):
        try:
            if os.path.exists(JSON_PATH):
                with open(JSON_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.produse = data if isinstance(data, list) else [data]
            else:
                self.produse = []
        except Exception as e:
            show_dialog(self.root, "Eroare", f"Nu am putut citi data.json:\n{e}", "error")
            self.produse = []
        self._actualizeaza_lista()

    def _salveaza_fisier(self):
        try:
            with open(JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(self.produse, f, indent=4, ensure_ascii=False)
        except Exception as e:
            show_dialog(self.root, "Eroare", f"Eroare la salvare:\n{e}", "error")

    # ── Construire UI ──────────────────────────────────────────────

    def _creaza_interfata(self):
        # ── Header ──
        header = ctk.CTkFrame(self.root, fg_color=BG_CARD, corner_radius=12, height=56)
        header.pack(fill="x", padx=16, pady=(16, 8))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="⚡  Price Tracker",
            font=("Segoe UI Black", 20), text_color=ACCENT,
        ).pack(side="left", padx=16, pady=10)

        self.lbl_count = ctk.CTkLabel(
            header, text="0 produse",
            font=("Segoe UI", 12), text_color=TEXT_SECONDARY,
        )
        self.lbl_count.pack(side="right", padx=16)

        # ── Zona scrollabilă pentru carduri ──
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.root, fg_color=BG_DARK, corner_radius=0,
            scrollbar_button_color=BORDER_COLOR,
            scrollbar_button_hover_color=ACCENT,
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=16, pady=4)

        # ── Separator ──
        sep = ctk.CTkFrame(self.root, fg_color=BORDER_COLOR, height=1, corner_radius=0)
        sep.pack(fill="x", padx=24, pady=(6, 2))

        # ── Formular editare ──
        frame_form = ctk.CTkFrame(self.root, fg_color=BG_CARD, corner_radius=12)
        frame_form.pack(fill="x", padx=16, pady=(8, 8))
        frame_form.columnconfigure(1, weight=1)

        self.lbl_form_title = ctk.CTkLabel(
            frame_form, text="✏️  Detalii produs",
            font=("Segoe UI Semibold", 14), text_color=TEXT_PRIMARY,
        )
        self.lbl_form_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(12, 6))

        labels = [
            ("Tag:", "Numele sau descrierea produsului"),
            ("Email:", "Adresa de email pentru notificări"),
            ("Link:", "Link-ul complet al produsului"),
            ("Preț țintă:", "Prețul dorit (în RON)"),
        ]
        self.entries = {}
        for i, (lbl, placeholder) in enumerate(labels, start=1):
            ctk.CTkLabel(
                frame_form, text=lbl,
                font=("Segoe UI Semibold", 12), text_color=TEXT_SECONDARY,
            ).grid(row=i, column=0, sticky="w", padx=(14, 8), pady=5)

            entry = ctk.CTkEntry(
                frame_form, height=34,
                font=("Segoe UI", 12),
                placeholder_text=placeholder,
                fg_color=BG_INPUT, border_color=BORDER_COLOR,
                text_color=TEXT_PRIMARY,
                corner_radius=8,
            )
            entry.grid(row=i, column=1, sticky="ew", padx=(0, 14), pady=5)
            self.entries[lbl] = entry

        # ── Butoane acțiuni ──
        frame_butoane = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_butoane.pack(fill="x", padx=16, pady=(0, 16))

        AnimatedButton(
            frame_butoane, text="＋  Adaugă produs", command=self._adauga_produs,
            fg_color=GREEN, hover_color=GREEN_HOVER, text_color="#111",
            font=("Segoe UI Semibold", 12), height=38, corner_radius=10,
            pulse_color=GREEN,
        ).pack(side="left", padx=(0, 6))

        AnimatedButton(
            frame_butoane, text="💾  Salvează", command=self._salveaza_selectat,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="#fff",
            font=("Segoe UI Semibold", 12), height=38, corner_radius=10,
        ).pack(side="left", padx=6)

        AnimatedButton(
            frame_butoane, text="🗑  Șterge", command=self._sterge_produs,
            fg_color=RED, hover_color=RED_HOVER, text_color="#fff",
            font=("Segoe UI Semibold", 12), height=38, corner_radius=10,
            pulse_color=RED,
        ).pack(side="left", padx=6)

        AnimatedButton(
            frame_butoane, text="🔄  Reîncarcă", command=self._incarca_date,
            fg_color=YELLOW, hover_color=YELLOW_HOVER, text_color="#111",
            font=("Segoe UI Semibold", 12), height=38, corner_radius=10,
            pulse_color=YELLOW,
        ).pack(side="right", padx=(6, 0))

    # ── Actualizare listă ──────────────────────────────────────────

    def _actualizeaza_lista(self):
        for w in self._card_widgets:
            w.destroy()
        self._card_widgets.clear()

        for i, p in enumerate(self.produse):
            sel = (i == self.index_selectat)
            card = ProductCard(
                self.scroll_frame, i, p,
                selected=sel,
                on_click=self._selecteaza_produs,
            )
            card.pack(fill="x", padx=4, pady=3)
            self._card_widgets.append(card)

        self.lbl_count.configure(
            text=f"{len(self.produse)} produs{'e' if len(self.produse) != 1 else ''}"
        )

        if self.index_selectat is None:
            self._goleste_formular()

    # ── Selectare produs ───────────────────────────────────────────

    def _selecteaza_produs(self, idx):
        self.index_selectat = idx
        produs = self.produse[idx]

        self._goleste_formular()
        self.entries["Tag:"].insert(0, produs.get("tag", ""))
        self.entries["Email:"].insert(0, produs.get("email", ""))
        self.entries["Link:"].insert(0, produs.get("link", ""))
        self.entries["Preț țintă:"].insert(0, produs.get("target_price", 0))
        self.lbl_form_title.configure(text=f"✏️  Editare — {produs.get('tag', '?')[:50]}")

        # Actualizează highlight-ul cardurilor fără a le recrea
        self._actualizeaza_highlight()

    # ── Acțiuni CRUD ───────────────────────────────────────────────

    def _citeste_formular(self):
        try:
            pret = int(self.entries["Preț țintă:"].get() or 0)
        except ValueError:
            show_dialog(self.root, "Atenție", "Prețul țintă trebuie să fie un număr întreg.", "warning")
            return None
        return {
            "tag": self.entries["Tag:"].get().strip(),
            "email": self.entries["Email:"].get().strip(),
            "link": self.entries["Link:"].get().strip(),
            "target_price": pret,
        }

    def _adauga_produs(self):
        date = self._citeste_formular()
        if date is None:
            return
        if not date["tag"] and not date["link"]:
            show_dialog(self.root, "Atenție", "Completează cel puțin Tag-ul sau Link-ul.", "warning")
            return
        self.produse.append(date)
        self.index_selectat = len(self.produse) - 1
        self._salveaza_fisier()
        self._actualizeaza_lista()
        self._toast("Produsul a fost adăugat  ✓", GREEN)

    def _salveaza_selectat(self):
        if self.index_selectat is None:
            show_dialog(self.root, "Atenție", "Selectează mai întâi un produs din listă.", "warning")
            return
        date = self._citeste_formular()
        if date is None:
            return
        self.produse[self.index_selectat] = date
        self._salveaza_fisier()
        self._actualizeaza_lista()
        self._toast("Modificările au fost salvate  ✓", ACCENT)

    def _sterge_produs(self):
        if self.index_selectat is None:
            show_dialog(self.root, "Atenție", "Selectează mai întâi un produs din listă.", "warning")
            return
        tag = self.produse[self.index_selectat].get("tag", "?")

        def _executa_stergere():
            self.produse.pop(self.index_selectat)
            self.index_selectat = None
            self._salveaza_fisier()
            self._actualizeaza_lista()
            self._goleste_formular()
            self._toast("Produs șters", RED)

        show_dialog(
            self.root, "Confirmare",
            f"Ștergi produsul \"{tag}\"?",
            "confirm", on_confirm=_executa_stergere,
        )

    # ── Toast notification ─────────────────────────────────────────

    def _toast(self, mesaj, culoare):
        toast = ctk.CTkFrame(self.root, fg_color=culoare, corner_radius=8, height=36)
        toast.place(relx=0.5, rely=0.02, anchor="n")
        lbl = ctk.CTkLabel(
            toast, text=f"  {mesaj}  ",
            font=("Segoe UI Semibold", 12),
            text_color="#fff" if culoare != GREEN and culoare != YELLOW else "#111",
        )
        lbl.pack(padx=16, pady=6)
        # Dispare automat după 2s cu fade
        self.root.after(2000, lambda: self._fade_out_toast(toast, 6))

    def _fade_out_toast(self, widget, steps_left):
        if steps_left <= 0:
            widget.destroy()
            return
        # Micșorăm opacitatea simulată prin schimbarea culorii
        widget.place_forget() if steps_left == 1 else None
        self.root.after(40, lambda: self._fade_out_toast(widget, steps_left - 1))

    # ── Highlight carduri (fără recreare) ──────────────────────────

    def _actualizeaza_highlight(self):
        for i, card in enumerate(self._card_widgets):
            sel = (i == self.index_selectat)
            card.configure(
                fg_color=LIST_SELECT if sel else BG_CARD,
                border_color=ACCENT if sel else BORDER_COLOR,
            )
            card._selected = sel

    # ── Utilitar ───────────────────────────────────────────────────

    def _goleste_formular(self):
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.lbl_form_title.configure(text="✏️  Detalii produs")

    def run(self):
        self.root.mainloop()


# ── Pornire aplicație ──────────────────────────────────────────────
if __name__ == "__main__":
    app = PriceTrackerApp()
    app.run()