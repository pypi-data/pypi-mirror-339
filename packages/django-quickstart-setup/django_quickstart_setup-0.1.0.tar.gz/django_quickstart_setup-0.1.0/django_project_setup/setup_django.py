import os
import subprocess
import sys

def create_virtualenv(env_name):
    if not os.path.exists(env_name):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", env_name])
    else:
        print("Virtual environment already exists.")

def activate_virtualenv(env_name):
    if os.name == 'nt':  # Check if Windows OS
        activate_script = os.path.join(env_name, "Scripts", "activate.bat")
    else:
        activate_script = os.path.join(env_name, "bin", "activate")
    
    if os.path.exists(activate_script):
        print(f"Activating virtual environment: {activate_script}")
        subprocess.run([activate_script], shell=True)
    else:
        print("Virtual environment activation script not found!")

def install_dependencies():
    print("Installing Django and dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "django"])

def create_django_project(project_name):
    print(f"Creating Django project: {project_name}")
    subprocess.run(["django-admin", "startproject", project_name])
    return os.path.join(os.getcwd(), project_name)

def create_django_app(project_path, app_name):
    print(f"Creating Django app: {app_name}")
    os.chdir(project_path)
    subprocess.run(["python", "manage.py", "startapp", app_name])
    return os.path.join(project_path, app_name)

def configure_settings(project_path, app_name):
    settings_file = os.path.join(project_path, project_path.split(os.sep)[-1], "settings.py")
    
    # Read the current settings file
    with open(settings_file, 'r') as f:
        settings_content = f.read()
        settings_content += f"""import os"""
    # Add app to INSTALLED_APPS
    
    settings_content = settings_content.replace(
        "INSTALLED_APPS = [",
        f"INSTALLED_APPS = [\n    '{app_name}',"
    )
    
    # Add static and media settings
    settings_content += f"""

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Templates
TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]
"""
    
    # Write the updated settings
    with open(settings_file, 'w') as f:
        f.write(settings_content)

def configure_urls(project_path, app_name):
    # Configure main urls.py
    main_urls_file = os.path.join(project_path, project_path.split(os.sep)[-1], "urls.py")
    main_urls_content = f"""from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('{app_name}.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
    
    with open(main_urls_file, 'w') as f:
        f.write(main_urls_content)
    
    # Create app urls.py
    app_urls_file = os.path.join(project_path, app_name, "urls.py")
    app_urls_content = f"""from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
"""
    
    with open(app_urls_file, 'w') as f:
        f.write(app_urls_content)

def create_views(app_path):
    views_file = os.path.join(app_path, "views.py")
    views_content = f"""from django.shortcuts import render

def index(request):
    return render(request, '{os.path.basename(app_path)}/index.html')
"""
    
    with open(views_file, 'w') as f:
        f.write(views_content)

def create_templates(project_path, app_name):
    # Create templates directory
    templates_dir = os.path.join(project_path, 'templates', app_name)
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create index.html
    index_file = os.path.join(templates_dir, 'index.html')
    index_content = """<!DOCTYPE html>
<html>
<head>
    <title>Welcome to Django</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f0f0;
        }
        .container {
            text-align: center;
            padding: 2rem;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to Django!</h1>
        <p>Your project has been successfully set up.</p>
        <p>Let your friends know about this amazing python module .</p>
    </div>
</body>
</html>
"""
    
    with open(index_file, 'w') as f:
        f.write(index_content)

def create_static_and_media_dirs(project_path):
    # Create static and media directories
    static_dir = os.path.join(project_path, 'static')
    media_dir = os.path.join(project_path, 'media')
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(media_dir, exist_ok=True)

def main():
    virtualenv = input("Enter the virtual environment name (if it doesn't exist it will be created): ")
    project_name = input("Enter the project name: ")
    app_name = input("Enter the app name: ")

    # Create virtual environment
    create_virtualenv(virtualenv)

    # Activate virtual environment
    activate_virtualenv(virtualenv)

    # Install dependencies
    install_dependencies()

    # Create Django project and get its path
    project_path = create_django_project(project_name)

    # Create Django app and get its path
    app_path = create_django_app(project_path, app_name)

    # Configure settings
    configure_settings(project_path, app_name)

    # Configure URLs
    configure_urls(project_path, app_name)

    # Create views
    create_views(app_path)

    # Create templates
    create_templates(project_path, app_name)

    # Create static and media directories
    create_static_and_media_dirs(project_path)

    print(f"\nDjango project {project_name} with app {app_name} has been set up!")
    print("\nNext steps:")
    print(f"1. Activate your virtual environment: {os.path.join(virtualenv, 'Scripts', 'activate.bat') if os.name == 'nt' else os.path.join(virtualenv, 'bin', 'activate')}")
    print("2. Run migrations: python manage.py migrate")
    print("3. Create superuser: python manage.py createsuperuser")
    print("4. Run development server: python manage.py runserver")

if __name__ == "__main__":
    main() 