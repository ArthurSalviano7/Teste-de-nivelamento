import pymupdf
import csv
import zipfile
import scraping

def extract_tables_from_pdf():
    doc = pymupdf.open("Anexo_I.pdf")
    final_table = []
    print("Extraindo e processando tabelas (Isso pode demorar um pouco)...")
    # Itera sobre cada página no arquivo e extrai a tabela
    for page in doc:
        tables = page.find_tables()
        for table in tables.tables:
            extracted_data = table.extract()
            for row in extracted_data[1:]: # Desconsidera a primeira linha de cada tabela (cabeçalho)
                if row[3] == "OD":
                    row[3] = "Seg. Odontológica"
                if row[4] == "AMB":
                    row[4] = "Seg. Ambulatorial"
                final_table.append(row)  # Extrai as linhas da tabela e adiciona a lista

    print("Tabelas processadas!")
    return final_table

def write_list_to_csv(table):
    print("Realizando escrita de arquivo CSV...")

    with zipfile.ZipFile('Teste_Arthur_Salviano_Ferreira.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        with open('Teste_Arthur_Salviano_Ferreira.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['PROCEDIMENTO', 'RN(alteração)', 'VIGÊNCIA', 'OD', 'AMB', 'HCO', 'HSO', 'REF', 'PAC', 'DUT', 'SUBGRUPO', 'GRUPO', 'CAPÍTULO'])
            writer.writerows(table)

    print("Arquivo CSV criado e compactado!")

def main():
    # Extração e download de arquivos
    link1, link2 = scraping.find_anexo_links()
    scraping.download_zip_files(link1, link2)

    # Transformação dos dados e criação do CSV
    extracted_data = extract_tables_from_pdf()
    write_list_to_csv(extracted_data)

if __name__ == "__main__":
    main()