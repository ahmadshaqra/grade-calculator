# Grade Calculator

A simple grade calculator app (for Monash University).\
by **Ahmad Abu-Shaqra**

## Instructions to Build Executable

First, be sure to have installed `pyinstaller` on your system. Open a terminal and enter the following command:

```bash
pip install pyinstaller
```

Next, ensure that your terminal is in the project directory, you can check this using the following command:

```bash
pwd
```

Finally, run the following `pyinstaller` command to build the executable:

```bash
pyinstaller main.py --name=GradeCalculator --add-data="assets:assets" --icon=assets/icon.ico --onefile -w
```

After successfully building your executable, you will find the `main.exe` file in the `dist` folder.
