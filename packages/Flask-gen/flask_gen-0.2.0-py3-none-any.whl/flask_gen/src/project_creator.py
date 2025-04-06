import os

def check_project_exists(project_dir, project_name):
    """
    Checks if a project already exists at the given path.
    Returns True if it exists, False otherwise.
    """
    if os.path.exists(project_dir):
        print(f"A project named '{project_name}' already exists at location {project_dir}.")
        return True
    return False

def create_project_directories(project_dir):
    """
    Creates the necessary directories for the project.
    """
    directories = [
        os.path.join(project_dir, "core"),
        os.path.join(project_dir, "core", "templates"),
        os.path.join(project_dir, "core", "templates", "errors"),  # For error pages
        os.path.join(project_dir, "core", "static"),  # For static files
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory created: {directory}")

def generate_core_init_content():
    """
    Generates content for the core/__init__.py file
    """
    return "from .settings import create_app\n"

def generate_core_settings_content(project_name):
    """
    Generates content for the core/settings.py file
    """
    content = f'''import os
from flask import Flask, render_template
from config import Config
from extensions import db, migrate

DEBUG = True

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from core.urls import register_blueprints
    register_blueprints(app)

    # Error handling if application is not in debug mode
    if not DEBUG:
        @app.errorhandler(404)
        def not_found_error(error):
            return render_template("errors/404.html"), 404

        @app.errorhandler(403)
        def forbidden_error(error):
            return render_template("errors/403.html"), 403

        @app.errorhandler(500)
        def internal_error(error):
            return render_template("errors/500.html"), 500

    return app
'''
    return content

def generate_core_urls_content():
    """
    Generates content for the core/urls.py file
    """
    content = '''"""
To register your application blueprints, import them and add them here.

Example:
    from blog.routes.urls import blog_register_blueprints

    def register_blueprints(app):
        blog_register_blueprints(app)
"""

def register_blueprints(app):
    pass
'''
    return content

def generate_base_html_content(project_name):
    """
    Generates content for the core/templates/base.html file
    """
    content = f'''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{% block title %}}{project_name}{{% endblock %}}</title>
</head>
<body>
    {{% block content %}}{{% endblock %}}
</body>
</html>
'''
    return content

def generate_error_template_content(error_code):
    """
    Generates content for error pages.
    """
    content = f'''{{% extends "base.html" %}}
{{% block content %}}
<h1>Error {error_code}</h1>
{{% endblock %}}
'''
    return content

def generate_config_content():
    """
    Generates content for the config.py file
    """
    content = '''import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
'''
    return content

def generate_extensions_content():
    """
    Generates content for the extensions.py file
    """
    content = '''from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
'''
    return content

def generate_app_content():
    """
    Generates content for the app.py file
    """
    content = '''from core.settings import create_app, DEBUG

app = create_app()

if __name__ == '__main__':
    app.run(debug=DEBUG)
'''
    return content

def generate_requirements_content():
    """
    Generates content for the requirements.txt file
    """
    content = '''Flask
Flask-SQLAlchemy
Flask-Migrate
python-dotenv
'''
    return content

def generate_env_example_content():
    """
    Generates content for the .env.example file
    """
    content = '''SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///site.db
FLASK_ENV=development
'''
    return content

def create_file(filepath, content):
    """
    Creates a file with the specified content.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"File created: {filepath}")

def init_project(project_name, base_path):
    """
    Initializes a complete Flask project with default configuration,
    Flask-SQLAlchemy, Flask-Migrate, error handling, and an example .env file.
    """
    project_dir = os.path.join(base_path, project_name)

    # Check if project already exists
    if check_project_exists(project_dir, project_name):
        return  # Exit the function without creating the project

    print(f"Creating project in: {project_dir}")

    # Create necessary directories
    create_project_directories(project_dir)

    # Create files with their content
    files_to_create = {
        # core/__init__.py
        os.path.join(project_dir, "core", "__init__.py"): generate_core_init_content(),

        # core/settings.py
        os.path.join(project_dir, "core", "settings.py"): generate_core_settings_content(project_name),

        # core/urls.py
        os.path.join(project_dir, "core", "urls.py"): generate_core_urls_content(),

        # core/templates/base.html
        os.path.join(project_dir, "core", "templates", "base.html"): generate_base_html_content(project_name),

        # core/templates/errors/*.html
        os.path.join(project_dir, "core", "templates", "errors", "404.html"): generate_error_template_content(404),
        os.path.join(project_dir, "core", "templates", "errors", "403.html"): generate_error_template_content(403),
        os.path.join(project_dir, "core", "templates", "errors", "500.html"): generate_error_template_content(500),

        # config.py
        os.path.join(project_dir, "config.py"): generate_config_content(),

        # extensions.py
        os.path.join(project_dir, "extensions.py"): generate_extensions_content(),

        # app.py
        os.path.join(project_dir, "app.py"): generate_app_content(),

        # requirements.txt
        os.path.join(project_dir, "requirements.txt"): generate_requirements_content(),

        # .env.example
        os.path.join(project_dir, ".env.example"): generate_env_example_content(),

        # core/static/styles.css (empty CSS file)
        os.path.join(project_dir, "core", "static", "styles.css"): '/* Add your custom CSS styles here */',
    }

    for filepath, content in files_to_create.items():
        create_file(filepath, content)