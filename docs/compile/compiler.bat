python -m nuitka --standalone --show-progress --follow-imports --windows-uac-admin --plugin-enable=pyqt5 --windows-disable-console --windows-icon-from-ico=recipient.ico recipient.py
xcopy locale recipient.dist\\locale /s /e /i