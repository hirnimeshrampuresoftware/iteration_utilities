#ifndef PYIU_HELPER_H
#define PYIU_HELPER_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "helpercompat.h"

#ifdef PyIU_DEBUG
  #define PyIU_ASSERT(e) if (!(e)) { fprintf(stderr, "Assertion failed: %s\nFile: %s\nLine: %d\n", #e, __FILE__, __LINE__); abort(); }
#else
  #define PyIU_ASSERT(e)
#endif

#define PyIU_Set_CheckExact(ob) (Py_TYPE(ob) == &PySet_Type)

#define PyIU_SMALL_ARG_STACK_SIZE 5

extern PyObject *PyIU_global_zero;
extern PyObject *PyIU_global_one;
extern PyObject *PyIU_global_two;
extern PyObject *PyIU_global_0tuple;

PyObject *PyIU_CreateIteratorTuple(PyObject *tuple);
PyObject *PyIU_TupleReverse(PyObject *tuple);
PyObject *PyIU_TupleCopy(PyObject *tuple);
void PyIU_TupleInsert(PyObject *tuple, Py_ssize_t where, PyObject *v, Py_ssize_t num);
void PyIU_TupleRemove(PyObject *tuple, Py_ssize_t where, Py_ssize_t num);
PyObject *PyIU_TupleGetSlice(PyObject *tuple, Py_ssize_t num);
void PyIU_InitializeConstants(void);

/******************************************************************************
 * Function call abstractions
 *
 * To support the different calling conventions across Python versions
 *****************************************************************************/

static inline PyObject*
PyIU_CallWithOneArgument(PyObject *callable, PyObject *arg1) {
    #if PyIU_USE_VECTORCALL
        PyObject *args[1];
        args[0] = arg1;
        return _PyObject_Vectorcall(callable, args, 1, NULL);
    #elif PyIU_USE_FASTCALL
        PyObject *args[1];
        args[0] = arg1;
        return _PyObject_FastCall(callable, args, 1);
    #else
        PyObject *result;
        PyObject *args = PyTuple_New(1);
        if (args == NULL) {
            return NULL;
        }
        Py_INCREF(arg1);
        PyTuple_SET_ITEM(args, 0, arg1);
        result = PyObject_Call(callable, args, NULL);
        Py_DECREF(args);
        return result;
    #endif
}

static inline PyObject*
PyIU_CallWithTwoArguments(PyObject *callable, PyObject *arg1, PyObject *arg2) {
    #if PyIU_USE_VECTORCALL
        PyObject *args[2];
        args[0] = arg1;
        args[1] = arg2;
        return _PyObject_Vectorcall(callable, args, 2, NULL);
    #elif PyIU_USE_FASTCALL
        PyObject *args[2];
        args[0] = arg1;
        args[1] = arg2;
        return _PyObject_FastCall(callable, args, 2);
    #else
        PyObject *result;
        PyObject *args = PyTuple_New(2);
        if (args == NULL) {
            return NULL;
        }
        Py_INCREF(arg1);
        Py_INCREF(arg2);
        PyTuple_SET_ITEM(args, 0, arg1);
        PyTuple_SET_ITEM(args, 1, arg2);
        result = PyObject_Call(callable, args, NULL);
        Py_DECREF(args);
        return result;
    #endif
}

#define PyIU_USE_CPYTHON_INTERNALS PYIU_CPYTHON

static inline void
PyIU_CopyTupleToArray(PyObject *tuple, PyObject **array, size_t n_objects) {
    #if PyIU_USE_CPYTHON_INTERNALS
        memcpy(array, ((PyTupleObject *)tuple)->ob_item, n_objects * sizeof(PyObject *));
    #else
        Py_ssize_t i;
        for (i = 0; i < n_objects; i++) {
            array[i] = PyTuple_GET_ITEM(tuple, i);
        }
    #endif
}

static inline void
PyIU_CopyListToArray(PyObject *list, PyObject **array, size_t n_objects) {
    #if PyIU_USE_CPYTHON_INTERNALS
        memcpy(array, ((PyListObject *)list)->ob_item, n_objects * sizeof(PyObject *));
    #else
        Py_ssize_t i;
        for (i = 0; i < n_objects; i++) {
            array[i] = PyList_GET_ITEM(list, i);
        }
    #endif
}

#undef PyIU_USE_TUPLE_INTERNALS

#endif
