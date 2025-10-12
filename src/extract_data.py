from docling.document_converter import DocumentConverter
import pandas as pd
import os
import re


def extract_data():
    path_files = '../data/processed'
    converter = DocumentConverter()

    df = pd.read_csv('../data/raw/SB_publication_PMC.csv', encoding='utf-8')
    list_link = df['Link'].tolist()

    for link in list_link:
        doc = converter.convert(link).document
        doc_md = doc.export_to_markdown()

        first_line = doc_md.splitlines()[0]
        titulo = re.sub(r'^#\s*', '', first_line).strip()
        name_file = re.sub(r'[^\w\s-]', '', titulo).replace(' ', '_') + ".md"
        os.makedirs(path_files, exist_ok=True)
        caminho_arquivo = os.path.join(path_files, name_file)
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(doc_md)


if __name__ == '__main__':
    extract_data()
