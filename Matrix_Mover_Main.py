from commands import *

def main():
    app = QApplication([])
    window = commands()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()