from configparser import ConfigParser
import inspect
import logging
from pathlib import Path

from advys_configuracoes.config_gerais import ENCODING

NOME_CONFIG = "py_advys.ini"
CONFIG_DIR = Path.home() / ".Py Advys Config"


def caminho_configuracao_ini():
    return Path.home() / ".Py Advys Config" / NOME_CONFIG


def cria_configuracao_ini_padrao(arquivo_config):

    logging.info(f"Criando arquivo {NOME_CONFIG}...")

    # Configuração padrão se o ARQUIVO DE CONFIGURAÇÃO não existir
    config = ConfigParser()

    # Parâmetros - estrutura/atualiza_estrutura.py
    caminho_estrutura = Path.cwd() / "src" / "estrutura_dir.json"
    raiz = CONFIG_DIR / "Estrutura"
    raiz.mkdir(parents=True, exist_ok=True)
    config['atualiza_caminhos'] = {
        "caminho_estrutura": str(caminho_estrutura),
        "raiz": str(raiz)
    }

    # Parâmetros - estrutura/atualiza_imagens.py
    caminho_imagens = Path.home() / "Imagens Automação Advys"
    caminho_imagens.mkdir(parents=True, exist_ok=True)
    config['atualiza_imagens'] = {
        "caminho_imagens": str(caminho_imagens)
    }

    # Escreve
    with open(arquivo_config, "w", encoding=ENCODING) as arquivo_config:
        config.write(arquivo_config)

    logging.info(f"Arquivo {NOME_CONFIG} criado.")


def carrega_configuracao_ini(script):
    #
    logging.info(f"Carregando arquivo {NOME_CONFIG}")

    #
    config = ConfigParser()
    config_criado = None

    #
    arquivo_ini = caminho_configuracao_ini()
    config.read(arquivo_ini)
    print(config.sections())

    if script in config:
        return config[script]

    #
    logging.info(f"Arquivo {NOME_CONFIG} carregado.")

    return config_criado



if __name__ == "__main__":
    py_advys_ini = Path.cwd() / "py_advyis.ini"
    cria_configuracao_ini_padrao(py_advys_ini)
    config = carrega_configuracao_ini("atualiza_caminhos")
    print(config)
