#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <opcode.h>
#include <stdio.h>

#define PUSH_OP(a, b)             \
    do {                          \
        bytecode[bc_len] = a;     \
        bytecode[bc_len + 1] = b; \
        bc_len += 2;              \
        op_len++;                 \
    } while (0)

enum opcode {
    O_NOP,
    O_MARK,
    O_FOR,
    O_JMP_BACK,
    O_GET_ITEM,
    O_INP,
    O_DICT,
    O_CONST,
    O_SLICE,
    O_MOV,
    O_STORE_TUPLE,
    O_VEC_SUB,
    O_VEC_ADD,
    O_VEC_CROSS,
    O_ASSERT,
};

uint8_t magic[] = {
    // (a, b) = d[inp[0]]
    O_CONST, 2,
    O_INP,
    O_GET_ITEM,
    O_DICT,
    O_GET_ITEM,
    O_STORE_TUPLE, 0,
    O_CONST, 3,
    O_CONST, 4,
    O_SLICE,
    O_INP,
    O_GET_ITEM,
    // for (c, d) in inp[1:]
    O_FOR, /* mark */ 0, /* end */ 1,
    O_DICT,
    O_GET_ITEM,
    O_STORE_TUPLE, 1,
    // (c, d) -= (a, b)
    O_VEC_SUB, 1, 0,
    // for k in d
    O_DICT,
    O_FOR, 2, 3,
    O_DICT,
    O_GET_ITEM,
    // (e, f) = d[k]
    O_STORE_TUPLE, 2,
    // (e, f) -= (a, b)
    O_VEC_SUB, 2, 0,
    O_VEC_CROSS, 1, 2,
    O_ASSERT,
    O_JMP_BACK, 2,
    O_MARK, 3,
    O_VEC_ADD, 1, 0,
    O_MOV, 0, 1,
    O_JMP_BACK, 0,
    O_MARK, 1};

int main(void) {
    puts("you'll never guess my flag >:)");
    char inp[32];
    fgets(inp, 32, stdin);
    inp[strcspn(inp, "\n")] = '\0';
    if (strlen(inp) != 21 || inp[0] != 'h') {
        puts("not even close >:)");
        return 0;
    }
    Py_Initialize();
    PyObject* d = PyDict_New();
    PyRun_String("def dicegang():\n x = input().encode()\n for (a, b) in zip(x, bytes.fromhex('4e434e0a53455f0a584f4b4646530a5e424344410a435e0d4e0a484f0a5e424b5e0a4f4b5953')):\n  if a ^ 42 != b:\n   return False\n return True", Py_file_input, PyDict_New(), d);
    PyObject* f = PyDict_GetItem(d, PyUnicode_FromString("dicegang"));
    PyCodeObject* c = (PyCodeObject*)PyFunction_GetCode(f);
    c->co_names = PyTuple_New(0);
    // PyTuple_SetItem(c->co_names, 0, PyUnicode_FromString("print"));
    c->co_varnames = PyTuple_New(0);
    c->co_nlocals = 6;
    c->co_stacksize = 300;
    c->co_consts = PyTuple_New(7);
    PyTuple_SetItem(c->co_consts, 0, PyUnicode_FromString(inp));
    char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}";
    int xvals[] = {13, -13, 42, 40, -47, -20, 14, -1, 9, 42, -34, 44, 46, 22, -25, -44, 8, 1, -17, -14, 9, 43, 40, 33, -28, 10, 35, 4, -42, 21, 3, -8, -32, -18, 27, -10, 4, -21, -27, 13, 11, -33, -13, 26, 36, -27, -13, 42, -32, -12, -29, 8, 34, -37, 25, -34, -13, 1, -30, 27, -5, 37, 20, -49, 9};
    int yvals[] = {22, -9, 15, 0, 8, -29, -36, 48, -27, -22, -9, -5, 1, -39, 42, 14, 14, 2, -39, 31, 21, -18, 12, 9, 25, -17, -20, -32, -22, 19, 26, -6, -2, -42, -39, 26, 41, 34, 10, -47, -47, -34, -33, -34, -29, -40, -42, 23, -24, -23, -39, 30, 8, -13, 38, -7, 13, -25, 33, -10, 37, 1, -46, -2, 45};
    PyObject* ptd = PyDict_New();
    for (int i = 0; i < sizeof(charset) - 1; i++) {
        PyObject* pt = PyTuple_New(2);
        PyTuple_SetItem(pt, 0, PyLong_FromLong(xvals[i]));
        PyTuple_SetItem(pt, 1, PyLong_FromLong(yvals[i]));
        PyDict_SetItem(ptd, PyUnicode_FromStringAndSize(charset + i, 1), pt);
    }
    PyTuple_SetItem(c->co_consts, 1, ptd);
    PyTuple_SetItem(c->co_consts, 2, Py_False);
    PyTuple_SetItem(c->co_consts, 3, Py_True);
    PyTuple_SetItem(c->co_consts, 4, PyLong_FromLong(0));
    PyTuple_SetItem(c->co_consts, 5, PyLong_FromLong(1));
    PyTuple_SetItem(c->co_consts, 6, Py_None);
    char bytecode[100000] = {0};
    int bc_len = 0;
    int op_len = 0;
    int marks[256] = {0};
    int relocs[1000] = {0};
    int reloci[1000] = {0};
    uint8_t relocm[1000] = {0};
    int r_len = 0;
    int ip = 0;
    while (ip < sizeof(magic)) {
        int l;
        switch (magic[ip]) {
            // case O_DEBUG:
            //     PUSH_OP(LOAD_GLOBAL, 0);
            //     PUSH_OP(ROT_TWO, 0);
            //     PUSH_OP(CALL_FUNCTION, 1);
            //     PUSH_OP(POP_TOP, 0);
            //     break;
            case O_INP:
                PUSH_OP(LOAD_CONST, 0);
                break;
            case O_DICT:
                PUSH_OP(LOAD_CONST, 1);
                break;
            case O_CONST:
                ip++;
                PUSH_OP(LOAD_CONST, 2 + magic[ip]);
                break;
            case O_NOP:
                PUSH_OP(NOP, 0);
                break;
            case O_FOR:
                PUSH_OP(GET_ITER, 0);
                ip++;
                marks[magic[ip]] = op_len;
                PUSH_OP(FOR_ITER, 0);
                relocs[r_len] = bc_len - 1;
                reloci[r_len] = op_len;
                ip++;
                relocm[r_len] = magic[ip];
                r_len++;
                break;
            case O_MARK:
                ip++;
                marks[magic[ip]] = op_len;
                break;
            case O_JMP_BACK:
                PUSH_OP(JUMP_ABSOLUTE, 0);
                relocs[r_len] = bc_len - 1;
                reloci[r_len] = -1;
                ip++;
                relocm[r_len] = magic[ip];
                r_len++;
                break;
            case O_GET_ITEM:
                PUSH_OP(ROT_TWO, 0);
                PUSH_OP(BINARY_SUBSCR, 0);
                break;
            case O_STORE_TUPLE:
                ip++;
                l = magic[ip] * 2;
                PUSH_OP(UNPACK_SEQUENCE, 2);
                PUSH_OP(STORE_FAST, l);
                PUSH_OP(STORE_FAST, l + 1);
                break;
            case O_SLICE:
                PUSH_OP(BUILD_SLICE, 0);
                break;
            // case O_WO:
            //     ip ++;
            //     l = magic[ip] * 2;
            //     PUSH_OP(LOAD_FAST, l);
            //     PUSH_OP(LOAD_FAST, l + 1);
            //     PUSH_OP(BUILD_TUPLE, 2);
            //     break;
            case O_MOV:
                ip++;
                l = magic[ip] * 2;
                ip++;
                PUSH_OP(LOAD_FAST, magic[ip] * 2);
                PUSH_OP(STORE_FAST, l);
                PUSH_OP(LOAD_FAST, magic[ip] * 2 + 1);
                PUSH_OP(STORE_FAST, l + 1);
                break;
            case O_VEC_SUB:
                ip++;
                l = magic[ip] * 2;
                ip++;
                PUSH_OP(LOAD_FAST, l);
                PUSH_OP(LOAD_FAST, magic[ip] * 2);
                PUSH_OP(BINARY_SUBTRACT, 0);
                PUSH_OP(STORE_FAST, l);
                PUSH_OP(LOAD_FAST, l + 1);
                PUSH_OP(LOAD_FAST, magic[ip] * 2 + 1);
                PUSH_OP(BINARY_SUBTRACT, 0);
                PUSH_OP(STORE_FAST, l + 1);
                break;
            case O_VEC_ADD:
                ip++;
                l = magic[ip] * 2;
                ip++;
                PUSH_OP(LOAD_FAST, l);
                PUSH_OP(LOAD_FAST, magic[ip] * 2);
                PUSH_OP(BINARY_ADD, 0);
                PUSH_OP(STORE_FAST, l);
                PUSH_OP(LOAD_FAST, l + 1);
                PUSH_OP(LOAD_FAST, magic[ip] * 2 + 1);
                PUSH_OP(BINARY_ADD, 0);
                PUSH_OP(STORE_FAST, l + 1);
                break;
            case O_VEC_CROSS:
                ip++;
                l = magic[ip] * 2;
                ip++;
                PUSH_OP(LOAD_FAST, l);
                PUSH_OP(LOAD_FAST, magic[ip] * 2 + 1);
                PUSH_OP(BINARY_MULTIPLY, 0);
                PUSH_OP(LOAD_FAST, l + 1);
                PUSH_OP(LOAD_FAST, magic[ip] * 2);
                PUSH_OP(BINARY_MULTIPLY, 0);
                PUSH_OP(BINARY_SUBTRACT, 0);
                PUSH_OP(LOAD_CONST, 4);
                PUSH_OP(COMPARE_OP, 5);
                break;
            case O_ASSERT:
                PUSH_OP(POP_JUMP_IF_TRUE, op_len + 3);
                PUSH_OP(LOAD_CONST, 2);
                PUSH_OP(RETURN_VALUE, 0);
        }
        ip++;
    }
    for (int i = 0; i < r_len; i++) {
        int m = marks[relocm[i]];
        int ins = reloci[i];
        if (ins == -1) {
            assert(m < 256);
            bytecode[relocs[i]] = m;
        } else if (m >= ins) {
            assert(m - ins < 256);
            bytecode[relocs[i]] = m - ins;
        } else {
            assert(ins - m < 256);
            bytecode[relocs[i]] = ins - m;
        }
    }
    PUSH_OP(LOAD_CONST, 3);
    PUSH_OP(RETURN_VALUE, 0);
    c->co_code = PyBytes_FromStringAndSize(bytecode, bc_len);
    PyRun_String("if dicegang():\n print('ok fine you got the flag')\nelse:\n print('nope >:)')", Py_file_input, PyDict_New(), d);
    Py_Finalize();
    return 0;
}
