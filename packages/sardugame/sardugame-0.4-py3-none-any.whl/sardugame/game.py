import tkinter as tk

class SarduGame:
    def __init__(self):
        # Creazione della finestra
        self.window = tk.Tk()
        self.window.title("SarduGame")
        self.window.geometry("800x600")
        self.window.iconbitmap("C:\\Users\\Giovanni\\Desktop\\sardugame\\sardugame\\icon.ico")  # Impostazione dell'icona
        self.canvas = tk.Canvas(self.window, width=800, height=600)
        self.canvas.pack()

        # Variabili di stato
        self.objects = []  # Per tenere traccia degli oggetti creati
        self.x = 100  # Posizione orizzontale
        self.y = 100  # Posizione verticale

        # Mappatura dei colori italiani ai colori riconosciuti da tkinter
        self.color_map = {
            "rosso": "red",
            "blu": "blue",
            "verde": "green",
            "giallo": "yellow",
            "arancio": "orange",
            "viola": "purple",
            "rosa": "pink",
            "nero": "black",
            "bianco": "white"
        }

        # Ascolta i tasti premuti
        self.window.bind("<KeyPress-w>", self.move_up)
        self.window.bind("<KeyPress-s>", self.move_down)
        self.window.bind("<KeyPress-a>", self.move_left)
        self.window.bind("<KeyPress-d>", self.move_right)

    def crea(self, shape_info):
        """Crea un oggetto basato sul tipo e colore specificato (ad esempio 'cubo.rosso')."""
        # Separa la forma e il colore dalla stringa usando il punto (.)
        shape_type, color = shape_info.split(".")

        # Se il colore è presente nella mappa, usa il colore corrispondente
        if color in self.color_map:
            color = self.color_map[color]
        else:
            # Se il colore non è nella mappa, usa un colore predefinito
            color = "black"

        # Crea l'oggetto in base al tipo e al colore
        if shape_type == "cubo":
            # Crea un cubo (quadrato)
            self.objects.append({
                'type': 'cubo',
                'id': self.canvas.create_rectangle(self.x, self.y, self.x + 50, self.y + 50, outline="black", fill=color)
            })

        elif shape_type == "rettangolo":
            # Crea un rettangolo
            self.objects.append({
                'type': 'rettangolo',
                'id': self.canvas.create_rectangle(self.x, self.y, self.x + 100, self.y + 50, outline="black", fill=color)
            })

        elif shape_type == "triangolo":
            # Crea un triangolo
            self.objects.append({
                'type': 'triangolo',
                'id': self.canvas.create_polygon(self.x, self.y, self.x + 50, self.y - 50, self.x + 100, self.y, outline="black", fill=color)
            })

    def mostra(self, shape_info):
        """Mostra la forma e il colore specificato."""
        # Chiamato per creare l'oggetto con forma e colore specificato
        self.crea(shape_info)
        self.window.mainloop()

    def move_up(self, event):
        """Muovi gli oggetti su."""
        self.y -= 10
        self.update_objects()

    def move_down(self, event):
        """Muovi gli oggetti giù."""
        self.y += 10
        self.update_objects()

    def move_left(self, event):
        """Muovi gli oggetti a sinistra."""
        self.x -= 10
        self.update_objects()

    def move_right(self, event):
        """Muovi gli oggetti a destra."""
        self.x += 10
        self.update_objects()

    def update_objects(self):
        """Aggiorna la posizione di tutti gli oggetti in base al loro tipo."""
        for obj in self.objects:
            if obj['type'] == 'cubo':
                # Per il cubo (quadrato), muoviamo solo le coordinate (x, y)
                self.canvas.coords(obj['id'], self.x, self.y, self.x + 50, self.y + 50)

            elif obj['type'] == 'rettangolo':
                # Per il rettangolo, muoviamo solo le coordinate
                self.canvas.coords(obj['id'], self.x, self.y, self.x + 100, self.y + 50)

            elif obj['type'] == 'triangolo':
                # Per il triangolo, muoviamo i 3 vertici
                self.canvas.coords(obj['id'], self.x, self.y, self.x + 50, self.y - 50, self.x + 100, self.y)
