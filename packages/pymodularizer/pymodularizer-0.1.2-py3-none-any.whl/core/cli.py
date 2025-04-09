import typer
from pathlib import Path
from .generator import create_structure
from ..helpers.module import create_module
from .templates import get_default_structure, project_templates

app = typer.Typer(help="Gerador de projetos Python modularizados.")

@app.command()
def new(
    name: str = typer.Option("meu_projeto", help="Nome do projeto"),
    version: str = typer.Option("0.1.0", help="Versão do projeto"),
    src: str = typer.Option("src", help="Nome da pasta de código fonte"),
    main: str = typer.Option("main.py", help="Nome do arquivo principal"),
    type: str = typer.Option("custom", help="Tipo do projeto: custom, simple_script, python_package, modular_application, fastapi_api, flask_api")
):
    """Cria um novo projeto Python."""
    project_path = Path(name)
    project_path.mkdir(parents=True, exist_ok=True)

    if type == "custom":
        structure = get_default_structure(src, main)
    elif type in project_templates["project_types"]:
        structure = project_templates["project_types"][type]["structure"]
    else:
        typer.echo("❌ Tipo de projeto inválido. Use 'custom' ou um dos tipos predefinidos.")
        raise typer.Exit(code=1)

    create_structure(project_path, structure)

    for file in project_templates["common_files"]:
        (project_path / file).write_text(f"# {file}\n")

    typer.echo(f"✅ Projeto '{name}' do tipo '{type}' criado com sucesso!")

@app.command()
def module(
    name: str = typer.Argument(..., help="Nome do módulo"),
    path: str = typer.Option("src", help="Pasta onde o módulo será criado")
):
    """Cria um novo módulo dentro da pasta fonte."""
    create_module(name, path)
    typer.echo(f"📦 Módulo '{name}' criado dentro de '{path}'")

@app.command()
def list_templates():
    """
    Lista os tipos de projeto disponíveis no gerador.
    """
    from .templates import project_templates

    print("\n📦 Tipos de projeto disponíveis:\n")
    for name, data in project_templates["project_types"].items():
        print(f"🔹 {name} - {data['description']}")


