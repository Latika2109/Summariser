import sys
from PyQt5.QtWidgets import QApplication
from api_client import APIClient
from login_window import LoginWindow
from upload_window import UploadWindow


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    
    # create API client
    api_client = APIClient()
    
    # show login window
    login_window = LoginWindow(api_client)
    
    if login_window.exec_() == LoginWindow.Accepted:
        # login successful, show main window
        main_window = UploadWindow(api_client, login_window.user_data)
        main_window.show()
        sys.exit(app.exec_())
    else:
        # login cancelled
        sys.exit(0)


if __name__ == '__main__':
    main()
