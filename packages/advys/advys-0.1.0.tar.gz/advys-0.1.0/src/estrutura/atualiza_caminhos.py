import argparse
import json
from pathlib import Path
import re

# módulos instalados
from unidecode import unidecode

# módulos criados
from estrutura.config import DIR_DESENVOLVIMENTO_REDE, CODIFICACAO_PADRAO, CAMINHOS_PY
from estrutura.utils import cria_arquivo_python, adiciona_linha_ao_arquivo


def ler_json(arquivo_json:Path):
    if not arquivo_json.exists():
        print("Arquivo estrutura_dir.json não encontrado")
        return

    with open(
        arquivo_json,
        "r",
        encoding=CODIFICACAO_PADRAO
    ) as arquivo_json:
        estrutura = json.load(arquivo_json)

    return estrutura


def cria_variavel(prefixo, nome):
    # Validações
    if not isinstance(prefixo, str):
        raise ValueError("O argumento 'prefixo' deve ser uma string.")
    if not isinstance(nome, str):
        raise ValueError("O argumento 'nome' deve ser uma string.")

    nome = re.sub("[.-/\\ ]", "_", nome)
    variavel = unidecode(f"{prefixo[:3]}_" + nome).upper()

    return variavel


def criar_caminhos_estrutura(arquivo, estrutura, raiz: Path, iniciar=True):
    if iniciar:
        cria_arquivo_python(arquivo)
    for item in estrutura:
        nome = item["nome"]
        tipo = item["tipo"]
        conteudo = item.get("conteudo")
        caminho = raiz / f"{nome}"
        if tipo == "diretório" and not caminho.exists():
            caminho.mkdir(exist_ok=True, parents=True)
        var = cria_variavel(tipo, nome)
        linha = f"{var} = home / '{caminho.relative_to(Path.home()).as_posix()}'"
        adiciona_linha_ao_arquivo(linha, arquivo)
        if conteudo:
            criar_caminhos_estrutura(arquivo, conteudo, caminho, iniciar=False)


if __name__ == "__main__":

    # Cria argumento pra definir o local do arquivo
    parser = argparse.ArgumentParser(description="Meu script Python")
    parser.add_argument("-ce", "--caminho_estrutura", help="Caminho para estrutura json")
    parser.add_argument("-r", "--raiz", help="Define o caminho raiz da estrutura")
    args = parser.parse_args()

    #
    raiz = DIR_DESENVOLVIMENTO_REDE / "Automações"
    if args.raiz:
        raiz = Path(args.raiz)

    # Local padrão do arquivo estrutura_dir.json
    caminho_estrutura_json = Path(__file__).parent / "estrutura_dir.json"


    if args.caminho_estrutura:
        caminho_estrutura_json = Path(args.caminho_estrutura)

    estrutura = ler_json(caminho_estrutura_json)


    criar_caminhos_estrutura(CAMINHOS_PY,estrutura, raiz, iniciar=True)