cmake_minimum_required (VERSION 3.10)
project (Qtendo)



#Compile .ui files
set (UI_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/ui")
set (UI_FILES
    "${UI_ROOT}/window.ui"
    "${UI_ROOT}/emulator.ui")

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



#Compile python
set (PY_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/src")
set (PY_MAIN "${PY_ROOT}/main.py")
set (PY_FILES ${PY_FILES}
    "${PY_ROOT}/utils.py"
    "${PY_ROOT}/main_window.py"
    "${PY_ROOT}/emulators/emulator.py"
    "${PY_ROOT}/emulators/emulators.py"
    "${PY_ROOT}/emulators/fceux.py"
    "${PY_ROOT}/emulators/zsnes.py"
    "${PY_ROOT}/emulators/mupen64plus.py"
    "${PY_ROOT}/emulators/dolphin.py"
    "${PY_ROOT}/emulators/citra.py")

foreach (PY_FILE ${PY_FILES})
    string (REPLACE "${CMAKE_CURRENT_SOURCE_DIR}/" "" TARGET_FILE ${PY_FILE})
    set (PY_FILE_TUPLE_LIST_PRE ${PY_FILE_TUPLE_LIST_PRE} "( '${PY_FILE}', '${TARGET_FILE}' ), ")
endforeach ()
string (LENGTH "${PY_FILE_TUPLE_LIST_PRE}" LEN_PRE)
math (EXPR LEN "${LEN_PRE} - 2")
string (SUBSTRING "${PY_FILE_TUPLE_LIST_PRE}" 0 ${LEN} PY_FILE_TUPLE_LIST_LIST)
string (REPLACE ";" "" PY_FILE_TUPLE_LIST "${PY_FILE_TUPLE_LIST_PRE}")

configure_file ("${CMAKE_CURRENT_SOURCE_DIR}/cmake/setup.py.in" "${CMAKE_BINARY_DIR}/setup.py")

find_program (PYTHON python3)
add_custom_target (cx ALL DEPENDS ui resources SOURCES ${PY_MAIN} ${PY_FILES})
add_custom_command (TARGET cx
    DEPENDS ui
    COMMAND echo "Running setup.py"
    COMMAND ${PYTHON} setup.py install)
