#include <Python.h>
#include <random>
#include <algorithm>
#include <array>

enum class TETROMINO {
    I, O, T, S, Z, J, L, COUNT
};

const std::array<std::array<unsigned char, 3>, static_cast<size_t>(TETROMINO::COUNT)> COLORS = {{
    {0, 255, 255},  // I
    {255, 255, 0},  // O
    {128, 0, 128},  // T
    {0, 255, 0},    // S
    {255, 0, 0},    // Z
    {0, 0, 255},    // J
    {255, 165, 0}   // L
}};

static PyObject* py_generate7bag(PyObject*, PyObject* args) {
    int size;
    if (!PyArg_ParseTuple(args, "i", &size)) {
        return nullptr;
    }

    PyObject* list = PyList_New(size);
    if (!list) return nullptr;

    static std::random_device rd;
    static std::mt19937 gen(rd());

    std::vector<TETROMINO> bag;
    for (int i = 0; i < size; ) {
        if (bag.empty()) {
            bag = {TETROMINO::I, TETROMINO::O, TETROMINO::T,
                   TETROMINO::S, TETROMINO::Z, TETROMINO::J, TETROMINO::L};
            std::shuffle(bag.begin(), bag.end(), gen);
        }

        PyList_SET_ITEM(list, i++, PyLong_FromLong(static_cast<int>(bag.back())));
        bag.pop_back();
    }

    return list;
}

static PyObject* py_get_colors(PyObject*, PyObject* args) {
    int tetromino_int;
    if (!PyArg_ParseTuple(args, "i", &tetromino_int)) {
        return nullptr;
    }

    if (tetromino_int < 0 || tetromino_int >= static_cast<int>(TETROMINO::COUNT)) {
        PyErr_SetString(PyExc_ValueError, "Invalid TETROMINO value.");
        return nullptr;
    }

    TETROMINO type = static_cast<TETROMINO>(tetromino_int);
    const auto& color = COLORS[static_cast<size_t>(type)];

    return Py_BuildValue("(BBB)", color[0], color[1], color[2]);
}

static PyMethodDef TetrisAPI_Methods[] = {
    {"generate7bag", py_generate7bag, METH_VARARGS, "Generate a 7-bag sequence of TETROMINOs."},
    {"get_colors", py_get_colors, METH_VARARGS, "Get RGB color of a TETROMINO."},
    {nullptr, nullptr, 0, nullptr}
};

static struct PyModuleDef TetrisAPI_Module = {
    PyModuleDef_HEAD_INIT,
    "TetrisAPI",
    "Tetris API Module",
    -1,
    TetrisAPI_Methods
};

PyMODINIT_FUNC PyInit_TetrisAPI(void) {
    return PyModule_Create(&TetrisAPI_Module);
}
