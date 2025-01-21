from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.pagesizes import C7, inch, A4, landscape, portrait, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import utils, colors
from reportlab.lib.units import cm, mm

def gera_pdf(name, img, num, r, c, e, t):

    ROL = (100*mm, 80*mm)

    def myFirstPage(canvas, doc):
            canvas.saveState()
            canvas.rotate(90)
            canvas.restoreState()

    def pega_imagem(path, width=1*cm):
        img = utils.ImageReader(path)
        w,h = img.getSize()
        aspect = h / float(w)

        return Image(path, width=width, height=(width*aspect))

    # Cria a estrutura do documento
    doc = SimpleDocTemplate(
        "C:\\SORTEIODIGITAL\\cupons\\Cupom_{}.pdf".format(name), 
        pagesize=landscape(ROL),
        topMargin=0*mm,
        leftMargin=0*mm,
        rightMargin=0*mm,
        bottomMargin=0*mm,
        showBoundary=True
        )

    # lista para os elementos
    elementos = []

    # Estilo simples
    styleSheet = getSampleStyleSheet()

    styleCabecalho = ParagraphStyle(
        name='meuEstilo',
        parent=styleSheet['Normal'],
        fontName = 'Helvetica',
        fontSize=6,
        spaceBefore=0,
        spaceAfter=0,
        leading=3
    )

    styleFormulario = ParagraphStyle(
        name='meuEstilo',
        parent=styleSheet['Normal'],
        fontName = 'Helvetica',
        fontSize=14,
        spaceBefore=-4,
        spaceAfter=-4,
        leading=10
    )

    styleNumero = ParagraphStyle(
        name='meuEstilo',
        parent=styleSheet['Normal'],
        fontName = 'Helvetica',
        fontSize=9,
        spaceBefore=-4,
        spaceAfter=-4,
        leading=10
    )

    # Logo
    img = pega_imagem('{}'.format(img), width=2.5*cm) 

    cupom = Paragraph('''
        <para align=center spaceb=3><strong>CUPOM PROMOCIONAL</strong></para>
    ''', style=styleCabecalho)

    razao = Paragraph('''
    
        <para align=center spaceb=3><strong>Razão: {}.</strong></para>
    '''.format(r), style=styleCabecalho)

    cnpj = Paragraph('''
        <para align=center spaceb=3><strong>CNPJ: {}</strong></para>
    '''.format(c), style=styleCabecalho)

    endereco = Paragraph('''
        <para align=center spaceb=3><strong>Endereço: {}</strong></para>
    '''.format(e), style=styleCabecalho)

    fone = Paragraph('''
        <para align=center spaceb=3><strong>Telefone: {}</strong></para>
    '''.format(t), style=styleCabecalho)

    numero = Paragraph('''
        <strong>Nº: {}</strong>
    '''.format(num), style=styleNumero)

    nome = Paragraph('''
        <strong>Nome: </strong>
    ''', style=styleFormulario)

    cpf = Paragraph('''
        <strong>CPF: </strong>
    ''', style=styleFormulario)

    rg = Paragraph('''
        <strong>RG: </strong>
    ''', style=styleFormulario)

    endereco2 = Paragraph('''
        <strong>Endereço: </strong>
    ''', style=styleFormulario)

    fone2 = Paragraph('''
        <strong>Telefone: </strong>
    ''', style=styleFormulario)

    dataLogo = [
        [img],
        [cupom],
    ]

    dataCabecalho = [    
        [razao],
        [cnpj],    
        [endereco],
        [fone]
    ]


    dataFormulario = [
        [numero],
        [''],
        [nome],
        [cpf],
        [rg],
        [endereco2],
        [fone2],
    ]

    dataTudo = [
        [dataLogo],
        [dataCabecalho],
    ]

    tableStyle = [
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]

    tableFormularioStyle = [
        
        ('LINEBELOW', (0,2), (-1,-1), 1, colors.black),        
    ]
    
    
    table = Table(
        dataTudo, 
        colWidths=[100*mm],
        style=tableStyle
    )

    tableFormulario = Table(
        dataFormulario,
        colWidths=[100*mm],
        rowHeights=[3*mm,1*mm,7*mm,7*mm,7*mm,7*mm,7*mm],        
        style=tableFormularioStyle
    )

    elementos.append(table)
    elementos.append(tableFormulario)
    doc.build(elementos, onFirstPage=myFirstPage)

# if __name__ == '__main__':
#     gera_pdf("{}".format(str(155)), "C:\\SORTEIODIGITAL\\static\\logo.jpeg","L & G ALIMENTOS DO BRASIL LTDA", "26.554.435/0001-71","Av. Antônio da Rocha Viana, R. Isaura Parente. Rio Branco - AC.","(68) 3223-5115")
    