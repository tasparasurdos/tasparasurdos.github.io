import os
import shutil
import random
import re
import pandas as pd
from jinja2 import Environment, FileSystemLoader

def generate_website(url_tecnologias=None, url_recursos=None):
    # URLs padrão
    if url_tecnologias is None:
        url_tecnologias = 'https://docs.google.com/spreadsheets/d/1g-zamZFp5FHTGxZOA0vT3ULXjwROhWS0mz0_K1xTvXc/export?format=csv'
    if url_recursos is None:
        url_recursos = 'https://docs.google.com/spreadsheets/d/1lePYinFlYePVYPwwUqy1Xa1r1FF_l3vaAkRxntSvWq4/export?format=csv&gid=1735795033'

    # Definir diretórios
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    docs_dir = os.path.join(base_dir, 'docs')
    os.makedirs(docs_dir, exist_ok=True)

    # Função para carregar registros
    def load_records(url):
        print(f"Carregando dados de: {url}")
        df = pd.read_csv(url)
        records = df.to_dict(orient='records')
        records.sort(key=lambda x: x.get('titulo', '').lower())
        print(f"  → {len(records)} registros carregados.")
        return records

    # Carregar dados
    tecnologias = load_records(url_tecnologias)
    recursos = load_records(url_recursos)

    # Gerar opções para dropdowns
    drop_categories = sorted({tech['categoria'] for tech in tecnologias})
    drop_etapas = sorted({et.strip() for tech in tecnologias for et in tech.get('etapas', '').split(';') if et.strip()})
    drop_custos = sorted({tech['custo'] for tech in tecnologias})
    drop_plataformas = sorted({p.strip() for tech in tecnologias for p in re.split(r'[;,]', tech.get('plataformas', '')) if p.strip()})
    drop_internet = sorted({tech['requer_internet'] for tech in tecnologias})

    # Agrupar tecnologias por categoria
    categorias = {}
    for tech in tecnologias:
        categorias.setdefault(tech['categoria'], []).append(tech)
    for lista in categorias.values():
        lista.sort(key=lambda x: x['titulo'].lower())

    # Configurar Jinja2
    template_dir = os.path.join(base_dir, 'website', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))

    # Copiar assets
    shutil.copytree(os.path.join(base_dir, 'website', 'assets'), os.path.join(docs_dir, 'assets'), dirs_exist_ok=True)
    for page in ('sobre.html', 'contato.html', 'equipe.html', 'ebook.html'):
        shutil.copy(os.path.join(template_dir, page), docs_dir)

    # Função de renderização
    def render(path, template, context):
        out_file = os.path.join(docs_dir, path)
        print(f"Gerando: {out_file}")
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(env.get_template(template).render(context))

    # Renderizar páginas
    render('index.html', 'index.html', {
        'tecnologias': tecnologias,
        'recursos_aleatorios': random.sample(recursos, min(12, len(recursos))),
        'drop_categories': drop_categories,
        'drop_etapas': drop_etapas,
        'drop_custos': drop_custos,
        'drop_plataformas': drop_plataformas,
        'drop_internet': drop_internet
    })

    os.makedirs(os.path.join(docs_dir, 'tecnologias'), exist_ok=True)
    for tech in tecnologias:
        categoria_nome = tech['categoria']
        render(f"tecnologias/{tech['slug']}.html", 'tecnologia.html', {
            'tecnologia': tech,
            'categoria': categoria_nome,
            'categoria_descricao': tech.get('categoria_descricao', ''),
            'categoria_tecnologias': categorias[categoria_nome]
        })

    render('recursos.html', 'recursos.html', {'recursos': recursos})

    mapa = {
        'index': 'index.html',
        'sobre': 'sobre.html',
        'contato': 'contato.html',
        'ebook': 'ebook.html',
        'equipe': 'equipe.html',
        'recursos': 'recursos.html',
        'tecnologias': [f"tecnologias/{t['slug']}.html" for t in tecnologias]
    }
    render('mapa.html', 'mapa.html', {'mapa': mapa})

if __name__ == '__main__':
    generate_website()