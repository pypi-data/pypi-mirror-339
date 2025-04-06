# flask_gen/cli.py

import click
from flask_gen.src import app_creator, project_creator

@click.group(help="Flask Project Generator CLI")
def cli():
   """Command line interface for generating Flask projects."""
   pass

@cli.command("project", help="Initialize a complete Flask project")
@click.argument("name")
@click.argument("path", default=".")
def init_project(name, path):
   """
   Initialize a complete Flask project.
   
   NAME: project name.
   PATH: destination path (default: current directory).
   """
   project_creator.init_project(name, path)
   click.echo(f"Project '{name}' initialized at {path}.")

@cli.command("app", help="Initialize a new Flask application (blueprint)")
@click.argument("name")
@click.argument("path", default=".")
def init_app(name, path):
   """
   Initialize a new application (blueprint).

   NAME: application name.
   PATH: project directory where the application will be created (default: current directory).
   """
   app_creator.init_app(name, path)
   click.echo(f"Application '{name}' initialized at {path}.")

if __name__ == "__main__":
   cli()