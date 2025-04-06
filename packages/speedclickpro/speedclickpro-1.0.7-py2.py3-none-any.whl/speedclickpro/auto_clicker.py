import pyautogui
import keyboard
import time
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os
import json
from PIL import Image, ImageTk
import webbrowser
from datetime import datetime

# Import language module
from .languages import Translator, LANGUAGES

class AutoClicker:
    def __init__(self):
        self.running = False
        self.positions = []  # Will store (x, y, duration) tuples
        self.click_thread = None
        self.click_speed = 0  #  clicks per second (CPS) - normal mode
        self.advanced_mode = False  # โหมดขั้นสูงที่ใช้ความเร็วสูงสุด
        self.profiles = {"Default": []}  # Store click profiles
        self.current_profile = "Default"
        self.sequence_mode = False  # Animation sequence mode toggle
        self.default_duration = 5  # Default duration in seconds
        
        # Set up the profiles directory
        # When installed via pip, use user's home directory for profiles
        self.profiles_dir = os.path.join(os.path.expanduser("~"), ".speedclickpro", "profiles")
        os.makedirs(self.profiles_dir, exist_ok=True)
        
        # Try to load saved profiles
        self.load_saved_profiles()
        
        # Initialize translator
        self.translator = Translator()
        self.program_name = self.translator.get_text("program_name")
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title(self.program_name)
        self.root.geometry("1050x740")  # เพิ่มความสูงเริ่มต้น
        self.root.minsize(1050, 740)  # กำหนดขนาดขั้นต่ำให้เห็นองค์ประกอบทั้งหมด
        
        # Set app icon
        try:
            # Set the icon if available
            # When installed via pip, look for icons in the package directory
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "icon.png")
            if os.path.exists(icon_path):
                icon = ImageTk.PhotoImage(Image.open(icon_path))
                self.root.iconphoto(True, icon)
        except Exception as e:
            print(f"Could not load icon: {e}")
            
        # Setup theme colors
        self.colors = {
            "primary": "#2c3e50",  # Dark blue
            "secondary": "#3498db",  # Light blue
            "accent": "#e74c3c",  # Red
            "success": "#2ecc71",  # Green
            "warning": "#f39c12",  # Orange
            "light": "#ecf0f1",  # Light gray
            "dark": "#2c3e50",  # Dark blue
            "very_dark": "#1a252f"  # Very dark blue
        }
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("TH Sarabun New", 12, "bold"), background=self.colors["secondary"])
        self.style.configure("success.TButton", background=self.colors["success"])
        self.style.configure("danger.TButton", background=self.colors["accent"])
        self.style.configure("TLabel", font=("TH Sarabun New", 12))
        self.style.configure("Header.TLabel", font=("TH Sarabun New", 18, "bold"))
        self.style.configure("Status.TLabel", background=self.colors["primary"], foreground=self.colors["light"])
        
        # Thai fonts
        self.thai_font = ("TH Sarabun New", 12)
        self.thai_font_bold = ("TH Sarabun New", 12, "bold")
        self.thai_font_large = ("TH Sarabun New", 18, "bold")
        
        # Configure root window
        self.root.configure(bg=self.colors["light"])
        
        # Create the UI elements
        self.create_widgets()
        
        # ปรับขนาดหน้าต่างให้พอดีกับ UI
        self.root.update_idletasks()  # อัพเดตงานทั้งหมดก่อน
        self.root.after(100, self.adjust_window_size)
        
        # Set the keyboard hook for Ctrl+G to toggle clicking
        keyboard.add_hotkey('ctrl+g', self.toggle_clicking)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def create_widgets(self):
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill='both', expand=True)
        
        # Create header
        self.create_header()
        
        # Create main content area with left and right panels
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel (two-thirds of the width)
        self.left_panel = ttk.Frame(self.content_frame)
        self.left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right panel (one-third of the width)
        self.right_panel = ttk.Frame(self.content_frame)
        self.right_panel.pack(side='right', fill='both', expand=False, padx=(10, 0), pady=10)
        
        # Add content to panels
        self.create_left_panel()
        self.create_right_panel()
        
        # Create status bar
        self.create_status_bar()
        
        # Create footer
        self.create_footer()
    
    def change_language(self, event=None):
        """Change the application language"""
        # Get the selected language code from the combobox
        selected = self.language_combo.get()
        if selected:
            # Extract the language code (first two characters)
            lang_code = selected.split(' ')[0]
            
            # Update the translator language
            self.translator.set_language(lang_code)
            
            # Update the program name
            self.program_name = self.translator.get_text("program_name")
            self.root.title(self.program_name)
            
            # Recreate the UI with new language
            self.refresh_ui()
            
            # Show language changed message
            self.status_var.set(f"{self.translator.get_text('ready')}")
    
    def refresh_ui(self):
        """Refresh the UI with current language"""
        # Destroy current widgets
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Recreate widgets
        self.create_header()
        
        # Create main content area with left and right panels
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel (two-thirds of the width)
        self.left_panel = ttk.Frame(self.content_frame)
        self.left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right panel (one-third of the width)
        self.right_panel = ttk.Frame(self.content_frame)
        self.right_panel.pack(side='right', fill='both', expand=False, padx=(10, 0), pady=10)
        
        # Add content to panels
        self.create_left_panel()
        self.create_right_panel()
        
        # Update status bar text
        self.status_var.set(self.translator.get_text("ready"))
        
    def create_header(self):
        # Header container with background color
        header = ttk.Frame(self.main_container, style='Header.TFrame')
        header.pack(fill='x', pady=(0, 10))
        
        # Header content with padding
        header_content = ttk.Frame(header)
        header_content.pack(fill='x', padx=20, pady=15)
        
        # Logo and title
        title_frame = ttk.Frame(header_content)
        title_frame.pack(side='left')
        
        # Add logo image if available
        try:
            # Look for logo in the package directory
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "logo.png")
            if os.path.exists(logo_path):
                # Load and resize logo
                original_logo = Image.open(logo_path)
                resized_logo = original_logo.resize((180, 90), Image.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(resized_logo)
                
                # Display logo
                logo_label = ttk.Label(title_frame, image=self.logo_image)
                logo_label.pack(side='left', padx=(0, 15))
            else:
                # Fallback to text logo
                logo_label = ttk.Label(title_frame, text="🖱️", font=("TH Sarabun New", 24))
                logo_label.pack(side='left', padx=(0, 10))
        except Exception as e:
            print(f"Could not load logo: {e}")
            # Fallback to text logo
            logo_label = ttk.Label(title_frame, text="🖱️", font=("TH Sarabun New", 24))
            logo_label.pack(side='left', padx=(0, 10))
        
        # Program name and subtitle
        name_frame = ttk.Frame(title_frame)
        name_frame.pack(side='left')
        
        title_label = ttk.Label(name_frame, text=self.program_name, style="Header.TLabel", font=("TH Sarabun New", 24, "bold"), foreground="#e74c3c")
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(name_frame, text=self.translator.get_text("program_subtitle"), style="TLabel", font=self.thai_font_bold)
        subtitle_label.pack(anchor='w')
        
        # Mode indicator on the right
        mode_frame = ttk.Frame(header_content)
        mode_frame.pack(side='right')
        
        mode_icon = ttk.Label(mode_frame, text="⚡", font=("TH Sarabun New", 18))
        mode_icon.pack(side='left', padx=(0, 5))
        
        # Mode label will show '90 CPS Mode' or 'Ultimate Speed' based on advanced_mode
        self.mode_label = ttk.Label(mode_frame, text="Super Fast Mode", font=self.thai_font_bold, foreground=self.colors["accent"])
        self.mode_label.pack(side='left')
    
    def create_left_panel(self):
        # Positions panel
        positions_frame = ttk.LabelFrame(self.left_panel, text=f" {self.translator.get_text('positions_frame')} ", padding=(10, 5))
        positions_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Toolbar for positions
        toolbar = ttk.Frame(positions_frame)
        toolbar.pack(fill='x', pady=(0, 5))
        
        # Position counter
        self.position_counter = ttk.Label(toolbar, text=self.translator.get_text('positions_count', 0), font=self.thai_font)
        self.position_counter.pack(side='left')
        
        # Add and clear buttons
        btn_frame = ttk.Frame(toolbar)
        btn_frame.pack(side='right')
        
        self.add_pos_btn = ttk.Button(btn_frame, text=self.translator.get_text('add_position'), command=self.add_position, style="success.TButton")
        self.add_pos_btn.pack(side='left', padx=5)
        
        self.clear_pos_btn = ttk.Button(btn_frame, text=self.translator.get_text('clear_positions'), command=self.clear_positions, style="danger.TButton")
        self.clear_pos_btn.pack(side='left')
        
        # Positions list with scrollbar inside a container
        list_container = ttk.Frame(positions_frame)
        list_container.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview for positions
        columns = ("number", "x", "y")
        self.positions_tree = ttk.Treeview(list_container, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        
        # Add duration column
        columns = ("number", "x", "y", "duration")
        self.positions_tree = ttk.Treeview(list_container, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.positions_tree.heading("number", text=self.translator.get_text('column_number'))
        self.positions_tree.heading("x", text=self.translator.get_text('column_x'))
        self.positions_tree.heading("y", text=self.translator.get_text('column_y'))
        self.positions_tree.heading("duration", text=self.translator.get_text('column_duration'))
        
        self.positions_tree.column("number", width=50)
        self.positions_tree.column("x", width=80)
        self.positions_tree.column("y", width=80)
        self.positions_tree.column("duration", width=80)
        
        self.positions_tree.pack(fill='both', expand=True)
        scrollbar.config(command=self.positions_tree.yview)
        
        # Right-click menu for positions
        self.position_menu = tk.Menu(self.positions_tree, tearoff=0)
        self.position_menu.add_command(label=self.translator.get_text('delete_position'), command=self.delete_selected_position)
        self.position_menu.add_command(label=self.translator.get_text('edit_position'), command=self.edit_selected_position)
        self.position_menu.add_command(label=self.translator.get_text('edit_duration'), command=self.edit_duration)
        
        self.positions_tree.bind("<Button-3>", self.show_position_menu)
        
        # Statistics panel
        stats_frame = ttk.LabelFrame(self.left_panel, text=f" {self.translator.get_text('stats_frame')} ", padding=(10, 5))
        stats_frame.pack(fill='x', pady=(0, 10))
        
        # Statistics grid
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill='x', pady=5)
        
        # Click counter
        click_count_label = ttk.Label(stats_grid, text=self.translator.get_text('click_count'), font=self.thai_font)
        click_count_label.grid(row=0, column=0, sticky='w', padx=5, pady=2)
        
        self.click_count_var = tk.StringVar(value="0")
        click_count_value = ttk.Label(stats_grid, textvariable=self.click_count_var, font=self.thai_font_bold)
        click_count_value.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        # Runtime
        runtime_label = ttk.Label(stats_grid, text=self.translator.get_text('runtime'), font=self.thai_font)
        runtime_label.grid(row=1, column=0, sticky='w', padx=5, pady=2)
        
        self.runtime_var = tk.StringVar(value="00:00:00")
        runtime_value = ttk.Label(stats_grid, textvariable=self.runtime_var, font=self.thai_font_bold)
        runtime_value.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        # Last started
        last_run_label = ttk.Label(stats_grid, text=self.translator.get_text('last_started'), font=self.thai_font)
        last_run_label.grid(row=0, column=2, sticky='w', padx=5, pady=2)
        
        self.last_run_var = tk.StringVar(value="-")
        last_run_value = ttk.Label(stats_grid, textvariable=self.last_run_var, font=self.thai_font_bold)
        last_run_value.grid(row=0, column=3, sticky='w', padx=5, pady=2)
        
        # Last stopped
        last_stop_label = ttk.Label(stats_grid, text=self.translator.get_text('last_stopped'), font=self.thai_font)
        last_stop_label.grid(row=1, column=2, sticky='w', padx=5, pady=2)
        
        self.last_stop_var = tk.StringVar(value="-")
        last_stop_value = ttk.Label(stats_grid, textvariable=self.last_stop_var, font=self.thai_font_bold)
        last_stop_value.grid(row=1, column=3, sticky='w', padx=5, pady=2)
    
    def create_right_panel(self):
        # Animation Mode panel
        animation_frame = ttk.LabelFrame(self.right_panel, text=" Animation Mode ", padding=(10, 5))
        animation_frame.pack(fill='x', pady=(0, 10))
        
        # Animation mode toggle
        self.sequence_mode_var = tk.BooleanVar(value=self.sequence_mode)
        sequence_mode_cb = ttk.Checkbutton(
            animation_frame, 
            text=self.translator.get_text('sequence_mode'), 
            variable=self.sequence_mode_var,
            command=self.toggle_sequence_mode,
            style="TCheckbutton"
        )
        sequence_mode_cb.pack(anchor='w', pady=5)
        
        # โหมดขั้นสูง (Advanced Mode)
        advanced_mode_frame = ttk.Frame(animation_frame)
        advanced_mode_frame.pack(fill='x', pady=5)
        
        self.advanced_mode_var = tk.BooleanVar(value=self.advanced_mode)
        advanced_mode_cb = ttk.Checkbutton(
            advanced_mode_frame, 
            text="โหมดขั้นสูง (Ultimate Speed)", 
            variable=self.advanced_mode_var,
            command=self.toggle_advanced_mode,
            style="TCheckbutton"
        )
        advanced_mode_cb.pack(side='left', pady=5)
        
        # ไอคอนความเร็ว
        speed_icon = ttk.Label(advanced_mode_frame, text="⚡", font=("TH Sarabun New", 14), foreground=self.colors["warning"])
        speed_icon.pack(side='left')
        
        # Default duration selector
        duration_frame = ttk.Frame(animation_frame)
        duration_frame.pack(fill='x', pady=5)
        
        duration_label = ttk.Label(duration_frame, text=self.translator.get_text('enter_duration'), font=self.thai_font)
        duration_label.pack(side='left')
        
        self.default_duration_var = tk.StringVar(value=str(self.default_duration))
        self.default_duration_entry = ttk.Entry(duration_frame, width=5, textvariable=self.default_duration_var)
        self.default_duration_entry.pack(side='right')
        
        # Control panel
        control_frame = ttk.LabelFrame(self.right_panel, text=f" {self.translator.get_text('control_frame')} ", padding=(10, 5))
        control_frame.pack(fill='x', pady=(0, 10))
        
        # Start/Stop buttons
        btn_container = ttk.Frame(control_frame)
        btn_container.pack(fill='x', pady=10)
        
        self.start_btn = ttk.Button(
            btn_container, 
            text=self.translator.get_text('start_clicking'), 
            command=self.start_clicking,
            style="success.TButton"
        )
        self.start_btn.pack(fill='x', pady=(0, 5))
        
        self.stop_btn = ttk.Button(
            btn_container, 
            text=self.translator.get_text('stop_clicking'), 
            command=self.toggle_clicking,
            style="danger.TButton"
        )
        self.stop_btn.pack(fill='x')
        
        # Keyboard shortcut info
        shortcut_frame = ttk.Frame(control_frame)
        shortcut_frame.pack(fill='x', pady=10)
        
        shortcut_label = ttk.Label(
            shortcut_frame, 
            text=self.translator.get_text('shortcut_info'), 
            font=self.thai_font_bold,
            foreground=self.colors["secondary"]
        )
        shortcut_label.pack()
        
        # Settings panel
        settings_frame = ttk.LabelFrame(self.right_panel, text=f" {self.translator.get_text('settings_frame')} ", padding=(10, 5))
        settings_frame.pack(fill='x', pady=(0, 10))
        
        # Always on top
        always_on_top_var = tk.BooleanVar(value=False)
        always_on_top = ttk.Checkbutton(
            settings_frame, 
            text=self.translator.get_text('always_on_top'), 
            variable=always_on_top_var,
            command=lambda: self.root.attributes('-topmost', always_on_top_var.get()),
            style="TCheckbutton"
        )
        always_on_top.pack(anchor='w', pady=5)
        
        # Mini mode
        mini_mode_var = tk.BooleanVar(value=False)
        mini_mode = ttk.Checkbutton(
            settings_frame, 
            text=self.translator.get_text('mini_mode'), 
            variable=mini_mode_var,
            command=self.toggle_mini_mode,
            style="TCheckbutton"
        )
        mini_mode.pack(anchor='w', pady=5)
        
        # Language selection
        lang_frame = ttk.Frame(settings_frame)
        lang_frame.pack(fill='x', pady=5)
        
        lang_label = ttk.Label(lang_frame, text=self.translator.get_text('language'), font=self.thai_font)
        lang_label.pack(side='left', padx=(0, 5))
        
        # Language dropdown
        self.language_var = tk.StringVar(value=self.translator.current_lang)
        self.language_combo = ttk.Combobox(lang_frame, textvariable=self.language_var, state="readonly")
        
        # Populate language options
        langs = self.translator.get_languages()
        self.language_combo['values'] = [f"{code} - {name}" for code, name in langs.items()]
        for i, lang_code in enumerate(langs.keys()):
            if lang_code == self.translator.current_lang:
                self.language_combo.current(i)
                break
        
        self.language_combo.pack(side='right', fill='x', expand=True)
        self.language_combo.bind("<<ComboboxSelected>>", self.change_language)
        
        # Profiles panel
        profiles_frame = ttk.LabelFrame(self.right_panel, text=f" {self.translator.get_text('profiles_frame')} ", padding=(10, 5))
        profiles_frame.pack(fill='x', expand=True)
        
        # Profile selector
        profile_select_frame = ttk.Frame(profiles_frame)
        profile_select_frame.pack(fill='x', pady=5)
        
        profile_label = ttk.Label(profile_select_frame, text=self.translator.get_text('profile'), font=self.thai_font)
        profile_label.pack(side='left')
        
        self.profile_var = tk.StringVar(value=self.current_profile)
        self.profile_combo = ttk.Combobox(profile_select_frame, textvariable=self.profile_var, state="readonly")
        self.update_profile_dropdown()
        self.profile_combo.pack(side='right', fill='x', expand=True, padx=5)
        
        # Profile buttons
        profile_btn_frame = ttk.Frame(profiles_frame)
        profile_btn_frame.pack(fill='x', pady=5)
        
        save_profile_btn = ttk.Button(profile_btn_frame, text=self.translator.get_text('save_profile'), command=self.save_profile)
        save_profile_btn.pack(side='left', padx=(0, 5), fill='x', expand=True)
        
        load_profile_btn = ttk.Button(profile_btn_frame, text=self.translator.get_text('load_profile'), command=self.load_profile)
        load_profile_btn.pack(side='right', fill='x', expand=True)
    
    def create_status_bar(self):
        # Status bar frame
        status_frame = ttk.Frame(self.root, style="Status.TFrame")
        status_frame.pack(side='bottom', fill='x')
        
        # Status bar with padding
        self.status_var = tk.StringVar()
        self.status_var.set(self.translator.get_text('ready'))
        
        # Add debug info about profiles during startup
        if hasattr(self, 'profiles'):
            profile_names = list(self.profiles.keys())
            print(f"Available profiles: {profile_names}")
        
        status_bar = ttk.Label(
            status_frame, 
            textvariable=self.status_var, 
            style="Status.TLabel",
            font=self.thai_font,
            anchor='w'
        )
        status_bar.pack(fill='x', padx=10, pady=5)
    
    def create_footer(self):
        # Footer container
        footer = ttk.Frame(self.root)
        footer.pack(side='bottom', fill='x', pady=5)
        
        # Version info
        version_label = ttk.Label(footer, text=f"{self.program_name} {self.translator.get_text('version')} 1.0.7", font=("TH Sarabun New", 10))
        version_label.pack(side='left', padx=10)
        
        # Credits info
        credits_label = ttk.Label(footer, text=self.translator.get_text('copyright'), font=("TH Sarabun New", 10))
        credits_label.pack(side='right', padx=10)
    
    def add_position(self):
        self.root.iconify()  # Minimize window
        time.sleep(2)  # Give user time to position mouse
        x, y = pyautogui.position()
        
        # Add position with default duration
        try:
            duration = float(self.default_duration_var.get())
        except ValueError:
            duration = self.default_duration
            self.default_duration_var.set(str(duration))
            
        self.positions.append((x, y, duration))
        self.root.deiconify()  # Restore window
        
        self.update_position_display()
        self.status_var.set(self.translator.get_text('position_added', x, y))
    
    def update_position_display(self):
        # Clear the current list
        for item in self.positions_tree.get_children():
            self.positions_tree.delete(item)
        
        # Add each position to the treeview
        for i, position in enumerate(self.positions):
            if len(position) == 2:  # Backwards compatibility with old format
                x, y = position
                duration = self.default_duration
                # Update to new format
                self.positions[i] = (x, y, duration)
            else:
                x, y, duration = position
                
            self.positions_tree.insert('', 'end', values=(i+1, x, y, duration))
        
        # Update position counter
        self.position_counter.config(text=self.translator.get_text('positions_count', len(self.positions)))
    
    def clear_positions(self):
        self.positions = []
        self.update_position_display()
        self.status_var.set(self.translator.get_text('all_positions_cleared'))
        self.click_count_var.set("0")
    
    def start_clicking(self):
        # Just call toggle_clicking if we're not already running
        if not self.running:
            self.toggle_clicking()
    
    def clicking_loop(self):
        clicks = 0
        start_time = time.time()
        
        while self.running:
            if self.sequence_mode:
                # Animation sequence mode - follow positions in order with specified duration
                for position in self.positions:
                    if not self.running:
                        break
                        
                    # Get position data
                    if len(position) == 2:  # Backwards compatibility check
                        x, y = position
                        duration = self.default_duration
                    else:
                        x, y, duration = position
                    
                    # Update status to show which position is active
                    position_index = self.positions.index(position) + 1
                    self.status_var.set(f"Position {position_index} active - {duration}s")
                    
                    # Create a countdown loop that continuously clicks for the duration
                    start_wait = time.time()
                    click_interval = 0  # Click as fast as possible
                    last_click_time = 0
                    
                    # Click continuously at this position for the duration period
                    while self.running and (time.time() - start_wait) < duration:
                        current_time = time.time()
                        
                        # Click if enough time has passed since last click
                        if current_time - last_click_time >= click_interval:
                            pyautogui.click(x, y)
                            clicks += 1
                            last_click_time = current_time
                            
                            # Update click counter
                            if clicks % 10 == 0:
                                self.click_count_var.set(str(clicks))
                                
                                # Update runtime
                                elapsed = int(time.time() - start_time)
                                hours, remainder = divmod(elapsed, 3600)
                                minutes, seconds = divmod(remainder, 60)
                                self.runtime_var.set(f"{hours:02}:{minutes:02}:{seconds:02}")
                        
                        # Update remaining time in status bar (every 0.5 seconds)
                        remaining = duration - (time.time() - start_wait)
                        if remaining > 0 and int(remaining * 10) % 5 == 0:  # Update status every 0.5 seconds
                            self.status_var.set(f"Position {position_index} - {remaining:.1f}s remaining - {clicks} clicks")
                            
                        # Short sleep to prevent CPU overload
                        time.sleep(0.001)
            else:
                # Regular mode - rapid clicking all positions without timing
                for position in self.positions:
                    if not self.running:
                        break
                        
                    # Get position data
                    if len(position) == 2:  # Backwards compatibility check
                        x, y = position
                    else:
                        x, y, _ = position  # Ignore duration in regular mode
                        
                    pyautogui.click(x, y)
                    clicks += 1
                    
                    # Update click counter every 10 clicks to avoid too many UI updates
                    if clicks % 10 == 0:
                        self.click_count_var.set(str(clicks))
                        
                        # Update runtime
                        elapsed = int(time.time() - start_time)
                        hours, remainder = divmod(elapsed, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        self.runtime_var.set(f"{hours:02}:{minutes:02}:{seconds:02}")
                    
                    # ตรวจสอบโหมดขั้นสูง
                if not self.advanced_mode:
                    # โหมดปกติ - 90 CPS
                    time.sleep(self.click_speed)
                # โหมดขั้นสูงไม่มี delay เพื่อความเร็วสูงสุด
    
    def toggle_clicking(self):
        if self.running:
            # Stop clicking
            self.running = False
            self.start_btn.config(state='normal')
            self.status_var.set(self.translator.get_text('stopped'))
            
            # Update stop time
            self.last_stop_var.set(datetime.now().strftime("%H:%M:%S"))
        else:
            # Start clicking if positions exist
            if not self.positions:
                messagebox.showwarning(self.translator.get_text('warning'), 
                                    self.translator.get_text('add_position_first'))
                return
                
            self.running = True
            self.start_btn.config(state='disabled')
            
            # กำหนดข้อความสถานะตามโหมด
            if self.advanced_mode:
                self.status_var.set("กำลังทำงาน (โหมดขั้นสูง - ความเร็วสูงสุด)")
                # อัพเดตไอคอนแสดงโหมด
                self.mode_label.config(text="Ultimate Speed", foreground=self.colors["warning"])
            else:
                self.status_var.set(self.translator.get_text('working'))
                # อัพเดตไอคอนแสดงโหมด
                self.mode_label.config(text="90 CPS Mode", foreground=self.colors["accent"])
            
            # Reset stats
            self.click_count_var.set("0")
            self.runtime_var.set("00:00:00")
            
            # Update start time
            self.last_run_var.set(datetime.now().strftime("%H:%M:%S"))
            
            # Start the clicking thread if it's not already running
            if not self.click_thread or not self.click_thread.is_alive():
                self.click_thread = threading.Thread(target=self.clicking_loop)
                self.click_thread.daemon = True
                self.click_thread.start()
    
    # New utility functions for the enhanced UI
    def show_position_menu(self, event):
        # Get the position that was clicked
        item = self.positions_tree.identify_row(event.y)
        if item:
            self.positions_tree.selection_set(item)
            self.position_menu.post(event.x_root, event.y_root)
    
    def delete_selected_position(self):
        selected = self.positions_tree.selection()
        if selected:
            # Get the index from the selected item
            item_values = self.positions_tree.item(selected[0], 'values')
            if item_values:
                index = int(item_values[0]) - 1
                if 0 <= index < len(self.positions):
                    del self.positions[index]
                    self.update_position_display()
                    self.status_var.set(self.translator.get_text('position_deleted', index+1))
    
    def edit_selected_position(self):
        selected = self.positions_tree.selection()
        if selected:
            # Get the index from the selected item
            item_values = self.positions_tree.item(selected[0], 'values')
            if item_values:
                index = int(item_values[0]) - 1
                if 0 <= index < len(self.positions):
                    # Get current position
                    current_x, current_y, current_duration = self.positions[index]
                    
                    # Ask user to reposition cursor
                    if messagebox.askyesno(self.translator.get_text('edit_position'), 
                                          self.translator.get_text('confirm_edit')):
                        self.root.iconify()  # Minimize window
                        time.sleep(2)  # Give user time to position mouse
                        new_x, new_y = pyautogui.position()
                        self.positions[index] = (new_x, new_y, current_duration)
                        self.root.deiconify()  # Restore window
                        
                        self.update_position_display()
                        self.status_var.set(self.translator.get_text('position_edited', index+1, new_x, new_y))
    
    def edit_duration(self):
        selected = self.positions_tree.selection()
        if selected:
            # Get the index from the selected item
            item_values = self.positions_tree.item(selected[0], 'values')
            if item_values:
                index = int(item_values[0]) - 1
                if 0 <= index < len(self.positions):
                    # Get current position
                    x, y, current_duration = self.positions[index]
                    
                    # Ask user for new duration
                    new_duration = simpledialog.askfloat(
                        self.translator.get_text('edit_duration'),
                        self.translator.get_text('enter_duration'),
                        initialvalue=current_duration,
                        minvalue=0.1,
                        maxvalue=3600
                    )
                    
                    if new_duration is not None:
                        self.positions[index] = (x, y, new_duration)
                        self.update_position_display()
                        self.status_var.set(f"{self.translator.get_text('edit_duration')}: {index+1} ({new_duration}s)")
    
    def toggle_sequence_mode(self):
        """Toggle between regular clicking and animation sequence mode"""
        self.sequence_mode = self.sequence_mode_var.get()
        if self.sequence_mode:
            self.status_var.set(self.translator.get_text('sequence_mode'))
        else:
            self.status_var.set(self.translator.get_text('ready'))
            
    def toggle_advanced_mode(self):
        """Toggle between normal speed (90 CPS) and ultimate speed mode"""
        self.advanced_mode = self.advanced_mode_var.get()
        if self.advanced_mode:
            self.status_var.set("โหมดขั้นสูง - ความเร็วสูงสุด")
            # แสดงข้อความเตือน
            messagebox.showwarning("โหมดขั้นสูง", 
                                   "คุณเปิดใช้โหมดขั้นสูงที่ใช้ความเร็วสูงสุด\nจะใช้ทรัพยากรเครื่องมากขึ้น แต่จะได้ความเร็วสูงสุด")
        else:
            self.status_var.set("กลับสู่โหมดปกติ - 90 CPS")
    
    def toggle_mini_mode(self):
        # This function would toggle between full and mini mode UI
        # Mini mode would hide non-essential UI elements and resize the window
        pass
        
    def adjust_window_size(self):
        """ตรวจสอบและปรับขนาดหน้าต่างให้แสดงองค์ประกอบทั้งหมดได้"""
        # รับขนาดที่ต้องการของเนื้อหาทั้งหมด
        required_height = self.main_container.winfo_reqheight()
        current_height = self.root.winfo_height()
        
        # ถ้าความสูงที่ต้องการมากกว่าความสูงปัจจุบัน ให้ปรับขนาดหน้าต่าง
        if required_height > current_height - 50:  # หักค่าความสูงของแถบหัวเรื่อง
            new_height = required_height + 50  # เพิ่มพื้นที่เผื่อแถบหัวเรื่อง
            current_width = self.root.winfo_width()
            self.root.geometry(f"{current_width}x{new_height}")
            
        # บันทึกขนาดขั้นต่ำให้เห็นองค์ประกอบทั้งหมด
        min_width = max(1050, self.main_container.winfo_reqwidth())
        min_height = max(740, required_height + 50)
        self.root.minsize(min_width, min_height)
    
    def load_saved_profiles(self):
        """Load profiles from saved json file"""
        profile_file = os.path.join(self.profiles_dir, "saved_profiles.json")
        
        if os.path.exists(profile_file):
            try:
                with open(profile_file, 'r') as f:
                    # Read JSON data
                    data = json.load(f)
                    
                    # Convert loaded data to proper format
                    for name, positions in data.items():
                        # Convert positions list to list of tuples if needed
                        formatted_positions = []
                        for pos in positions:
                            if isinstance(pos, list):
                                # Convert from JSON list to tuple
                                if len(pos) == 2:
                                    formatted_positions.append((pos[0], pos[1], self.default_duration))
                                else:  # len == 3
                                    formatted_positions.append(tuple(pos))
                            elif isinstance(pos, dict) and 'x' in pos and 'y' in pos:
                                # Handle dictionary format if present
                                duration = pos.get('duration', self.default_duration)
                                formatted_positions.append((pos['x'], pos['y'], duration))
                            else:
                                # Already a tuple, just add it
                                formatted_positions.append(pos)
                        
                        self.profiles[name] = formatted_positions
                        
                    print(f"Loaded {len(self.profiles)} profiles")
            except Exception as e:
                print(f"Error loading profiles: {e}")
    
    def save_profile(self):
        # Ask for profile name if not the default
        profile_name = self.profile_var.get()
        if profile_name == "Default":
            profile_name = simpledialog.askstring(self.translator.get_text('save_profile'), 
                                                 self.translator.get_text('profile_name_prompt'))
            if not profile_name:
                return
        
        # Save the current positions to the profile
        self.profiles[profile_name] = self.positions.copy()
        self.current_profile = profile_name
        
        # Update the profile dropdown
        self.profile_combo['values'] = tuple(self.profiles.keys())
        self.profile_var.set(profile_name)
        
        # Save profiles to file
        try:
            # Prepare data for JSON serialization (convert tuples to lists)
            profiles_data = {}
            for name, positions in self.profiles.items():
                # Convert tuples to lists for JSON serialization
                profiles_data[name] = [list(pos) for pos in positions]
            
            # Save to file
            profile_file = os.path.join(self.profiles_dir, "saved_profiles.json")
            with open(profile_file, 'w') as f:
                json.dump(profiles_data, f, indent=2)
                
            self.status_var.set(self.translator.get_text('profile_saved', profile_name))
        except Exception as e:
            messagebox.showerror(self.translator.get_text('error'), 
                                self.translator.get_text('profile_save_error', str(e)))
    
    def load_profile(self):
        profile_name = self.profile_var.get()
        if profile_name in self.profiles:
            self.positions = self.profiles[profile_name].copy()
            self.update_position_display()
            self.status_var.set(self.translator.get_text('profile_loaded', profile_name))
        else:
            messagebox.showerror(self.translator.get_text('error'), 
                               self.translator.get_text('profile_not_found', profile_name))
    
    def update_profile_dropdown(self):
        """Update the profile dropdown with current profiles"""
        if hasattr(self, 'profile_combo'):
            self.profile_combo['values'] = tuple(self.profiles.keys())
            if self.current_profile in self.profiles:
                self.profile_var.set(self.current_profile)
    
    def on_close(self):
        self.running = False
        if self.click_thread and self.click_thread.is_alive():
            self.click_thread.join(1)
        self.root.destroy()

if __name__ == "__main__":
    pyautogui.FAILSAFE = True  # Move mouse to corner to stop program
    app = AutoClicker()
