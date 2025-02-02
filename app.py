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
                             columns=["Tipo", "Categoria", "Valor", "Inquilino", "Observações", "Divida Percentual"])

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
                salvar_em_excel("Despesa", categoria, valor_gv, observacoes, divida_percentual_1, "GV")  # Salvar para o GV
                salvar_em_excel("Despesa", categoria, valor_jlp, observacoes, divida_percentual_2, "JLP")  # Salvar para o JLP
            else:
               salvar_em_excel("Despesa", categoria, valor_float, observacoes, None, prédio_selecionado)
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

def adicionar_nova_despesa():
    print("Adicionando nova despesa")

    '''
    CATEGORIAS PADRÕES, QUERO MONTAR UMA LÓGICA QUE ADICIONE NOVAS
    categorias_despesas = [
        "SERVIÇOS", "TARIFAS", "VIAGENS", "MOBILIÁRIO", "EQUIPAMENTOS", 
        "PROJETOS", "CONDOMÍNIO", "CONTABILIDADE", "DIVERSAS", "ESCRITÓRIO", 
        "MÃO DE OBRA", "MATERIAIS", "RETIRADAS E RETIRADAS EXTRAS", "FGTS", 
        "GPS", "PIS E COFINS", "CONTRIBUIÇÃO SOCIAL E IMPOSTO DE RENDA"
    ]

    '''
import os
import pandas as pd
import customtkinter as ctk

# Arquivos para armazenar categorias de despesas e receitas
arquivo_categorias_despesas = "categorias_despesas.xlsx"
arquivo_categorias_receitas = "categorias_receitas.xlsx"

# Listas padrão de categorias
categorias_padrao_despesas = [
    "SERVIÇOS", "TARIFAS", "VIAGENS", "MOBILIÁRIO", "EQUIPAMENTOS",
    "PROJETOS", "CONDOMÍNIO", "CONTABILIDADE", "DIVERSAS", "ESCRITÓRIO",
    "MÃO DE OBRA", "MATERIAIS", "RETIRADAS E RETIRADAS EXTRAS", "FGTS",
    "GPS", "PIS E COFINS", "CONTRIBUIÇÃO SOCIAL E IMPOSTO DE RENDA"
]

categorias_padrao_receitas = ["ALUGUÉIS", "APLICAÇÕES FINANCEIRAS"]

# Verifica se o arquivo de despesas existe, caso contrário, cria um novo
if os.path.exists(arquivo_categorias_despesas):
    df_despesas = pd.read_excel(arquivo_categorias_despesas)
    categorias_despesas = df_despesas["Categorias"].tolist()
else:
    categorias_despesas = categorias_padrao_despesas.copy()
    df_despesas = pd.DataFrame({"Categorias": categorias_despesas})
    df_despesas.to_excel(arquivo_categorias_despesas, index=False)

# Verifica se o arquivo de receitas existe, caso contrário, cria um novo
if os.path.exists(arquivo_categorias_receitas):
    df_receitas = pd.read_excel(arquivo_categorias_receitas)
    categorias_receitas = df_receitas["Categorias"].tolist()
else:
    categorias_receitas = categorias_padrao_receitas.copy()
    df_receitas = pd.DataFrame({"Categorias": categorias_receitas})
    df_receitas.to_excel(arquivo_categorias_receitas, index=False)

def salvar_categorias_no_excel(tipo):
    """Salva as categorias de despesas ou receitas no arquivo Excel correspondente."""
    if tipo == "despesas":
        df = pd.DataFrame({"Categorias": categorias_despesas})
        df.to_excel(arquivo_categorias_despesas, index=False)
    elif tipo == "receitas":
        df = pd.DataFrame({"Categorias": categorias_receitas})
        df.to_excel(arquivo_categorias_receitas, index=False)

def adicionar_nova_categoria(tipo):
    """Adiciona uma nova categoria de receita ou despesa"""
    def salvar_categoria():
        nova_categoria = campo_nova_categoria.get().strip().upper()
        
        if tipo == "despesas":
            categorias = categorias_despesas
        else:
            categorias = categorias_receitas

        if nova_categoria and nova_categoria not in categorias:
            categorias.append(nova_categoria)
            salvar_categorias_no_excel(tipo)
            campo_nova_categoria.delete(0, ctk.END)
            label_status_categoria.configure(text=f"Categoria '{nova_categoria}' adicionada!", text_color="green")
        elif nova_categoria in categorias:
            label_status_categoria.configure(text="Essa categoria já existe!", text_color="orange")
        else:
            label_status_categoria.configure(text="Por favor, insira um nome válido.", text_color="red")

    # Janela para adicionar nova categoria
    janela_nova_categoria = ctk.CTkToplevel()
    janela_nova_categoria.title(f"Adicionar Nova Categoria de {tipo.capitalize()}")
    janela_nova_categoria.geometry("400x200")
    
    ctk.CTkLabel(janela_nova_categoria, text=f"Nova Categoria de {tipo.capitalize()}", font=("Arial", 18, "bold")).pack(pady=10)
    
    ctk.CTkLabel(janela_nova_categoria, text="Nome da nova categoria:").pack(pady=5)
    campo_nova_categoria = ctk.CTkEntry(janela_nova_categoria, placeholder_text="Ex: NOVA CATEGORIA", width=200)
    campo_nova_categoria.pack(pady=5)
    
    ctk.CTkButton(janela_nova_categoria, text="Adicionar", command=salvar_categoria).pack(pady=10)
    
    label_status_categoria = ctk.CTkLabel(janela_nova_categoria, text="", font=("Arial", 12))
    label_status_categoria.pack(pady=5)

def excluir_categoria(tipo):
    """Abre uma janela para excluir uma categoria de receita ou despesa"""
    def remover_categoria():
        categoria_selecionada = combo_categorias.get()
        
        if tipo == "despesas":
            categorias = categorias_despesas
        else:
            categorias = categorias_receitas

        if categoria_selecionada:
            categorias.remove(categoria_selecionada)
            salvar_categorias_no_excel(tipo)
            combo_categorias.configure(values=categorias)
            combo_categorias.set("")
            label_status_excluir.configure(text=f"Categoria '{categoria_selecionada}' excluída!", text_color="green")
        else:
            label_status_excluir.configure(text="Selecione uma categoria para excluir.", text_color="red")

    # Janela para excluir categoria
    janela_excluir_categoria = ctk.CTkToplevel()
    janela_excluir_categoria.title(f"Excluir Categoria de {tipo.capitalize()}")
    janela_excluir_categoria.geometry("400x200")
    
    ctk.CTkLabel(janela_excluir_categoria, text=f"Excluir Categoria de {tipo.capitalize()}", font=("Arial", 18, "bold")).pack(pady=10)
    
    ctk.CTkLabel(janela_excluir_categoria, text="Selecione a categoria:").pack(pady=5)
    categorias = categorias_despesas if tipo == "despesas" else categorias_receitas
    combo_categorias = ctk.CTkComboBox(janela_excluir_categoria, values=categorias)
    combo_categorias.pack(pady=5)
    
    ctk.CTkButton(janela_excluir_categoria, text="Excluir", command=remover_categoria).pack(pady=10)
    
    label_status_excluir = ctk.CTkLabel(janela_excluir_categoria, text="", font=("Arial", 12))
    label_status_excluir.pack(pady=5)



prédio_selecionado = None

# Função para selecionar o prédio
def selecionar_predio(predio):
    global prédio_selecionado, label_predio  # Garante que estamos acessando a variável global
    prédio_selecionado = predio

    if not label_predio.winfo_exists():  # Se o label foi destruído
        print("label_predio foi destruído. Criando novamente...")
        label_predio = ctk.CTkLabel(frame_menu, text="")  # Recria o label no frame correto
        label_predio.pack(pady=10)  # Adiciona o label à interface

    label_predio.configure(text=f"Prédio Selecionado: {prédio_selecionado}")




# Configuração principal do CTk
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.geometry("800x600")
root.title("Gerenciador Financeiro")

# Menu lateral
frame_menu = ctk.CTkFrame(root, width=200, corner_radius=0)
frame_menu.pack(side="left", fill="y")

ctk.CTkLabel(frame_menu, text="Menu", font=("Arial", 16, "bold")).pack(pady=20)

ctk.CTkButton(frame_menu, text="GV", command=lambda: selecionar_predio("GV"), width=180).pack(pady=10)
ctk.CTkButton(frame_menu, text="JLP", command=lambda: selecionar_predio("JLP"), width=180).pack(pady=10)

# Lista de sócios global
socios = []

from tkinter import messagebox
# Função para carregar os dados dos sócios a partir de um arquivo Excel
def carregar_socios():
    """ Carregar os sócios de um arquivo Excel se existir """
    if os.path.exists("socios.xlsx"):
        df = pd.read_excel("socios.xlsx")
        global socios
        socios = df.to_dict(orient="records")  # Carregar os sócios como um dicionário
    else:
        messagebox.showwarning('Atenção!', 'Nenhum arquivo sócios.xlsx encontrado!')
        socios = []  # Se não houver arquivo, inicia com lista vazia

# Função para salvar os sócios em um arquivo Excel
def salvar_socios():
    """ Salvar os dados de sócios em um arquivo Excel """
    df = pd.DataFrame(socios)
    df.to_excel("socios.xlsx", index=False)
    print("Socios salvos com sucesso!")

# Função para adicionar um sócio
def adicionar_socio():
    nome_socio = campo_nome_socio.get().strip()
    porcentagem_socio = campo_porcentagem_socio.get().strip()

    if nome_socio and porcentagem_socio:
        try:
            porcentagem = float(porcentagem_socio)
            if 0 < porcentagem <= 100:
                # Não há mais verificação de soma das porcentagens
                # Adiciona o sócio à lista de sócios
                socios.append({"nome": nome_socio, "porcentagem": porcentagem, "prédio": "", "selected": False})
                campo_nome_socio.delete(0, ctk.END)
                campo_porcentagem_socio.delete(0, ctk.END)
                exibir_socios()  # Atualiza a lista de sócios
                salvar_socios()  # Salva os sócios no arquivo
                label_status.configure(text="Sócio adicionado com sucesso!", text_color="green")
            else:
                label_status.configure(text="Porcentagem deve ser entre 0 e 100.", text_color="red")
        except ValueError:
            label_status.configure(text="Porcentagem inválida. Insira um número.", text_color="red")
    else:
        label_status.configure(text="Por favor, preencha todos os campos.", text_color="red")
# Função para exibir os sócios e suas porcentagens
def exibir_socios():
    """ Exibir os sócios com checkbox para selecionar o prédio e exclusão """
    for widget in frame_socios.winfo_children():
        widget.destroy()  # Limpa os widgets antigos

    for socio in socios:
        # Exibir nome e porcentagem do sócio, com checkbox para seleção de prédio
        socio_frame = ctk.CTkFrame(frame_socios)
        socio_frame.pack(pady=5, fill="x")

        ctk.CTkLabel(socio_frame, text=f"{socio['nome']} - {socio['porcentagem']}%", font=("Arial", 12)).pack(side="left", padx=10)
        
        # Checkbox para escolher o prédio (GV ou JLP)
        var_prédio = ctk.StringVar(value=socio['prédio'])
        checkbox_gv = ctk.CTkRadioButton(socio_frame, text="GV", variable=var_prédio, value="GV", command=lambda s=socio, v=var_prédio: atualizar_predio_socio(s, v))
        checkbox_gv.pack(side="left", padx=5)
        checkbox_jlp = ctk.CTkRadioButton(socio_frame, text="JLP", variable=var_prédio, value="JLP", command=lambda s=socio, v=var_prédio: atualizar_predio_socio(s, v))
        checkbox_jlp.pack(side="left", padx=5)

        # Checkbox para selecionar o sócio para exclusão
        var_selected = ctk.BooleanVar(value=socio['selected'])
        checkbox_delete = ctk.CTkCheckBox(socio_frame, text="Excluir", variable=var_selected, command=lambda s=socio, v=var_selected: atualizar_selecao_exclusao(s, v))
        checkbox_delete.pack(side="right", padx=5)

# Função para atualizar o prédio do sócio (GV ou JLP)
def atualizar_predio_socio(socio, var_prédio):
    """ Atualiza o prédio atribuído ao sócio """
    socio['prédio'] = var_prédio.get()
    salvar_socios()  # Salva novamente após atualização do prédio

# Função para atualizar a seleção de exclusão do sócio
def atualizar_selecao_exclusao(socio, var_selected):
    """ Marca o sócio para exclusão ou não """
    socio['selected'] = var_selected.get()
    salvar_socios()  # Salva novamente após alteração de seleção

# Função para limpar a lista de sócios selecionados
def limpar_socios_selecionados():
    global socios
    # Filtra os sócios que não estão selecionados para exclusão
    socios = [socio for socio in socios if not socio['selected']]
    exibir_socios()  # Atualiza a interface com a lista filtrada
    salvar_socios()  # Salva novamente no Excel

    label_status.configure(text="Sócios selecionados foram excluídos!", text_color="green")

# Função para atualizar o conteúdo do frame principal
def atualizar_menu_rateio():
    global campo_nome_socio, campo_porcentagem_socio, label_status, frame_socios  # Tornando essas variáveis globais
    
    # Limpa o conteúdo atual da área de conteúdo
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    ctk.CTkLabel(frame_conteudo, text="Cadastro de Sócios e Rateio", font=("Arial", 18, "bold")).pack(pady=10)

    # Campo para adicionar um novo sócio
    ctk.CTkLabel(frame_conteudo, text="Nome do Sócio:").pack(pady=5)
    campo_nome_socio = ctk.CTkEntry(frame_conteudo, placeholder_text="Nome do Sócio", width=300)
    campo_nome_socio.pack(pady=5)
    
    ctk.CTkLabel(frame_conteudo, text="Porcentagem de Rateio:").pack(pady=5)
    campo_porcentagem_socio = ctk.CTkEntry(frame_conteudo, placeholder_text="Porcentagem", width=300)
    campo_porcentagem_socio.pack(pady=5)

    # Botão para adicionar o sócio
    ctk.CTkButton(frame_conteudo, text="Adicionar Sócio", command=adicionar_socio).pack(pady=10)

    # Frame para exibir a lista de sócios
    frame_socios = ctk.CTkFrame(frame_conteudo)
    frame_socios.pack(pady=10, fill="x")

    # Exibir os sócios atuais
    exibir_socios()

    # Botão para limpar os sócios selecionados
    ctk.CTkButton(frame_conteudo, text="Limpar Sócios Selecionados", command=limpar_socios_selecionados).pack(pady=10)

    # Status do processo
    label_status = ctk.CTkLabel(frame_conteudo, text="", font=("Arial", 12))
    label_status.pack(pady=10)


def atualizar_menu_categorias(tipo):
    """ Atualiza o conteúdo da área principal com os campos para adicionar ou excluir categorias """
    # Limpa o conteúdo atual da área de conteúdo
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    
    if tipo == "adicionar_despesa":
        label_predio = ctk.CTkLabel(frame_conteudo, text="Prédio Selecionado: Nenhum", font=("Arial", 14, "bold"))
        label_predio.pack(pady=10)
        label_predio.configure(text=f"Prédio Selecionado: {prédio_selecionado}")
        ctk.CTkLabel(frame_conteudo, text="Adicionar Nova Categoria (Despesa)", font=("Arial", 18, "bold")).pack(pady=10)
        
        ctk.CTkLabel(frame_conteudo, text="Nome da nova categoria:").pack(pady=5)
        campo_nova_categoria = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: NOVA CATEGORIA", width=200)
        campo_nova_categoria.pack(pady=5)
        
        def salvar_categoria():
            nova_categoria = campo_nova_categoria.get().strip().upper()
            
            if nova_categoria and nova_categoria not in categorias_despesas:
                categorias_despesas.append(nova_categoria)
                salvar_categorias_no_excel("despesas")
                campo_nova_categoria.delete(0, ctk.END)
                label_status_categoria.configure(text=f"Categoria '{nova_categoria}' adicionada!", text_color="green")
            elif nova_categoria in categorias_despesas:
                label_status_categoria.configure(text="Essa categoria já existe!", text_color="orange")
            else:
                label_status_categoria.configure(text="Por favor, insira um nome válido.", text_color="red")

        ctk.CTkButton(frame_conteudo, text="Adicionar", command=salvar_categoria).pack(pady=10)
        
        label_status_categoria = ctk.CTkLabel(frame_conteudo, text="", font=("Arial", 12))
        label_status_categoria.pack(pady=5)

    elif tipo == "excluir_despesa":
        label_predio = ctk.CTkLabel(frame_conteudo, text="Prédio Selecionado: Nenhum", font=("Arial", 14, "bold"))
        label_predio.pack(pady=10)
        label_predio.configure(text=f"Prédio Selecionado: {prédio_selecionado}")
        ctk.CTkLabel(frame_conteudo, text="Excluir Categoria (Despesa)", font=("Arial", 18, "bold")).pack(pady=10)
        
        ctk.CTkLabel(frame_conteudo, text="Selecione a categoria:").pack(pady=5)
        combo_categorias = ctk.CTkComboBox(frame_conteudo, values=categorias_despesas)
        combo_categorias.pack(pady=5)
        
        def remover_categoria():
            categoria_selecionada = combo_categorias.get()
            
            if categoria_selecionada:
                categorias_despesas.remove(categoria_selecionada)
                salvar_categorias_no_excel("despesas")
                combo_categorias.configure(values=categorias_despesas)
                combo_categorias.set("")
                label_status_excluir.configure(text=f"Categoria '{categoria_selecionada}' excluída!", text_color="green")
            else:
                label_status_excluir.configure(text="Selecione uma categoria para excluir.", text_color="red")

        ctk.CTkButton(frame_conteudo, text="Excluir", command=remover_categoria).pack(pady=10)
        
        label_status_excluir = ctk.CTkLabel(frame_conteudo, text="", font=("Arial", 12))
        label_status_excluir.pack(pady=5)

    elif tipo == "adicionar_receita":
        label_predio = ctk.CTkLabel(frame_conteudo, text="Prédio Selecionado: Nenhum", font=("Arial", 14, "bold"))
        label_predio.pack(pady=10)
        label_predio.configure(text=f"Prédio Selecionado: {prédio_selecionado}")
        ctk.CTkLabel(frame_conteudo, text="Adicionar Nova Categoria (Receita)", font=("Arial", 18, "bold")).pack(pady=10)
        
        ctk.CTkLabel(frame_conteudo, text="Nome da nova categoria:").pack(pady=5)
        campo_nova_categoria = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: NOVA CATEGORIA", width=200)
        campo_nova_categoria.pack(pady=5)
        
        def salvar_categoria():
            nova_categoria = campo_nova_categoria.get().strip().upper()
            
            if nova_categoria and nova_categoria not in categorias_receitas:
                categorias_receitas.append(nova_categoria)
                salvar_categorias_no_excel("receitas")
                campo_nova_categoria.delete(0, ctk.END)
                label_status_categoria.configure(text=f"Categoria '{nova_categoria}' adicionada!", text_color="green")
            elif nova_categoria in categorias_receitas:
                label_status_categoria.configure(text="Essa categoria já existe!", text_color="orange")
            else:
                label_status_categoria.configure(text="Por favor, insira um nome válido.", text_color="red")

        ctk.CTkButton(frame_conteudo, text="Adicionar", command=salvar_categoria).pack(pady=10)
        
        label_status_categoria = ctk.CTkLabel(frame_conteudo, text="", font=("Arial", 12))
        label_status_categoria.pack(pady=5)

    elif tipo == "excluir_receita":
        label_predio = ctk.CTkLabel(frame_conteudo, text="Prédio Selecionado: Nenhum", font=("Arial", 14, "bold"))
        label_predio.pack(pady=10)
        label_predio.configure(text=f"Prédio Selecionado: {prédio_selecionado}")
        ctk.CTkLabel(frame_conteudo, text="Excluir Categoria (Receita)", font=("Arial", 18, "bold")).pack(pady=10)
        
        ctk.CTkLabel(frame_conteudo, text="Selecione a categoria:").pack(pady=5)
        combo_categorias = ctk.CTkComboBox(frame_conteudo, values=categorias_receitas)
        combo_categorias.pack(pady=5)
        
        def remover_categoria():
            categoria_selecionada = combo_categorias.get()
            
            if categoria_selecionada:
                categorias_receitas.remove(categoria_selecionada)
                salvar_categorias_no_excel("receitas")
                combo_categorias.configure(values=categorias_receitas)
                combo_categorias.set("")
                label_status_excluir.configure(text=f"Categoria '{categoria_selecionada}' excluída!", text_color="green")
            else:
                label_status_excluir.configure(text="Selecione uma categoria para excluir.", text_color="red")

        ctk.CTkButton(frame_conteudo, text="Excluir", command=remover_categoria).pack(pady=10)
        
        label_status_excluir = ctk.CTkLabel(frame_conteudo, text="", font=("Arial", 12))
        label_status_excluir.pack(pady=5)
    
#INQUILINOS

import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

# Lista de inquilinos cadastrados (essa estrutura pode ser substituída por um banco de dados ou arquivo)
inquilinos = []

# Função para carregar os inquilinos do arquivo Excel
def carregar_inquilinos():
    try:
        # Carregar o arquivo Excel com os inquilinos
        df_inquilinos = pd.read_excel("inquilinos.xlsx")

        # Limpar espaços extras nas colunas
        df_inquilinos.columns = df_inquilinos.columns.str.strip()

        # Verificar se o arquivo tem as colunas esperadas
        if 'nome' not in df_inquilinos.columns or 'valor_aluguel' not in df_inquilinos.columns:
            print("Colunas 'nome' ou 'valor_aluguel' não encontradas no arquivo.")
            return
        
        # Limpar lista de inquilinos
        inquilinos.clear()
        
        # Preencher a lista com os dados do Excel
        for _, row in df_inquilinos.iterrows():
            inquilinos.append({
                "nome": row["nome"],
                "valor_aluguel": row["valor_aluguel"],
                "valor_iptu": row.get("valor_iptu", 0),  # Se não houver valor_iptu, atribui 0
                "valor_condominio": row.get("valor_condominio", 0)  # Se não houver valor_condominio, atribui 0
            })

        # Verificar se a lista foi carregada corretamente
        print("Inquilinos carregados:", inquilinos)

    except Exception as e:
        print(f"Erro ao carregar inquilinos: {e}")

# Função para adicionar ou editar inquilino
def salvar_inquilino():
    nome_inquilino = campo_nome_inquilino.get().strip()
    valor_aluguel = campo_valor_aluguel.get().strip()
    valor_iptu = campo_iptu.get().strip()
    valor_condominio = campo_condominio.get().strip()

    if not nome_inquilino or not valor_aluguel or not valor_iptu or not valor_condominio:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    try:
        valor_aluguel = float(valor_aluguel.replace(",", "."))
        valor_iptu = float(valor_iptu.replace(",", "."))
        valor_condominio = float(valor_condominio.replace(",", "."))
    except ValueError:
        messagebox.showerror("Erro", "Valores inválidos.")
        return

    inquilinos.append({
        "nome": nome_inquilino,
        "valor_aluguel": valor_aluguel,
        "valor_iptu": valor_iptu,
        "valor_condominio": valor_condominio
    })

    # Salvar o novo inquilino no arquivo Excel
    df_inquilinos = pd.DataFrame(inquilinos)  # Convertendo a lista de inquilinos para DataFrame
    df_inquilinos.to_excel("inquilinos.xlsx", index=False)

    messagebox.showinfo("Sucesso", f"Inquilino {nome_inquilino} cadastrado com sucesso!")

    # Limpar os campos após salvar
    campo_nome_inquilino.delete(0, 'end')
    campo_valor_aluguel.delete(0, 'end')
    campo_iptu.delete(0, 'end')
    campo_condominio.delete(0, 'end')

    
# Função para exibir o formulário de cadastro de inquilino
def exibir_formulario_cadastro_inquilino():
    # Limpar o conteúdo anterior do frame
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    # Título do formulário
    ctk.CTkLabel(frame_conteudo, text="Cadastro de Inquilino", font=("Arial", 18, "bold")).pack(pady=10)

    # Campo para nome do inquilino
    ctk.CTkLabel(frame_conteudo, text="Nome do Inquilino:").pack(pady=5)
    global campo_nome_inquilino
    campo_nome_inquilino = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: João Silva", width=250)
    campo_nome_inquilino.pack(pady=5)

    # Campo para valor do aluguel
    ctk.CTkLabel(frame_conteudo, text="Valor do Aluguel:").pack(pady=5)
    global campo_valor_aluguel
    campo_valor_aluguel = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: 1500,00", width=250)
    campo_valor_aluguel.pack(pady=5)

    # Campo para valor do IPTU
    ctk.CTkLabel(frame_conteudo, text="Valor do IPTU:").pack(pady=5)
    global campo_iptu
    campo_iptu = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: 200,00", width=250)
    campo_iptu.pack(pady=5)

    # Campo para valor do condomínio
    ctk.CTkLabel(frame_conteudo, text="Valor do Condomínio:").pack(pady=5)
    global campo_condominio
    campo_condominio = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: 300,00", width=250)
    campo_condominio.pack(pady=5)

    # Botão para salvar o cadastro do inquilino
    ctk.CTkButton(frame_conteudo, text="Salvar Inquilino", command=salvar_inquilino).pack(pady=10)

# Função para selecionar um inquilino do combo
# Função para selecionar o inquilino e carregar os valores de aluguel, IPTU e condomínio

def carregar_inquilinos():
    try:
        # Carregar os dados de inquilinos do Excel
        df_inquilinos = pd.read_excel("inquilinos.xlsx")
        # Converter os dados para uma lista de dicionários
        inquilinos = df_inquilinos.to_dict(orient="records")
        return inquilinos
    except FileNotFoundError:
        return []  # Caso o arquivo não exista, retorna uma lista vazia

# Carregar os inquilinos ao iniciar
inquilinos = carregar_inquilinos()

def selecionar_inquilino():
    inquilino_selecionado = combo_inquilinos.get()
    
    # Buscar o inquilino no banco de dados de inquilinos
    for inquilino in inquilinos:
        if inquilino["nome"] == inquilino_selecionado:
            campo_valor_atual_aluguel.delete(0, "end")
            campo_valor_atual_aluguel.insert(0, f"{inquilino['valor_aluguel']:.2f}")
            
            campo_valor_iptu.delete(0, "end")
            campo_valor_iptu.insert(0, f"{inquilino['valor_iptu']:.2f}")
            
            campo_valor_condominio.delete(0, "end")
            campo_valor_condominio.insert(0, f"{inquilino['valor_condominio']:.2f}")
            break

# Função para alterar o valor do aluguel

def alterar_valor_aluguel():
    inquilino_selecionado = combo_inquilinos.get()
    novo_valor_aluguel = campo_valor_atual_aluguel.get().strip()
    novo_valor_iptu = campo_valor_iptu.get().strip()  # Adicionando IPTU
    novo_valor_condominio = campo_valor_condominio.get().strip()  # Adicionando Condomínio

    if not novo_valor_aluguel or not novo_valor_iptu or not novo_valor_condominio:
        messagebox.showerror("Erro", "Informe todos os valores (aluguel, IPTU e condomínio).")
        return

    try:
        # Limpar espaços e substituir a vírgula por ponto para valores decimais
        novo_valor_aluguel = campo_valor_atual_aluguel.get().strip().replace(",", ".")
        novo_valor_iptu = campo_valor_iptu.get().strip().replace(",", ".")
        novo_valor_condominio = campo_valor_condominio.get().strip().replace(",", ".")

        # Tentar converter os valores para float
        novo_valor_aluguel = float(novo_valor_aluguel)
        novo_valor_iptu = float(novo_valor_iptu)
        novo_valor_condominio = float(novo_valor_condominio)
    except ValueError:
        messagebox.showerror("Erro", "Um dos valores é inválido. Certifique-se de inserir números válidos.")
        return


    # Atualizar o valor do aluguel, IPTU e condomínio do inquilino selecionado
    for inquilino in inquilinos:
        if inquilino["nome"] == inquilino_selecionado:
            inquilino["valor_aluguel"] = novo_valor_aluguel
            inquilino["valor_iptu"] = novo_valor_iptu  # Atualizando IPTU
            inquilino["valor_condominio"] = novo_valor_condominio  # Atualizando Condomínio
            messagebox.showinfo("Sucesso", f"Valores de {inquilino_selecionado} atualizados com sucesso!")
            break

    # Salvar os inquilinos atualizados no arquivo Excel
    df_inquilinos = pd.DataFrame(inquilinos)  # Convertendo a lista de inquilinos para DataFrame
    df_inquilinos.to_excel("inquilinos.xlsx", index=False)

# Função para exibir o formulário de alteração do valor do aluguel, IPTU e condomínio
def exibir_formulario_alteracao_aluguel():
    # Limpar o conteúdo anterior do frame
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    # Título do formulário
    ctk.CTkLabel(frame_conteudo, text="Alterar Valores do Inquilino", font=("Arial", 18, "bold")).pack(pady=10)

    # ComboBox para selecionar o inquilino
    ctk.CTkLabel(frame_conteudo, text="Selecionar Inquilino:").pack(pady=5)
    global combo_inquilinos
    combo_inquilinos = ctk.CTkComboBox(frame_conteudo, values=[inquilino["nome"] for inquilino in inquilinos])
    combo_inquilinos.pack(pady=5)

    # Botão para carregar os valores atuais do inquilino
    ctk.CTkButton(frame_conteudo, text="Carregar Valores Atuais", command=selecionar_inquilino).pack(pady=5)

    # Campo para alterar o valor do aluguel
    ctk.CTkLabel(frame_conteudo, text="Novo Valor do Aluguel:").pack(pady=5)
    global campo_valor_atual_aluguel
    campo_valor_atual_aluguel = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: 1600,00", width=250)
    campo_valor_atual_aluguel.pack(pady=5)

    # Campo para o novo valor do IPTU
    ctk.CTkLabel(frame_conteudo, text="Novo Valor do IPTU:").pack(pady=5)
    global campo_valor_iptu
    campo_valor_iptu = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: 200,00", width=250)
    campo_valor_iptu.pack(pady=5)

    # Campo para o novo valor do condomínio
    ctk.CTkLabel(frame_conteudo, text="Novo Valor do Condomínio:").pack(pady=5)
    global campo_valor_condominio
    campo_valor_condominio = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: 300,00", width=250)
    campo_valor_condominio.pack(pady=5)

    # Botão para alterar os valores (aluguel, IPTU, condomínio)
    ctk.CTkButton(frame_conteudo, text="Alterar Valores", command=alterar_valor_aluguel).pack(pady=10)


def validar_mes(mes):
    try:
        # Verifica se o mês tem o formato correto (YYYY-MM)
        datetime.strptime(mes, "%Y-%m")
        return True
    except ValueError:
        return False

# Função para pedir o mês ao usuário
def pedir_mes_usuario():
    # Bloquear outras ações até o mês ser inserido
    frame_menu.pack_forget()
    label_instrucoes.pack(pady=10)
    entry_mes.pack(pady=10)
    botao_confirmar.pack(pady=10)
    botao_lancar_despesas.configure(state="disabled")
    botao_lancar_receitas.configure(state="disabled")
    botao_transferir_receita.configure(state="disabled")

# Função para confirmar a entrada do mês
def confirmar_mes():
    global mes_usuario
    mes_usuario = entry_mes.get()
    if validar_mes(mes_usuario):
        print(f"Mês selecionado: {mes_usuario}")
        frame_menu.pack(side="left", fill="y")  # Liberar o menu após inserir o mês
        label_instrucoes.pack_forget()
        entry_mes.pack_forget()
        botao_confirmar.pack_forget()
        botao_lancar_despesas.configure(state="normal")
        botao_lancar_receitas.configure(state="normal")
        botao_transferir_receita.configure(state="normal")
    else:
        # Caso o mês seja inválido
        label_instrucoes.configure(text="Mês inválido! Tente novamente (Formato: YYYY-MM)")
        entry_mes.delete(0, tk.END)


def salvar_lancamento_em_excel(tipo, valor, categoria, predio_destino, inquilino, saldo_inicial, mes_usuario):
    if not predio_destino:
        return
    
    nome_arquivo = f"{predio_destino}_{mes_usuario}.xlsx"
    print(nome_arquivo)
    
    # Adicionar as informações do lançamento (valor, categoria, data, inquilino e saldo inicial)
    novo_dado = pd.DataFrame([[tipo, categoria, float(valor), datetime.now().strftime("%d/%m/%Y"), saldo_inicial, inquilino]], 
                             columns=["Tipo", "Categoria", "Valor", "Data", "Saldo Inicial", "Inquilino"])
    
    # Verificar se o arquivo já existe
    if os.path.exists(nome_arquivo):
        df_existente = pd.read_excel(nome_arquivo)
        df_final = pd.concat([df_existente, novo_dado], ignore_index=True)
    else:
        df_final = novo_dado

    # Salvar no Excel
    df_final.to_excel(nome_arquivo, index=False)
    print(f"{tipo} de R${valor} na categoria '{categoria}' salva em {nome_arquivo}!")


import customtkinter as ctk

def atualizar_lancamento(tipo):
    global mes_usuario
    """ Atualiza o conteúdo da área principal com os campos para lançar despesas, receitas ou transferir receita """
    # Limpa o conteúdo atual da área de conteúdo
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    
    if tipo == "lancar_despesas":
        label_predio = ctk.CTkLabel(frame_conteudo, text="Prédio Selecionado: Nenhum", font=("Arial", 14, "bold"))
        label_predio.pack(pady=10)
        label_predio.configure(text=f"Prédio Selecionado: {prédio_selecionado}")
        
        ctk.CTkLabel(frame_conteudo, text="Lançar Despesas", font=("Arial", 18, "bold")).pack(pady=10)
        
        ctk.CTkLabel(frame_conteudo, text="Valor da Despesa:").pack(pady=5)
        campo_valor_despesa = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: 100,00", width=200)
        campo_valor_despesa.pack(pady=5)
        
        ctk.CTkLabel(frame_conteudo, text="Categoria:").pack(pady=5)
        combo_categoria_despesa = ctk.CTkComboBox(frame_conteudo, values=categorias_despesas)
        combo_categoria_despesa.pack(pady=5)

        # Checkbox para despesa dividida
        dividir_despesa_var = ctk.BooleanVar()
        check_dividir_despesa = ctk.CTkCheckBox(frame_conteudo, text="Despesa dividida entre os prédios?", variable=dividir_despesa_var)
        check_dividir_despesa.pack(pady=5)
        
        # Campos de porcentagem
        frame_porcentagem = ctk.CTkFrame(frame_conteudo)
        
        ctk.CTkLabel(frame_porcentagem, text="GV (%):").pack(side="left", padx=5)
        campo_porcentagem_gv = ctk.CTkEntry(frame_porcentagem, width=50)
        campo_porcentagem_gv.pack(side="left", padx=5)

        ctk.CTkLabel(frame_porcentagem, text="JLP (%):").pack(side="left", padx=5)
        campo_porcentagem_jlp = ctk.CTkEntry(frame_porcentagem, width=50)
        campo_porcentagem_jlp.pack(side="left", padx=5)

        frame_porcentagem.pack(pady=5)
        frame_porcentagem.pack_forget()  # Esconde o frame inicialmente

        # Atualiza a visibilidade do campo de porcentagem
        def toggle_campos_porcentagem():
            if dividir_despesa_var.get():
                frame_porcentagem.pack(pady=5)
            else:
                frame_porcentagem.pack_forget()

        check_dividir_despesa.configure(command=toggle_campos_porcentagem)

        def salvar_despesa():
            valor = campo_valor_despesa.get().strip()
            categoria = combo_categoria_despesa.get()

            if not valor or not categoria:
                label_status_lancamento.configure(text="Preencha todos os campos corretamente.", text_color="red")
                return
            
            valor = float(valor.replace(",", "."))  # Converte para número

            if dividir_despesa_var.get():
                try:
                    porcentagem_gv = float(campo_porcentagem_gv.get().strip())
                    porcentagem_jlp = float(campo_porcentagem_jlp.get().strip())

                    if porcentagem_gv + porcentagem_jlp != 100:
                        label_status_lancamento.configure(text="As porcentagens devem somar 100%.", text_color="red")
                        return

                    valor_gv = round(valor * (porcentagem_gv / 100), 2)
                    valor_jlp = round(valor * (porcentagem_jlp / 100), 2)

                    # Salva nos dois prédios com os valores divididos
                    # Modificando a chamada para incluir "Não existe" no lugar do inquilino
                    salvar_lancamento_em_excel("Despesa", valor_gv, categoria, "GV", " ", 0, mes_usuario)
                    salvar_lancamento_em_excel("Despesa", valor_jlp, categoria, "JLP", " ", 0, mes_usuario)


                    label_status_lancamento.configure(
                        text=f"Despesa de R${valor} dividida entre os prédios: GV ({porcentagem_gv}%) e JLP ({porcentagem_jlp}%) registrada!",
                        text_color="green"
                    )
                except ValueError:
                    label_status_lancamento.configure(text="Insira valores válidos para as porcentagens.", text_color="red")
                    return
            else:
                salvar_lancamento_em_excel("Despesa", valor, categoria, prédio_selecionado, " ", 0, mes_usuario)
                label_status_lancamento.configure(
                    text=f"Despesa de R${valor} na categoria '{categoria}', no prédio {prédio_selecionado} registrada!",
                    text_color="green"
                )

        ctk.CTkButton(frame_conteudo, text="Registrar Despesa", command=salvar_despesa).pack(pady=10)

        label_status_lancamento = ctk.CTkLabel(frame_conteudo, text="", font=("Arial", 12))
        label_status_lancamento.pack(pady=5)


    elif tipo == "lancar_receitas":
        # Chama a função para carregar os inquilinos antes de renderizar o ComboBox
        carregar_inquilinos()

        label_predio = ctk.CTkLabel(frame_conteudo, text="Prédio Selecionado: Nenhum", font=("Arial", 14, "bold"))
        label_predio.pack(pady=10)
        label_predio.configure(text=f"Prédio Selecionado: {prédio_selecionado}")
        
        ctk.CTkLabel(frame_conteudo, text="Lançar Receita", font=("Arial", 18, "bold")).pack(pady=10)
        
        ctk.CTkLabel(frame_conteudo, text="Valor da Receita:").pack(pady=5)
        campo_valor_receita = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: 1500,00", width=200)
        campo_valor_receita.pack(pady=5)
        
        ctk.CTkLabel(frame_conteudo, text="Categoria:").pack(pady=5)
        combo_categoria_receita = ctk.CTkComboBox(frame_conteudo, values=categorias_receitas)
        combo_categoria_receita.pack(pady=5)

        # ComboBox para selecionar o inquilino
        ctk.CTkLabel(frame_conteudo, text="Inquilino:").pack(pady=5)
        combo_inquilino = ctk.CTkComboBox(frame_conteudo, values=[inquilino['nome'] for inquilino in inquilinos])
        combo_inquilino.pack(pady=5)
        
        # Checkbox para dividir a receita
        dividir_receita_var = ctk.BooleanVar()
        check_dividir_receita = ctk.CTkCheckBox(frame_conteudo, text="Receita dividida entre os prédios?", variable=dividir_receita_var)
        check_dividir_receita.pack(pady=5)
        
        # Campos de porcentagem
        frame_porcentagem = ctk.CTkFrame(frame_conteudo)
        
        ctk.CTkLabel(frame_porcentagem, text="GV (%):").pack(side="left", padx=5)
        campo_porcentagem_gv = ctk.CTkEntry(frame_porcentagem, width=50)
        campo_porcentagem_gv.pack(side="left", padx=5)

        ctk.CTkLabel(frame_porcentagem, text="JLP (%):").pack(side="left", padx=5)
        campo_porcentagem_jlp = ctk.CTkEntry(frame_porcentagem, width=50)
        campo_porcentagem_jlp.pack(side="left", padx=5)

        frame_porcentagem.pack(pady=5)
        frame_porcentagem.pack_forget()  # Esconde o frame inicialmente

        # Atualiza a visibilidade do campo de porcentagem
        def toggle_campos_porcentagem():
            if dividir_receita_var.get():
                frame_porcentagem.pack(pady=5)
            else:
                frame_porcentagem.pack_forget()

        check_dividir_receita.configure(command=toggle_campos_porcentagem)

        def salvar_receita():
            valor = campo_valor_receita.get().strip()
            categoria = combo_categoria_receita.get()
            inquilino_selecionado = combo_inquilino.get()  # Recupera o nome do inquilino

            if not valor or not categoria or not inquilino_selecionado:
                label_status_lancamento.configure(text="Preencha todos os campos corretamente.", text_color="red")
                return
            
            valor = float(valor.replace(",", "."))  # Converte para número

            if dividir_receita_var.get():
                try:
                    porcentagem_gv = float(campo_porcentagem_gv.get().strip())
                    porcentagem_jlp = float(campo_porcentagem_jlp.get().strip())

                    if porcentagem_gv + porcentagem_jlp != 100:
                        label_status_lancamento.configure(text="As porcentagens devem somar 100%.", text_color="red")
                        return

                    valor_gv = round(valor * (porcentagem_gv / 100), 2)
                    valor_jlp = round(valor * (porcentagem_jlp / 100), 2)

                    # Salva nos dois prédios com os valores divididos
                    salvar_lancamento_em_excel("Receita", valor_gv, categoria, "GV", inquilino_selecionado, 0, mes_usuario)  # Passando inquilino e saldo inicial
                    salvar_lancamento_em_excel("Receita", valor_jlp, categoria, "JLP", inquilino_selecionado, 0, mes_usuario)  # Passando inquilino e saldo inicial

                    label_status_lancamento.configure(
                        text=f"Receita de R${valor} dividida entre os prédios: GV ({porcentagem_gv}%) e JLP ({porcentagem_jlp}%) registrada!",
                        text_color="green"
                    )
                except ValueError:
                    label_status_lancamento.configure(text="Insira valores válidos para as porcentagens.", text_color="red")
                    return
            else:
                saldo_inicial = 0  # Ajuste o saldo inicial conforme necessário
                salvar_lancamento_em_excel("Receita", valor, categoria, prédio_selecionado, inquilino_selecionado, saldo_inicial, mes_usuario)
                label_status_lancamento.configure(
                    text=f"Receita de R${valor} na categoria '{categoria}', no prédio {prédio_selecionado} registrada!",
                    text_color="green"
                )

        ctk.CTkButton(frame_conteudo, text="Registrar Receita", command=salvar_receita).pack(pady=10)

        label_status_lancamento = ctk.CTkLabel(frame_conteudo, text="", font=("Arial", 12))
        label_status_lancamento.pack(pady=5)



    elif tipo == "transferir_receita":
        label_predio = ctk.CTkLabel(frame_conteudo, text="Prédio Selecionado: Nenhum", font=("Arial", 14, "bold"))
        label_predio.pack(pady=10)
        label_predio.configure(text=f"Prédio Selecionado: {prédio_selecionado}")
        """ Interface para transferência de receita entre prédios """
        ctk.CTkLabel(frame_conteudo, text="Transferir Receita", font=("Arial", 18, "bold")).pack(pady=10)
        
        ctk.CTkLabel(frame_conteudo, text="Valor:").pack(pady=5)
        campo_valor = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: 1000.00", width=200)
        campo_valor.pack(pady=5)
        
        ctk.CTkLabel(frame_conteudo, text="Origem:").pack(pady=5)
        combo_origem = ctk.CTkComboBox(frame_conteudo, values=["GV", "JLP"], width=200)
        combo_origem.pack(pady=5)
        
        ctk.CTkLabel(frame_conteudo, text="Destino:").pack(pady=5)
        combo_destino = ctk.CTkComboBox(frame_conteudo, values=["GV", "JLP"], width=200)
        combo_destino.pack(pady=5)
        
        ctk.CTkLabel(frame_conteudo, text="Observações (opcional):").pack(pady=5)
        campo_observacoes = ctk.CTkEntry(frame_conteudo, placeholder_text="Observações", width=200)
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
        
        ctk.CTkButton(frame_conteudo, text="Salvar", command=salvar).pack(pady=10)
        
        label_status = ctk.CTkLabel(frame_conteudo, text="", font=("Arial", 12))
        label_status.pack(pady=5)

#DASHBOARD
import re  # Para validar o formato YYYY-MM

import os
import re
import customtkinter as ctk
from tkinter import messagebox

def abrir_dashboard():
    """ Abre o menu para selecionar o mês e o prédio para exibir o dashboard """
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    ctk.CTkLabel(frame_conteudo, text="Selecionar Balancete", font=("Arial", 18, "bold")).pack(pady=10)

    ctk.CTkLabel(frame_conteudo, text="Digite o mês e ano (YYYY-MM):").pack(pady=5)
    campo_mes_ano = ctk.CTkEntry(frame_conteudo, placeholder_text="Ex: 2025-01", width=200)
    campo_mes_ano.pack(pady=5)

    ctk.CTkLabel(frame_conteudo, text="Selecione o prédio:").pack(pady=5)
    combo_predio = ctk.CTkComboBox(frame_conteudo, values=["GV", "JLP"])
    combo_predio.pack(pady=5)

    def carregar_balancete():
        mes_ano = campo_mes_ano.get().strip()
        predio = combo_predio.get()

        # Validação do formato YYYY-MM
        if not re.match(r"^\d{4}-\d{2}$", mes_ano):
            messagebox.showwarning("Erro", "Formato inválido! Use YYYY-MM.")
            return
        
        # Definir os nomes dos arquivos
        arquivo_predio = f"{predio}_{mes_ano}.xlsx"
        outro_predio = "GV" if predio == "JLP" else "JLP"
        arquivo_outro_predio = f"{outro_predio}_{mes_ano}.xlsx"
        arquivo_transferencias = "transferencias.xlsx"
        arquivo_socios = f"socios.xlsx"  # Adicionando arquivo dos sócios

        # Verificar se os arquivos existem
        arquivos_obrigatorios = [arquivo_predio, arquivo_socios]
        arquivos_faltando = [arq for arq in arquivos_obrigatorios if not os.path.exists(arq)]

        if arquivos_faltando:
            messagebox.showwarning("Erro", f"Os seguintes arquivos não foram encontrados:\n" + "\n".join(arquivos_faltando))
            return

        if not os.path.exists(arquivo_transferencias):
            # Cria um DataFrame vazio com as colunas desejadas
            colunas = ["Valor", "Origem", "Destino", "Observações", "Data"]
            df_transferencias = pd.DataFrame(columns=colunas)
            
            # Salva como Excel
            df_transferencias.to_excel(arquivo_transferencias, index=False)
            print(f"Arquivo '{arquivo_transferencias}' criado com sucesso!")

        # Agora carrega o arquivo normalmente
        df_transferencias = pd.read_excel(arquivo_transferencias)
        print("Arquivo carregado com sucesso!")
            

        # Se tudo estiver ok, exibir os dados no dashboard
        exibir_dashboard(mes_ano, predio, arquivo_predio, arquivo_outro_predio, arquivo_transferencias, arquivo_socios)

    ctk.CTkButton(frame_conteudo, text="Carregar Balancete", command=carregar_balancete).pack(pady=10)

    label_status = ctk.CTkLabel(frame_conteudo, text="", font=("Arial", 12))
    label_status.pack(pady=5)


def exibir_dashboard(mes_ano, predio, arquivo_predio, arquivo_outro_predio, arquivo_transferencias, arquivo_socios):
    """ Exibe o balancete com base nos arquivos Excel """
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    ctk.CTkLabel(frame_conteudo, text=f"Balancete - {predio} ({mes_ano})", font=("Arial", 18, "bold")).pack(pady=10)
    
    try:
        # Carregar os arquivos Excel
        df_predio = pd.read_excel(arquivo_predio, header=0)
        df_transferencias = pd.read_excel(arquivo_transferencias, header=0)
        df_socios = pd.read_excel(arquivo_socios, header=0)

        # Normalizar nomes das colunas
        df_predio.columns = df_predio.columns.str.strip().str.title()
        df_transferencias.columns = df_transferencias.columns.str.strip().str.title()
        df_socios.columns = df_socios.columns.str.strip().str.title()

        # Converter valores para float
        df_predio["Valor"] = pd.to_numeric(df_predio["Valor"], errors="coerce").fillna(0)
        df_transferencias["Valor"] = pd.to_numeric(df_transferencias["Valor"], errors="coerce").fillna(0)
        df_socios["Porcentagem"] = pd.to_numeric(df_socios["Porcentagem"], errors="coerce").fillna(0) / 100

        # Calcular totais de receita e despesa
        receita_total = df_predio[df_predio["Tipo"].str.upper() == "RECEITA"]["Valor"].sum()
        despesa_total = df_predio[df_predio["Tipo"].str.upper() == "DESPESA"]["Valor"].sum()
        
        # Verificar se há um "Saldo Inicial" no mês anterior (coluna 5)
        # Verificar se há um "Saldo Inicial" no mês anterior (coluna 5)
        saldo_inicial = df_predio.iloc[0, 4] if df_predio.shape[1] > 4 and pd.notna(df_predio.iloc[0, 4]) else 0
        saldo_final = receita_total - despesa_total + saldo_inicial

        # Inicializar saldo_restante com o saldo final
        saldo_restante = saldo_final

        # Exibir resumo financeiro
        ctk.CTkLabel(frame_conteudo, text=f"Receita Total: R${receita_total:,.2f}", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(frame_conteudo, text=f"Despesa Total: R${despesa_total:,.2f}", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(frame_conteudo, text=f"Saldo Inicial: R${saldo_inicial:,.2f}", font=("Arial", 14), text_color="blue").pack(pady=10)
        ctk.CTkLabel(frame_conteudo, text=f"Saldo Final: R${saldo_final:,.2f}", font=("Arial", 16, "bold"), 
                     text_color="green" if saldo_final >= 0 else "red").pack(pady=10)

        # Exibir transferências
        df_transferencias["Data"] = pd.to_datetime(df_transferencias["Data"], dayfirst=True, errors="coerce")
        df_transferencias_filtradas = df_transferencias[df_transferencias["Data"].dt.strftime("%Y-%m") == mes_ano]
        df_transferencias_filtradas = df_transferencias_filtradas[ 
            (df_transferencias_filtradas["Origem"] == predio) | (df_transferencias_filtradas["Destino"] == predio)
        ]

        # Exibir transferências
        if not df_transferencias_filtradas.empty:
            ctk.CTkLabel(frame_conteudo, text="Transferências no período:", font=("Arial", 14, "bold")).pack(pady=10)
            for _, row in df_transferencias_filtradas.iterrows():
                ctk.CTkLabel(frame_conteudo, text=f"{row['Origem']} transferiu R${row['Valor']:,.2f} para {row['Destino']}",
                             font=("Arial", 12)).pack(pady=2)
        else:
            ctk.CTkLabel(frame_conteudo, text="Nenhuma transferência registrada.", font=("Arial", 12)).pack(pady=5)

        # Verificar se o saldo é negativo e perguntar ao usuário
        if saldo_final < 0:
            ctk.CTkLabel(frame_conteudo, text="Saldo negativo! Deseja usar esse saldo como saldo inicial para o próximo mês?", font=("Arial", 14, "bold")).pack(pady=10)
            distribui_frame = ctk.CTkFrame(frame_conteudo)
            distribui_frame.pack(pady=10)

            def confirmar_distribuicao_negativa():
                # Atualizar saldo inicial no arquivo do próximo mês com saldo negativo
                mes_ano_proximo = (pd.to_datetime(mes_ano, format="%Y-%m") + pd.DateOffset(months=1)).strftime("%Y-%m")
                arquivo_proximo_mes = f"{predio}_{mes_ano_proximo}.xlsx"
                colunas_esperadas = ["Tipo", "Categoria", "Valor", "Data", "Saldo Inicial"]
                
                if not os.path.exists(arquivo_proximo_mes):
                    novo_df = pd.DataFrame({
                        "Tipo": ["Saldo Inicial"],
                        "Categoria": ["Inicial"],
                        "Valor": [saldo_restante],
                        "Data": [pd.to_datetime(f"{mes_ano_proximo}-01")],
                        "Saldo Inicial": [saldo_restante]
                    })
                    novo_df.to_excel(arquivo_proximo_mes, index=False)
                else:
                    df_proximo_mes = pd.read_excel(arquivo_proximo_mes, header=0)
                    df_proximo_mes.columns = df_proximo_mes.columns.str.strip().str.title()
                    if df_proximo_mes.shape[1] > 4:
                        df_proximo_mes.iloc[0, 4] = saldo_restante
                        df_proximo_mes.to_excel(arquivo_proximo_mes, index=False)

                messagebox.showinfo("Saldo Inicial", f"O saldo inicial de {predio} para o próximo mês ({mes_ano_proximo}) é R${saldo_restante:,.2f}.")
            
            ctk.CTkButton(distribui_frame, text="Confirmar Transferência de Saldo Negativo", command=confirmar_distribuicao_negativa).pack(pady=5)

        # Caso o saldo seja positivo, exibe a opção de distribuir entre os sócios
        elif saldo_final > 0:
            # Criar interface bonita para a entrada de valor
            distribui_frame = ctk.CTkFrame(frame_conteudo)
            distribui_frame.pack(pady=10)

            ctk.CTkLabel(distribui_frame, text="Quanto deseja distribuir?", font=("Arial", 14)).pack(pady=5)

            valor_distribuicao_entry = ctk.CTkEntry(distribui_frame, placeholder_text=f"Saldo Final: R${saldo_final:,.2f}")
            valor_distribuicao_entry.pack(pady=5)

            def confirmar_distribuicao():
                try:
                    valor_distribuicao = float(valor_distribuicao_entry.get())
                    if 0 < valor_distribuicao <= saldo_final:
                        # Filtrar sócios do prédio atual
                        socios_predio = df_socios[df_socios["Prédio"] == predio]

                        if not socios_predio.empty:
                            ctk.CTkLabel(frame_conteudo, text="Distribuição entre sócios:", font=("Arial", 14, "bold")).pack(pady=10)

                            # Exibir os sócios em formato de "tabela"
                            header_frame = ctk.CTkFrame(frame_conteudo)
                            header_frame.pack(pady=5)

                            ctk.CTkLabel(header_frame, text="Nome", width=20).pack(side="left", padx=10)
                            ctk.CTkLabel(header_frame, text="Porcentagem", width=20).pack(side="left", padx=10)
                            ctk.CTkLabel(header_frame, text="Valor a Receber", width=20).pack(side="left", padx=10)

                            for _, row in socios_predio.iterrows():
                                socio_frame = ctk.CTkFrame(frame_conteudo)
                                socio_frame.pack(pady=5)

                                ctk.CTkLabel(socio_frame, text=row['Nome'], width=20).pack(side="left", padx=10)
                                ctk.CTkLabel(socio_frame, text=f"{row['Porcentagem'] * 100:.2f}%", width=20).pack(side="left", padx=10)
                                valor_socio = valor_distribuicao * row["Porcentagem"]
                                ctk.CTkLabel(socio_frame, text=f"R${valor_socio:,.2f}", width=20).pack(side="left", padx=10)

                            saldo_restante = saldo_final - valor_distribuicao
                            ctk.CTkLabel(frame_conteudo, text=f"Saldo restante: R${saldo_restante:,.2f}", font=("Arial", 14, "bold"), text_color="blue").pack(pady=10)

                            # Atualizar saldo inicial no arquivo do próximo mês
                            mes_ano_proximo = (pd.to_datetime(mes_ano, format="%Y-%m") + pd.DateOffset(months=1)).strftime("%Y-%m")
                            arquivo_proximo_mes = f"{predio}_{mes_ano_proximo}.xlsx"
                            
                            # Criar ou atualizar o arquivo do próximo mês com a estrutura solicitada
                            if not os.path.exists(arquivo_proximo_mes):
                                novo_df = pd.DataFrame({
                                    "Tipo": ["Saldo Inicial"],
                                    "Categoria": ["Inicial"],
                                    "Valor": [saldo_restante],
                                    "Data": [pd.to_datetime(f"{mes_ano_proximo}-01")],
                                    "Saldo Inicial": [saldo_restante]
                                })
                                novo_df.to_excel(arquivo_proximo_mes, index=False)
                            else:
                                df_proximo_mes = pd.read_excel(arquivo_proximo_mes, header=0)
                                df_proximo_mes.columns = df_proximo_mes.columns.str.strip().str.title()
                                if df_proximo_mes.shape[1] > 4:
                                    df_proximo_mes.iloc[0, 4] = saldo_restante
                                    df_proximo_mes.to_excel(arquivo_proximo_mes, index=False)

                            messagebox.showinfo("Saldo Inicial", f"O saldo inicial de {predio} para o próximo mês ({mes_ano_proximo}) é R${saldo_restante:,.2f}.")
                        else:
                            ctk.CTkLabel(frame_conteudo, text="Nenhum sócio cadastrado para este prédio.", font=("Arial", 12)).pack(pady=5)
                    else:
                        messagebox.showwarning("Valor inválido", f"O valor a ser distribuído deve ser entre 0 e R${saldo_final:,.2f}")
                except ValueError:
                    messagebox.showwarning("Valor inválido", "Por favor, insira um valor válido para distribuição.")

            ctk.CTkButton(distribui_frame, text="Confirmar Distribuição", command=confirmar_distribuicao).pack(pady=5)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar os arquivos: {e}")




# Agora, nos botões, você chama a função de atualização de acordo com o tipo:
ctk.CTkButton(frame_menu, text="Adicionar Categoria (Despesa)", command=lambda: atualizar_menu_categorias("adicionar_despesa"), width=180).pack(pady=10)
ctk.CTkButton(frame_menu, text="Excluir Categoria (Despesa)", command=lambda: atualizar_menu_categorias("excluir_despesa"), width=180).pack(pady=10)
ctk.CTkButton(frame_menu, text="Adicionar Categoria (Receita)", command=lambda: atualizar_menu_categorias("adicionar_receita"), width=180).pack(pady=10)
ctk.CTkButton(frame_menu, text="Excluir Categoria (Receita)", command=lambda: atualizar_menu_categorias("excluir_receita"), width=180).pack(pady=10)
botao_lancar_despesas = ctk.CTkButton(frame_menu, text="Lançar Despesas", command=lambda: atualizar_lancamento("lancar_despesas"), state="disabled", width=180)
botao_lancar_despesas.pack(pady=10)

botao_lancar_receitas = ctk.CTkButton(frame_menu, text="Lançar Receitas", command=lambda: atualizar_lancamento("lancar_receitas"), state="disabled", width=180)
botao_lancar_receitas.pack(pady=10)

botao_transferir_receita = ctk.CTkButton(frame_menu, text="Transferir Receita", command=lambda: atualizar_lancamento("transferir_receita"), state="disabled", width=180)
ctk.CTkButton(frame_menu, text="Carregar Sócios", command=carregar_socios, width=180).pack(pady=10)
ctk.CTkButton(frame_menu, text="Atualizar Rateio", command=atualizar_menu_rateio, width=180).pack(pady=10)
btn_dashboard = ctk.CTkButton(frame_menu, text="Visualizar Dashboard", command=abrir_dashboard, width=180).pack(pady=10)
ctk.CTkButton(frame_menu, text="Cadastrar Novo Inquilino", command=exibir_formulario_cadastro_inquilino, width=180).pack(pady=10)
ctk.CTkButton(frame_menu, text="Alterar Aluguel", command=exibir_formulario_alteracao_aluguel, width=180).pack(pady=10)
label_instrucoes = ctk.CTkLabel(frame_menu, text="Por favor, insira o mês de lançamento (Formato: YYYY-MM):")
label_instrucoes.pack(pady=10)
entry_mes = ctk.CTkEntry(frame_menu)
entry_mes.pack(pady=10)
botao_confirmar = ctk.CTkButton(frame_menu, text="Confirmar Mês", command=confirmar_mes)
botao_confirmar.pack(pady=10)



# Área de conteúdo principal
frame_conteudo = ctk.CTkFrame(root)
frame_conteudo.pack(side="right", fill="both", expand=True, padx=20, pady=20)

label_predio = ctk.CTkLabel(frame_conteudo, text="Prédio Selecionado: Nenhum", font=("Arial", 14, "bold"))
label_predio.pack(pady=10)



#LOGICA DE RATEIO ENTRE OS SOCIOS


# Loop da aplicação
root.mainloop()

