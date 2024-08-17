import os
import sys
from tkinter.filedialog import askopenfilename

import customtkinter as ctk

from executor import Executor, ExecutorThread
from ui.CTkMenuBar import CTkTitleMenu, CustomDropdownMenu
from ui.Extras.ctktable import CTkTable
from utils import get_available_package_list

# Set the app theme, irrespective of system theme
ctk.set_appearance_mode("Dark")

try:
    import pyi_splash

    pyi_splash.close()
except:
    pass


class ConsoleLogger:
    """Write captured stdout and stderr into console widget"""

    def __init__(self, textbox):  # pass reference to text widget
        self.consolebox = textbox  # keep ref

    def write(self, text):
        self.consolebox.configure(state="normal")  # make field editable
        self.consolebox.update_idletasks()  # real-time update ! important
        self.consolebox.insert("end", text)  # write text to textbox
        self.consolebox.see("end")  # scroll to end
        self.consolebox.configure(state="disabled")  # make field readonly

    def flush(self):  # needed for file like object
        pass


class ExecutorGUI:
    def __init__(self):

        try:
            base_path = sys._MEIPASS
            os.chdir(base_path)
        except Exception:
            base_path = os.path.abspath(".")

        file_path = os.path.join(base_path, "VERSION")
        self.app_icon_path = os.path.join(base_path, "icon\logo_high.ico")
        try:
            with open(file_path) as file:
                self.version = file.read()
        except:
            self.version = "1.0.0"

        APP_TITLE = "PyScript Engine"
        self.thread = None

        console_bg = "#171717"
        bg_color = "#212121"
        light_dark = "#2a2a2a"
        light_text_color = "#f2f2f2"

        self.window = ctk.CTk()
        self.window.title(APP_TITLE)
        self.window.resizable(0, 0) # Not resizeable

        self.window.rowconfigure(0, minsize=10, weight=1)
        self.window.columnconfigure(0, minsize=450, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        self.window.iconbitmap(default=self.app_icon_path)
        self.window.config(bg=bg_color)

        # ***********************  Menu  **********************
        menu = CTkTitleMenu(self.window)

        FileMenu = menu.add_cascade("File")
        FileMenuDropDown = CustomDropdownMenu(widget=FileMenu)
        FileMenuDropDown.add_option(option="Exit", command=self.window.quit)

        MoreMenu = menu.add_cascade("Help")
        MoreMenuDropDown = CustomDropdownMenu(widget=MoreMenu)
        MoreMenuDropDown.add_option(option="Packages", command=self.packages_window)
        MoreMenuDropDown.add_option(option="About", command=self.about_window)
        self.window.config(menu=menu)

        # ******************  Window Frames  ******************
        input_frame = ctk.CTkFrame(self.window, fg_color=light_dark)
        console_frame = ctk.CTkFrame(self.window, fg_color=bg_color)

        input_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        console_frame.grid(row=0, column=1, sticky="n")

        # ***********************   GUI  ***********************
        # *********************  User Input  *******************
        python_input_label = ctk.CTkLabel(
            input_frame,
            text="Python Script",
            font=(..., 14, "bold"),
            text_color=light_text_color,
        )
        self.python_input_filename_label = ctk.CTkEntry(
            input_frame,
            width=250,
            state="normal",
            placeholder_text="..._ngx\code\example.py",
        )
        self.browse_file_btn = ctk.CTkButton(
            input_frame, width=80, text="Browse...", command=self.open_python_file
        )

        self.btn_exec_script = ctk.CTkButton(
            input_frame,
            text="Run Script",
            state="disabled",
            command=self.thread_exec_script,  # directly executing in thread helps in sys path update
            fg_color="#164523",
            hover_color="#1c572c",
            height=50,
        )
        self.btn_cancel = ctk.CTkButton(
            input_frame,
            text="Cancel",
            state="disabled",
            command=self.kill_thread_execution,  # directly executing in thread helps in sys path update
            fg_color="#3D506B",
            hover_color="#2E3E55",
            height=50,
        )

        python_input_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        self.python_input_filename_label.grid(
            row=1, column=0, sticky="ew", padx=(20, 3), pady=0, columnspan=2
        )
        self.browse_file_btn.grid(row=1, column=3, sticky="ew", padx=(3, 20), pady=10)
        self.btn_exec_script.grid(row=2, sticky="nsew", padx=20, pady=10, columnspan=4)
        self.btn_cancel.grid(row=3, sticky="nsew", padx=20, pady=10, columnspan=4)

        # ********************  Console  *********************

        console_label = ctk.CTkLabel(
            console_frame,
            text="Console",
            font=(..., 12, "normal"),
            text_color=light_text_color,
        )
        self.console_window = ctk.CTkTextbox(
            console_frame,
            height=700,
            width=1000,
            wrap="word",
            fg_color=console_bg,
            text_color=light_text_color,
        )
        clear_console_btn = ctk.CTkButton(
            console_frame,
            width=60,
            height=20,
            corner_radius=5,
            text_color="#bfbfbf",
            text="Clear All",
            border_width=1,
            command=self.clear_console,
            fg_color="transparent",
            hover_color="#373737",
        )
        copy_to_clipboard_btn = ctk.CTkButton(
            console_frame,
            width=80,
            text="Copy to clipboard",
            command=self.copy_to_clipboard,
            fg_color="#474747",
            hover_color="#373737",
        )

        console_label.grid(row=1, column=0, padx=(2, 0), pady=5, sticky="w")
        clear_console_btn.grid(row=1, column=1, sticky="e", pady=(5, 0), padx=12)
        self.console_window.grid(
            row=2, column=0, sticky="n", pady=(0, 0), padx=(0, 8), columnspan=2
        )
        copy_to_clipboard_btn.grid(row=3, column=1, sticky="se", pady=10, padx=10)

        self.window.mainloop()

    def packages_window(self):
        packages_win = ctk.CTkToplevel(self.window)
        # Because CTkToplevel currently is bugged on windows
        # and doesn't check if a user specified icon is set
        # we need to set the icon again after 200ms
        # https://github.com/TomSchimansky/CustomTkinter/issues/1163
        packages_win.after(200, lambda: packages_win.iconbitmap(self.app_icon_path))
        packages_win.title("Installed Packages")
        packages_win.resizable(0, 0)
        packages_win.attributes("-toolwindow", True)
        packages_win.grab_set()
        packages_frame = ctk.CTkScrollableFrame(packages_win, width=350, height=500)
        packages_frame.grid(row=0, column=0, sticky="ns")

        package_list = get_available_package_list()
        CTkTable(master=packages_frame, values=package_list).grid(
            row=0, column=0, padx=20, pady=20, sticky="ns"
        )

    def about_window(self):
        about_win = ctk.CTkToplevel(self.window)
        about_win.after(200, lambda: about_win.iconbitmap(self.app_icon_path))
        about_win.title("About")
        about_win.resizable(0, 0)
        about_win.attributes("-toolwindow", True)
        about_win.grab_set()
        about_frame = ctk.CTkFrame(about_win)
        about_frame.grid(row=0, column=0, sticky="ns")
        about_info = {
            "App Version": self.version,
            "Author": "Nandan Manjunatha",
            "Python": f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}",
            "Build": "x86 64-bit",
            "Credits": "CustomTkinter, Akascape",
        }
        about_info_str = "\n".join(
            [f"{key}: {value}" for key, value in about_info.items()]
        )
        ctk.CTkLabel(about_frame, text=about_info_str, justify="left").grid(
            row=0, column=0, padx=20, pady=20, sticky="e"
        )

    def redirect_logging(self):
        "Route stdout and stderr into console widget"
        logger = ConsoleLogger(self.console_window)
        sys.stdout = logger
        sys.stderr = logger

    def thread_exec_script(self):
        """Run in separate thread for unblocking GUI thread"""
        self.thread = ExecutorThread(
            target=self.begin_execution,
            args=[self.python_input_filename_label.get()],
            daemon=True,
        )
        self.thread.start()

    def kill_thread_execution(self):
        "Interrupt thread by raising SystemExit exception"
        self.disable_cancel_button()

        if self.thread:
            self.thread.raise_exception()

        self.enable_input_buttons()

    def begin_execution(self, file_path: str):
        """Start execution process"""
        self.disable_input_buttons()
        self.enable_cancel_button()

        executor = Executor()
        executor.execute_python_script(file_path)

        self.enable_input_buttons()
        self.disable_cancel_button()

    def enable_input_buttons(self):
        self.btn_exec_script.update()
        self.btn_exec_script.configure(state="normal")
        self.browse_file_btn.update()
        self.browse_file_btn.configure(state="normal")

    def disable_input_buttons(self):
        self.browse_file_btn.configure(state="disabled")
        self.browse_file_btn.update()

        self.btn_exec_script.configure(state="disabled")
        self.btn_exec_script.update()

    def enable_cancel_button(self):
        self.btn_cancel.update()
        self.btn_cancel.configure(state="normal")

    def disable_cancel_button(self):
        self.btn_cancel.configure(state="disabled")
        self.btn_cancel.update()

    def open_python_file(self):
        """Browser python file"""
        self.redirect_logging()
        filepath = askopenfilename(filetypes=[("Python Files", "*.py")])
        if not filepath:
            return
        self.python_input_filename_label.insert(0, filepath)
        self.python_input_filename_label.xview(len(filepath))
        self.btn_exec_script.configure(state="normal", fg_color="#0f732b")

    def copy_to_clipboard(self):
        self.window.clipboard_clear()
        self.window.clipboard_append(self.console_window.get("0.0", "end"))

    def clear_console(self):
        self.console_window.configure(state="normal")  # make field editable
        self.console_window.update_idletasks()  # real-time update ! important
        self.console_window.delete("0.0", "end")
        self.console_window.configure(state="disabled")  # make field readonly
