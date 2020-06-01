/*
The MIT License

Copyright (c) 2014- High-Mobility GmbH (https://high-mobility.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

#include <stdlib.h>
#include <stdio.h>
#include <Python.h>

#define PY_APP_NAME "pyapp"
#define PY_CALLBACK_FUNC_NAME "py_callback"

PyObject *pName, *pModule, *pDict, *pFunc_cb;
PyObject *pArgs, *pValue;

PyObject *pycb_cmdincoming, *pycb_cmdresp, *pycb_entprox, *pycb_extprox;

typedef enum cb_keyword
{
    eCB_KEYWRD_CMDINCOMING = 0x0,
    eCB_KEYWRD_CMDRESP,
    eCB_KEYWRD_ENTPROX,
    eCB_KEYWRD_EXTPROX,
    eCB_KEYWRD_TELEINCM,

    eCB_KEYWRD_MAX
}cb_keywrds_t;

extern int hm_link_main(void);
extern int py_hm_register_cb(PyObject *cb, cb_keywrds_t eKeywrd);
extern int py_hm_unregister_cb(void);
extern int py_sendcommand(char *pMsg, int len);
extern void py_set_issuer_pub(uint8_t *pub);
extern void py_set_dev_prv(uint8_t *prv);
extern void py_set_dev_cert(uint8_t *cert);
extern int py_generate_signature(uint8_t *buffer, uint16_t length, PyObject **pSign );
extern int py_store_accesscertificate(uint8_t *certf, uint8_t len, uint8_t *ser_num);
extern int py_get_accesscertificate(uint8_t *ser_num, PyObject **pAccessCert);
extern int py_delete_accesscertificate(uint8_t *ser_num);
extern int py_ble_advertisement_start(void);
extern int py_ble_advertisement_stop(void);
extern int hm_link_exit(void);

int pyBytes_toString(PyObject *pArray, char **str, int *length);

int callback_func_C_Pyobj(uint8_t val);
int init_py_env(void);
void debug_dump(char *ptr, int len);

int pyc_test_api(void)
{


 return 0;
}

int init_py_env()
{
    //printf("%s ,%s()\n", __FILE__, __FUNCTION__);

    // Set PYTHONPATH TO working directory
    setenv("PYTHONPATH",".",1);

//    Py_Finalize();

    //printf("Return: %s ,%s()\n", __FILE__, __FUNCTION__);

    return 0;
}

#if 0
int callback_func_C_Pyobj(uint8_t val)
{
	char hai[ ] = "hai";
	PyObject *pArgsTemp, *pArgs;
    char hello[10]={'1', '2', '3', '4', '5', '\0', '6', '7', '8', '9'};

    printf("%s ,%s(), null char = 0x%x\n", __FILE__, __FUNCTION__, '\0');
    printf("null char = 0x%x\n", hai[3]);

    /* pFunc is a new reference */
    if (pycallback && PyCallable_Check(pycallback)) {

        pArgs = PyTuple_New(1);
		pArgsTemp = Py_BuildValue("y#", hello, 10);
        PyTuple_SetItem(pArgs, 0, pArgsTemp);

        pValue = PyObject_CallObject(pycallback, pArgs);
        Py_DECREF(pArgs);
        if (pValue != NULL) {
            printf("Result of call: %ld\n", PyLong_AsLong(pValue));
            Py_DECREF(pValue);
        }
        else {
            Py_DECREF(pycallback);
            PyErr_Print();
            fprintf(stderr,"Call failed\n");
            return 1;
        }
    }
    else
    {
        fprintf(stderr," Function object is invalid\n");
    }

    printf("Returned: %s ,%s()\n", __FILE__, __FUNCTION__);
}
#endif

/* Return the number of arguments of the application command line */
static PyObject*
hm_pyc_cmain_thread(PyObject *self, PyObject *args)
{
	int ret = 0;

    //printf("DEBUG %d %s ,%s()\n", __LINE__, __FILE__, __FUNCTION__);

	init_py_env();

    //printf("DEBUG %d %s ,%s()\n", __LINE__, __FILE__, __FUNCTION__);
	PyEval_ReleaseLock();

    hm_link_main();
    //printf("DEBUG %d %s ,%s()\n", __LINE__, __FILE__, __FUNCTION__);

    return PyLong_FromLong(ret);
}

/* Return the number of arguments of the application command line */
static PyObject*
hm_pyc_cthread_exit(PyObject *self, PyObject *args)
{
	int ret = 0;
	py_hm_unregister_cb();

    printf("DEBUG %d %s ,%s()\n", __LINE__, __FILE__, __FUNCTION__);
    hm_link_exit();

    //printf(" CORE2 DEBUG %d %s ,%s()\n", __LINE__, __FILE__, __FUNCTION__);
    return PyLong_FromLong(ret);
}


/* Return the number of arguments of the application command line */
static PyObject*
hm_pyc_register_cb(PyObject *self, PyObject *args)
{
	PyObject *pCb = NULL;
	char *pChar;
	int ret=0;
	cb_keywrds_t eCbkeywrd;

	//	PyEval_ReleaseLock();

	if(PyArg_ParseTuple(args, "sO", &pChar, &pCb))
	{
	    //printf("** c key rx: %s\n", pChar);
        if (!PyCallable_Check(pCb)) {
        //PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            printf("C: ERROR: callback object not callable; for %s \n", pChar);
            return NULL;
        }
        else
        {
            // printf("%s(),  pycb \n", __FUNCTION__, );
            Py_XINCREF(pCb); /* Add a reference to callback */
        }
	}
	else
	{
		printf("%s(), invalid input parameters\n", __FUNCTION__);
		return NULL;
	}
		

	if (strcmp("py_cb_command_incoming", pChar) == 0 ) 
	{
#ifdef PYC_DEBUG
			printf("function(), %s(), pycb_cmdincoming\n", __FUNCTION__);
#endif

			pycb_cmdincoming = pCb;
			//Py_XINCREF(pycb_cmdincoming); /* Add a reference to callback */
			eCbkeywrd = eCB_KEYWRD_CMDINCOMING;
	}
	else if (strcmp("py_cb_command_response", pChar) == 0) 
	{
#ifdef PYC_DEBUG
    		printf("function(), %s(), pycb_cmdresp \n", __FUNCTION__);
#endif

			pycb_cmdresp = pCb;
			//Py_XINCREF(pycb_cmdresp); /* Add a reference to callback */
			eCbkeywrd = eCB_KEYWRD_CMDRESP;
	}
	else if (!strcmp("py_cb_entered_proximity", pChar)) 
	{
#ifdef PYC_DEBUG
			printf("function(), %s(), pycb_entprox \n", __FUNCTION__);
#endif

			pycb_entprox = pCb;
			//Py_XINCREF(pycb_entprox); /* Add a reference to callback */
			eCbkeywrd = eCB_KEYWRD_ENTPROX;
	}
	else if (!strcmp("py_cb_exited_proximity", pChar)) 
	{
#ifdef PYC_DEBUG
			printf("function(), %s(), pycb_extprox\n", __FUNCTION__);
#endif

			pycb_extprox = pCb;
			//Py_XINCREF(pycb_extprox); /* Add a reference to callback */
			eCbkeywrd = eCB_KEYWRD_EXTPROX;
	}
	else
	{
			printf("C: ERROR: python callback does not match to a valid name ");
			return NULL;

	}

	//---------------
	if(pCb != NULL)
	{
		//printf("C: py callback enum = %d\n", eCbkeywrd);
		py_hm_register_cb(pCb, eCbkeywrd);
	}

    return PyLong_FromLong(ret);
}


// wrapper function for send_command
static PyObject * hm_pyc_sendcommand(PyObject *self, PyObject *args) {  
	PyObject *pArray;
	int ret = 0;

	//printf("** Enter %s()\n", __FUNCTION__);

#if 0
    if (PyArg_ParseTuple(args, "S", &pArray)) {
        char *str = PyBytes_AsString(pArray);
        printf("%s() from Tuple, Bytes as str, : %s\n", __FUNCTION__, str);
    }
#endif

	if (PyArg_ParseTuple(args, "S", &pArray))
	{
		if (PyBytes_Check(pArray)) 
		{
			char *str = NULL;
			Py_ssize_t len = 0;

			/* Check for a string typecode. */
			if (PyBytes_AsStringAndSize(pArray, &str, &len) < 0) 
			{
				//goto error;
				printf("Error %s() converting Byte to String \n", __FUNCTION__);
				return PyLong_FromLong(-1);
			}

			/* Empty string is invalid */
			if (len == 0) 
			{
				printf("Error %s() converting Byte to String, len = 0\n", __FUNCTION__);
				return PyLong_FromLong(-1);
			}

#ifdef PYC_DEBUG
			printf("%s() from Tuple, Bytes as str, : %s, len = %d\n", __FUNCTION__, str, len)	
			debug_dump(str, len);
#endif
			py_sendcommand(str, len);
		}
		else
		{
				printf("Error %s() failed in Bytes Check \n", __FUNCTION__);
				return PyLong_FromLong(-1);
		}
	}
	else
	{
			printf("Error %s() failed in Bytes Check \n", __FUNCTION__);
			return PyLong_FromLong(-1);
	}

	//printf("Return %s()\n", __FUNCTION__);

	return PyLong_FromLong(ret);
}

// wrapper function for send_command
static PyObject * hm_pyc_generate_signature(PyObject *self, PyObject *args) {  
	PyObject *pArray, *pSign;

	//printf("** Enter %s()\n", __FUNCTION__);

	if (PyArg_ParseTuple(args, "S", &pArray))
	{
		if (PyBytes_Check(pArray)) 
		{
			char *str = NULL;
			Py_ssize_t len = 0;

			/* Check for a string typecode. */
			if (PyBytes_AsStringAndSize(pArray, &str, &len) < 0) 
			{
				//goto error;
				printf("Error %s() converting Byte to String \n", __FUNCTION__);
				return NULL;
			}

			/* Empty string is invalid */
			if (len == 0) 
			{
				printf("Error %s() converting Byte to String, len = 0\n", __FUNCTION__);
				return NULL;
			}

#ifdef PYC_DEBUG
			printf("%s() from Tuple, Bytes as str, : %s, len = %d\n", __FUNCTION__, str, len);
			debug_dump(str, len);
#endif

			py_generate_signature((uint8_t *)str, len, &pSign);
		}
		else
		{
			printf("Error %s() failed in Bytes Check \n", __FUNCTION__);
			return NULL;
		}
	}
	else
	{
		printf("Error %s() failed in parsing Tuple \n", __FUNCTION__);
		return NULL;
	}

	//printf("Return %s()\n", __FUNCTION__);
	//return PyLong_FromLong(ret);
	return pSign;
}

// wrapper function for advertisement start
static PyObject * hm_pyc_ble_advertisement_start(PyObject *self, PyObject *args) {  
	int ret = 0;

 	ret	= py_ble_advertisement_start();

	return PyLong_FromLong(ret);
}

// wrapper function for advertisement stop
static PyObject * hm_pyc_ble_advertisement_stop(PyObject *self, PyObject *args) {  
	int ret = 0;

 	ret	= py_ble_advertisement_stop();

	return PyLong_FromLong(ret);
}

// wrapper function for storing access certificate 
static PyObject * hm_pyc_store_access_certificate(PyObject *self, PyObject *args) {
	PyObject *pCertf, *pSerNum;
	int ret = 0;

	//printf("** Enter %s()\n", __FUNCTION__);

	if (PyArg_ParseTuple(args, "SS", &pCertf, &pSerNum))
	{
		if (PyBytes_Check(pCertf) && PyBytes_Check(pSerNum)) 
		{
			char *certStr = NULL, *serNumStr = NULL;
			Py_ssize_t len = 0, len_certf = 0;

			/* get the buffer as strings(char array) */
			if (PyBytes_AsStringAndSize(pCertf, &certStr, &len_certf) < 0) 
			{
				printf("Error %s() converting Byte to String \n", __FUNCTION__);
				return PyLong_FromLong(-1);
			}

			/* Empty string is invalid */
			if (len_certf == 0) 
			{
				printf("Error %s() Certf, converting Byte to String, len = 0\n", __FUNCTION__);
				return PyLong_FromLong(-1);
			}

#ifdef PYC_DEBUG
			printf("%s() from Tuple, Access Cert Bytes as str : %s, len = %d\n", __FUNCTION__, certStr, len_certf);
			debug_dump(certStr, len_certf);
#endif

			/* get the buffer as strings(char array) */
			if (PyBytes_AsStringAndSize(pSerNum, &serNumStr, &len) < 0) 
			{
				printf("Error %s() converting Byte to String \n", __FUNCTION__);
				return PyLong_FromLong(-1);
			}

			/* Empty string is invalid */
			if (len == 0) 
			{
				printf("Error %s() SerialNum, converting Byte to String, len = 0\n", __FUNCTION__);
				return PyLong_FromLong(-1);
			}

#ifdef PYC_DEBUG
			printf("%s() from Tuple, SerNum Bytes as str : %s, len = %d\n", __FUNCTION__, serNumStr, len);
			debug_dump(serNumStr, len);
#endif

			// pass it to database
			//int py_store_accesscertificate(certStr, len_certf, serNumStr);
			py_store_accesscertificate((uint8_t *)certStr, len_certf, (uint8_t *)serNumStr);

		}
		else
		{
			printf("Error %s() failed in Bytes Check \n", __FUNCTION__);
			return PyLong_FromLong(-1);
		}
	}
	else
	{
		printf("Error %s() failed in parsing Tuple \n", __FUNCTION__);
		return PyLong_FromLong(-1);
	}

	//printf("Return %s()\n", __FUNCTION__);
	return PyLong_FromLong(ret);
}

// wrapper function for getting access certificate
static PyObject * hm_pyc_get_access_certificate(PyObject *self, PyObject *args) {

	PyObject *pArray, *pAccessCert;

	//printf("** Enter %s()\n", __FUNCTION__);

	if (PyArg_ParseTuple(args, "S", &pArray))
	{
		if (PyBytes_Check(pArray))
		{
			char *str = NULL;
			Py_ssize_t len = 0;

			/* Check for a string typecode. */
			if (PyBytes_AsStringAndSize(pArray, &str, &len) < 0)
			{
				//goto error;
				printf("Error %s() converting Byte to String \n", __FUNCTION__);
				return NULL;
			}

			/* Empty string is invalid */
			if (len == 0)
			{
				printf("Error %s() converting Byte to String, len = 0\n", __FUNCTION__);
				return NULL;
			}

#ifdef PYC_DEBUG
			printf("%s() from Tuple, Bytes as str, : %s, len = %d\n", __FUNCTION__, str, len);
			debug_dump(str, len);
#endif

			//py_generate_signature((uint8_t *)str, len, &pSign);
			py_get_accesscertificate((uint8_t *)str, &pAccessCert);
		}
		else
		{
			printf("Error %s() failed in Bytes Check \n", __FUNCTION__);
			return NULL;
		}
	}
	else
	{
		printf("Error %s() failed in parsing Tuple \n", __FUNCTION__);
		return NULL;
	}

	//printf("Return %s()\n", __FUNCTION__);
	//return PyLong_FromLong(ret);
	return pAccessCert;
}

// wrapper function for delete access certificate
static PyObject * hm_pyc_delete_access_certificate(PyObject *self, PyObject *args) {
	int ret = 0;
	PyObject *pArray;
    //printf("DEBUG %d %s ,%s()\n", __LINE__, __FILE__, __FUNCTION__);

	if (PyArg_ParseTuple(args, "S", &pArray))
	{
		if (PyBytes_Check(pArray))
		{
			char *str = NULL;
			Py_ssize_t len = 0;

			/* Check for a string typecode. */
			if (PyBytes_AsStringAndSize(pArray, &str, &len) < 0)
			{
				//goto error;
				printf("Error %s() converting Byte to String \n", __FUNCTION__);
				return NULL;
			}

			/* Empty string is invalid */
			if (len == 0)
			{
				printf("Error %s() converting Byte to String, len = 0\n", __FUNCTION__);
				return NULL;
			}

#ifdef PYC_DEBUG
			debug_dump(str, len);
#endif

			py_delete_accesscertificate((uint8_t *)str);
		}
		else
		{
			printf("Error %s() failed in Bytes Check \n", __FUNCTION__);
			return NULL;
		}
	}
	else
	{
		printf("Error %s() failed in parsing Tuple \n", __FUNCTION__);
		return NULL;
	}

	return PyLong_FromLong(ret);
}

void debug_dump(char *ptr, int len)
{
    int i = 0;

	if(ptr == NULL)
	{
	    printf("Error %s() input ptr is NULL ", __FUNCTION__);
		return;
	}

    printf("Pyc, Dump: len = %d :", len);

    for(i=0; i<len; i++)
    {
        printf(" 0x%x, ", ptr[i]);
    }

    printf("\n");
}

// wrapper function for set_certs
static PyObject * hm_pyc_set_certs(PyObject *self, PyObject *args) {  
	PyObject *pdevCert, *pPrv, *pIssrPub;
	char *str_devCert= NULL , *str_prv = NULL, *str_issrPub = NULL;
	int len_devCert = 0, len_prv = 0, len_issrPub = 0;
	//Py_ssize_t len_devCert = 0, len_prv = 0, len_issrPub = 0;
	int ret = 0;

	//printf("*** Enter %s()\n", __FUNCTION__);

	if (PyArg_ParseTuple(args, "SSS", &pdevCert, &pPrv, &pIssrPub))
	{
		if(pyBytes_toString(pdevCert, &str_devCert, &len_devCert) != 0)
		{
			printf("*** Error Devcert bytes_tostring %s()\n", __FUNCTION__);
			return PyLong_FromLong(-1);
		}

		if(pyBytes_toString(pPrv, &str_prv, &len_prv) != 0)
		{
			printf("*** Error Prv bytes_tostring %s()\n", __FUNCTION__);
			return PyLong_FromLong(-1);
		}

		if(pyBytes_toString(pIssrPub, &str_issrPub, &len_issrPub) != 0)
		{
			printf("*** Error Pub bytes_tostring %s()\n", __FUNCTION__);
			return PyLong_FromLong(-1);
		}

#ifdef PYC_DEBUG
		printf(" %s(), Length: devcrt = %d, Prv = %d, Pub = %d \n", __FUNCTION__, len_devCert, len_prv, len_issrPub);
		//printf(" Ptr &str_devCert = %p, str_devCert = %p, *str_devCert = 0x%x\n", &str_devCert, str_devCert, *str_devCert);
#endif

		py_set_dev_prv((uint8_t *)str_prv);
#ifdef PYC_DEBUG
		debug_dump(str_prv, len_prv);
#endif


		py_set_dev_cert((uint8_t *)str_devCert);
#ifdef PYC_DEBUG
		debug_dump(str_devCert, len_devCert);
#endif


		py_set_issuer_pub((uint8_t *)str_issrPub);
#ifdef PYC_DEBUG
		debug_dump(str_issrPub, len_issrPub);
#endif

	 	//py_set_certs(str, len);
	}
	else
	{
			printf("Error %s() failed in Parsing Tuple \n", __FUNCTION__);
			return PyLong_FromLong(-1);
	}

	//printf("Return %s()\n", __FUNCTION__);
	return PyLong_FromLong(ret);
}


int pyBytes_toString(PyObject *pArray, char **str, int *length)
{
	int ret = 0;

	if (PyBytes_Check(pArray)) 
	{
		*str = NULL;
		Py_ssize_t len = 0;

		/* Check for a string typecode. */
		if (PyBytes_AsStringAndSize(pArray, str, &len) < 0) 
		{
			//goto error;
			printf("Error %s() converting Byte to String \n", __FUNCTION__);
			return -1;
		}

		/* Empty string is invalid */
		if (len == 0) 
		{
			printf("Error %s() converting Byte to String, len = 0\n", __FUNCTION__);
			return -1;
		}

		//printf("%s() from Tuple, Bytes as str, len = %d\n", __FUNCTION__, len);

		*length = len;
		//string = str;

#ifdef PYC_DEBUG
		debug_dump(*str, len);
#endif
		//py_sendcommand(str, len);
	}
	else
	{
			printf("Error %s() failed in Bytes Check \n", __FUNCTION__);
			return -1;
	}

	return ret;
}


static PyMethodDef EmbMethods[] = {
    {"cmain_thread", hm_pyc_cmain_thread, METH_VARARGS,
     "c layer main thread"},
    {"cthread_exit", hm_pyc_cthread_exit, METH_VARARGS,
     "c layer timer thread exit"},
   {"sendcommand", // name exposed to Python
        hm_pyc_sendcommand, // C wrapper function
        METH_VARARGS, // received variable args (but really just 1)
        "Sends bluetooth command"},
    {"set_certs", // name exposed to Python
        hm_pyc_set_certs, // C wrapper function
        METH_VARARGS, // received variable args (but really just 1)
        "Set Certifcates"},
    {"register_cb", hm_pyc_register_cb, METH_VARARGS,
     "Register python callback"},
    {"generate_signature", hm_pyc_generate_signature, METH_VARARGS,
     "generate signature"},
    {"store_certificate", hm_pyc_store_access_certificate, METH_VARARGS,
     "store certificate"},
    {"get_certificate", hm_pyc_get_access_certificate, METH_VARARGS,
     "get certificate"},
    {"delete_certificate", hm_pyc_delete_access_certificate, METH_VARARGS,
     "delete certificate"},
     {"ble_advertisement_start", hm_pyc_ble_advertisement_start, METH_VARARGS,
     "ble advertisement start"},
     {"ble_advertisement_stop", hm_pyc_ble_advertisement_stop, METH_VARARGS,
     "ble advertisement stop"},
   {NULL, NULL, 0, NULL}
};

static PyModuleDef EmbModule = {
    PyModuleDef_HEAD_INIT, "hm_pyc", NULL, -1, EmbMethods,
    NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit_hm_pyc(void)
{
    //printf("******* Enter %s() \n", __FUNCTION__);
    return PyModule_Create(&EmbModule);
}


