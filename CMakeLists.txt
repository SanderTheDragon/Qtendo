cmake_minimum_required (VERSION 3.10)
project (Qtendo LANGUAGES NONE)



#Compile .ui files
set (UI_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/ui")
set (UI_FILES
    "${UI_ROOT}/about.ui"
    "${UI_ROOT}/emulator.ui"
    "${UI_ROOT}/emulator_download.ui"
    "${UI_ROOT}/emulator_settings.ui"
    "${UI_ROOT}/settings.ui"
    "${UI_ROOT}/window.ui")

find_program (PYUIC5 pyuic5)
add_custom_target (ui SOURCES ${UI_FILES})
foreach (UI_FILE ${UI_FILES})
    #CMake regex won't work, so this is required
    string (SUBSTRING ${UI_FILE} 1 -1 UI_FILE_POST)
    string (REPLACE "/" ";" UI_FILE_PARTS ${UI_FILE_POST})
    list (REVERSE UI_FILE_PARTS)
    list (GET UI_FILE_PARTS 0 UI_FILE_PART)
    string (LENGTH ${UI_FILE_PART} LEN_PRE)
    math (EXPR LEN "${LEN_PRE} - 3")
    string (SUBSTRING ${UI_FILE_PART} 0 ${LEN} UI_FILE_TARGET_PRE)
    set (UI_FILE_TARGET "ui_${UI_FILE_TARGET_PRE}.py")
    list (REMOVE_AT UI_FILE_PARTS 0)
    list (INSERT UI_FILE_PARTS 0 ${UI_FILE_TARGET})
    list (REVERSE UI_FILE_PARTS)
    string (REPLACE ";" "/" PY_FILE_PRE "${UI_FILE_PARTS}")
    set (PY_FILE "/${PY_FILE_PRE}")
    add_custom_command (TARGET ui PRE_BUILD
        COMMAND echo "Compiling ${UI_FILE}"
        COMMAND ${PYUIC5} ${UI_FILE} > ${PY_FILE})
endforeach ()



#Compile .qrc files
set (QRC_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/res")
set (QRC_FILES
    "${QRC_ROOT}/icons.qrc")

find_program (PYRCC5 pyrcc5)
add_custom_target (resources SOURCES ${QRC_FILES})
foreach (QRC_FILE ${QRC_FILES})
    string (REPLACE "qrc" "py" PY_FILE ${QRC_FILE})
    add_custom_command (TARGET resources PRE_BUILD
        COMMAND echo "Compiling ${QRC_FILE}"
        COMMAND ${PYRCC5} ${QRC_FILE} > ${PY_FILE})
endforeach ()



#"Compile" python
set (PY_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/src")
set (PY_MAIN "${PY_ROOT}/main.py")
set (PY_FILES ${PY_FILES}
    "${PY_ROOT}/__init__.py"
    "${PY_ROOT}/main_window.py"
    "${PY_ROOT}/syntax.py"
    "${PY_ROOT}/system.py"
    "${PY_ROOT}/utils.py"

    "${PY_ROOT}/dialogs/__init__.py"
    "${PY_ROOT}/dialogs/about.py"
    "${PY_ROOT}/dialogs/emulator_settings.py"
    "${PY_ROOT}/dialogs/settings.py"

    "${PY_ROOT}/emulators/__init__.py"
    "${PY_ROOT}/emulators/citra.py"
    "${PY_ROOT}/emulators/dolphin.py"
    "${PY_ROOT}/emulators/emulator.py"
    "${PY_ROOT}/emulators/fceux.py"
    "${PY_ROOT}/emulators/mupen64plus.py"
    "${PY_ROOT}/emulators/zsnes.py"

    "${PY_ROOT}/roms/__init__.py"
    "${PY_ROOT}/roms/3ds.py"
    "${PY_ROOT}/roms/fds.py"
    "${PY_ROOT}/roms/gamecube.py"
    "${PY_ROOT}/roms/n64.py"
    "${PY_ROOT}/roms/nes.py"
    "${PY_ROOT}/roms/rom.py"
    "${PY_ROOT}/roms/snes.py"
    "${PY_ROOT}/roms/wii.py")

find_program (PYTHON python3)

if (CMAKE_BUILD_TYPE STREQUAL "Release")
    string (TOLOWER ${PROJECT_NAME} EXEC_NAME)

    find_program (PYINSTALLER pyinstaller
        PATHS "~/.local/bin")
    add_custom_target (pyinstaller ALL DEPENDS ui resources SOURCES ${PY_MAIN} ${PY_FILES})
    add_custom_command (TARGET pyinstaller
        DEPENDS ui
        COMMAND echo "Running PyInstaller..."
        COMMAND ${PYINSTALLER} -F ${PY_MAIN}
                    --distpath "${CMAKE_BINARY_DIR}"
                    --workpath "${CMAKE_BINARY_DIR}/build"
                    --hidden-import src.roms.3ds
                    --hidden-import src.roms.fds
                    --hidden-import src.roms.gamecube
                    --hidden-import src.roms.n64
                    --hidden-import src.roms.nes
                    --hidden-import src.roms.snes
                    --hidden-import src.roms.wii
                    --hidden-import PyQt5
                    --name ${EXEC_NAME})

    add_custom_target (qtendo SOURCES ${PY_MAIN} ${PY_FILES})
    add_custom_command (TARGET qtendo
        COMMAND echo "Running Qtendo..."
        COMMAND "${CMAKE_BINARY_DIR}/${EXEC_NAME}")
else ()
    add_custom_target (qtendo DEPENDS ui resources SOURCES ${PY_MAIN} ${PY_FILES})
    add_custom_command (TARGET qtendo
        COMMAND echo "Running Qtendo..."
        COMMAND PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR} ${PYTHON} ${PY_MAIN})
endif (CMAKE_BUILD_TYPE STREQUAL "Release")
