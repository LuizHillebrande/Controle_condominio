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
def salvar_em_excel(tipo, categoria, valor, inquilino=None, observacoes=None, divida_porcentagem=None, predio_destino=None):
    global prédio_selecionado
    if not prédio_selecionado:
        return
    
    # Criar nome do arquivo Excel para o prédio de destino
    mes_atual = datetime.now().strftime("%Y-%m")
    nome_arquivo = f"{predio_destino}_{mes_atual}.xlsx"
    
    # Adicionar as observações, inquilino e percentual de divisão, se houver
    novo_dado = pd.DataFrame([[tipo, categoria, float(valor), inquilino, observacoes, divida_porcentagem, datetime.now().strftime("%d/%m/%Y")]], 
                             columns=["Tipo", "Categoria", "Valor", "Inquilino", "Observações", "Divida Percentual", "Data"])

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
        divida_percentual_1 = campo_divida_percentual_1.get() if var_divida.get() else None
        divida_percentual_2 = campo_divida_percentual_2.get() if var_divida.get() else None

        if categoria and valor.strip():
            valor_float = float(valor)

            # Se a despesa for dividida, calcular os valores para os dois prédios
            if divida_percentual_1 and divida_percentual_2:
                valor_gv = valor_float * float(divida_percentual_1) / 100
                valor_jlp = valor_float * float(divida_percentual_2) / 100
                salvar_em_excel("Despesa", categoria, valor_gv, inquilino, observacoes, divida_percentual_1, "GV")  # Salvar para o GV
                salvar_em_excel("Despesa", categoria, valor_jlp, inquilino, observacoes, divida_percentual_2, "JLP")  # Salvar para o JLP
            else:
               salvar_em_excel("Despesa", categoria, valor_float, inquilino, observacoes, None, prédio_selecionado)
            label_status.configure(text=f"Despesa '{categoria}' de R${valor} salva!", text_color="green")
            campo_valor.delete(0, ctk.END)
            campo_inquilino.delete(0, ctk.END)
            campo_observacoes.delete(0, ctk.END)
            campo_divida_percentual_1.delete(0, ctk.END)
            campo_divida_percentual_2.delete(0, ctk.END)
        else:
            label_status.configure(text="Por favor, preencha todos os campos.", text_color="red")

    janela_despesas = ctk.CTkToplevel(root)
    janela_despesas.title(f"Lançar Despesas - {prédio_selecionado}")
    janela_despesas.geometry("500x450")

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

    # Checkbox para "Despesa dividida entre prédios?" e campos de porcentagem para cada prédio
    var_divida = ctk.BooleanVar(value=False)
    check_divida = ctk.CTkCheckBox(janela_despesas, text="Despesa dividida entre os prédios?", variable=var_divida, onvalue=True, offvalue=False)
    campo_divida_percentual_1 = ctk.CTkEntry(janela_despesas, placeholder_text="% para GV", width=200)
    campo_divida_percentual_2 = ctk.CTkEntry(janela_despesas, placeholder_text="% para JLP", width=200)

    ctk.CTkLabel(janela_despesas, text="Observações (opcional):", font=("Arial", 14)).pack(pady=10)
    campo_observacoes = ctk.CTkEntry(janela_despesas, placeholder_text="Observações", width=200)
    campo_observacoes.pack(pady=10)

    # Função que vai verificar a categoria e mostrar/ocultar o campo inquilino
    def toggle_inquilino(event=None):
        if combo_categorias.get() == "ALUGUÉIS":
            check_inquilino.pack(pady=10)
            campo_inquilino.pack(pady=5)
        else:
            check_inquilino.pack_forget()
            campo_inquilino.pack_forget()

    # Função que vai verificar se a despesa é dividida e exibir os campos de percentual
    def toggle_divida():
        if var_divida.get():
            campo_divida_percentual_1.pack(pady=10)
            campo_divida_percentual_2.pack(pady=10)
        else:
            campo_divida_percentual_1.pack_forget()
            campo_divida_percentual_2.pack_forget()

    # Adicionar o evento para atualizar quando a categoria for alterada
    combo_categorias.bind("<<ComboboxSelected>>", toggle_inquilino)
    
    # Inicializar a visibilidade do campo inquilino e divisão ao abrir a janela
    toggle_inquilino()
    toggle_divida()

    check_divida.pack(pady=10)
    
    # Atualiza a visibilidade do campo percentual com base no checkbox
    check_divida.configure(command=toggle_divida)

    ctk.CTkButton(janela_despesas, text="Salvar", command=salvar_despesa).pack(pady=10)
    
    label_status = ctk.CTkLabel(janela_despesas, text="", font=("Arial", 12))
    label_status.pack(pady=5)

# Função para lançar receitas
def lancar_receitas():
    def salvar_receita():
        categoria = combo_categorias.get()
        valor = campo_valor.get()
        observacoes = campo_observacoes.get()
        
        divida_percentual_1 = campo_divida_percentual_1.get() if var_divida.get() else None
        divida_percentual_2 = campo_divida_percentual_2.get() if var_divida.get() else None

        if categoria and valor.strip():
            valor_float = float(valor)

            # Se a receita for dividida, calcular os valores para os dois prédios
            if divida_percentual_1 and divida_percentual_2:
                valor_gv = valor_float * float(divida_percentual_1) / 100
                valor_jlp = valor_float * float(divida_percentual_2) / 100
                salvar_em_excel("Receita", categoria, valor_gv, observacoes=observacoes, divida_porcentagem=divida_percentual_1, predio_destino="GV")  # Salvar para o GV
                salvar_em_excel("Receita", categoria, valor_jlp, observacoes=observacoes, divida_porcentagem=divida_percentual_2, predio_destino="JLP")  # Salvar para o JLP
            else:
                salvar_em_excel("Receita", categoria, valor_float, observacoes=observacoes, predio_destino=prédio_selecionado)


            label_status.configure(text=f"Receita '{categoria}' de R${valor} salva!", text_color="green")
            campo_valor.delete(0, ctk.END)
            campo_observacoes.delete(0, ctk.END)
            campo_divida_percentual_1.delete(0, ctk.END)
            campo_divida_percentual_2.delete(0, ctk.END)
        else:
            label_status.configure(text="Por favor, preencha todos os campos.", text_color="red")

    janela_receitas = ctk.CTkToplevel(root)
    janela_receitas.title(f"Lançar Receitas - {prédio_selecionado}")
    janela_receitas.geometry("500x450")

    ctk.CTkLabel(janela_receitas, text="Lançar Receitas", font=("Arial", 18, "bold")).pack(pady=10)
    ctk.CTkLabel(janela_receitas, text="Selecione a categoria:", font=("Arial", 14)).pack(pady=10)
    
    combo_categorias = ctk.CTkComboBox(janela_receitas, values=categorias_receitas, width=300)
    combo_categorias.pack(pady=5)

    ctk.CTkLabel(janela_receitas, text="Insira o valor:", font=("Arial", 14)).pack(pady=10)
    campo_valor = ctk.CTkEntry(janela_receitas, placeholder_text="Ex: 500.00", width=200)
    campo_valor.pack(pady=10)
    
    # Checkbox para "Receita dividida entre os prédios?" e campos de porcentagem para cada prédio
    var_divida = ctk.BooleanVar(value=False)
    check_divida = ctk.CTkCheckBox(janela_receitas, text="Receita dividida entre os prédios?", variable=var_divida, onvalue=True, offvalue=False)
    campo_divida_percentual_1 = ctk.CTkEntry(janela_receitas, placeholder_text="% para GV", width=200)
    campo_divida_percentual_2 = ctk.CTkEntry(janela_receitas, placeholder_text="% para JLP", width=200)

    ctk.CTkLabel(janela_receitas, text="Observações (opcional):", font=("Arial", 14)).pack(pady=10)
    campo_observacoes = ctk.CTkEntry(janela_receitas, placeholder_text="Observações", width=200)
    campo_observacoes.pack(pady=10)

    # Função que vai verificar se a receita é dividida e exibir os campos de percentual
    def toggle_divida():
        if var_divida.get():
            campo_divida_percentual_1.pack(pady=10)
            campo_divida_percentual_2.pack(pady=10)
        else:
            campo_divida_percentual_1.pack_forget()
            campo_divida_percentual_2.pack_forget()

    check_divida.pack(pady=10)
    
    # Atualiza a visibilidade do campo percentual com base no checkbox
    check_divida.configure(command=toggle_divida)

    ctk.CTkButton(janela_receitas, text="Salvar", command=salvar_receita).pack(pady=10)
    
    label_status = ctk.CTkLabel(janela_receitas, text="", font=("Arial", 12))
    label_status.pack(pady=5)

def salvar_transferencia(valor, origem, destino, observacoes=None):
    """ Salva a transferência entre prédios em um arquivo Excel """
    nome_arquivo = "transferencias.xlsx"
    nova_transferencia = pd.DataFrame([
        [float(valor), origem, destino, observacoes, datetime.now().strftime("%d/%m/%Y")]
    ], columns=["Valor", "Origem", "Destino", "Observações", "Data"])

    if os.path.exists(nome_arquivo):
        df_existente = pd.read_excel(nome_arquivo)
        df_final = pd.concat([df_existente, nova_transferencia], ignore_index=True)
    else:
        df_final = nova_transferencia

    df_final.to_excel(nome_arquivo, index=False)
    print(f"Transferência de R${valor} de {origem} para {destino} registrada!")

def transferir_receita():
    """ Interface para transferência de receita entre prédios """
    janela_transf = ctk.CTkToplevel(root)
    janela_transf.title("Transferência de Receita")
    janela_transf.geometry("400x300")
    
    ctk.CTkLabel(janela_transf, text="Transferir Receita", font=("Arial", 18, "bold")).pack(pady=10)
    
    ctk.CTkLabel(janela_transf, text="Valor:").pack(pady=5)
    campo_valor = ctk.CTkEntry(janela_transf, placeholder_text="Ex: 1000.00", width=200)
    campo_valor.pack(pady=5)
    
    ctk.CTkLabel(janela_transf, text="Origem:").pack(pady=5)
    combo_origem = ctk.CTkComboBox(janela_transf, values=["GV", "JLP"], width=200)
    combo_origem.pack(pady=5)
    
    ctk.CTkLabel(janela_transf, text="Destino:").pack(pady=5)
    combo_destino = ctk.CTkComboBox(janela_transf, values=["GV", "JLP"], width=200)
    combo_destino.pack(pady=5)
    
    ctk.CTkLabel(janela_transf, text="Observações (opcional):").pack(pady=5)
    campo_observacoes = ctk.CTkEntry(janela_transf, placeholder_text="Observações", width=200)
    campo_observacoes.pack(pady=5)
    
    def salvar():
        valor = campo_valor.get()
        origem = combo_origem.get()
        destino = combo_destino.get()
        observacoes = campo_observacoes.get()
        
        if origem == destino:
            label_status.configure(text="Erro: Origem e destino devem ser diferentes!", text_color="red")
            return
        
        if valor.strip():
            salvar_transferencia(valor, origem, destino, observacoes)
            label_status.configure(text=f"Transferência de R${valor} registrada!", text_color="green")
            campo_valor.delete(0, ctk.END)
            campo_observacoes.delete(0, ctk.END)
        else:
            label_status.configure(text="Por favor, insira um valor.", text_color="red")
    
    ctk.CTkButton(janela_transf, text="Salvar", command=salvar).pack(pady=10)
    
    label_status = ctk.CTkLabel(janela_transf, text="", font=("Arial", 12))
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
ctk.CTkButton(root, text="Transferir Receita entre os prédios", command=transferir_receita, width=200).pack(pady=10)

# Loop da aplicação
root.mainloop()
