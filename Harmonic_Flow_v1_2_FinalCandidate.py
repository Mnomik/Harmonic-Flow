import customtkinter as ctk
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PANEL_BG = "#262626"
PANEL_SIDE_WIDTH = 310

VALID_KEYS = [f"{i}A" for i in range(1,13)] + [f"{i}B" for i in range(1,13)]

WHEEL_OUTER_RADIUS = 270

WHEEL_MID_RADIUS = 185

WHEEL_INNER_RADIUS = 85

ARC_STEPS = 240

SELECTED_FILL = "#031008"

SELECTED_OUTLINE = "#20c97d"

CAMELOT_COLORS = {
    "1B":"#9D8CFF","2B":"#4AAEFF","3B":"#14C8FF","4B":"#2FEAD8",
    "5B":"#41E8B2","6B":"#72E96D","7B":"#D0EA45","8B":"#FFD12A",
    "9B":"#FFAA33","10B":"#FF7855","11B":"#FF5FC8","12B":"#C38CFF",
    "1A":"#7B6FE6","2A":"#4198E6","3A":"#25B4D4","4A":"#31C9B4",
    "5A":"#3AC892","6A":"#63C863","7A":"#A7C843","8A":"#E6B93A",
    "9A":"#E6953A","10A":"#E66B52","11A":"#D454AF","12A":"#A86FE6",
}

CAMELOT_TO_OPENKEY = {
    "1A": "6m",  "1B": "6d",  "2A": "7m",  "2B": "7d",
    "3A": "8m",  "3B": "8d",  "4A": "9m",  "4B": "9d",
    "5A": "10m", "5B": "10d", "6A": "11m", "6B": "11d",
    "7A": "12m", "7B": "12d", "8A": "1m",  "8B": "1d",
    "9A": "2m",  "9B": "2d",  "10A": "3m", "10B": "3d",
    "11A": "4m", "11B": "4d", "12A": "5m", "12B": "5d",
}

CAMELOT_DISPLAY = {
    "8B": ("Do Mayor","C"), "8A": ("La Menor","Am"),
    "9B": ("Sol Mayor","G"), "9A": ("Mi Menor","Em"),
    "10B": ("Re Mayor","D"), "10A": ("Si Menor","Bm"),
    "11B": ("La Mayor","A"), "11A": ("Fa# Menor","F#m"),
    "12B": ("Mi Mayor","E"), "12A": ("Do# Menor","C#m"),
    "1B": ("Si Mayor","B"), "1A": ("Sol# Menor","G#m"),
    "2B": ("Fa# Mayor","F#"), "2A": ("Re# Menor","D#m"),
    "3B": ("Reb Mayor","Db"), "3A": ("Sib Menor","Bbm"),
    "4B": ("Lab Mayor","Ab"), "4A": ("Fa Menor","Fm"),
    "5B": ("Mib Mayor","Eb"), "5A": ("Do Menor","Cm"),
    "6B": ("Sib Mayor","Bb"), "6A": ("Sol Menor","Gm"),
    "7B": ("Fa Mayor","F"), "7A": ("Re Menor","Dm"),
}

MOOD_DATA = {
    "1A": ("OSCURO Y PROFUNDO","• techno hipnótico\n• tensión controlada\n• atmósferas densas\n• energía subterránea"),
    "1B": ("POTENTE Y ELEGANTE","• peak time\n• autoridad musical\n• sensación de control\n• impacto inmediato"),
    "2A": ("TENSO Y EMOCIONAL","• melodic techno\n• progresión emocional\n• suspense armónico\n• intensidad creciente"),
    "2B": ("LUMINOSO Y ENERGÉTICO","• energía abierta\n• pista activa\n• sensación expansiva\n• impulso positivo"),
    "3A": ("MELANCÓLICO Y PROFUNDO","• progressive house\n• emoción contenida\n• viajes musicales\n• reflexión"),
    "3B": ("INSPIRADOR Y POSITIVO","• house melódico\n• sensación ascendente\n• optimismo\n• fluidez"),
    "4A": ("PROFUNDO Y CÁLIDO","• deep house\n• groove elegante\n• atmósferas cálidas\n• confort musical"),
    "4B": ("ATMOSFÉRICO Y ENVOLVENTE","• warm up\n• creación de ambiente\n• espacio sonoro\n• suavidad"),
    "5A": ("HIPNÓTICO Y FLUIDO","• organic house\n• repetición envolvente\n• trance suave\n• continuidad"),
    "5B": ("GROOVE ELEGANTE","• house clásico\n• ritmo constante\n• sofisticación\n• movimiento natural"),
    "6A": ("RELAJADO Y ORGÁNICO","• sunset vibes\n• sesiones abiertas\n• sensación natural\n• fluidez emocional"),
    "6B": ("ALEGRE Y POSITIVO","• vocal house\n• ambiente amigable\n• optimismo\n• conexión social"),
    "7A": ("EMOTIVO Y MELÓDICO","• melodías intensas\n• carga emocional\n• momentos memorables\n• profundidad"),
    "7B": ("ESTABLE Y FAMILIAR","• transiciones seguras\n• equilibrio\n• sensación conocida\n• continuidad"),
    "8A": ("EMOCIONAL E INTROSPECTIVO","• breakdowns\n• momentos profundos\n• atmósferas melódicas\n• transición emocional"),
    "8B": ("ENERGÉTICO Y EUFÓRICO","• momentos peak time\n• subida de energía\n• sensación positiva\n• conexión con la pista"),
    "9A": ("REFLEXIVO Y NOSTÁLGICO","• progressive\n• desarrollo musical\n• introspección\n• narrativa sonora"),
    "9B": ("OPTIMISTA Y FESTIVO","• groove positivo\n• sensación de avance\n• energía abierta\n• momentos de celebración"),
    "10A": ("DRAMÁTICO E INTENSO","• tensión emocional\n• contrastes fuertes\n• impacto narrativo\n• profundidad"),
    "10B": ("ENERGÍA Y MOVIMIENTO","• clímax\n• impulso rítmico\n• intensidad alta\n• pista activa"),
    "11A": ("ÉPICO Y EMOCIONAL","• melodic peak\n• grandes melodías\n• emoción expansiva\n• momentos únicos"),
    "11B": ("TRIUNFAL Y RADIANTE","• hands-up moment\n• máxima positividad\n• euforia\n• celebración"),
    "12A": ("MISTERIOSO Y UNDERGROUND","• techno profundo\n• atmósferas oscuras\n• tensión elegante\n• exploración sonora"),
    "12B": ("BRILLANTE Y POSITIVO","• cierre positivo\n• sensación luminosa\n• energía equilibrada\n• armonía")
}

class HarmonicEngine:
    @staticmethod
    def wrap(n):
        return ((n - 1) % 12) + 1

    @classmethod
    def build_compatibility(cls, key):
        num = int(key[:-1])
        mode = key[-1]

        other = "B" if mode == "A" else "A"

        return {
            "perfect": [key, f"{cls.wrap(num-1)}{other}"],
            "boost_1": [f"{cls.wrap(num+1)}{mode}"],
            "boost_2": [f"{cls.wrap(num-3)}{mode}"],
            "boost_3": [f"{cls.wrap(num+2)}{mode}", f"{cls.wrap(num-5)}{mode}"],
            "drop_1": [f"{num}{other}", f"{cls.wrap(num-1)}{mode}"],
            "drop_2": [f"{cls.wrap(num+3)}{mode}"],
            "drop_3": [f"{cls.wrap(num-2)}{mode}", f"{cls.wrap(num+5)}{mode}"],
            "mood": [f"{cls.wrap(num-3)}{other}"]
        }

class CamelotWheel(ctk.CTkCanvas):
    def __init__(self, master, size=500, on_select=None, **kwargs):
        super().__init__(master, width=size, height=size, 
                         bg="#05070b", highlightthickness=0, **kwargs)
        
        self.size = size
        self.center = size // 2
        self.center_x = size // 2
        self.center_y = (size // 2) - 70
        self.on_select = on_select
        self.selected_key = None
        
        # Radios de los anillos
        self.outer_radius = WHEEL_OUTER_RADIUS
        self.mid_radius = WHEEL_MID_RADIUS
        self.inner_radius = WHEEL_INNER_RADIUS
        
        # Segmentos (se llenan al dibujar)
        self.segments = {}
        
        # Bindings
        self.bind("<Button-1>", self.on_click)
        # self.bind("<B1-Motion>", self.on_drag)
        # self.bind("<ButtonRelease-1>", self.on_release)
        
        self.draw_wheel()
    
    def draw_wheel(self):
        self.delete("all")
        self.segments = {}
        
        # 12 segmentos de 30° cada uno
        segment_angle = 30
        
        for i in range(12):
            # Ángulo con rotación aplicada
            start_angle = (i * segment_angle + 75) % 360
            
            # Keys (1-12, el índice 0 es 12)
            key_num = 12 if i == 0 else (12 - i)
            key_b = f"{key_num}B"  # Exterior (Mayor)
            key_a = f"{key_num}A"  # Interior (Menor)
            
            # Dibujar segmento exterior (B - Mayor)
            self.draw_segment(
                start_angle, segment_angle,
                self.mid_radius, self.outer_radius,
                CAMELOT_COLORS[key_b], key_b
            )
            
            # Dibujar segmento interior (A - Menor)
            self.draw_segment(
                start_angle, segment_angle,
                self.inner_radius, self.mid_radius,
                CAMELOT_COLORS[key_a], key_a
            )
        
        
        self.create_oval(
            self.center_x-self.outer_radius,
            self.center_y-self.outer_radius,
            self.center_x+self.outer_radius,
            self.center_y+self.outer_radius,
            outline="",
            width=0
        )

# Círculo central
        self.create_oval(
            self.center_x - self.inner_radius,
            self.center_y - self.inner_radius,
            self.center_x + self.inner_radius,
            self.center_y + self.inner_radius,
            fill="#000000", outline="#0b0b0b", width=1
        )
        
        # Texto central
        if self.selected_key:
            self.create_text(
                self.center_x, self.center_y - 28,
                text=self.selected_key,
                font=("Segoe UI", 42, "bold"),
                fill=CAMELOT_COLORS.get(self.selected_key, "#ffffff")
            )
            self.create_text(
                self.center_x, self.center_y + 18,
                text=CAMELOT_DISPLAY.get(self.selected_key, ("",""))[0],
                font=("Segoe UI", 18, "bold"),
                fill="#cccccc"
            )
            self.create_text(
                self.center_x, self.center_y + 52,
                text=f"({CAMELOT_DISPLAY.get(self.selected_key, ('',''))[1]})",
                font=("Segoe UI", 15),
                fill="#888888"
            )
        else:
            self.create_text(
                self.center_x, self.center_y,
                text="Professional Harmonic Mixing Assistant",
                font=("Segoe UI", 40),
                fill="#ffffff"
            )
    
    
    def saturate(self, hex_color, factor=1.15):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2],16)
        g = int(hex_color[2:4],16)
        b = int(hex_color[4:6],16)

        avg = (r+g+b)/3

        r = max(0,min(255,int(avg+(r-avg)*factor)))
        g = max(0,min(255,int(avg+(g-avg)*factor)))
        b = max(0,min(255,int(avg+(b-avg)*factor)))

        return f"#{r:02x}{g:02x}{b:02x}"

    def draw_segment(self, start_angle, extent, inner_r, outer_r, color, key):
        """Dibuja un segmento de arco."""
        selected_offset = 1 if key == self.selected_key else 0
        # Convertir a radianes
        start_rad = math.radians(start_angle)
        end_rad = math.radians(start_angle + extent)
        
        # Puntos del polígono
        points = []
        
        # Arco exterior
        steps = ARC_STEPS
        for j in range(steps + 1):
            angle = start_rad + (end_rad - start_rad) * j / steps
            x = self.center_x + (outer_r + selected_offset) * math.cos(angle)
            y = self.center_y - (outer_r + selected_offset) * math.sin(angle)
            points.extend([x, y])
        
        # Arco interior (en reversa)
        for j in range(steps, -1, -1):
            angle = start_rad + (end_rad - start_rad) * j / steps
            x = self.center_x + inner_r * math.cos(angle)
            y = self.center_y - inner_r * math.sin(angle)
            points.extend([x, y])
        
        # Dibujar
        outline = SELECTED_OUTLINE if key == self.selected_key else ""
        width = 2 if key == self.selected_key else 0
        
        
        draw_color = self.saturate(color, 1.18)
        if key == self.selected_key:
            draw_color = SELECTED_FILL

        segment_id = self.create_polygon(
            points, fill=draw_color, outline=outline, width=width
        )

        
        # Guardar referencia
        self.segments[segment_id] = {
            "key": key,
            "start": start_angle,
            "extent": extent,
            "inner_r": inner_r,
            "outer_r": outer_r
        }
        
        # Texto del segmento
        mid_angle = math.radians(start_angle + extent / 2)
        mid_r = ((inner_r + outer_r) / 2) + 2
        text_x = self.center_x + mid_r * math.cos(mid_angle)
        text_y = self.center_y - mid_r * math.sin(mid_angle)
        
        name, note = CAMELOT_DISPLAY.get(key, ("",""))

        txt_color = "#e8f7ee" if key == self.selected_key else "#000000"

        camelot_font = 21 if key.endswith("B") else 17
        camelot_y = text_y - 18 if key.endswith("B") else text_y - 22

        self.create_text(text_x, camelot_y,
            text=key,
            font=("Segoe UI", camelot_font, "bold"),
            fill=txt_color)

        self.create_text(text_x, text_y+1,
            text=name,
            font=("Segoe UI", 9, "bold"),
            fill=txt_color)

        self.create_text(text_x, text_y+20,
            text=f"({note})",
            font=("Segoe UI", 7),
            fill=txt_color)
    
    def on_click(self, event):
        items = self.find_overlapping(event.x-1,event.y-1,event.x+1,event.y+1)
        for item in reversed(items):
            if item in self.segments:
                key = self.segments[item]["key"]
                self.selected_key = key
                self.draw_wheel()
                if self.on_select:
                    self.on_select(key)
                break
    
    
    def select_key(self, key):
        """Selección programática."""
        if key in VALID_KEYS:
            self.selected_key = key
            self.draw_wheel()


class CamelotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Harmonic Flow")
        self.configure(fg_color="#05070b")
        self.center_window(1360, 720)
        self.minsize(1280, 680)
        self.selected_key = "8B"

        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.pack(fill="both", expand=True, padx=10, pady=10)

        self.left_panel = ctk.CTkFrame(self.main, width=PANEL_SIDE_WIDTH, fg_color="transparent")
        self.left_panel.pack(side="left", fill="y", padx=(0, 4))
        self.left_panel.pack_propagate(False)

        self.left_content = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.left_content.place(relx=0.0, rely=0.5, relwidth=1.0, anchor="w")

        self.brand_block = ctk.CTkFrame(self.left_content, fg_color="transparent")
        self.brand_block.pack(fill="x", padx=8, pady=(0, 14))

        ctk.CTkLabel(
            self.brand_block,
            text="HARMONIC FLOW",
            font=("Segoe UI Semibold", 24, "bold"),
            text_color="#2dd4bf"
        ).pack(anchor="center")

        ctk.CTkLabel(
            self.brand_block,
            text="Harmonic Mixing Assistant for DJs",
            font=("Segoe UI", 11),
            text_color="#7c8798"
        ).pack(anchor="center", pady=(2, 0))

        self.center_panel = ctk.CTkFrame(self.main, fg_color="transparent", corner_radius=0)
        self.center_panel.pack(side="left", fill="both", expand=True)

        self.right_panel = ctk.CTkFrame(self.main, width=PANEL_SIDE_WIDTH, fg_color="transparent")
        self.right_panel.pack(side="right", fill="y", padx=(4, 0))
        self.right_panel.pack_propagate(False)

        self.right_content = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.right_content.place(relx=0.0, rely=0.5, relwidth=1.0, anchor="w")

        self.build_left_panel()

        self.wheel = CamelotWheel(
            self.center_panel, size=700, on_select=self.on_key_selected
        )
        self.wheel.pack(expand=True, anchor="n", pady=(0, 0))

        self.on_key_selected("8B")

    def build_left_panel(self):
        self.key_card = ctk.CTkFrame(
            self.left_content, fg_color="#262626", corner_radius=18, height=205
        )
        self.key_card.pack(fill="x", padx=8, pady=(6, 6))
        self.key_card.pack_propagate(False)

        ctk.CTkLabel(
            self.key_card, text="TONALIDAD SELECCIONADA",
            font=("Segoe UI Semibold", 18, "bold"), text_color="#2dd4bf"
        ).pack(pady=(20, 10))

        self.key_label = ctk.CTkLabel(
            self.key_card, text="8B", font=("Segoe UI", 42, "bold")
        )
        self.key_label.pack()

        self.note_label = ctk.CTkLabel(
            self.key_card, text="", font=("Segoe UI", 18, "bold"),
            text_color="#34d399"
        )
        self.note_label.pack(pady=5)

        self.open_label = ctk.CTkLabel(
            self.key_card, text="", font=("Segoe UI", 13)
        )
        self.open_label.pack(pady=5)

        self.mood_card = ctk.CTkFrame(
            self.left_content, fg_color="#262626", corner_radius=18, height=250
        )
        self.mood_card.pack(fill="x", padx=8, pady=(0, 6))
        self.mood_card.pack_propagate(False)

        ctk.CTkLabel(
            self.mood_card, text="MOOD",
            font=("Segoe UI Semibold", 18, "bold"), text_color="#2dd4bf"
        ).pack(pady=(12, 10))

        self.mood_title = ctk.CTkLabel(
            self.mood_card, text="", font=("Segoe UI Semibold", 16, "bold"),
            justify="left", wraplength=245
        )
        self.mood_title.pack(pady=(20, 18))

        self.mood_text = ctk.CTkLabel(
            self.mood_card, text="", font=("Segoe UI", 18),
            justify="left", wraplength=240
        )
        self.mood_text.pack(expand=True)
        self.creator_credit = ctk.CTkLabel(
            self.left_content,
            text="created by RoniMnonik",
            font=("Segoe UI", 10),
            text_color="#7c8798"
        )
        self.creator_credit.pack(pady=(8, 0))

    def update_left_panel(self, key):
        self.key_label.configure(text=key, text_color=CAMELOT_COLORS.get(key, "#ffffff"))
        name, note = CAMELOT_DISPLAY.get(key, ("", ""))
        self.note_label.configure(
            text=f"{name} ({note})",
            text_color=CAMELOT_COLORS.get(key, "#34d399")
        )
        self.open_label.configure(text=f"Open Key: {CAMELOT_TO_OPENKEY.get(key, '')}")
        title, body = MOOD_DATA.get(key, ("MOOD NO DEFINIDO", "Información pendiente."))
        self.mood_title.configure(text=title)
        self.mood_text.configure(text=body)

    def update_right_panel(self, key):
        for widget in self.right_content.winfo_children():
            widget.destroy()

        compat_card = ctk.CTkFrame(
            self.right_content, fg_color="#262626", corner_radius=18, height=455
        )
        compat_card.pack(fill="x", padx=8, pady=(6, 6))
        compat_card.pack_propagate(False)

        ctk.CTkLabel(
            compat_card, text="COMPATIBILIDAD ARMÓNICA",
            font=("Segoe UI Semibold", 18, "bold"), text_color="#2dd4bf"
        ).pack(anchor="w", padx=14, pady=(12, 10))

        data = HarmonicEngine.build_compatibility(key)
        sections = [
            ("Perfect Match", "Mezcla perfecta", "#22c55e", data["perfect"]),
            ("Boost +1", "Energía suave", "#eab308", data["boost_1"]),
            ("Boost +2", "Más energía", "#f59e0b", data["boost_2"]),
            ("Boost +3", "Energía máxima", "#ef476f", data["boost_3"]),
            ("Drop -1", "Cambio suave", "#3b82f6", data["drop_1"]),
            ("Drop -2", "Cambio moderado", "#8b5cf6", data["drop_2"]),
            ("Drop -3", "Cambio dramático", "#ec4899", data["drop_3"]),
            ("Mood / Especial", "Para ambientes", "#06b6d4", data["mood"]),
        ]

        for title, subtitle, color, values in sections:
            row = ctk.CTkFrame(compat_card, fg_color="transparent", height=47)
            row.pack(fill="x", padx=12, pady=(0, 2))
            row.pack_propagate(False)

            accent = ctk.CTkFrame(row, width=3, height=47, fg_color=color)
            accent.pack(side="left", fill="y", padx=(0, 10))

            txt = ctk.CTkFrame(row, fg_color="transparent")
            txt.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(
                txt, text=title, font=("Segoe UI Semibold", 15), text_color=color
            ).pack(anchor="w")
            ctk.CTkLabel(
                txt, text=subtitle, font=("Segoe UI", 16), text_color="white"
            ).pack(anchor="w")

            badges = ctk.CTkFrame(row, fg_color="transparent")
            badges.pack(side="right", padx=(4, 0))
            for value in values:
                ctk.CTkLabel(
                    badges, text=value, width=54, height=32,
                    fg_color=CAMELOT_COLORS.get(value, color),
                    text_color="#000000", corner_radius=6,
                    font=("Segoe UI", 12, "bold")
                ).pack(side="left", padx=2)

        info = ctk.CTkFrame(
            self.right_content, fg_color="#262626", corner_radius=18, height=175
        )
        info.pack(fill="x", padx=8, pady=(0, 2))
        info.pack_propagate(False)

        ctk.CTkLabel(
            info, text="INFORMACIÓN",
            font=("Segoe UI Semibold", 18, "bold"), text_color="#2dd4bf"
        ).pack(anchor="center", pady=(12, 10))

        name, note = CAMELOT_DISPLAY.get(key, ("", ""))
        tipo = "Mayor" if key.endswith("B") else "Menor"

        body = ctk.CTkFrame(info, fg_color="transparent")
        body.pack(expand=True)
        for label, value in [
            ("Camelot", key),
            ("Tonalidad", f"{name} ({note})"),
            ("Tipo", tipo),
            ("Open Key", CAMELOT_TO_OPENKEY.get(key, ""))
        ]:
            row = ctk.CTkFrame(body, fg_color="transparent")
            row.pack(anchor="center")
            ctk.CTkLabel(
                row, text=f"{label}:", font=("Segoe UI", 11), text_color="#9fb0c7"
            ).pack(side="left", padx=(0, 8))
            ctk.CTkLabel(
                row, text=value, font=("Segoe UI", 11, "bold"),
                text_color=CAMELOT_COLORS.get(key, "#ffffff")
            ).pack(side="left")

    def on_key_selected(self, key):
        self.selected_key = key
        if self.wheel.selected_key != key:
            self.wheel.select_key(key)
        self.update_left_panel(key)
        self.update_right_panel(key)

    def center_window(self, width, height):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, (sw - width) // 2)
        y = max(0, (sh - height) // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    app = CamelotApp()
    app.mainloop()
