from configparser import ConfigParser
import inspect
import logging
from pathlib import Path

from advys_configuracoes.config_gerais import ENCODING, BIBLIOTECA
from advys_validadores.arquivo import verifica_arquivo

nome_arquivo_ini = "py_advys.ini"
dir_config = Path.home() / f".{BIBLIOTECA} Config"
caminho_arquivo = dir_config / nome_arquivo_ini





def caminho_configuracao_ini():
    return verifica_arquivo(caminho_arquivo)


def criar_arquivo_ini_padrao(arquivo_config:Path):
    """
    Cria um arquivo de configuração .ini padrão
    """
    if arquivo_config.exists():
        logging.info(
            f"Arquivo {arquivo_config.name} já existe, pulando a criação..."
        )
        return

    logging.info(f"Criando arquivo {arquivo_config.name}...")

    # Configuração padrão se o ARQUIVO DE CONFIGURAÇÃO não existir
    config = ConfigParser()

    # Configura parâmetros - estrutura/atualiza_estrutura.py
    caminho_estrutura = Path.cwd() / "src" / "estrutura_dir.json"
    raiz = dir_config / "Estrutura"
    raiz.mkdir(parents=True, exist_ok=True)
    config['atualiza_caminhos'] = {
        "caminho_estrutura": str(caminho_estrutura),
        "raiz": str(raiz)
    }

    # Configura parâmetros - estrutura/atualiza_imagens.py
    caminho_imagens = Path.home() / "Imagens Automação Advys"
    caminho_imagens.mkdir(parents=True, exist_ok=True)
    config['atualiza_imagens'] = {
        "caminho_imagens": str(caminho_imagens)
    }

    # Escreve as configurações no arquivo
    with open(arquivo_config, "w", encoding=ENCODING) as a:
        config.write(a)

    logging.info(f"Arquivo {nome_arquivo_ini} criado.")


def carrega_configuracao_ini(arquivo_config:Path):
    
    #
    logging.info(f"Carregando arquivo {arquivo_config.name}")
    arquivo = verifica_arquivo(arquivo_config)

    config = ConfigParser()
    config.read(arquivo, encoding=ENCODING)
    return config




if __name__ == "__main__":
    py_advys_ini = caminho_configuracao_ini()
    cfg = carrega_configuracao_ini(py_advys_ini)
    print(cfg['atualiza_caminhos']['caminho_estrutura'])
