import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime


def obter_pasta_relatorios(tipo_relatorio):
    agora = datetime.now()

    meses = {
        1: "01-Janeiro",
        2: "02-Fevereiro",
        3: "03-Marco",
        4: "04-Abril",
        5: "05-Maio",
        6: "06-Junho",
        7: "07-Julho",
        8: "08-Agosto",
        9: "09-Setembro",
        10: "10-Outubro",
        11: "11-Novembro",
        12: "12-Dezembro"
    }

    pasta = os.path.join(
        "relatorios",
        str(agora.year),
        meses[agora.month], 
        tipo_relatorio
    )
     
    os.makedirs(pasta, exist_ok=True)
    return pasta


def gerar_relatorio_movimentos(movimentos):     
    
    agora = datetime.now()

    pasta = obter_pasta_relatorios("movimentos")

    nome_arquivo = os.path.join(
        pasta,
        f"movimentos_{agora.strftime('%d_%H%M%S')}.pdf"
    )


    pdf = canvas.Canvas(nome_arquivo, pagesize=A4)

    largura, altura = A4

    y = altura - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Relatório de Movimentações")

    y -= 40

    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawString(50, y, "Data")
    pdf.drawString(150, y, "Tipo")
    pdf.drawString(250, y, "Produto")
    pdf.drawString(450, y, "Qtd")

    y -= 20

    pdf.setFont("Helvetica", 10)

    for mov in movimentos:
        pdf.drawString(50, y, mov.date.strftime("%d/%m/%Y"))

        pdf.drawString(150, y, mov.movement_type)

        pdf.drawString(250, y, mov.product.name)

        pdf.drawString(450, y, str(mov.amount))

        y -= 18

        if y <= 50:
            pdf.showPage()

            y = altura - 50

    pdf.save()

    return nome_arquivo


def gerar_relatorio_produtos(produtos):

    agora = datetime.now()

    pasta = obter_pasta_relatorios("produtos")

    nome_arquivo = os.path.join(pasta, f"produtos_{agora.strftime('%Y%m%d_%H%M%S')}.pdf")

    pdf = canvas.Canvas(nome_arquivo, pagesize=A4
    )

    largura, altura = A4

    y = altura - 40

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(30, y, "RELATÓRIO DE PRODUTOS")

    y -= 20

    pdf.setFont("Helvetica", 10)
    pdf.drawString(30, y, f"Gerado em: {agora.strftime('%d/%m/%Y %H:%M')}"
    )

    y -= 30

    for produto in produtos:

        fornecedor = (produto.supplier.name if produto.supplier else "-")

        categoria = (produto.category.name if produto.category else "-")

        usuario = (produto.submission_user.username if produto.submission_user else "-")

        pdf.setFont("Helvetica-Bold", 11)

        pdf.drawString(30, y, produto.name)

        y -= 18

        pdf.setFont("Helvetica", 9)

        pdf.drawString(40, y, f"Código: {produto.code}")

        y -= 14

        pdf.drawString(40, y, f"Categoria: {categoria}")

        y -= 14

        pdf.drawString(40, y, f"Fornecedor: {fornecedor}")

        y -= 14

        pdf.drawString(40, y, f"Quantidade em estoque: {produto.amount}")

        y -= 14

        pdf.drawString(40, y, f"Preço Compra: R$ {produto.unity_purchase_price:.2f}")

        y -= 14

        pdf.drawString(40, y, f"Preço Venda: R$ {produto.unity_sale_price:.2f}")

        y -= 14

        pdf.drawString(40, y, f"Data Cadastro: {produto.submission_date.strftime('%d/%m/%Y %H:%M')}")

        y -= 14

        pdf.drawString(40, y, f"Cadastrado por: {usuario}")

        y -= 20

        pdf.line(30, y, 550, y)

        y -= 20

        if y <= 80:

            pdf.showPage()

            y = altura - 40

            pdf.setFont("Helvetica", 9)

    pdf.save()

    return nome_arquivo


def gerar_relatorio_fornecedores(fornecedores):

    agora = datetime.now()

    pasta = obter_pasta_relatorios("fornecedores")

    nome_arquivo = os.path.join(pasta, f"fornecedores_{agora.strftime('%Y%m%d_%H%M%S')}.pdf")

    pdf = canvas.Canvas(nome_arquivo, pagesize=A4)

    largura, altura = A4

    y = altura - 40

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(30, y, "RELATÓRIO DE FORNECEDORES")

    y -= 20

    pdf.setFont("Helvetica", 10)
    pdf.drawString(30, y, f"Gerado em: {agora.strftime('%d/%m/%Y %H:%M')}")

    y -= 30

    for fornecedor in fornecedores:

        pdf.setFont("Helvetica-Bold", 11)

        pdf.drawString(30, y, fornecedor.name)

        y -= 18

        pdf.setFont("Helvetica", 9)

        pdf.drawString(40, y, f"Contato: {fornecedor.contact}")

        y -= 14

        pdf.drawString(40, y, f"Email: {fornecedor.email}")

        y -= 14

        pdf.drawString(40, y, f"Descrição: {fornecedor.description}")

        y -= 14

        pdf.drawString(40, y, f"Data Cadastro: {fornecedor.create_at.strftime('%d/%m/%Y %H:%M')}")

        y -= 14

        y -= 20

        pdf.line(30, y, 550, y)

        y -= 20

        if y <= 80:

            pdf.showPage()

            y = altura - 40

            pdf.setFont("Helvetica", 9)

    pdf.save()

    return nome_arquivo


def gerar_relatorio_categorias(categorias):

    agora = datetime.now()

    pasta = obter_pasta_relatorios("categorias")

    nome_arquivo = os.path.join(pasta, f"categorias_{agora.strftime('%Y%m%d_%H%M%S')}.pdf")

    pdf = canvas.Canvas(nome_arquivo, pagesize=A4)

    largura, altura = A4

    y = altura - 40

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(30, y, "RELATÓRIO DE CATEGORIAS")

    y -= 20

    pdf.setFont("Helvetica", 10)
    pdf.drawString(30, y, f"Gerado em: {agora.strftime('%d/%m/%Y %H:%M')}")

    y -= 30

    for categoria in categorias:

        pdf.setFont("Helvetica-Bold", 11)

        pdf.drawString(30, y, categoria.name)

        y -= 18

        pdf.setFont("Helvetica", 9)

        pdf.drawString(40, y, f"Descrição: {categoria.description}")

        y -= 14

        pdf.drawString(40, y, f"Data Cadastro: {categoria.create_at.strftime('%d/%m/%Y %H:%M')}")

        y -= 14

        y -= 20

        pdf.line(30, y, 550, y)

        y -= 20

        if y <= 80:

            pdf.showPage()

            y = altura - 40

            pdf.setFont("Helvetica", 9)

    pdf.save()

    return nome_arquivo


def gerar_relatorio_usuarios(usuarios):

    agora = datetime.now()

    pasta = obter_pasta_relatorios("usuarios")

    nome_arquivo = os.path.join(pasta, f"usuarios_{agora.strftime('%Y%m%d_%H%M%S')}.pdf")

    pdf = canvas.Canvas(nome_arquivo, pagesize=A4)

    largura, altura = A4

    y = altura - 40

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(30, y, "RELATÓRIO DE USUÁRIOS")

    y -= 20

    pdf.setFont("Helvetica", 10)
    pdf.drawString(30, y, f"Gerado em: {agora.strftime('%d/%m/%Y %H:%M')}")

    y -= 30

    for usuario in usuarios:

        pdf.setFont("Helvetica-Bold", 11)

        pdf.drawString(30, y, usuario.full_name)

        y -= 18

        pdf.setFont("Helvetica", 9)

        pdf.drawString(40, y, f"Usuário: {usuario.username}")

        y -= 14
        
        pdf.drawString(40, y, f"Email: {usuario.email}")

        y -= 14
       
        pdf.drawString(40, y, f"Contato: {usuario.contact}")

        y -= 14
        pdf.drawString(40, y, f"Cargo: {usuario.position}")

        y -= 14
        pdf.drawString(40, y, f"Perfil: {usuario.role}")

        y -= 14

        pdf.drawString(40, y, f"Data Cadastro: {usuario.created_at.strftime('%d/%m/%Y %H:%M')}")

        y -= 20

        pdf.line(30, y, 550, y)

        y -= 20

        if y <= 80:

            pdf.showPage()

            y = altura - 40

            pdf.setFont("Helvetica", 9)

    pdf.save()

    return nome_arquivo 