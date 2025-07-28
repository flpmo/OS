import streamlit as st
from datetime import datetime
from pdf_generator import gerar_pdf
import os

st.set_page_config(page_title="Ordem de Serviço - NF Auto Service")

st.title("📄 Gerador de Ordem de Serviço")

# Inicializa contagem de peças
if "num_pecas" not in st.session_state:
    st.session_state.num_pecas = 1

# Inicializa o caminho do PDF na sessão
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

with st.form("os_form"):

    st.header("🔧 Dados do cliente e veículo")
    nome = st.text_input("Nome do Cliente")
    telefone = st.text_input("Telefone")
    veiculo = st.text_input("Veículo")
    placa = st.text_input("Placa")
    km = st.text_input("KM")
    data_entrada = st.date_input("Data de Entrada", value=datetime.today())
    data_saida = st.date_input("Data de Saída", value=datetime.today())
    garantia = st.date_input("Garantia", value=datetime.today())

    st.header("🧾 Peças Utilizadas")

    # Botões para adicionar ou remover peças
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.form_submit_button("➕ Adicionar peça"):
            st.session_state.num_pecas += 1
    with col2:
        if st.session_state.num_pecas > 1:
            if st.form_submit_button("➖ Remover peça"):
                st.session_state.num_pecas -= 1

    pecas = []
    for i in range(st.session_state.num_pecas):
        desc = st.text_input(f"Descrição da peça {i+1}", key=f"peca_desc_{i}")
        preco = st.number_input(f"Preço da peça {i+1}", key=f"peca_preco_{i}", min_value=0.0, step=0.01)
        pecas.append({"descricao": desc, "preco": preco})

    st.header("🛠️ Mão de obra")
    mao_obra = st.text_area("Descrição da Mão de Obra")
    preco_total = st.number_input("Valor total", min_value=0.0, step=0.01)
    observacoes = st.text_area("Observações")

    gerar = st.form_submit_button("📥 Gerar PDF")

# Fora do form: processar geração e mostrar botão de download
if gerar:
    data = {
        "nome": nome,
        "telefone": telefone,
        "veiculo": veiculo,
        "placa": placa,
        "km": km,
        "data_entrada": data_entrada.strftime("%d/%m/%Y"),
        "data_saida": data_saida.strftime("%d/%m/%Y"),
        "garantia": garantia,
        "pecas": pecas,
        "mao_obra": mao_obra,
        "preco_total": preco_total,
        "observacoes": observacoes
    }

    pdf_path = gerar_pdf(data)
    st.session_state.pdf_path = pdf_path

# Exibir botão de download, se PDF tiver sido gerado
if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
    with open(st.session_state.pdf_path, "rb") as f:
        st.download_button(
            label="📄 Baixar PDF",
            data=f,
            file_name=os.path.basename(st.session_state.pdf_path),
            mime="application/pdf"
        )
