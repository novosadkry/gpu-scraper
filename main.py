import signal
from app import App

app = App()

if __name__ == '__main__':
    try:
        app.start()
    except:
        app.stop()
