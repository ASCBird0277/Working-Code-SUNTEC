from pywinauto import Application

app = Application().connect(title_re=".*Revu*", backend="win32", visible_only=False)
for win in app.windows():
    print(f"Window Title: {win.window_text()}, Handle: {win.handle}")

