"""
Huggingface Dataset Uploader

Several different choices to upload datasets to huggingface

Created by Christopher (Egrigor86)
"""
__version__ = "0.1.0"

import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import datasets
from huggingface_hub import HfApi

class HFUploaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HF Dataset Uploader")

        self.dataset_name = tk.StringVar()
        self.choice = tk.StringVar(value="1")
        self.use_system_prompt = tk.BooleanVar()
        self.system_prompt = tk.StringVar()
        self.log_output = tk.StringVar()

        # GUI Layout
        tk.Label(root, text="Dataset Name:").grid(row=0, column=0, sticky="w")
        tk.Entry(root, textvariable=self.dataset_name, width=40).grid(row=0, column=1, pady=5, columnspan=2)

        tk.Label(root, text="Upload Type:").grid(row=1, column=0, sticky="w")
        choices = [
            ("All JSON fields (structured)", "1"),
            ("Only 'fact' or 'answer' (text-based)", "2"),
            ("Q&A only", "3"),
            ("Q&A with tags + optional system prompt", "4"),
            ("Text files as dataset", "5"),
        ]
        for i, (label, val) in enumerate(choices, start=2):
            tk.Radiobutton(root, text=label, variable=self.choice, value=val, command=self.toggle_prompt).grid(row=i, column=1, sticky="w")

        self.system_prompt_check = tk.Checkbutton(root, text="Include System Prompt", variable=self.use_system_prompt, command=self.toggle_prompt_entry)
        self.system_prompt_check.grid(row=7, column=1, sticky="w")

        self.system_prompt_entry = tk.Entry(root, textvariable=self.system_prompt, width=40, state="disabled")
        self.system_prompt_entry.grid(row=8, column=1, pady=5)

        tk.Button(root, text="Upload Dataset", command=self.upload_dataset).grid(row=9, column=1, pady=10)

        self.log = tk.Label(root, textvariable=self.log_output, fg="blue", wraplength=400, justify="left")
        self.log.grid(row=10, column=0, columnspan=3, pady=10)

    def toggle_prompt(self):
        if self.choice.get() == "4":
            self.system_prompt_check.configure(state="normal")
        else:
            self.system_prompt_check.configure(state="disabled")
            self.system_prompt_entry.configure(state="disabled")
            self.use_system_prompt.set(False)
            self.system_prompt.set("")

    def toggle_prompt_entry(self):
        if self.use_system_prompt.get():
            self.system_prompt_entry.configure(state="normal")
        else:
            self.system_prompt_entry.configure(state="disabled")
            self.system_prompt.set("")

    def process_text_files(self):
        data_entries = []
        for filename in os.listdir():
            if filename.endswith('.txt'):
                with open(filename, 'r', encoding='utf-8') as f:
                    data_entries.append({"content": f.read()})
        return data_entries

    def process_json_files(self):
        full, fact, qa, ans, tagged = [], [], [], [], []
        max_id = 0
        for filename in os.listdir():
            if filename.endswith('.json'):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        try:
                            data = json.loads(content)
                            if not isinstance(data, list):
                                raise ValueError()
                        except:
                            data = json.loads(f"[{content.replace('}\n{', '}, {')}]")

                        for entry in data:
                            if "id" in entry and entry["id"] > max_id:
                                max_id = entry["id"]
                            if "fact" in entry:
                                full.append(entry)
                                fact.append({"content": entry["fact"]})
                            elif "question" in entry and "answer" in entry:
                                qa.append(entry)
                                ans.append({"content": entry["answer"]})
                                tagged_entry = {"prompt": entry["question"], "response": entry["answer"]}
                                if "tags" in entry:
                                    tagged_entry["tags"] = entry["tags"]
                                if "system" in entry:
                                    tagged_entry["system"] = entry["system"]
                                tagged.append(tagged_entry)
                except:
                    self.log_output.set(f"Skipping bad JSON file: {filename}")
        return full, fact, qa, ans, tagged

    def upload_dataset(self):
        try:
            access_token = os.getenv("HF_TOKEN")
            if not access_token:
                messagebox.showerror("Error", "HF_TOKEN not set in environment variables.")
                return

            name = self.dataset_name.get().strip()
            if not name:
                messagebox.showwarning("Warning", "Dataset name cannot be empty.")
                return

            text_data = self.process_text_files()
            full, fact, qa, ans, tagged = self.process_json_files()

            dataset = None
            if self.choice.get() == "1":
                dataset = datasets.Dataset.from_list(full + qa)
            elif self.choice.get() == "2":
                dataset = datasets.Dataset.from_list(fact + ans)
            elif self.choice.get() == "3":
                dataset = datasets.Dataset.from_list(qa)
            elif self.choice.get() == "4":
                if self.use_system_prompt.get():
                    for entry in tagged:
                        if "system" not in entry:
                            entry["system"] = self.system_prompt.get()
                dataset = datasets.Dataset.from_list(tagged)
            elif self.choice.get() == "5":
                dataset = datasets.Dataset.from_list(text_data)
            else:
                messagebox.showerror("Error", "Invalid choice.")
                return

            dataset.save_to_disk(f"./{name}")
            HfApi().create_repo(repo_id=name, token=access_token, repo_type="dataset", exist_ok=True)
            dataset.push_to_hub(name, token=access_token)

            self.log_output.set(f"Dataset '{name}' uploaded successfully.")
        except Exception as e:
            self.log_output.set(f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = HFUploaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

