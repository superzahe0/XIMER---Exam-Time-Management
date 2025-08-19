````markdown
# XIMER - Exam Time Management

XIMER is a Python Tkinter application that helps divide exam time across questions.

## Features
- Total exam timer (fixed, only decreases).
- Per-question timer that counts down independently.
- Redistribution of remaining total time across unanswered questions when finishing early.
- Negative per-question timer if time runs out.
- Pause/Resume functionality.
- Reset to start over.

## Requirements
- Python 3.8+
- Tkinter (comes bundled with most Python installations)

## Run the App
1. Clone or download the repository:
   ```bash
   git clone https://github.com/superzahe0/XIMER.git
   cd XIMER
````

2. Run the program:

   ```bash
   python XIMER.py
   ```

## Build as Executable (Windows)

1. Install pyinstaller:

   ```bash
   pip install pyinstaller
   ```

2. Create the executable:

   ```bash
   pyinstaller --onefile --windowed XIMER.py
   ```

3. The file `XIMER.exe` will be located in the `dist/` folder.
   Share this file with others and they can run the app without Python.

## Keyboard Shortcuts

* **Spacebar** → Pause/Resume the timer.

## License

MIT License

```
```
