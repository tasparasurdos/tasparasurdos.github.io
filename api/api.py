import os
import shutil
import json
from collections import defaultdict
import pandas as pd

def generate_api(url_tecnologias=None, url_recursos=None):
    # URLs padrão
    if url_tecnologias is None:
        url_tecnologias = 'https://docs.google.com/spreadsheets/d/1g-zamZFp5FHTGxZOA0vT3ULXjwROhWS0mz0_K1xTvXc/export?format=csv'
    if url_recursos is None:
        url_recursos = 'https://docs.google.com/spreadsheets/d/1lePYinFlYePVYPwwUqy1Xa1r1FF_l3vaAkRxntSvWq4/export?format=csv&gid=1735795033'

    # Definir diretórios
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    docs_dir = os.path.join(base_dir, 'docs')
    api_dir = os.path.join(docs_dir, 'api')
    os.makedirs(api_dir, exist_ok=True)
    site_url = 'https://tasparasurdos.github.io/api/'
    imagens_url = 'https://tasparasurdos.github.io/imagens/'  # Novo local centralizado para imagens

    # Copiar index.html
    shutil.copy(os.path.join(base_dir, 'api', 'index.html'), os.path.join(api_dir, 'index.html'))

    # Colunas para JSON
    colunas_json = [
        'titulo', 'descricao', 'orientacao', 'dicas', 'etapas_justificativa', 'imagem',
        'categoria', 'custo', 'requer_internet', 'plataformas', 'autor', 'link', 'etapas'
    ]

    # Função para gravar JSON
    def write_json(filename, data):
        with open(os.path.join(api_dir, filename), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # Processar tecnologias
    try:
        df = pd.read_csv(url_tecnologias)
        print("Dados de tecnologias carregados com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar 'tecnologias': {e}")
        exit(1)

    records = df.to_dict(orient='records')
    indice = []
    categorias = defaultdict(list)
    custos = defaultdict(list)
    etapas_ensino = defaultdict(list)
    requer_internet_dict = defaultdict(list)
    plataformas_dict = defaultdict(list)
    desc_cat = {}

    for row in records:
        tech_data = {col: row.get(col) for col in colunas_json}
        if tech_data.get('imagem'):
            tech_data['imagem'] = f"{imagens_url}{tech_data['imagem']}"  # Atualiza para o novo caminho
        slug = row.get('slug')
        write_json(f"{slug}.json", tech_data)

        indice.append({
            'titulo': row['titulo'],
            'icone': f"{imagens_url}{slug}-icon.jpg",  # Atualiza para o novo caminho
            'slug': slug,
            'custo': row['custo'],
            'requer_internet': row['requer_internet'],
            'plataformas': row['plataformas'],
            'etapas': row['etapas'],
            'apresentacao': row.get('apresentacao'),
            'link': f"{site_url}{slug}.json",
        })

        categorias[row['categoria']].append({
            'titulo': row['titulo'],
            'icone': f"{imagens_url}{slug}-icon.jpg",  # Atualiza para o novo caminho
            'imagem': f"{imagens_url}{row['imagem']}",  # Atualiza para o novo caminho
            'slug': slug,
            'custo': row['custo'],
            'requer_internet': row['requer_internet'],
            'plataformas': row['plataformas'],
            'etapas': row['etapas'],
            'apresentacao': row.get('apresentacao'),
        })
        desc_cat[row['categoria']] = row.get('categoria_descricao')
        custos[row['custo']].append({'titulo': row['titulo'], 'arquivo': f"{slug}.json"})
        etapas = row['etapas'].split(';') if row['etapas'] else ['Não especificado']
        for etapa in etapas:
            etapa = etapa.strip()
            if etapa:
                etapas_ensino[etapa].append({'titulo': row['titulo'], 'arquivo': f"{slug}.json"})
        requer_internet_dict[row['requer_internet']].append({'titulo': row['titulo'], 'arquivo': f"{slug}.json"})
        plataformas = row['plataformas'].split(',') if row['plataformas'] else ['Não especificado']
        for plat in plataformas:
            plat = plat.strip()
            if plat:
                plataformas_dict[plat].append({'titulo': row['titulo'], 'arquivo': f"{slug}.json"})

    indice.sort(key=lambda x: x['titulo'].lower())
    for d in (categorias, custos, etapas_ensino, requer_internet_dict, plataformas_dict):
        for key in d:
            d[key].sort(key=lambda x: x['titulo'].lower())

    categorias_com_desc = {cat: {'descricao': desc_cat[cat], 'tecnologias': items} for cat, items in categorias.items()}
    write_json('indice.json', indice)
    write_json('categorias.json', categorias_com_desc)
    write_json('custo.json', dict(custos))
    write_json('etapas_ensino.json', dict(etapas_ensino))
    write_json('requer_internet.json', dict(requer_internet_dict))
    write_json('plataformas.json', dict(plataformas_dict))

    # Processar recursos
    try:
        df_rec = pd.read_csv(url_recursos)
        print("Dados de recursos carregados com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar 'recursos': {e}")
        exit(1)
    recursos = df_rec.to_dict(orient='records')
    write_json('recursos.json', recursos)
    print("Processamento concluído com sucesso!")

if __name__ == '__main__':
    generate_api()