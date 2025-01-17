import customtkinter as ctk

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("Dark")  # Alternativa: "Light" ou "System"
ctk.set_default_color_theme("green")  # Tema: "blue", "dark-blue", "green"

# Criando a janela principal
root = ctk.CTk()
root.title("Gerenciador Financeiro")
root.geometry("600x400")

# Categorias de despesas e receitas
categorias_despesas = ["ALUGUÉIS", "APLICAÇÕES FINANCEIRAS"]
categorias_receitas = [
    "SERVIÇOS", "TARIFAS", "VIAGENS", "MOBILIÁRIO", "EQUIPAMENTOS", 
    "PROJETOS", "CONDOMÍNIO", "CONTABILIDADE", "DIVERSAS", "ESCRITÓRIO", 
    "MÃO DE OBRA", "MATERIAIS", "RETIRADAS E RETIRADAS EXTRAS", "FGTS", 
    "GPS", "PIS E COFINS", "CONTRIBUIÇÃO SOCIAL E IMPOSTO DE RENDA"
]

# Função para lançar despesas
def lancar_despesas():
    def salvar_despesa():
        categoria = combo_categorias.get()
        valor = campo_valor.get()
        if categoria and valor.strip():
            print(f"Despesa Lançada: {categoria} - R${valor}")
            label_status.configure(text=f"Despesa '{categoria}' de R${valor} salva com sucesso!", text_color="green")
            campo_valor.delete(0, ctk.END)
        else:
            label_status.configure(text="Por favor, selecione uma categoria e insira um valor válido.", text_color="red")

    janela_despesas = ctk.CTkToplevel(root)
    janela_despesas.title("Lançar Despesas")
    janela_despesas.geometry("500x300")
    
    # Layout
    ctk.CTkLabel(janela_despesas, text="Lançar Despesas", font=("Arial", 18, "bold")).pack(pady=10)
    ctk.CTkLabel(janela_despesas, text="Selecione a categoria:", font=("Arial", 14)).pack(pady=10)
    
    # Dropdown de categorias
    combo_categorias = ctk.CTkComboBox(janela_despesas, values=categorias_despesas, width=300)
    combo_categorias.pack(pady=5)
    
    # Campo de entrada para valor
    ctk.CTkLabel(janela_despesas, text="Insira o valor:", font=("Arial", 14)).pack(pady=10)
    campo_valor = ctk.CTkEntry(janela_despesas, placeholder_text="Ex: 150.00", width=200)
    campo_valor.pack(pady=10)
    
    # Botão de salvar
    ctk.CTkButton(janela_despesas, text="Salvar", command=salvar_despesa).pack(pady=10)
    
    # Label de status
    label_status = ctk.CTkLabel(janela_despesas, text="", font=("Arial", 12))
    label_status.pack(pady=5)

# Função para lançar receitas
def lancar_receitas():
    def salvar_receita():
        categoria = combo_categorias.get()
        valor = campo_valor.get()
        if categoria and valor.strip():
            print(f"Receita Lançada: {categoria} - R${valor}")
            label_status.configure(text=f"Receita '{categoria}' de R${valor} salva com sucesso!", text_color="green")
            campo_valor.delete(0, ctk.END)
        else:
            label_status.configure(text="Por favor, selecione uma categoria e insira um valor válido.", text_color="red")

    janela_receitas = ctk.CTkToplevel(root)
    janela_receitas.title("Lançar Receitas")
    janela_receitas.geometry("500x300")
    
    # Layout
    ctk.CTkLabel(janela_receitas, text="Lançar Receitas", font=("Arial", 18, "bold")).pack(pady=10)
    ctk.CTkLabel(janela_receitas, text="Selecione a categoria:", font=("Arial", 14)).pack(pady=10)
    
    # Dropdown de categorias
    combo_categorias = ctk.CTkComboBox(janela_receitas, values=categorias_receitas, width=300)
    combo_categorias.pack(pady=5)
    
    # Campo de entrada para valor
    ctk.CTkLabel(janela_receitas, text="Insira o valor:", font=("Arial", 14)).pack(pady=10)
    campo_valor = ctk.CTkEntry(janela_receitas, placeholder_text="Ex: 500.00", width=200)
    campo_valor.pack(pady=10)
    
    # Botão de salvar
    ctk.CTkButton(janela_receitas, text="Salvar", command=salvar_receita).pack(pady=10)
    
    # Label de status
    label_status = ctk.CTkLabel(janela_receitas, text="", font=("Arial", 12))
    label_status.pack(pady=5)

# Botões na janela principal
ctk.CTkLabel(root, text="Gerenciador Financeiro", font=("Arial", 20, "bold")).pack(pady=20)
ctk.CTkButton(root, text="Lançar Despesas", command=lancar_despesas, width=200).pack(pady=10)
ctk.CTkButton(root, text="Lançar Receitas", command=lancar_receitas, width=200).pack(pady=10)

# Loop da aplicação
root.mainloop()
