import subprocess as sb
import logging

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger(__name__)

def run(cmd, check=True):
    lg.info(f"(+) Running: {' '.join(cmd)}")
    try:
        return sb.run(cmd, check=check, text=True, capture_output=True)
    except sb.CalledProcessError as e:
        lg.error(f"(-) Command failed: {' '.join(cmd)}")
        lg.error(e.stderr)
        raise

Packages = [
    "python3-spyder", "golang", "clang", "VirtualBox",
    "fastfetch", "cpufetch", "obs-studio", "code",
    "librewolf", "zig", "gh", "telegram-desktop", "signal-desktop", "yt-dlp",
    "discord", "steam", "ghostty", "ani-cli", "krita", "gimp",
    "inkscape", "vlc", "rustup", "cargo", "distrobox", "micro",
    "acpi", "kubernetes", "podman", "nginx", "sqlite",
    "python3-pycryptodomex", "python3-sympy", "systemd-devel",
    "gem", "lsd", "duf", "tldr", "git-credential-libsecret",
    "valgrind", "cava", "tmux", "poetry", "fd", "strace", "wireshark",
    "topgrade"
]

def is_installed(pkg):
    result = sb.run(["rpm", "-q", pkg], text=True, capture_output=True)
    return result.returncode == 0


def repo_exists(name):
    result = run(["dnf", "repolist"])
    return name in result.stdout

def repo_vscode():
    lg.info("(+) Adding VS Code repository...")

    repo_content = """[code]
name=Visual Studio Code
baseurl=https://packages.microsoft.com/yumrepos/vscode
enabled=1
autorefresh=1
type=rpm-md
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc
"""

    run(["sudo", "rpm", "--import", "https://packages.microsoft.com/keys/microsoft.asc"])

    p = sb.Popen(["sudo", "tee", "/etc/yum.repos.d/vscode.repo"], stdin=sb.PIPE, text=True)
    p.communicate(repo_content)


def repo_librewolf():
    lg.info("(+) Checking Librewolf repo...")

    if repo_exists("librewolf"):
        lg.info("(+) Librewolf repo already exists")
        return

    run([
        "sudo", "dnf", "config-manager",
        "addrepo", "--from-repofile=https://repo.librewolf.net/librewolf.repo"
    ])


def rpm_fusion():
    lg.info("(+) Installing RPM Fusion...")

    version = run(["rpm", "-E", "%fedora"]).stdout.strip()

    free = f"https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-{version}.noarch.rpm"
    nonfree = f"https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{version}.noarch.rpm"

    run(["sudo", "dnf", "install", "-y", free])
    run(["sudo", "dnf", "install", "-y", nonfree])


def copr_repos():
    lg.info("(+) Enabling COPR repos...")

    if repo_exists("ghostty") and repo_exists("ani-cli") and repo_exists("topgrade"):
        lg.info("(+) COPR repos already enabled")
        return

    run(["sudo", "dnf", "copr", "enable", "scottames/ghostty", "-y"])
    run(["sudo", "dnf", "copr", "enable", "derisis13/ani-cli", "-y"])
    run(["sudo", "dnf", "copr", "enable", "lilay/topgrade", "-y"])


def signal_repo():
    lg.info("(+) Adding Signal repo...")

    version = run(["rpm", "-E", "%fedora"]).stdout.strip()
    repo = f"https://download.opensuse.org/repositories/network:/im:/signal/Fedora_{version}/network:im:signal.repo"

    if "network_im_signal" in run(["dnf", "repolist"]).stdout:
        lg.info("(+) Signal repo already exists")
        return

    run(["sudo", "dnf", "config-manager", "addrepo", f"--from-repofile={repo}"])

def flathub_repo():
    lg.info("(+) Adding Flathub...")

    run([
        "flatpak", "remote-add",
        "--if-not-exists",
        "flathub",
        "https://dl.flathub.org/repo/flathub.flatpakrepo"
    ])


def onlyoffice_rpm():
    lg.info("(+) Installing OnlyOffice...")

    if is_installed("onlyoffice-desktopeditors"):
        lg.info("(+) OnlyOffice already installed")
        return

    path = "/tmp/onlyoffice.rpm"
    url = "https://github.com/ONLYOFFICE/DesktopEditors/releases/latest/download/onlyoffice-desktopeditors.x86_64.rpm"

    run(["curl", "-L", url, "-o", path])
    run(["sudo", "dnf", "install", "-y", path])

def install_packages():
    lg.info("(+) Updating system...")
    run(["sudo", "dnf", "update", "--refresh"])

    lg.info("(+) Installing packages...")

    for pkg in Packages:
        try:
            run(["sudo", "dnf", "install", "-y", pkg])
        except Exception:
            lg.warning(f"(!) Failed: {pkg}")

def main():
    steps = [
        repo_vscode,
        repo_librewolf,
        rpm_fusion,
        copr_repos,
        signal_repo,
        flathub_repo,
        onlyoffice_rpm,
        install_packages
    ]

    for step in steps:
        try:
            step()
        except Exception as e:
            lg.error(f"(X) Step failed: {step.__name__} -> {e}")


if __name__ == "__main__":
    main()
