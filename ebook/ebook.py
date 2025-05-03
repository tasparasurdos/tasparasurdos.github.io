import pandas as pd
import os
import subprocess
import shutil
import datetime

def generate_ebook(url_tecnologias=None, url_recursos=None):
    # URLs padrão (usadas se não fornecidas)
    if url_tecnologias is None:
        url_tecnologias = 'https://docs.google.com/spreadsheets/d/1g-zamZFp5FHTGxZOA0vT3ULXjwROhWS0mz0_K1xTvXc/export?format=csv'
    if url_recursos is None:
        url_recursos = 'https://docs.google.com/spreadsheets/d/1lePYinFlYePVYPwwUqy1Xa1r1FF_l3vaAkRxntSvWq4/export?format=csv'

    # Definir diretórios
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    docs_dir = os.path.join(base_dir, 'docs')
    output_dir = os.path.join(docs_dir, 'ebook')
    tmp_dir = os.path.join(base_dir, 'ebook', '.tmp')
    os.makedirs(output_dir, exist_ok=True)

    # Limpar arquivos antigos
    output_pdf = os.path.join(output_dir, 'ebook.pdf')
    if os.path.exists(output_pdf):
        os.remove(output_pdf)
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

    # Copiar capa.png para o diretório temporário
    capa_src = os.path.join(base_dir, 'ebook', 'conteudos', 'capa.png')
    capa_dst = os.path.join(tmp_dir, 'capa.png')
    if os.path.exists(capa_src):
        shutil.copy(capa_src, capa_dst)
        print(f"Imagem 'capa.png' copiada para {tmp_dir}")
    else:
        print(f"Erro: Imagem 'capa.png' não encontrada em {capa_src}")
        exit(1)

    # Copiar categoria.png para o diretório temporário
    categoria_src = os.path.join(base_dir, 'ebook', 'conteudos', 'categoria.png')
    categoria_dst = os.path.join(tmp_dir, 'categoria.png')
    if os.path.exists(categoria_src):
        shutil.copy(categoria_src, categoria_dst)
        print(f"Imagem 'categoria.png' copiada para {tmp_dir}")
    else:
        print(f"Erro: Imagem 'categoria.png' não encontrada em {categoria_src}")
        exit(1)

    # Copiar recursos.png para o diretório temporário
    recursos_src = os.path.join(base_dir, 'ebook', 'conteudos', 'recursos.png')
    recursos_dst = os.path.join(tmp_dir, 'recursos.png')
    if os.path.exists(recursos_src):
        shutil.copy(recursos_src, recursos_dst)
        print(f"Imagem 'recursos.png' copiada para {tmp_dir}")
    else:
        print(f"Erro: Imagem 'recursos.png' não encontrada em {recursos_src}")
        exit(1)

    # Carregar templates
    template_dir = os.path.join(base_dir, 'ebook', 'conteudos')
    try:
        template_categoria = open(os.path.join(template_dir, 'categoria_template.html'), 'r', encoding='utf-8').read()
        template_tecnologia = open(os.path.join(template_dir, 'tecnologia_template.html'), 'r', encoding='utf-8').read()
        template_recursos = open(os.path.join(template_dir, 'recursos.html'), 'r', encoding='utf-8').read()
        template_conclusao = open(os.path.join(template_dir, 'conclusao.html'), 'r', encoding='utf-8').read()
        template_equipe = open(os.path.join(template_dir, 'equipe.html'), 'r', encoding='utf-8').read()
        template_contracapa = open(os.path.join(template_dir, 'contracapa.html'), 'r', encoding='utf-8').read()
        print("Templates carregados com sucesso.")
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        exit(1)

    # Ler dados
    try:
        tecnologias_df = pd.read_csv(url_tecnologias)
        print("Dados de 'tecnologias' carregados com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar 'tecnologias': {e}")
        exit(1)
    try:
        recursos_df = pd.read_csv(url_recursos)
        print("Dados de 'recursos' carregados com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar 'recursos': {e}")
        exit(1)

    # Agrupar tecnologias por categoria
    grupos = tecnologias_df.groupby('categoria')

    # Função para formatar links
    def formatar_links(link_str):
        if not link_str or pd.isna(link_str):
            return ""
        pares = link_str.split(';')
        lista_html = "<ul>"
        for par in pares:
            if par:
                plataforma, link = par.split(',')
                lista_html += f"<li>{plataforma}: <a href='{link}' class='text-decoration-none'>{link}</a></li>"
        lista_html += "</ul>"
        return lista_html

    # Gerar HTML
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" type="text/css" href="file://{os.path.join(template_dir, 'style.css')}">
    </head>
    <body>
    """
    for page in ['capa.html', 'introducao.html', 'instrucoes.html']: # 'conceitos.html', 
        with open(os.path.join(template_dir, page), 'r', encoding='utf-8') as f:
            html_content += f"<div style='page-break-after: always;'>{f.read()}</div>"

    for categoria, grupo in grupos:
        descricao_categ = grupo['categoria_descricao'].iloc[0]
        conteudo_categ = template_categoria.format(categoria=categoria, descricao_categoria=descricao_categ)
        html_content += f"<div style='page-break-after: always;'>{conteudo_categ}</div>"
        for _, row in grupo.sort_values('titulo').iterrows():
            data = row.to_dict()
            imagem_path = f"file://{os.path.join(base_dir, 'imagens', data['imagem'])}"
            data['imagem'] = imagem_path
            data['links_formatados'] = formatar_links(data['link'])
            conteudo_tec = template_tecnologia.format(**data)
            html_content += f"<div style='page-break-after: always;'>{conteudo_tec}</div>"

    if recursos_df.empty:
        lista_recursos = "<p>Nenhum recurso disponível.</p>"
    else:
        lista_recursos = ""
        for _, row in recursos_df.iterrows():
            lista_recursos += f"<p><strong>{row['titulo']}</strong><br>"
            lista_recursos += f"<span class='text-muted'>{row['descricao']}</span><br>"
            lista_recursos += f"<a href='{row['link']}' class='text-decoration-none'>{row['link']}</a><hr>"
    html_content += f"<div style='page-break-after: always;'>{template_recursos.replace('{lista_recursos}', lista_recursos)}</div>"

    html_content += f"<div style='page-break-after: always;'>{template_conclusao}</div>"
    data_hora = datetime.datetime.now().strftime('%d/%m/%Y, às %H:%M:%S')
    html_content += f"<div style='page-break-after: always;'>{template_equipe.format(data_hora=data_hora)}</div>"
    html_content += f"<div style='page-break-after: always;'>{template_contracapa}</div>"
    html_content += "</body></html>"

    # Salvar HTML temporário e gerar PDF
    with open(os.path.join(tmp_dir, 'ebook.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Arquivo HTML temporário gerado.")
    try:
        subprocess.run(['wkhtmltopdf', '--enable-local-file-access', os.path.join(tmp_dir, 'ebook.html'), output_pdf], check=True)
        print(f"PDF gerado em: {output_pdf}")
    except FileNotFoundError:
        print("Erro: wkhtmltopdf não encontrado.")
        exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao gerar PDF: {e}")
        exit(1)

if __name__ == '__main__':
    generate_ebook()