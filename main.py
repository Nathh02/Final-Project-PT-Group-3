import tkinter as tk
from gui import DiskSchedulingApp


def main() -> None:
    root = tk.Tk()
    DiskSchedulingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()