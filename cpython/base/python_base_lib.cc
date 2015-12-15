// Copyright 2012 letv Inc. All Rights Reserved.
// Author: guoxiaohe@letv.com

#include <Python.h>

#include "hash.h"

static PyObject* get_fingerprint_i64(PyObject* self, PyObject* args) {
  char* key;
  if (!PyArg_ParseTuple(args, "s", &key)) {
    return NULL;
  }
  uint64 fp = base::Fingerprint(key);
  return PyInt_FromLong(fp);
}

static PyObject* get_fingerprint_i32(PyObject* self, PyObject* args) {
  char* key;
  if (!PyArg_ParseTuple(args, "s", &key)) {
    return NULL;
  }
  uint32 fp = base::Fingerprint32(key);
  return PyInt_FromLong(fp);
}

static PyMethodDef methods [] = {
  {"get_fingerprint_i64", (PyCFunction)get_fingerprint_i64, METH_VARARGS, NULL},
  {"get_fingerprint_i32", (PyCFunction)get_fingerprint_i32, METH_VARARGS, NULL},
};

PyMODINIT_FUNC initletvbase(void) {
  Py_InitModule3("letvbase", methods, "Letv.Inc base lib, the basic infrastructure, All\
                 the other module dependce on, avoid using different implements,\
                 we recommend wrap the c++ method lib to python call, guoxiaohe@letv.com");
}

