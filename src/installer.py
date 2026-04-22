import subprocess as sb
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger(__name__)

Packages = [
    "python3-spyder", "golang", "clang", "VirtualBox",
    "fastfetch", "cpufetch", "obs-studio", "vscode",
    "librewolf", "zig", "gh", "telegram-desktop", "yt-dlp"
    "discord", "steam", "ghostty", "ani-cli", "krita", "gimp",
    "inkscape", "vlc", "rustup", "cargo", "distrobox", "micro",
    "acpi", "kubernetes", "podman", "nginx", "sqlite", "python3-pycryptodomex",
    "python3-sympy"
]

def repo_vscode():
    lg.info("(+) Adding VS Code...")
    repo_content_vscode = """[code]
name=Visual Studio Code
baseurl=https://packages.microsoft.com/yumrepos/vscode
enabled=1
autorefresh=1
type=rpm-md
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc
"""
    sb.run(["sudo", "rpm", "--import", "https://packages.microsoft.com/keys/microsoft.asc"], check=True)
    p = sb.Popen(["sudo", "tee", "/etc/yum.repos.d/vscode.repo"], stdin=sb.PIPE, text=True)
    p.communicate(repo_content_vscode)


def repo_librewolf():
    lg.info("(+) Adding Librewolf Repository...")
    sb.run(["sudo", "dnf", "config-manager", "addrepo" ,"--from-repofile=https://repo.librewolf.net/librewolf.repo"], check=True)

def rpm_fusion():
    lg.info("(+) Installing RPM Fusion Repositories...")
    fedora_version = sb.check_output(["rpm", "-E", "%fedora"], text=True).strip()
    
    rpmfusion_free_repo = \
        f"https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-{fedora_version}.noarch.rpm"
    rpmfusion_non_free_repo = \
        f"https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{fedora_version}.noarch.rpm"
    
    sb.run(["sudo", "dnf", "install", rpmfusion_free_repo, "-y"], check=True)
    sb.run(["sudo", "dnf", "install", rpmfusion_non_free_repo, "-y"], check=True)
    lg.info("(+) Installed RPM Fusion!")

def copr_repos():
    lg.info("(+) Enabling Copr Repos...")
    sb.run(["sudo", "dnf", "copr", "enable", "scottames/ghostty", "-y"], check=True)
    sb.run(["sudo", "dnf", "copr", "enable", "derisis13/ani-cli", "-y"], check=True)

    lg.info("(+) Enabled Copr Repositories!")

def onlyoffice_rpm():
    lg.info("(+) Getting the rpm package...")
    onlyoffice_path = "/tmp/onlyoffice.rpm"
    rpm_link = \
        "https://github.com/ONLYOFFICE/DesktopEditors/releases/latest/download/onlyoffice-desktopeditors.x86_64.rpm"
    
    sb.run(["curl", "-L", rpm_link, "-o", onlyoffice_path], check=True)
    sb.run(["sudo", "dnf", "install", onlyoffice_path, "-y"], check=True)

def install_packages():
    lg.info("(+) Updating Repositories...")
    sb.run(["sudo", "dnf", "update", "--refresh"], check=True)
    
    lg.info("(+) Installing Packages")
    sb.run(["sudo", "dnf", "install", *Packages], check=True)


def main():
    repo_vscode()
    repo_librewolf()
    rpm_fusion()
    copr_repos()
    onlyoffice_rpm()
    install_packages()

if __name__ == "__main__":
    main()
