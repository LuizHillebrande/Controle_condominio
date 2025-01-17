import customtkinter as ctk
import pandas as pd
import os
from datetime import datetime

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# Criando a janela principal
root = ctk.CTk()
root.title("Gerenciador Financeiro")
root.geometry("600x400")

# Categorias de despesas e receitas
categorias_receitas = ["ALUGUÉIS", "APLICAÇÕES FINANCEIRAS"]  # Agora são receitas
categorias_despesas = [
    "SERVIÇOS", "TARIFAS", "VIAGENS", "MOBILIÁRIO", "EQUIPAMENTOS", 
    "PROJETOS", "CONDOMÍNIO", "CONTABILIDADE", "DIVERSAS", "ESCRITÓRIO", 
    "MÃO DE OBRA", "MATERIAIS", "RETIRADAS E RETIRADAS EXTRAS", "FGTS", 
    "GPS", "PIS E COFINS", "CONTRIBUIÇÃO SOCIAL E IMPOSTO DE RENDA"
]

# Variável global para armazenar o prédio selecionado
prédio_selecionado = ""

# Função para salvar os dados na planilha Excel
def salvar_em_excel(tipo, categoria, valor, inquilino=None, observacoes=None):
    global prédio_selecionado
    if not prédio_selecionado:
        return
    
    # Criar nome do arquivo Excel
    mes_atual = datetime.now().strftime("%Y-%m")
    nome_arquivo = f"{prédio_selecionado}_{mes_atual}.xlsx"
    
    # Adicionar as observações e inquilino, se houver
    novo_dado = pd.DataFrame([[tipo, categoria, float(valor), inquilino, observacoes, datetime.now().strftime("%d/%m/%Y")]], 
                             columns=["Tipo", "Categoria", "Valor", "Inquilino", "Observações", "Data"])

    # Verificar se o arquivo já existe
    if os.path.exists(nome_arquivo):
        df_existente = pd.read_excel(nome_arquivo)
        df_final = pd.concat([df_existente, novo_dado], ignore_index=True)
    else:
        df_final = novo_dado

    # Salvar no Excel
    df_final.to_excel(nome_arquivo, index=False)
    print(f"{tipo} '{categoria}' de R${valor} salva em {nome_arquivo}!")

# Função para lançar despesas
def lancar_despesas():
    def salvar_despesa():
        categoria = combo_categorias.get()
        valor = campo_valor.get()
        observacoes = campo_observacoes.get()
        
        # Se a categoria for "ALUGUEL", incluir o inquilino
        inquilino = campo_inquilino.get() if var_inquilino.get() else None
        
        if categoria and valor.strip():
            salvar_em_excel("Despesa", categoria, valor, inquilino, observacoes)
            label_status.configure(text=f"Despesa '{categoria}' de R${valor} salva!", text_color="green")
            campo_valor.delete(0, ctk.END)
            campo_inquilino.delete(0, ctk.END)
            campo_observacoes.delete(0, ctk.END)
        else:
            label_status.configure(text="Por favor, preencha todos os campos.", text_color="red")

    janela_despesas = ctk.CTkToplevel(root)
    janela_despesas.title(f"Lançar Despesas - {prédio_selecionado}")
    janela_despesas.geometry("500x350")

    ctk.CTkLabel(janela_despesas, text="Lançar Despesas", font=("Arial", 18, "bold")).pack(pady=10)
    ctk.CTkLabel(janela_despesas, text="Selecione a categoria:", font=("Arial", 14)).pack(pady=10)
    
    combo_categorias = ctk.CTkComboBox(janela_despesas, values=categorias_despesas, width=300)
    combo_categorias.pack(pady=5)

    ctk.CTkLabel(janela_despesas, text="Insira o valor:", font=("Arial", 14)).pack(pady=10)
    campo_valor = ctk.CTkEntry(janela_despesas, placeholder_text="Ex: 150.00", width=200)
    campo_valor.pack(pady=10)
    
    # Checkbox para inquilino e campo de entrada
    var_inquilino = ctk.BooleanVar(value=False)
    
    check_inquilino = ctk.CTkCheckBox(janela_despesas, text="Descrição do Inquilino", variable=var_inquilino, onvalue=True, offvalue=False)
    campo_inquilino = ctk.CTkEntry(janela_despesas, placeholder_text="Nome do Inquilino", width=200)

    ctk.CTkLabel(janela_despesas, text="Observações (opcional):", font=("Arial", 14)).pack(pady=10)
    campo_observacoes = ctk.CTkEntry(janela_despesas, placeholder_text="Observações", width=200)
    campo_observacoes.pack(pady=10)

    # Função que vai verificar a categoria e mostrar/ocultar o campo inquilino
    def toggle_inquilino(event=None):
        print(f"Categoria selecionada: {combo_categorias.get()}")  # Depuração
        if combo_categorias.get() == "ALUGUÉIS":
            print("Categoria 'ALUGUÉIS' selecionada. Exibindo campo Inquilino.")  # Depuração
            check_inquilino.pack(pady=10)
            campo_inquilino.pack(pady=5)
        else:
            print("Categoria diferente de 'ALUGUÉIS'. Ocultando campo Inquilino.")  # Depuração
            check_inquilino.pack_forget()
            campo_inquilino.pack_forget()

    # Adicionar o evento para atualizar quando a categoria for alterada
    combo_categorias.bind("<<ComboboxSelected>>", toggle_inquilino)
    
    # Inicializar a visibilidade do campo inquilino ao abrir a janela
    toggle_inquilino()

    ctk.CTkButton(janela_despesas, text="Salvar", command=salvar_despesa).pack(pady=10)
    
    label_status = ctk.CTkLabel(janela_despesas, text="", font=("Arial", 12))
    label_status.pack(pady=5)

# Função para lançar receitas
def lancar_receitas():
    def salvar_receita():
        categoria = combo_categorias.get()
        valor = campo_valor.get()
        observacoes = campo_observacoes.get()
        
        if categoria and valor.strip():
            salvar_em_excel("Receita", categoria, valor, observacoes=observacoes)
            label_status.configure(text=f"Receita '{categoria}' de R${valor} salva!", text_color="green")
            campo_valor.delete(0, ctk.END)
            campo_observacoes.delete(0, ctk.END)
        else:
            label_status.configure(text="Por favor, preencha todos os campos.", text_color="red")

    janela_receitas = ctk.CTkToplevel(root)
    janela_receitas.title(f"Lançar Receitas - {prédio_selecionado}")
    janela_receitas.geometry("500x300")

    ctk.CTkLabel(janela_receitas, text="Lançar Receitas", font=("Arial", 18, "bold")).pack(pady=10)
    ctk.CTkLabel(janela_receitas, text="Selecione a categoria:", font=("Arial", 14)).pack(pady=10)
    
    combo_categorias = ctk.CTkComboBox(janela_receitas, values=categorias_receitas, width=300)
    combo_categorias.pack(pady=5)

    ctk.CTkLabel(janela_receitas, text="Insira o valor:", font=("Arial", 14)).pack(pady=10)
    campo_valor = ctk.CTkEntry(janela_receitas, placeholder_text="Ex: 500.00", width=200)
    campo_valor.pack(pady=10)

    ctk.CTkLabel(janela_receitas, text="Observações (opcional):", font=("Arial", 14)).pack(pady=10)
    campo_observacoes = ctk.CTkEntry(janela_receitas, placeholder_text="Observações", width=200)
    campo_observacoes.pack(pady=10)

    ctk.CTkButton(janela_receitas, text="Salvar", command=salvar_receita).pack(pady=10)
    
    label_status = ctk.CTkLabel(janela_receitas, text="", font=("Arial", 12))
    label_status.pack(pady=5)

# Função para selecionar o prédio
def selecionar_predio(predio):
    global prédio_selecionado
    prédio_selecionado = predio
    label_predio.configure(text=f"Prédio Selecionado: {prédio_selecionado}")

# Interface principal
ctk.CTkLabel(root, text="Gerenciador Financeiro", font=("Arial", 20, "bold")).pack(pady=20)

# Seleção de prédio
ctk.CTkLabel(root, text="Selecione o prédio:", font=("Arial", 14)).pack(pady=10)
frame_botoes = ctk.CTkFrame(root)
frame_botoes.pack(pady=5)

ctk.CTkButton(frame_botoes, text="GV", command=lambda: selecionar_predio("GV"), width=80).pack(side="left", padx=10)
ctk.CTkButton(frame_botoes, text="JLP", command=lambda: selecionar_predio("JLP"), width=80).pack(side="left", padx=10)

label_predio = ctk.CTkLabel(root, text="Prédio Selecionado: Nenhum", font=("Arial", 14, "bold"))
label_predio.pack(pady=10)

# Botões para lançar despesas e receitas
ctk.CTkButton(root, text="Lançar Despesas", command=lancar_despesas, width=200).pack(pady=10)
ctk.CTkButton(root, text="Lançar Receitas", command=lancar_receitas, width=200).pack(pady=10)

# Loop da aplicação
root.mainloop()
