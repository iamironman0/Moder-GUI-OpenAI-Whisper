from tkinter import filedialog, messagebox
import threading
import customtkinter as ctk
import whisper
import torch

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.main_window()
        self.file_path = None

    def main_window(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("Audio Transcriber")
        self.geometry("1100x580")
        self.minsize(1100,580)
        self.maxsize(1100,580)
        self.protocol("WM_DELETE_WINDOW", self.close_app)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Audio Transcriber", font=("", 28, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.model_option = ctk.CTkOptionMenu(self.sidebar_frame, values=["Tiny", "Base", "Small", "Medium", "Large"])
        self.model_option.grid(row=1, column=0, padx=20, pady=10)

        self.language_option = ctk.CTkOptionMenu(self.sidebar_frame, values=["Arabic", "English"])
        self.language_option.grid(row=2, column=0, padx=20, pady=10)

        self.task_option = ctk.CTkOptionMenu(self.sidebar_frame, values=["Transcribe", "Translate"])
        self.task_option.grid(row=3, column=0, padx=20, pady=10)

        self.open_file_button = ctk.CTkButton(self.sidebar_frame, text="Choose File", command=self.open_file, font=("", 12, "bold"))
        self.open_file_button.grid(row=4, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("System")

        self.textbox = ctk.CTkTextbox(self, width=250, wrap="word")
        self.textbox.grid(row=0, column=1, rowspan=2, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.textbox.insert("0.0", "Ouput:\n\n")
        self.textbox.configure(state="disabled")

        self.message_label = ctk.CTkLabel(self, text="")
        self.message_label.grid(row=2, column=1, padx=0, pady=0)

        self.start_button = ctk.CTkButton(self, text="Start", command=self.run_task, font=("", 14, "bold"), width=256)
        self.start_button.grid(row=3, column=1, padx=20, pady=20)
        self.start_button.configure(state="disabled")

        self.export_button = ctk.CTkButton(self, text="Save Text", command=self.export_text, font=("", 14, "bold"), width=256)
        self.export_button.grid(row=3, column=2, padx=20, pady=20)

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def export_text(self):
        text = self.textbox.get("0.0", "end")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile="output.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)

        messagebox.showinfo("Export Successful", f"The file has been saved to {file_path}")

    def close_app(self):
        self.destroy()
        self.quit()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.flac;*.wav")], title="Select An Audio File")
        if file_path:
            self.start_button.configure(state="normal")
            self.message_label.configure(text=f"Selected File: {file_path}")
            self.file_path = file_path
        else:
            self.start_button.configure(state="disabled")
            self.message_label.configure(text="Note: No File Selected, Click (Choose File) Button to Select a File.")

    def run_transcribe(self):
        model = self.model_option.get().lower()
        audio = self.file_path
        language = self.language_option.get()
        task = self.task_option.get()

        try:
            self.start_button.configure(state="disabled")
            self.export_button.configure(state="disabled")
            self.open_file_button.configure(state="disabled")
            self.message_label.configure(text=f"Transcribing Started, Please Wait...\nModel: {model}\nLanguage: {language}\nTask: {task}")
            model = whisper.load_model(model)

            text = model.transcribe(audio, language=language, task=task, fp16=torch.cuda.is_available())
            format_text = text["text"].strip().capitalize()

            self.export_button.configure(state="normal")
            self.open_file_button.configure(state="normal")
            self.textbox.configure(state="normal")
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", format_text)
            self.textbox.configure(state="disabled")

            self.message_label.configure(text="Transcribing Completed.")

            self.start_button.configure(state="normal")

        except Exception:
            error_message = "An error has occurred:\nThe program encountered an unexpected error and was unable to complete the requested action. Please try again."
            self.message_label.configure(text=error_message)
            
    def run_task(self):
        threading.Thread(target=self.run_transcribe).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()
