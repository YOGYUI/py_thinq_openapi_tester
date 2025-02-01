if __name__ == '__main__':
    import sys
    from GUI import MainWindow
    from ThinQ import ThinqCore
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    # QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    # QApplication.setStyle('fusion')
    mainWnd = MainWindow(ThinqCore())
    mainWnd.show()
    app.exec()
