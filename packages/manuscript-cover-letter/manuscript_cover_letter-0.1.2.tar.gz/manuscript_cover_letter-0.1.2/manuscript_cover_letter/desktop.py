import os
import manuscript_cover_letter.about as about
import subprocess


def update_desktop_database():
    applications_dir = os.path.expanduser("~/.local/share/applications")
    try:
        subprocess.run(
            ["update-desktop-database", applications_dir],
            check=True
        )
        print("Banco de dados de atalhos atualizado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao atualizar o banco de dados: {e}")
    except FileNotFoundError:
        print("O comando 'update-desktop-database' não foi encontrado. Verifique se o pacote 'desktop-file-utils' está instalado.")

def create_desktop_file():
    base_dir_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir_path, 'icons', 'logo.png')

    script_path = os.path.expanduser(f"~/.local/bin/{about.__program_name__}")

    desktop_entry = f"""[Desktop Entry]
Name={about.__program_name__}
Comment={about.__description__}
Exec={script_path}
Terminal=false
Type=Application
Icon={icon_path}
StartupNotify=true
Categories=Education;
Keywords=organizer;python;
Encoding=UTF-8
StartupWMClass={about.__package__}
"""
    path = os.path.expanduser(f"~/.local/share/applications/{about.__program_name__}.desktop")
    
    if not os.path.exists(path):  # Evita sobrescrever
        with open(path, "w") as f:
            f.write(desktop_entry)
        os.chmod(path, 0o755)
        print(f"Arquivo .desktop criado em {path}")
        update_desktop_database()
    
if __name__ == '__main__':
    create_desktop_file()
