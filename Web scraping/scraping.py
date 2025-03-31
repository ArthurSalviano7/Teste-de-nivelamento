from zipfile import ZipFile
from bs4 import BeautifulSoup
import requests

def find_anexo_links():
        html = requests.get("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos").content
        soup = BeautifulSoup(html, 'html.parser')

        anexo_link1 = None
        anexo_link2 = None

        for link in soup.find_all("a"):
                if "Anexo I." == link.text:
                        anexo_link1 = link.get("href")
                        
                if "Anexo II." == link.text:
                        anexo_link2 = link.get("href")
        return anexo_link1, anexo_link2


def download_zip_files(link1, link2):
        print("Baixando arquivos...")
        anexo_response = requests.get(link1)
        with open("Anexo_I.pdf", "wb") as file:
                file.write(anexo_response.content)

        anexo_response = requests.get(link2)
        with open("Anexo_II.pdf", "wb") as file:
                file.write(anexo_response.content)

        print("Arquivos baixados!")

        # Criando arquivo .zip
        with ZipFile('Anexos.zip', 'w') as zipf:
                print("Compactando arquivos...")
                try:
                        zipf.write('Anexo_I.pdf')
                        zipf.write('Anexo_II.pdf')
                except Exception as ex:
                        print("Erro na criação do arquivo Zip:", ex)

                print("Arquivos compactados!")