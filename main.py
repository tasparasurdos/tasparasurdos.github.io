import os
import shutil
from ebook.ebook import generate_ebook
from website.website import generate_website
from api.api import generate_api

# URLs das planilhas
URL_TECNOLOGIAS = 'https://docs.google.com/spreadsheets/d/1g-zamZFp5FHTGxZOA0vT3ULXjwROhWS0mz0_K1xTvXc/export?format=csv'
URL_RECURSOS = 'https://docs.google.com/spreadsheets/d/1lePYinFlYePVYPwwUqy1Xa1r1FF_l3vaAkRxntSvWq4/export?format=csv'

def main():
    base_dir = os.path.abspath('.')
    docs_dir = os.path.join(base_dir, 'docs')

    # Perguntar sobre limpeza de docs/
    if os.path.exists(docs_dir):
        clean = input("Deseja limpar o diretório 'docs/' antes de gerar? (s/n): ")
        if clean.lower() == 's':
            shutil.rmtree(docs_dir)
    os.makedirs(docs_dir, exist_ok=True)

    # Menu interativo
    print("O que você deseja gerar?")
    print("1. API")
    print("2. Ebook")
    print("3. Site")
    print("4. Todos")
    choice = input("Digite o número da opção desejada: ")

    if choice == '1':
        generate_api(URL_TECNOLOGIAS, URL_RECURSOS)
    elif choice == '2':
        generate_ebook(URL_TECNOLOGIAS, URL_RECURSOS)
    elif choice == '3':
        generate_website(URL_TECNOLOGIAS, URL_RECURSOS)
    elif choice == '4':
        generate_api(URL_TECNOLOGIAS, URL_RECURSOS)
        generate_ebook(URL_TECNOLOGIAS, URL_RECURSOS)
        generate_website(URL_TECNOLOGIAS, URL_RECURSOS)
    else:
        print("Opção inválida.")
        return

    # Copiar imagens
    shutil.copytree(os.path.join(base_dir, 'imagens'), os.path.join(docs_dir, 'imagens'), dirs_exist_ok=True)

if __name__ == '__main__':
    main()