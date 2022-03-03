PUBLISH_DIR=../publish-win

CLIENT_EXE=LabSupportClient.exe
CLIENT_CON_EXE=LSCWithConsole.exe
UPDATER_EXE=Update.exe
INF_DIR=app\src\updates
INF_FILENAME=inf.json

CLIENT=$(PUBLISH_DIR)\$(CLIENT_EXE)
CLIENT_WITH_CONSOLE=$(PUBLISH_DIR)\$(CLIENT_CON_EXE)
UPDATER=$(PUBLISH_DIR)\$(UPDATER_EXE)
JSON=$(PUBLISH_DIR)\$(INF_DIR)\$(INF_FILENAME)
ZIP=$(PUBLISH_DIR)\LS_Windows.zip

JSON_SRC=../app/src/updates/inf.json
CLIENT_SRCS=../LabSupportClient.py ../app/src/GUI.py ../app/src/Student.py ../app/src/config.py ../app/src/emailWriter.py ../app/src/SheetReader.py ../app/src/tooltip.py ../app/src/ui_utils.py ../app/src/platform.py ../app/src/updates/updater.py
UPDATER_SRCS=../app/src/updates/updater.py ../Update.py

TARGETS= $(CLIENT) $(CLIENT_WITH_CONSOLE) $(UPDATER) $(JSON) $(ZIP)

PYTHON_EXECUTABLE=..\venv\Scripts\python.exe
PYTHON_FLAGS=-OO -m
PYINS_FLAGS=--clean --exclude matplotlib --exclude scipy --exclude pandas --hidden-import='pkg_resources.py2_warn'

$(ZIP): $(CLIENT) $(CLIENT_WITH_CONSOLE) $(JSON)
	cd publish && 7z.exe a -tzip LS_WINDOWS.zip app $(CLIENT_EXE) $(CLIENT_CON_EXE)

.PHONY:
all: $(TARGETS)

.PHONY:
client: $(CLIENT)

.PHONY:
client_all: $(CLIENT) $(CLIENT_WITH_CONSOLE)

.PHONY:
client_console: $(CLIENT_WITH_CONSOLE)

.PHONY:
updater: $(UPDATER)

$(CLIENT): $(CLIENT_SRCS)
	$(PYTHON_EXECUTABLE) $(PYTHON_FLAGS) PyInstaller -Fw ../LabSupportClient.py --distpath $(PUBLISH_DIR) $(PYINS_FLAGS)

$(CLIENT_WITH_CONSOLE): $(CLIENT_SRCS)
	$(PYTHON_EXECUTABLE) $(PYTHON_FLAGS) PyInstaller -F ../LabSupportClient.py --distpath=$(PUBLISH_DIR) $(PYINS_FLAGS) --name LSCWithConsole.exe

$(UPDATER): $(UPDATER_SRCS)
	$(PYTHON_EXECUTABLE) $(PYTHON_FLAGS) PyInstaller -F --distpath $(PUBLISH_DIR) $(PYINS_FLAGS) ../Update.py

$(JSON): $(JSON_SRC)
	cp $(JSON_SRC) $(PUBLISH_DIR)\$(INF_DIR)\


$(PYTHON_EXECUTABLE):
	python3 -m venv venv

.PHONY:
venv_: $(PYTHON_EXECUTABLE)
	$(PYTHON_EXECUTABLE) -m pip install wheel
	$(PYTHON_EXECUTABLE) -m pip install PyInstaller
	$(PYTHON_EXECUTABLE) -m pip install gspread
	$(PYTHON_EXECUTABLE) -m pip install oauth2client
	$(PYTHON_EXECUTABLE) -m pip install google-api-python-client==1.8.0

test_script:
	$(PYTHON_EXECUTABLE) LabSupportClient.py

# .PHONY:
# publish: LabSupportClient.py Update.py app/src/GUI.py app/src/Student.py app/src/config.py
# 	$(PYTHON_EXECUTABLE) -m PyInstaller -Fw LabSupportClient.py --distpath $(PUBLISH_DIR)
# 	$(PYTHON_EXECUTABLE) -m PyInstaller -F LabSupportClient.py --distpath $(PUBLISH_DIR) --name LSCWithConsole.exe
# 	$(PYTHON_EXECUTABLE) -m PyInstaller -Fw Update.py --distpath $(PUBLISH_DIR)
# 	cp .\app\src\updates\inf.json .\publish\app\src\updates\inf.json
# 	cd publish && 7z.exe a -tzip LS_WINDOWS.zip app LabSupportClient.exe

.PHONY:
clean:
	rm -rf ./publish/*
