import tkinter as tk
from tkinter import ttk


class SmartDustbin:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Dustbin Simulation")
        self.root.geometry("1000x650")
        self.root.minsize(850, 550)
        self.root.configure(bg="#eef2f5")

        # Simulation variables
        self.fill_level = 0
        self.lid_open = False
        self.close_timer = None

        # Colors
        self.background = "#eef2f5"
        self.white = "#ffffff"
        self.dark = "#1f2937"
        self.gray = "#64748b"
        self.green = "#16a34a"
        self.orange = "#f59e0b"
        self.red = "#dc2626"
        self.blue = "#2563eb"

        self.create_interface()
        self.update_display()

    # =========================================================
    # GUI
    # =========================================================

    def create_interface(self):
        title = tk.Label(
            self.root,
            text="SMART DUSTBIN SIMULATION",
            font=("Arial", 24, "bold"),
            bg=self.background,
            fg=self.dark
        )
        title.pack(pady=(20, 2))

        subtitle = tk.Label(
            self.root,
            text="Software-based simulation using Python",
            font=("Arial", 11),
            bg=self.background,
            fg=self.gray
        )
        subtitle.pack()

        main_frame = tk.Frame(self.root, bg=self.background)
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)

        # -----------------------------------------------------
        # LEFT: Dustbin visualization
        # -----------------------------------------------------

        left_frame = tk.Frame(
            main_frame,
            bg=self.white,
            highlightbackground="#d1d5db",
            highlightthickness=1
        )
        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            left_frame,
            text="BIN VISUALIZATION",
            font=("Arial", 12, "bold"),
            bg=self.white,
            fg=self.dark
        ).pack(pady=15)

        self.canvas = tk.Canvas(
            left_frame,
            bg=self.white,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=15, pady=10)
        self.canvas.bind("<Configure>", lambda event: self.draw_dustbin())

        # -----------------------------------------------------
        # RIGHT: Dashboard
        # -----------------------------------------------------

        right_frame = tk.Frame(
            main_frame,
            bg=self.white,
            width=350,
            highlightbackground="#d1d5db",
            highlightthickness=1
        )
        right_frame.pack(side="right", fill="y", padx=(10, 0))
        right_frame.pack_propagate(False)

        tk.Label(
            right_frame,
            text="CONTROL & SENSOR PANEL",
            font=("Arial", 12, "bold"),
            bg=self.white,
            fg=self.dark
        ).pack(anchor="w", padx=20, pady=(18, 15))

        self.system_status = self.create_status(right_frame, "System Status")
        self.lid_status = self.create_status(right_frame, "Lid Status")
        self.ir_status = self.create_status(right_frame, "IR Sensor")
        self.distance_status = self.create_status(
            right_frame, "Ultrasonic Distance"
        )
        self.fill_status = self.create_status(right_frame, "Fill Level")

        tk.Label(
            right_frame,
            text="Fill Level",
            font=("Arial", 10),
            bg=self.white,
            fg=self.gray
        ).pack(anchor="w", padx=20, pady=(15, 4))

        self.progress = ttk.Progressbar(
            right_frame,
            orient="horizontal",
            mode="determinate",
            maximum=100
        )
        self.progress.pack(fill="x", padx=20)

        self.alert = tk.Label(
            right_frame,
            text="",
            font=("Arial", 10, "bold"),
            bg=self.white,
            fg=self.green,
            wraplength=300
        )
        self.alert.pack(anchor="w", padx=20, pady=12)

        self.create_button(
            right_frame,
            "Detect Person",
            self.detect_person
        ).pack(fill="x", padx=20, pady=4)

        self.create_button(
            right_frame,
            "Add Waste (+10%)",
            self.add_waste
        ).pack(fill="x", padx=20, pady=4)

        self.create_button(
            right_frame,
            "Empty Bin",
            self.empty_bin
        ).pack(fill="x", padx=20, pady=4)

        self.create_button(
            right_frame,
            "Reset Simulation",
            self.reset_simulation
        ).pack(fill="x", padx=20, pady=4)

        tk.Label(
            self.root,
            text="IR Sensor → Automatic Lid | Ultrasonic Sensor → Fill Level",
            font=("Arial", 9),
            bg=self.background,
            fg=self.gray
        ).pack(pady=(0, 12))

    # =========================================================
    # STATUS ROW
    # =========================================================

    def create_status(self, parent, name):
        frame = tk.Frame(parent, bg=self.white)
        frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            frame,
            text=name,
            font=("Arial", 10),
            bg=self.white,
            fg=self.gray
        ).pack(side="left")

        value = tk.Label(
            frame,
            text="--",
            font=("Arial", 11, "bold"),
            bg=self.white,
            fg=self.dark
        )
        value.pack(side="right")

        return value

    # =========================================================
    # BUTTON
    # =========================================================

    def create_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 10, "bold"),
            bg="#f8fafc",
            fg=self.dark,
            activebackground="#dbeafe",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground="#cbd5e1",
            padx=10,
            pady=10,
            cursor="hand2"
        )

    # =========================================================
    # IR SENSOR SIMULATION
    # =========================================================

    def detect_person(self):
        self.ir_status.config(
            text="PERSON DETECTED",
            fg=self.blue
        )

        self.system_status.config(
            text="ACTIVE",
            fg=self.green
        )

        self.open_lid()

        if self.close_timer is not None:
            self.root.after_cancel(self.close_timer)

        self.close_timer = self.root.after(
            2500,
            self.close_lid
        )

    # =========================================================
    # LID CONTROL
    # =========================================================

    def open_lid(self):
        self.lid_open = True

        self.lid_status.config(
            text="OPEN",
            fg=self.green
        )

        self.draw_dustbin()

    def close_lid(self):
        self.lid_open = False

        self.lid_status.config(
            text="CLOSED",
            fg=self.dark
        )

        self.ir_status.config(
            text="NO PERSON",
            fg=self.gray
        )

        self.draw_dustbin()

    # =========================================================
    # WASTE CONTROL
    # =========================================================

    def add_waste(self):
        self.fill_level += 10

        if self.fill_level > 100:
            self.fill_level = 100

        self.open_lid()

        if self.close_timer is not None:
            self.root.after_cancel(self.close_timer)

        self.close_timer = self.root.after(
            2500,
            self.close_lid
        )

        self.update_display()

    def empty_bin(self):
        self.fill_level = 0
        self.update_display()

    def reset_simulation(self):
        if self.close_timer is not None:
            self.root.after_cancel(self.close_timer)
            self.close_timer = None

        self.fill_level = 0
        self.lid_open = False

        self.system_status.config(
            text="READY",
            fg=self.blue
        )

        self.lid_status.config(
            text="CLOSED",
            fg=self.dark
        )

        self.ir_status.config(
            text="NO PERSON",
            fg=self.gray
        )

        self.update_display()

    # =========================================================
    # ULTRASONIC SENSOR SIMULATION
    # =========================================================

    def calculate_distance(self):
        # Virtual bin height = 40 cm.
        # 0% full  = 40 cm distance
        # 100% full = 0 cm distance
        return 40 - (self.fill_level * 0.40)

    # =========================================================
    # UPDATE DASHBOARD
    # =========================================================

    def update_display(self):
        distance = self.calculate_distance()

        self.distance_status.config(
            text=f"{distance:.1f} cm"
        )

        self.fill_status.config(
            text=f"{self.fill_level}%"
        )

        self.progress["value"] = self.fill_level

        if self.fill_level >= 100:
            self.alert.config(
                text="BIN FULL - Please empty the bin.",
                fg=self.red
            )
            self.system_status.config(
                text="BIN FULL",
                fg=self.red
            )

        elif self.fill_level >= 80:
            self.alert.config(
                text="WARNING - Bin is nearly full.",
                fg=self.orange
            )
            self.system_status.config(
                text="WARNING",
                fg=self.orange
            )

        else:
            self.alert.config(
                text="Bin has sufficient capacity.",
                fg=self.green
            )

            if self.system_status.cget("text") not in ("ACTIVE",):
                self.system_status.config(
                    text="READY",
                    fg=self.blue
                )

        self.draw_dustbin()

    # =========================================================
    # DRAW DUSTBIN
    # =========================================================

    def draw_dustbin(self):
        canvas = self.canvas
        canvas.delete("all")

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width < 300:
            width = 300

        if height < 300:
            height = 300

        center_x = width / 2

        # Dustbin dimensions
        bin_width = min(220, width * 0.55)
        bin_height = min(300, height * 0.65)

        left = center_x - bin_width / 2
        right = center_x + bin_width / 2

        bottom = height - 60
        top = bottom - bin_height

        # -----------------------------------------------------
        # ULTRASONIC SENSOR WAVES
        # -----------------------------------------------------

        sensor_x = right + 40
        sensor_y = top + 70

        for radius in (12, 22, 32):
            canvas.create_arc(
                sensor_x - radius,
                sensor_y - radius,
                sensor_x + radius,
                sensor_y + radius,
                start=210,
                extent=120,
                style="arc",
                outline=self.blue,
                width=2
            )

        canvas.create_oval(
            sensor_x - 5,
            sensor_y - 5,
            sensor_x + 5,
            sensor_y + 5,
            fill=self.blue,
            outline=""
        )

        # -----------------------------------------------------
        # DUSTBIN BODY
        # -----------------------------------------------------

        canvas.create_rectangle(
            left,
            top,
            right,
            bottom,
            fill="#cbd5e1",
            outline="#475569",
            width=3
        )

        # -----------------------------------------------------
        # WASTE
        # -----------------------------------------------------

        if self.fill_level > 0:
            waste_top = (
                bottom -
                (bin_height * self.fill_level / 100)
            )

            if self.fill_level >= 90:
                waste_color = self.red
            elif self.fill_level >= 70:
                waste_color = self.orange
            else:
                waste_color = self.green

            canvas.create_rectangle(
                left + 3,
                waste_top,
                right - 3,
                bottom - 3,
                fill=waste_color,
                outline=""
            )

        # -----------------------------------------------------
        # LID
        # -----------------------------------------------------

        lid_y = top - 25

        if self.lid_open:
            # Open lid
            canvas.create_polygon(
                left - 5,
                lid_y + 10,
                right + 5,
                lid_y - 45,
                right + 5,
                lid_y - 28,
                left - 5,
                lid_y + 28,
                fill="#94a3b8",
                outline="#475569",
                width=3
            )
        else:
            # Closed lid
            canvas.create_rectangle(
                left - 12,
                lid_y,
                right + 12,
                lid_y + 18,
                fill="#94a3b8",
                outline="#475569",
                width=3
            )

        # -----------------------------------------------------
        # HANDLE
        # -----------------------------------------------------

        handle_y = lid_y - 4

        if self.lid_open:
            handle_y = lid_y - 35

        canvas.create_rectangle(
            center_x - 28,
            handle_y - 9,
            center_x + 28,
            handle_y,
            fill="#64748b",
            outline="#475569"
        )

        # -----------------------------------------------------
        # TEXT
        # -----------------------------------------------------

        canvas.create_text(
            center_x,
            top + 30,
            text="SMART BIN",
            fill=self.dark,
            font=("Arial", 14, "bold")
        )

        canvas.create_text(
            center_x,
            bottom + 25,
            text=f"{self.fill_level}% FULL",
            fill=self.dark,
            font=("Arial", 14, "bold")
        )

        if self.lid_open:
            ir_text = "IR SENSOR: PERSON"
            ir_color = self.blue
        else:
            ir_text = "IR SENSOR: CLEAR"
            ir_color = self.gray

        canvas.create_text(
            center_x,
            bottom + 47,
            text=ir_text,
            fill=ir_color,
            font=("Arial", 10, "bold")
        )

        canvas.create_text(
            sensor_x + 10,
            sensor_y + 50,
            text=f"{self.calculate_distance():.1f} cm",
            fill=self.blue,
            font=("Arial", 10, "bold")
        )


# =============================================================
# START PROGRAM
# =============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartDustbin(root)
    root.mainloop()
