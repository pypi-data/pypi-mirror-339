#define PY_SSIZE_T_CLEAN
#include <Python.h>

/**
 * Read the pointer from the Python capsule and into the output pointer provided by the user.
 * 
 * Note: this is to be called directly from Mojo, not from Python.
 *
 * Returns 0 on success, a negative number on failure.
 */  
int mos_capsule_get_pointer(PyObject * capsule, const char* capsule_name, void** output) {
    
    // Check if it's a valid PyCapsule
    if (!PyCapsule_IsValid(capsule, capsule_name)) {
        Py_DECREF(capsule);
        *output = NULL;
        return -1;
    }
    
    // We need to increase the reference count otherwise we get garbage. This creates a memory leak.
    Py_INCREF(capsule);
    // Extract the capsule pointer
    *output = PyCapsule_GetPointer(capsule, capsule_name);
    
    return 0;
}

const char* mos_capsule_get_name(PyObject * capsule) {
    // Read the capsuke name, mostly for debugging.
    // We need to increase the reference count otherwise we get garbage. This creates a memory leak.
    Py_INCREF(capsule);
    const char * name = PyCapsule_GetName(capsule);
    return name;
} 

/** 
  * A python accessible extension function for testing.
  */
static PyObject* arrow_stream(PyObject* self, PyObject* args) {
    PyObject* obj;
    
    // Parse the Python object passed
    if (!PyArg_ParseTuple(args, "O", &obj)) {
        return NULL;
    }
    
    // Check if the object has __arrow_c_stream attribute
    if (!PyObject_HasAttrString(obj, "__arrow_c_stream__")) {
        PyErr_SetString(PyExc_TypeError, "Object does not have __arrow_c_stream__ attribute");
        return NULL;
    }
    
    // Get the __arrow_c_stream__ attribute
    PyObject* stream_func = PyObject_GetAttrString(obj, "__arrow_c_stream__");
    if (!stream_func) {
        return NULL;
    }
    
    // Call the __arrow_c_stream__ function
    PyObject* capsule = PyObject_CallObject(stream_func, NULL);
    Py_DECREF(stream_func);
    
    if (!capsule) {
        return NULL;
    }
    
    // Check if it's a valid PyCapsule
    if (!PyCapsule_IsValid(capsule, "arrow_array_stream")) {
        Py_DECREF(capsule);
        PyErr_SetString(PyExc_TypeError, "__arrow_c_stream__ did not return a valid ArrowArrayStream capsule");
        return NULL;
    }
    
    // For demonstration, we'll return the capsule itself
    // In a real application, you'd likely want to process the stream
    return capsule;
}

// Method definitions
static PyMethodDef MojoArrowSysMethods[] = {
    {"arrow_stream", arrow_stream, METH_VARARGS, "Get ArrowArrayStream from Python object"},
    {NULL, NULL, 0, NULL}  // Sentinel
};

// Module definition
static struct PyModuleDef mojo_arrow_sys_module = {
    PyModuleDef_HEAD_INIT,
    "mojo_arrow_sys",   // Module name
    "Mojo Arrow System Module for accessing Arrow C streams",  // Doc string
    -1,  // Size of per-interpreter state or -1
    MojoArrowSysMethods
};

// Module initialization function
PyMODINIT_FUNC PyInit_mojo_arrow_sys(void) {
    return PyModule_Create(&mojo_arrow_sys_module);
}
