import ctypes
import ida_typeinf

"""
/// Parse many declarations and store them in a til.
/// If there are any errors, they will be printed using 'printer'.
/// This function uses default include path and predefined macros from the
/// database settings. It always uses the #HTI_DCL bit.
/// \param til        type library to store the result
/// \param input      input string or file name (see hti_flags)
/// \param printer    function to output error messages (use msg or nullptr or your own callback)
/// \param htiflags  combination of \ref HTI
/// \return number of errors, 0 means ok.

idaman int ida_export parse_decls(
        til_t til,
        const char* input,
        printer_t *printer,
        int hti_flags);
"""

import ctypes

def parse_decls_ctypes(decls: str, hti_flags: int) -> tuple[int, str]:
    assert isinstance(decls, str), "decls must be a string"
    assert isinstance(hti_flags, int), "hti_flags must be an int"
    c_decls = decls.encode("utf-8")
    c_til = None
    ida_dll = ctypes.CDLL("ida")
    ida_dll.parse_decls.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_int]
    ida_dll.parse_decls.restype = ctypes.c_int

    errors = []
    @ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p)
    def magic_printer(fmt: bytes, arg1: bytes):
        print("magic_printer", fmt)
        if fmt.count(b"%") == 1 and b"%s" in fmt:
            formatted = fmt.replace(b"%s", arg1).decode("utf-8")
            return len(formatted) + 1
        else:
            errors.append(f"unsupported magic_printer fmt: {repr(fmt)}")
            return 0

    result = ida_dll.parse_decls(c_til, c_decls, magic_printer, hti_flags)
    return result, errors

bad_decl = """struct Bar2 {
 int x;
};
struct Foo4
{
 Bar xx;
    int a;
    int b;
    int z;
};"""

num_errors, message = parse_decls_ctypes(bad_decl, ida_typeinf.PT_SIL | ida_typeinf.PT_EMPTY | ida_typeinf.PT_TYP)
print(f"errors: {errors}, message: {message}")