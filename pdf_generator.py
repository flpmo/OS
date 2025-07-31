from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        data = self.formatar_data()
        self.set_font("Arial", "I", 8)
        #self.set_text_color(100)
        self.cell(0, 5, f"São Paulo, {data}    ", ln=True, align="R")

        if os.path.exists("nf.png"):
            self.image("nf.png", 10, 8, 33)
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "NF Auto Service - Ordem de Serviço", ln=True, align="C")
        self.set_font("Arial", "", 9)
        self.cell(0, 5, "R. Rafael da Silva e Sousa, 470 - Cidade Líder", ln=True, align="C")
        self.cell(0, 5, "São Paulo - SP, 08280-090", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(100)
        self.cell(0, 10, "NF Auto Service  |  Instagram: @nf.autoservice_  |  Tel: (11) 2746-1887  |  Whatsapp: (11) 94747-8952  ", align="C")
        
    def formatar_data(self):
        meses = {
            1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
            5: "maio", 6: "junho", 7: "julho", 8: "agosto",
            9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
        }
        hoje = datetime.now()
        return f"{hoje.day} de {meses[hoje.month]} de {hoje.year}"

def gerar_pdf(dados):
    # ID incremental
    id_path = "last_id.txt"
    if os.path.exists(id_path):
        with open(id_path) as f:
            last_id = int(f.read().strip())
    else:
        last_id = 0
    new_id = str(last_id + 1).zfill(3)
    with open(id_path, "w") as f:
        f.write(str(new_id))

    data = datetime.now().strftime("%Y%m%d")
    filename = f"OS__{data}_{new_id}.pdf"

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_font("Arial", "", 12)

    # Cliente e Veículo
    pdf.cell(0, 10, f"Cliente: {dados['nome']}  |  Tel: {dados['telefone']}", ln=True)
    pdf.cell(0, 10, f"Veículo: {dados['veiculo']}  |  Placa: {dados['placa']}  |  KM: {dados['km']}", ln=True)
    pdf.cell(0, 10, f"Entrada: {dados['data_entrada']}  |  Saída: {dados['data_saida']}  |  Garantia: {dados['garantia']}", ln=True)

    pdf.ln(5)
    if dados["observacoes"]:
        pdf.multi_cell(0, 10, f"Observações: {dados['observacoes']}")

    # Tabela de peças
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(140, 10, "Descrição", border=1)
    pdf.cell(40, 10, "Preço (R$)", border=1, ln=True)
    pdf.set_font("Arial", "", 12)
    total = 0
    for peca in dados["pecas"]:
        descricao = peca.get("descricao", "").strip()
        preco = float(peca.get("preco", 0))
        try:
            preco_float = float(peca['preco'])
        except (ValueError, TypeError):
            preco_float = 0.0  # ou outro valor padrão ou erro

        pdf.cell(140, 10, descricao, border=1)
        pdf.cell(40, 10, f"{preco_float:.2f}", border=1, ln=True)
        total += preco_float

    # Mão de obra
    pdf.cell(140, 10, f"Mão de obra: {dados['mao_obra']}", border=1)

    try:
        mao_obra_val = float(dados.get('preco_total', 0))
    except (ValueError, TypeError):
        mao_obra_val = 0.0

    pdf.cell(40, 10, f"{mao_obra_val:.2f}", border=1, ln=True)
    total += mao_obra_val

    # Total
    pdf.set_font("Arial", "B", 12)
    pdf.cell(140, 10, "Total", border=1)
    pdf.cell(40, 10, f"{total:.2f}", border=1, ln=True)

    # Contato final
    pdf.ln(10)
    pdf.set_font("Arial", "", 10)
    
    pdf.multi_cell(180, 6, "Condições de Garantia: A garantia só terá validade, desde que sejam feitas as revisões pré-agendadas por esta oficina. A garantia perderá a validade se costatada qualquer manutenção feita por outro profissional que não seja desta oficina. É de responsabilidade do próprietário informar qualquer anormalidade do serviço, após ser executado. Havendo decisão do proprietário de prosseguir ou postergar os reparos ou danos apresentados posteriormente, o mesmo assume a responsabilidade e perda da garantia. Não há garantia para peça fornecida pelo cliente.\n\n");
    pdf.set_font("Arial", "B", 14)
    pdf.multi_cell(0, 6, "NF Auto Service")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, "Tel: (11) 2746-1887")
    pdf.cell(0, 6, "Whatsapp: (11) 94747-8952", ln=1, link="https://wa.me/5511947478952")
    pdf.cell(0, 6, "Instagram: @nf.autoservice_", ln=1, link="https://www.instagram.com/nf.autoservice_/")



    pdf.output(filename)
    return filename
