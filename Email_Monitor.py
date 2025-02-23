import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from datetime import datetime
import sys
from PIL import Image, ImageTk  # For handling and resizing images

# Gmail API Scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class EmailMonitor:
    def __init__(self):
        self.service = None
        self.credential_path = "token.pickle"
        self.credentials_json = "credentials.json"  # Update this if your file has a different name

        try:
            # Setup GUI
            self.root = tk.Tk()
            self.root.title("Email Monitor")
            self.root.geometry("800x600")
            self.root.configure(bg='#2c3e50')

            # Set the app icon (resized to 32x32 or 64x64 for Windows)
            try:
                # Check if running as executable or script
                if getattr(sys, 'frozen', False):
                    # Running as executable, look in the data directory
                    base_path = sys._MEIPASS
                else:
                    # Running as script, look in the current directory
                    base_path = os.path.dirname(os.path.abspath(__file__))

                icon_path = os.path.join(base_path, "acenelog.png")
                if os.path.exists(icon_path):
                    icon_image = Image.open(icon_path)
                    icon_image = icon_image.resize((64, 64), Image.LANCZOS)  # Resize for icon
                    photo = ImageTk.PhotoImage(icon_image)
                    self.root.iconphoto(True, photo)
                else:
                    raise FileNotFoundError(f"Icon file not found at {icon_path}")
            except Exception as e:
                messagebox.showwarning("Icon Error", f"Failed to set app icon: {str(e)}")

            self.setup_gui()
            self.authenticate_gmail()

        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize the application: {str(e)}")
            self.root.destroy()
            sys.exit(1)

    def authenticate_gmail(self):
        try:
            creds = None
            if os.path.exists(self.credential_path):
                with open(self.credential_path, 'rb') as token:
                    creds = pickle.load(token)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_json, SCOPES)
                    creds = flow.run_local_server(port=0)

                with open(self.credential_path, 'wb') as token:
                    pickle.dump(creds, token)

            self.service = build('gmail', 'v1', credentials=creds)

        except Exception as e:
            messagebox.showerror("Authentication Error", f"Failed to authenticate with Gmail: {str(e)}")

    def setup_gui(self):
        try:
            # Define tag colors for alternating rows
            self.tag_colors = {'odd': '#34495e', 'even': '#2c3e50'}

            # Logo display at the top
            try:
                # Check if running as executable or script
                if getattr(sys, 'frozen', False):
                    base_path = sys._MEIPASS
                else:
                    base_path = os.path.dirname(os.path.abspath(__file__))

                logo_path = os.path.join(base_path, "acenelog.png")
                if os.path.exists(logo_path):
                    logo_image = Image.open(logo_path)
                    logo_image = logo_image.resize((100, 100), Image.LANCZOS)  # Resize to 100x100 pixels
                    photo = ImageTk.PhotoImage(logo_image)
                    logo_label = tk.Label(self.root, image=photo, bg='#2c3e50')
                    logo_label.image = photo  # Keep a reference to avoid garbage collection
                    logo_label.pack(pady=20)
                else:
                    raise FileNotFoundError(f"Logo file not found at {logo_path}")
            except Exception as e:
                messagebox.showwarning("Logo Error", f"Failed to display logo: {str(e)}")

            # Email input with padding and styling
            tk.Label(self.root, text="Enter Email Address:", bg='#2c3e50', foreground='white',
                     font=('Helvetica', 14)).pack(pady=10)

            self.email_entry = tk.Entry(self.root, width=40, font=('Helvetica', 12), relief='flat', bd=2, bg='white',
                                        highlightthickness=1, highlightbackground='#3498db')
            self.email_entry.pack(pady=10, padx=20, ipady=5)  # Padding

            # Display button with padding and styling
            self.display_button = tk.Button(self.root, text="Display Emails", command=self.display_emails, bg='#3498db',
                                            foreground='white', font=('Helvetica', 10), relief='flat', bd=2)
            self.display_button.pack(pady=10, padx=20, ipady=5)  # Padding

            # Email list with dividers, padding (no scrollbar, height fixed to 10 for 10 emails)
            self.email_list_frame = tk.Frame(self.root, bg='#2c3e50')
            self.email_list_frame.pack(pady=20, padx=20, fill="both", expand=True)  # Increased padding

            self.email_list = ttk.Treeview(self.email_list_frame, columns=("Date", "Subject", "Preview"),
                                           show="headings", height=10)
            self.email_list.heading("Date", text="Date")
            self.email_list.heading("Subject", text="Subject")
            self.email_list.heading("Preview", text="Preview")
            self.email_list.column("Date", width=100, anchor='w')  # Constrained width
            self.email_list.column("Subject", width=200, anchor='w')  # Constrained width
            self.email_list.column("Preview", width=300, anchor='w')  # Constrained width
            self.email_list.pack(side="left", fill="both", expand=True, padx=10, pady=10)  # Increased padding

            # Add dividers (grid lines) to Treeview
            self.email_list.configure(style='Treeview')
            self.email_list.tag_configure('odd', background=self.tag_colors['odd'], foreground='white')
            self.email_list.tag_configure('even', background=self.tag_colors['even'], foreground='white')

            # Menu bar
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)

            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=file_menu)
            file_menu.add_command(label="Exit", command=self.exit_program)

            about_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="About", menu=about_menu)
            about_menu.add_command(label="About Email Monitor", command=self.show_about)

            settings_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Settings", menu=settings_menu)
            settings_menu.add_command(label="Page Settings", command=self.show_settings)

        except Exception as e:
            messagebox.showerror("GUI Setup Error", f"Failed to set up the GUI: {str(e)}")

    def display_emails(self):
        try:
            target_email = self.email_entry.get().strip()
            if not target_email:
                messagebox.showwarning("Warning", "Please enter an email address.")
                return

            # Show progress bar while loading
            progress = ttk.Progressbar(self.root, length=300, mode='indeterminate')
            progress.pack(pady=10)
            progress.start()

            self.list_emails(f"from:{target_email}")
            messagebox.showinfo("Displayed", f"Displaying emails from {target_email}")

            progress.stop()
            progress.destroy()

        except Exception as e:
            messagebox.showerror("Display Error", f"Failed to display emails: {str(e)}")

    def list_emails(self, query):
        try:
            results = self.service.users().messages().list(userId='me', q=query).execute()
            messages = results.get('messages', [])

            for item in self.email_list.get_children():
                self.email_list.delete(item)

            # Limit to 10 most recent messages (newest first)
            messages = messages[-10:] if len(messages) > 10 else messages  # Get last 10 (newest) if available
            for i, msg in enumerate(reversed(messages)):  # Reverse to show newest first
                msg_data = self.service.users().messages().get(userId='me', id=msg['id']).execute()
                headers = msg_data['payload']['headers']
                date = subject = preview = "N/A"

                for header in headers:
                    if header['name'] == 'Date':
                        # Handle date with "(UTC)" or other variations
                        date_str = header['value'].rsplit('(', 1)[0].strip()  # Remove "(UTC)" or similar
                        try:
                            date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
                            date_str = date.strftime('%Y-%m-%d %I:%M %p')  # 12-hour format: YYYY-MM-DD HH:MM AM/PM
                        except ValueError:
                            # Fallback for simpler date formats (e.g., without timezone)
                            try:
                                date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S')
                                date_str = date.strftime('%Y-%m-%d %I:%M %p')
                            except ValueError:
                                date_str = "Invalid Date"
                    elif header['name'] == 'Subject':
                        subject = header['value']

                preview = msg_data.get('snippet', "No preview")

                # Display only the subject (no sender)
                subject_display = subject

                # Insert with alternating row colors and limit text to fit
                tag = 'odd' if i % 2 == 0 else 'even'
                self.email_list.insert("", "end", values=(
                date_str, subject_display, preview[:100] + "..." if len(preview) > 100 else preview), tags=(tag,))
                # Configure text wrapping and limit to view
                self.email_list.column("Date", width=100, anchor='w')
                self.email_list.column("Subject", width=200, anchor='w')
                self.email_list.column("Preview", width=300, anchor='w')
                self.email_list.tag_configure(tag, background=self.tag_colors[tag], foreground='white')

        except Exception as e:
            messagebox.showerror("Email Listing Error", f"Failed to list emails: {str(e)}")

    def exit_program(self):
        try:
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Exit Error", f"Failed to exit the program: {str(e)}")

    def show_about(self):
        try:
            about_window = Toplevel(self.root)
            about_window.title("About Email Monitor")
            about_window.geometry("400x300")
            about_window.configure(bg='#2c3e50')
            about_window.transient(self.root)  # Keep on top of main window
            about_window.grab_set()  # Make modal

            # Main frame for centering
            main_frame = tk.Frame(about_window, bg='#2c3e50')
            main_frame.pack(expand=True, fill="both")

            # Logo (centered)
            try:
                # Check if running as executable or script
                if getattr(sys, 'frozen', False):
                    base_path = sys._MEIPASS
                else:
                    base_path = os.path.dirname(os.path.abspath(__file__))

                logo_path = os.path.join(base_path, "acenelog.png")
                if os.path.exists(logo_path):
                    logo_image = Image.open(logo_path)
                    logo_image = logo_image.resize((100, 100), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(logo_image)
                    logo_label = tk.Label(main_frame, image=photo, bg='#2c3e50')
                    logo_label.image = photo  # Keep reference
                    logo_label.pack(pady=10)
                else:
                    raise FileNotFoundError(f"Logo file not found at {logo_path}")
            except Exception as e:
                messagebox.showwarning("Logo Error", f"Failed to display logo: {str(e)}")

            # Program details (centered)
            details = """
            Email Monitor
            Version 1.0

            A simple application to display emails from a specified address.
            Owner: Opeyemi Adedotun
            Company: Acenet Technology
            """
            detail_label = tk.Label(main_frame, text=details, bg='#2c3e50', foreground='white', font=('Helvetica', 12),
                                    justify='center')
            detail_label.pack(pady=20)

            # Close button (centered)
            close_button = tk.Button(main_frame, text="Close", command=about_window.destroy, bg='#3498db',
                                     foreground='white', font=('Helvetica', 10))
            close_button.pack(pady=10)

        except Exception as e:
            messagebox.showerror("About Error", f"Failed to show about information: {str(e)}")

    def show_settings(self):
        try:
            settings_window = Toplevel(self.root)
            settings_window.title("Settings")
            settings_window.geometry("400x200")
            settings_window.configure(bg='#2c3e50')
            settings_window.transient(self.root)  # Keep on top of main window
            settings_window.grab_set()  # Make modal

            # Theme toggle (example setting)
            tk.Label(settings_window, text="Theme Settings", bg='#2c3e50', foreground='white',
                     font=('Helvetica', 14)).pack(pady=10)

            self.theme_var = tk.BooleanVar(value=True)  # Default to dark theme
            tk.Checkbutton(settings_window, text="Use Dark Theme", variable=self.theme_var, command=self.toggle_theme,
                           bg='#2c3e50', foreground='white', font=('Helvetica', 12), selectcolor='#2c3e50').pack(
                pady=10)

            # Close button
            tk.Button(settings_window, text="Close", command=settings_window.destroy, bg='#3498db', foreground='white',
                      font=('Helvetica', 10)).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Settings Error", f"Failed to show settings: {str(e)}")

    def toggle_theme(self):
        try:
            if self.theme_var.get():
                # Dark theme
                self.root.configure(bg='#2c3e50')
                for widget in self.root.winfo_children():
                    if isinstance(widget, tk.Label) or isinstance(widget, tk.Frame):
                        widget.config(bg='#2c3e50', foreground='white')
                    elif isinstance(widget, tk.Entry):
                        widget.config(bg='white', foreground='black', highlightbackground='#3498db')
                    elif isinstance(widget, tk.Button):
                        widget.config(bg='#3498db', foreground='white')
                self.email_list.configure(background='#34495e', foreground='white')
                self.email_list.tag_configure('odd', background=self.tag_colors['odd'])
                self.email_list.tag_configure('even', background=self.tag_colors['even'])
            else:
                # Light theme
                self.root.configure(bg='white')
                for widget in self.root.winfo_children():
                    if isinstance(widget, tk.Label) or isinstance(widget, tk.Frame):
                        widget.config(bg='white', foreground='black')
                    elif isinstance(widget, tk.Entry):
                        widget.config(bg='white', foreground='black', highlightbackground='#3498db')
                    elif isinstance(widget, tk.Button):
                        widget.config(bg='#0078d7', foreground='white')
                self.email_list.configure(background='white', foreground='black')
                self.email_list.tag_configure('odd', background='white')
                self.email_list.tag_configure('even', background='#f0f0f0')
        except Exception as e:
            messagebox.showerror("Theme Error", f"Failed to toggle theme: {str(e)}")

    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Runtime Error", f"Application crashed: {str(e)}")


def main():
    try:
        app = EmailMonitor()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()