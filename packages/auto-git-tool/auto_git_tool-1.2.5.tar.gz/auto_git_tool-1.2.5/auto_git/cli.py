import subprocess
from termcolor import colored
import os

def run_git_command(command, description=None, style="white", print_output=True):
    """Git komandalarni bajarish va natijasini qaytarish"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if description:
        print(colored(f"\n{' ' + description + ' ':─^100}", style))

    output = stdout.decode("utf-8").strip()
    error = stderr.decode("utf-8").strip()

    if print_output:
        if output:
            print(colored(output, style))
        if error:
            print(colored(error, "red"))

    return output


def ensure_git_repository():
    """Git repozitoriy mavjudligini tekshiradi, yo'q bo‘lsa yaratadi"""
    if not os.path.exists(".git"):
        print(colored("⚠️ Siz hali Git repozitoriyga ulanmagansiz!", "red"))
        run_git_command("git init", "Yangi Git repozitoriy yaratildi", "cyan")
        remote = input(colored("🔗 Ulanadigan Git remote URL ni kiriting: ", "yellow")).strip()
        if remote:
            run_git_command(f"git remote add origin {remote}", "Remote URL qo‘shildi", "green")
        else:
            print(colored("❌ Remote URL ko‘rsatilmagan, push bosqichi bajarilmaydi!", "red"))


def ensure_main_branch():
    """Agar hech qanday branch bo'lmasa, 'main' branchni yaratadi"""
    current_branch = run_git_command("git branch --show-current", print_output=False)

    if not current_branch:
        run_git_command("git checkout -b main", "main branch yaratildi", "blue")


def aic():
    """Auto Git: add → AI commit → push"""
    
    
    ensure_git_repository()
    ensure_main_branch()
    
    run_git_command("git add .", "Fayllar qo‘shildi (staged)", "green")

    run_git_command("git diff --cached --name-status", "O'zgargan fayllar", "yellow")

    aic_commit = run_git_command("aic", "AI asosidagi commit xabari", "cyan")
    aic_commit = aic_commit.strip("`'\" ").splitlines()[0]  

    if not aic_commit:
        print(colored("❌ AI commit xabari olinmadi!", "red"))
        return

    # 4. Commit
    run_git_command(f'git commit -m "{aic_commit}"', "Commit bajarildi", "magenta")

    # 5. Push
    run_git_command("git push origin main", "main branchiga push qilinmoqda", "blue")

    print(colored("\n✅ Hammasi muvaffaqiyatli yakunlandi!", "green"))
