import subprocess
import sys
import os


def open_hide_terminal(command, with_qt=True):
    """
    Ouvre un nouveau terminal indépendant et exécute la commande spécifiée.

    :param command: La commande à exécuter.
    :param with_qt: Désactive l'affichage si False (utile pour les applications Qt sans affichage).
    :param hide_terminal: Masque la fenêtre du terminal si True.
    :return: Le PID du processus du terminal ouvert.
    """
    hide_terminal = True
    env = dict(os.environ)
    if not with_qt:
        env['QT_QPA_PLATFORM'] = 'offscreen'

    process = None

    if sys.platform.startswith("win"):
        startupinfo = None
        creationflags = 0

        if hide_terminal:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            creationflags = subprocess.CREATE_NO_WINDOW  # Masque complètement la fenêtre du terminal

        process = subprocess.Popen(
            ["cmd.exe", "/c", command], env=env, shell=True, startupinfo=startupinfo, creationflags=creationflags
        )

    elif sys.platform.startswith("linux"):
        if hide_terminal:
            process = subprocess.Popen(["bash", "-c", command], env=env, stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL)
        else:
            try:
                process = subprocess.Popen(["gnome-terminal", "--", "bash", "-c", command + "; exec bash"], env=env)
            except FileNotFoundError:
                process = subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", command + "; exec bash"],
                                           env=env)

    elif sys.platform.startswith("darwin"):
        if hide_terminal:
            process = subprocess.Popen(["bash", "-c", command], env=env, stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL)
        else:
            process = subprocess.Popen(["osascript", "-e", f'tell app "Terminal" to do script "{command}"'])
    print("#######################")
    print(process.pid)
    if process:
        return process.pid
    else:
        raise RuntimeError("Impossible d'ouvrir le terminal.")


def open_terminal(command, with_qt=True):
    """
    Ouvre un nouveau terminal indépendant et exécute la commande spécifiée.
    :param command: La commande à exécuter.
    :param with_qt: Désactive l'affichage si False (utile pour les applications Qt sans affichage).
    :return: Le PID du processus du terminal ouvert.
    """
    env = dict(os.environ)
    if not with_qt:
        env['QT_QPA_PLATFORM'] = 'offscreen'

    process = None

    if sys.platform.startswith("win"):
        process = subprocess.Popen(["start", "cmd.exe", "/k", command], env=env, shell=True)
    elif sys.platform.startswith("linux"):
        try:
            process = subprocess.Popen(["gnome-terminal", "--", "bash", "-c", command + "; exec bash"], env=env)
        except FileNotFoundError:
            process = subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", command + "; exec bash"], env=env)
    elif sys.platform.startswith("darwin"):
        process = subprocess.Popen(["osascript", "-e", f'tell app "Terminal" to do script "{command}"'])
    print("$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(process.pid)
    if process:
        return process.pid
    else:
        raise RuntimeError("Impossible d'ouvrir le terminal.")




def execute_command(command: str, hidden: bool = True,env=None):
    """
    Exécute une commande dans un terminal caché ou visible avec option d'attente.

    :param command: La ligne de commande à exécuter
    :param hidden: Exécuter dans un terminal caché si True, visible sinon
    :param wait: Attendre la fin de l'exécution si True, sinon continuer en parallèle
    :return: (code de retour, PID du processus ou None en cas d'échec)
    """
    try:
        startupinfo = None
        creationflags = 0
        shell = False

        # Gestion spécifique pour Windows
        if os.name == "nt":
            if hidden:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                creationflags = subprocess.CREATE_NEW_CONSOLE
            else:
                command = f'start cmd.exe /k echo {command} & {command}'
            shell = True  # Nécessaire pour certaines commandes Windows
        if env is None:
            # Détermine la manière de lancer le processus
            process = subprocess.Popen(
                command,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                startupinfo=startupinfo,
                creationflags=creationflags,
            )
        else:
            # Détermine la manière de lancer le processus
            process = subprocess.Popen(
                command,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                startupinfo=startupinfo,
                creationflags=creationflags,
                env=env,
            )



        return 0, process.pid  # Succès avec PID

    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        return 1, None  # Erreur


def kill_process(pid: int):
    """
    Tue un processus à partir de son PID.
    :param pid: L'identifiant du processus à tuer
    :return: 0 si succès, 1 en cas d'erreur
    """
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=True)
        else:
            os.kill(pid, 9)  # Signal SIGKILL
        return 0
    except Exception as e:
        print(f"Erreur lors de la suppression du processus {pid}: {e}", file=sys.stderr)
        return 1
