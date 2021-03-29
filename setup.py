from cx_Freeze import setup, Executable

exe = Executable(
    script="arcade_project.py",
    base="Win32GUI",
    )

setup(
    name = "Arcade-project",
    version = "1.0",
    description = "dev° project by Arthur and Cyrian",
    executables = [exe]
    )