"""El bash que hay que usar al lanzar un .sh desde Python. En Windows, «bash» a secas es el de WSL
(C:\\Windows\\System32\\bash.exe), que sin distribución falla con «no tiene distribuciones instaladas»: hay que usar
el de Git Bash. Uso: from git_bash import BASH; subprocess.run([BASH, "script.sh", ...])."""
import os, shutil


def bash():
    if os.name != "nt": return "bash"
    for p in (os.environ.get("GIT_BASH", ""), r"C:\Program Files\Git\bin\bash.exe", r"C:\Program Files (x86)\Git\bin\bash.exe",
              os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\bin\bash.exe")):
        if p and os.path.exists(p): return p
    g = shutil.which("git")
    if g:
        p = os.path.join(os.path.dirname(os.path.dirname(g)), "bin", "bash.exe")
        if os.path.exists(p): return p
    b = shutil.which("bash")
    if b and "system32" not in b.lower(): return b
    raise SystemExit("No encuentro Git Bash (el bash de WSL no vale): instala Git for Windows o pon su ruta en GIT_BASH.")


BASH = bash()
