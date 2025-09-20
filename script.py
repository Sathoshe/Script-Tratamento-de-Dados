import tkinter as tk
from tkinter import filedialog, messagebox
import re

def process_file():
    input_file_path = entry_input.get()
    output_file_path = entry_output.get()
    separator = entry_separator.get()

    if not input_file_path or not output_file_path:
        messagebox.showerror("Erro", "Por favor, selecione os arquivos de entrada e saída.")
        return

    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Verifica se a linha já tem um separador
                if separator in line or '|' in line or ',' in line:
                    outfile.write(line + '\n')
                    continue

                # Procura por um padrão "email senha: password"
                match = re.search(r'([\w\.-]+@[\w\.-]+)\s*senha:\s*(.*)', line, re.IGNORECASE)
                if match:
                    email = match.group(1).strip()
                    password = match.group(2).strip()
                    outfile.write(f"{email}{separator}{password}\n")
                    continue

                # Se não encontrar o padrão acima, tenta separar por espaços
                parts = line.split()
                if len(parts) >= 2:
                    email = parts[0]
                    # A senha pode ser o resto da linha se tiver mais de duas partes
                    password = " ".join(parts[1:])
                    outfile.write(f"{email}{separator}{password}\n")
                else:
                    # Se não conseguir processar, salva a linha original no final do arquivo de saída com um aviso
                    outfile.write(f"### Linha não processada: {line}\n")
        
        messagebox.showinfo("Sucesso!", f"Arquivo processado com sucesso! Salvo em: {output_file_path}")

    except FileNotFoundError:
        messagebox.showerror("Erro", "O arquivo de entrada não foi encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def browse_input_file():
    filename = filedialog.askopenfilename(
        title="Selecione o arquivo de entrada",
        filetypes=(("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*"))
    )
    if filename:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, filename)

def browse_output_file():
    filename = filedialog.asksaveasfilename(
        title="Salvar arquivo como",
        defaultextension=".txt",
        filetypes=(("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*"))
    )
    if filename:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, filename)

# Configuração da janela principal
root = tk.Tk()
root.title("Processador de Dados de E-mail/Senha")
root.geometry("600x250")
root.resizable(False, False)

# Paleta de cores para um visual mais agradável
bg_color = "#f0f0f0"
primary_color = "#4CAF50" # Verde
button_color = "#e0e0e0"
entry_bg = "white"

root.config(bg=bg_color)

# Frame principal com padding
main_frame = tk.Frame(root, padx=20, pady=20, bg=bg_color)
main_frame.pack(expand=True, fill="both")

# Título
title_label = tk.Label(main_frame, text="Formatador de E-mails e Senhas", font=("Helvetica", 16, "bold"), bg=bg_color)
title_label.pack(pady=(0, 15))

# Opção de arquivo de entrada
frame_input = tk.Frame(main_frame, bg=bg_color)
frame_input.pack(fill="x", pady=5)
label_input = tk.Label(frame_input, text="Arquivo de Entrada:", width=18, anchor="w", bg=bg_color)
label_input.pack(side="left")
entry_input = tk.Entry(frame_input, width=50, bg=entry_bg)
entry_input.pack(side="left", fill="x", expand=True)
button_input = tk.Button(frame_input, text="Procurar...", command=browse_input_file, bg=button_color)
button_input.pack(side="left", padx=(5, 0))

# Opção de arquivo de saída
frame_output = tk.Frame(main_frame, bg=bg_color)
frame_output.pack(fill="x", pady=5)
label_output = tk.Label(frame_output, text="Arquivo de Saída:", width=18, anchor="w", bg=bg_color)
label_output.pack(side="left")
entry_output = tk.Entry(frame_output, width=50, bg=entry_bg)
entry_output.pack(side="left", fill="x", expand=True)
button_output = tk.Button(frame_output, text="Salvar Como...", command=browse_output_file, bg=button_color)
button_output.pack(side="left", padx=(5, 0))

# Opção de separador
frame_separator = tk.Frame(main_frame, bg=bg_color)
frame_separator.pack(fill="x", pady=5)
label_separator = tk.Label(frame_separator, text="Separador:", width=18, anchor="w", bg=bg_color)
label_separator.pack(side="left")
entry_separator = tk.Entry(frame_separator, width=10, bg=entry_bg)
entry_separator.insert(0, ",")
entry_separator.pack(side="left")

# Botão de processar
button_process = tk.Button(main_frame, text="Processar Arquivo", command=process_file,
                           bg=primary_color, fg="white", font=("Helvetica", 10, "bold"),
                           relief="flat", pady=10)
button_process.pack(pady=20, fill="x")

# Inicia a interface gráfica
root.mainloop()