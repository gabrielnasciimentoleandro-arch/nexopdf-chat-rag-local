"""Gera os PDFs autorais usados na base de demonstração.

Execute a partir da raiz do projeto:
    python scripts/generate_sample_pdfs.py
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "inputs"

DOCUMENTS = {
    "uso_responsavel_ia_tcc.pdf": {
        "title": "Uso responsável de inteligência artificial no TCC",
        "subtitle": "Guia prático para estudantes e orientadores",
        "sections": [
            (
                "1. A IA como ferramenta de apoio",
                [
                    "Os principais cuidados ao usar IA no TCC são manter a autoria humana, verificar afirmações em fontes confiáveis, respeitar as regras da instituição, registrar como a ferramenta foi usada e proteger dados pessoais ou sigilosos. Esses cuidados devem acompanhar todo o trabalho, do planejamento à revisão final.",
                    "Ferramentas de inteligência artificial podem apoiar a organização de ideias, a exploração inicial de um tema, a revisão de clareza e a comparação entre conceitos. Elas não substituem a autoria intelectual do estudante. O argumento central, as decisões metodológicas, a interpretação dos resultados e as conclusões devem permanecer sob responsabilidade humana.",
                    "Antes de utilizar uma resposta gerada por IA, o estudante deve conferir cada afirmação em fontes confiáveis. Modelos podem produzir informações plausíveis, porém incorretas, referências inexistentes ou interpretações fora de contexto. A revisão humana não é uma etapa opcional: ela é o principal mecanismo de controle de qualidade.",
                ],
            ),
            (
                "2. Transparência e integridade acadêmica",
                [
                    "O uso de IA deve respeitar as regras da instituição e as orientações do professor ou orientador. Quando a ferramenta tiver participação relevante, recomenda-se registrar sua finalidade, a data de uso, o modelo empregado e as etapas que receberam revisão humana. Esse registro permite explicar como o trabalho foi produzido e aumenta a transparência.",
                    "Uma resposta de chatbot não deve ser tratada automaticamente como fonte científica. Sempre que uma ideia depender de evidência externa, o estudante deve localizar, ler e citar a publicação original. A IA pode ajudar a encontrar termos de busca ou resumir um texto já fornecido, mas a citação deve apontar para a fonte efetivamente consultada.",
                ],
            ),
            (
                "3. Rastreabilidade do processo",
                [
                    "Um diário de pesquisa simples pode registrar pergunta, objetivo, documentos usados, resultado obtido, verificação realizada e decisão tomada. Também é útil salvar versões dos textos e manter uma tabela que conecte cada afirmação importante à sua fonte. Esse procedimento cria uma trilha de auditoria e facilita as conversas com a orientação.",
                    "Prompts e respostas não precisam ocupar o corpo do TCC, mas podem ser preservados como material de trabalho quando forem importantes para reproduzir o processo. A rastreabilidade é especialmente relevante em revisões de literatura, classificação de estudos e análise de dados, pois permite revisar decisões depois.",
                ],
            ),
            (
                "4. Privacidade e dados sensíveis",
                [
                    "Documentos com dados pessoais, resultados ainda não publicados, contratos ou informações sigilosas não devem ser enviados a serviços externos sem autorização. Antes do uso, é necessário avaliar a política de dados da ferramenta. Quando possível, prefira processamento local, remova identificadores e aplique o princípio da minimização: compartilhar somente o necessário.",
                    "O estudante continua responsável pelo conteúdo entregue mesmo quando utiliza IA. Uma prática segura combina propósito definido, fontes verificáveis, revisão crítica, transparência, proteção de dados e validação final pelo autor.",
                ],
            ),
        ],
    },
    "metodologia_revisao_tcc.pdf": {
        "title": "Revisão de literatura em Engenharia de Software",
        "subtitle": "Um fluxo reproduzível para trabalhos acadêmicos",
        "sections": [
            (
                "1. Definição da pergunta",
                [
                    "Uma revisão começa com uma pergunta clara e delimitada. A pergunta deve indicar o fenômeno de interesse, o contexto e, quando pertinente, a população, a intervenção e os resultados observados. Termos vagos tornam a busca difícil de reproduzir e aumentam o risco de selecionar estudos apenas por conveniência.",
                    "Após formular a pergunta, o pesquisador define palavras-chave, sinônimos e traduções. Em Engenharia de Software, nomes de técnicas e tecnologias mudam rapidamente; por isso, convém testar a estratégia de busca em diferentes bases e verificar se ela recupera alguns estudos previamente conhecidos.",
                ],
            ),
            (
                "2. Protocolo e critérios",
                [
                    "O protocolo descreve bases consultadas, expressão de busca, período, idiomas, tipos de publicação e critérios de inclusão e exclusão. Ele deve ser escrito antes da seleção principal. Essa antecipação reduz decisões oportunistas e cria um referencial para resolver dúvidas durante a triagem.",
                    "Os critérios devem ser aplicáveis de forma consistente. Por exemplo, incluir estudos que avaliem uma técnica em projetos reais é mais verificável do que incluir estudos considerados relevantes. Uma amostra de artigos pode ser avaliada por duas pessoas para alinhar o entendimento dos critérios.",
                ],
            ),
            (
                "3. Seleção e extração de dados",
                [
                    "A seleção costuma ocorrer em etapas: remoção de duplicatas, leitura de título e resumo e, por fim, leitura do texto completo. Em cada exclusão feita na etapa de texto completo, o motivo deve ser registrado. O conjunto final precisa ser rastreável desde o resultado bruto da busca.",
                    "Um formulário de extração ajuda a manter consistência. Ele pode conter identificação do estudo, objetivo, contexto, tamanho da amostra, método, métricas, resultados e limitações. Campos de texto livre são úteis, mas categorias definidas previamente tornam comparações mais seguras.",
                ],
            ),
            (
                "4. Síntese e análise crítica",
                [
                    "A síntese não é apenas uma coleção de resumos. O pesquisador deve comparar resultados, identificar convergências e divergências, observar diferenças de contexto e avaliar a força das evidências. Conclusões precisam refletir as limitações dos estudos e do próprio processo de revisão.",
                    "Ferramentas de IA podem auxiliar na busca dentro dos textos e na organização preliminar, desde que cada trecho permaneça ligado ao documento e à página de origem. Decisões de inclusão, interpretação e síntese exigem revisão humana. O registro dessas decisões aumenta a reprodutibilidade.",
                ],
            ),
        ],
    },
    "privacidade_e_qualidade_dados.pdf": {
        "title": "Privacidade e qualidade de dados em assistentes de pesquisa",
        "subtitle": "Controles essenciais para sistemas baseados em documentos",
        "sections": [
            (
                "1. Processamento local e minimização",
                [
                    "Um sistema local reduz a exposição de documentos porque extração, indexação e busca ocorrem no computador do usuário. Isso não elimina todos os riscos: arquivos temporários, cópias de segurança, registros de aplicação e acesso ao equipamento também devem ser considerados.",
                    "A minimização de dados recomenda coletar e manter apenas o necessário para a finalidade declarada. Antes de indexar uma base, remova documentos irrelevantes, anonimize dados pessoais quando possível e defina por quanto tempo o índice será mantido.",
                ],
            ),
            (
                "2. Qualidade da recuperação",
                [
                    "Sistemas de busca vetorial dividem documentos em trechos e transformam cada trecho em uma representação numérica. A pergunta recebe uma representação compatível e o sistema calcula similaridade para recuperar passagens relacionadas. O tamanho do trecho e sua sobreposição influenciam a quantidade de contexto disponível.",
                    "Similaridade alta não prova que um trecho contém a resposta correta. Ela apenas indica proximidade segundo o método de representação. Por esse motivo, a interface deve mostrar as fontes recuperadas, e o usuário deve poder abrir o documento original para confirmar significado, escopo e contexto.",
                ],
            ),
            (
                "3. Respostas fundamentadas",
                [
                    "Na arquitetura conhecida como geração aumentada por recuperação, ou RAG, o sistema recupera trechos antes de solicitar uma resposta ao modelo de linguagem. O prompt deve orientar o modelo a usar somente o contexto fornecido e a admitir quando a base não contiver informação suficiente.",
                    "Citações por arquivo e página aumentam a auditabilidade, mas não garantem correção por si sós. É necessário verificar se a afirmação realmente está apoiada pelo trecho citado. Uma resposta de qualidade separa evidência documental, inferência e ausência de informação.",
                ],
            ),
            (
                "4. Limitações e monitoramento",
                [
                    "PDFs digitalizados podem não conter texto selecionável e exigir reconhecimento óptico de caracteres. Tabelas, fórmulas e layouts em múltiplas colunas também podem ser extraídos fora de ordem. O sistema deve informar essas limitações e evitar transmitir falsa confiança.",
                    "A avaliação pode combinar perguntas com respostas conhecidas, inspeção dos trechos recuperados e registro de falhas. Métricas técnicas devem ser acompanhadas de análise humana. Melhorias futuras incluem OCR, reranqueamento, filtros por metadados, índices persistentes e controle de acesso.",
                ],
            ),
        ],
    },
}


def footer(canvas, document) -> None:
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#E2E5EF"))
    canvas.line(2 * cm, 1.45 * cm, A4[0] - 2 * cm, 1.45 * cm)
    canvas.setFillColor(colors.HexColor("#68738A"))
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(A4[0] - 2 * cm, 1.05 * cm, f"Página {document.page}")
    canvas.restoreState()


def build_pdf(filename: str, document: dict) -> None:
    path = OUTPUT / filename
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=30,
        textColor=colors.HexColor("#17213A"),
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    subtitle = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#626D84"),
        alignment=TA_CENTER,
        spaceAfter=30,
    )
    heading = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#574BE1"),
        spaceBefore=12,
        spaceAfter=10,
    )
    body = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=17,
        textColor=colors.HexColor("#28344C"),
        spaceAfter=12,
        alignment=0,
    )
    note = ParagraphStyle(
        "NoteCustom",
        parent=body,
        fontSize=9,
        leading=14,
        textColor=colors.HexColor("#68738A"),
        borderColor=colors.HexColor("#E4E2FF"),
        borderWidth=0.8,
        borderPadding=10,
        backColor=colors.HexColor("#F5F4FF"),
    )

    pdf = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2 * cm,
        title=document["title"],
        author="Projeto NexoPDF",
        subject="Base de demonstração para busca vetorial e RAG",
    )
    story = [
        Spacer(1, 1.4 * cm),
        Paragraph(document["title"], title),
        Paragraph(document["subtitle"], subtitle),
        Paragraph(
            "Este material foi criado exclusivamente para demonstrar um chatbot local baseado em documentos. Não substitui as normas da instituição nem a orientação acadêmica.",
            note,
        ),
        PageBreak(),
    ]
    for index, (section, paragraphs) in enumerate(document["sections"]):
        story.append(Paragraph(section, heading))
        for paragraph in paragraphs:
            story.append(Paragraph(paragraph, body))
        if index == 1:
            story.append(Spacer(1, 8))
    pdf.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Gerado: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, content in DOCUMENTS.items():
        build_pdf(name, content)
