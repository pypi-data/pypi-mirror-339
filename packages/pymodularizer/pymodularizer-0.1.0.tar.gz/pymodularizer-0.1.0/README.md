
# 🛠️ ProjectGen - Gerador de Projetos Python Modularizados

`ProjectGen` é uma ferramenta de linha de comando para gerar rapidamente estruturas de projetos Python — desde scripts simples até aplicações modulares com FastAPI ou Flask. Ideal para acelerar a criação de pacotes reutilizáveis, APIs e sistemas organizados por módulos.

---

## ✨ Recursos

- Geração de estruturas de projeto prontas para uso
- Suporte a múltiplos tipos: script simples, pacote, aplicação modular, API com FastAPI ou Flask
- Criação de novos módulos com um único comando
- Estrutura compatível com boas práticas de organização e testes
- CLI interativa via [Typer](https://typer.tiangolo.com/)
- Pronto para publicação no PyPI

---

## 🚀 Instalação

Você pode instalar diretamente via PyPI:

```bash
pip install projectgen
```

Ou localmente, após clonar o repositório:

```bash
git clone https://github.com/seuusuario/projectgen.git
cd projectgen
pip install .
```

---

## ⚙️ Uso

### Criar um novo projeto

```bash
projectgen new --name my_app --type modular_application
```

Opções disponíveis:

| Opção         | Descrição                                 | Padrão       |
|---------------|--------------------------------------------|--------------|
| `--name`      | Nome do projeto                            | `meu_projeto` |
| `--version`   | Versão inicial do projeto                  | `0.1.0`       |
| `--src`       | Nome da pasta de código fonte              | `src`         |
| `--main`      | Nome do arquivo principal                  | `main.py`     |
| `--type`      | Tipo do projeto (`custom`, `simple_script`, etc.) | `custom` |

### Adicionar um módulo

```bash
projectgen module meu_modulo --path src
```

Cria um módulo com estrutura básica dentro da pasta especificada (`src` por padrão).

### Listar templates disponíveis

```bash
projectgen list-templates
```

Mostra todos os tipos de projetos disponíveis que podem ser usados com o comando `new`.

---

## 🧱 Templates disponíveis

```bash
projectgen list-templates
```

| Tipo             | Descrição                                                           |
|------------------|---------------------------------------------------------------------|
| simple_script     | Projeto com um único script e módulos auxiliares                   |
| python_package    | Pacote instalável com módulos organizados                          |
| modular_application | Aplicação modular com serviços, módulos e configuração separada  |
| fastapi_api       | Estrutura pronta para uma API com FastAPI                          |
| flask_api         | Estrutura pronta para uma API com Flask                            |
| custom            | Estrutura personalizada definida pelo usuário                      |

---

## 🧪 Testes

Testes automatizados usam `pytest`. Execute com:

```bash
pytest
```

> As funções são testadas sem criar arquivos reais no sistema, usando `tmp_path`.

---

## 📂 Estrutura esperada

Exemplo de estrutura gerada:

```
my_app/
├── src/
│   ├── main.py
│   ├── modules/
│   ├── services/
│   └── config/
├── tests/
├── README.md
├── setup.cfg
├── pyproject.toml
└── requirements.txt
```

---

## 📦 Publicação no PyPI

Se você quiser clonar e adaptar para publicar seu próprio pacote, basta configurar:

- `pyproject.toml`
- `setup.cfg`
- `README.md`

E executar:

```bash
python -m build
python -m twine upload dist/*
```

---

## 🤝 Contribuindo

Pull requests são bem-vindos! Sinta-se à vontade para sugerir novos tipos de projeto, comandos e melhorias.

---

## 📝 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais detalhes.
