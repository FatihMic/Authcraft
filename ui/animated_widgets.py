import customtkinter as ctk

class AnimatedButton(ctk.CTkButton):
    """Hover (üzerine gelindiğinde) yumuşak renk efekti veren animasyonlu buton."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.default_color = self.cget("fg_color")
        self.hover_color_custom = kwargs.get("hover_color", "#89b4fa")
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event=None):
        self.configure(fg_color=self.hover_color_custom)

    def on_leave(self, event=None):
        self.configure(fg_color=self.default_color)


class FadeFrame(ctk.CTkFrame):
    """Ekran geçişlerinde ön plana getirme ve akıcı görünürlük sağlayan bileşen."""
    def animate_in(self, delay_ms=15):
        self.lift()
        def _step(step=1):
            if step <= 10:
                self.update_idletasks()
                self.after(delay_ms, lambda: _step(step + 1))
        _step()