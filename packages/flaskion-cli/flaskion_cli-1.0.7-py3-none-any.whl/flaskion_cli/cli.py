import os
import sys
import shutil
import subprocess

# Template path relative to the installed package
FLASKION_TEMPLATE = os.path.join(os.path.dirname(__file__), "flaskion_template")

def create_project():
    if len(sys.argv) < 3 or sys.argv[1] != "new":
        print("\nUsage: flaskion new <project-name>\n")
        sys.exit(1)

    project_name = sys.argv[2]
    project_path = os.path.join(os.getcwd(), project_name)

    if os.path.exists(project_path):
        print(f"\n Error: The folder '{project_name}' already exists.\n")
        sys.exit(1)

    if not os.path.exists(FLASKION_TEMPLATE):
        print(f"\n Error: Template folder not found at: {FLASKION_TEMPLATE}\n")
        sys.exit(1)

    print(f"\n📁 Creating new Flaskion project: \033[1m{project_name}\033[0m")

    try:
        shutil.copytree(FLASKION_TEMPLATE, project_path)
    except Exception as e:
        print(f"Failed to copy template: {e}")
        sys.exit(1)

    print("Initialising Git repository...")
    subprocess.run(["git", "init"], cwd=project_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("Creating virtual environment...")
    subprocess.run(["python3", "-m", "venv", "venv"], cwd=project_path)

    print("Installing dependencies...")
    pip_path = os.path.join(project_path, "venv", "bin", "pip")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], cwd=project_path)

    print(f"\n \033[1mFlaskion project '{project_name}' created successfully!\033[0m\n")
    print("Next steps:\n")
    print(f"   cd {project_name}")
    print("   source venv/bin/activate")
    print("   flask run\n")

if __name__ == "__main__":
    create_project()