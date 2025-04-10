# NOTE: This file has been automatically generated, do not modify!
# Architecture based on https://github.com/mrexodia/ida-pro-mcp (MIT License)
from typing import Annotated, Optional, TypedDict, Generic, TypeVar
from pydantic import Field

T = TypeVar("T")

class Metadata(TypedDict):
    path: str
    module: str
    base: str
    size: str
    md5: str
    sha256: str
    crc32: str
    filesize: str

class Function(TypedDict):
    address: str
    name: str
    size: str

class ConvertedNumber(TypedDict):
    decimal: str
    hexadecimal: str
    bytes: str
    ascii: Optional[str]
    binary: str

class Page(TypedDict, Generic[T]):
    data: list[T]
    next_offset: Optional[int]

class String(TypedDict):
    address: str
    length: int
    type: str
    string: str

class Xref(TypedDict):
    address: str
    type: str
    function: Optional[Function]

@mcp.tool()
def get_metadata() -> Metadata:
    """Get metadata about the current IDB"""
    return make_jsonrpc_request('get_metadata')

@mcp.tool()
def get_function_by_name(name: Annotated[str, Field(description='Name of the function to get')]) -> Function:
    """Get a function by its name"""
    return make_jsonrpc_request('get_function_by_name', name)

@mcp.tool()
def get_function_by_address(address: Annotated[str, Field(description='Address of the function to get')]) -> Function:
    """Get a function by its address"""
    return make_jsonrpc_request('get_function_by_address', address)

@mcp.tool()
def get_current_address() -> str:
    """Get the address currently selected by the user"""
    return make_jsonrpc_request('get_current_address')

@mcp.tool()
def get_current_function() -> Optional[Function]:
    """Get the function currently selected by the user"""
    return make_jsonrpc_request('get_current_function')

@mcp.tool()
def convert_number(text: Annotated[str, Field(description='Textual representation of the number to convert')], size: Annotated[Optional[int], Field(description='Size of the variable in bytes')]) -> ConvertedNumber:
    """Convert a number (decimal, hexadecimal) to different representations"""
    return make_jsonrpc_request('convert_number', text, size)

@mcp.tool()
def list_functions(offset: Annotated[int, Field(description='Offset to start listing from (start at 0)')], count: Annotated[int, Field(description='Number of functions to list (100 is a good default, 0 means remainder)')]) -> Page[Function]:
    """List all functions in the database (paginated)"""
    return make_jsonrpc_request('list_functions', offset, count)

@mcp.tool()
def list_strings(offset: Annotated[int, Field(description='Offset to start listing from (start at 0)')], count: Annotated[int, Field(description='Number of strings to list (100 is a good default, 0 means remainder)')]) -> Page[String]:
    """List all strings in the database (paginated)"""
    return make_jsonrpc_request('list_strings', offset, count)

@mcp.tool()
def search_strings(pattern: Annotated[str, Field(description='Substring to search for in strings')], offset: Annotated[int, Field(description='Offset to start listing from (start at 0)')], count: Annotated[int, Field(description='Number of strings to list (100 is a good default, 0 means remainder)')]) -> Page[String]:
    """Search for strings containing the given pattern (case-insensitive)"""
    return make_jsonrpc_request('search_strings', pattern, offset, count)

@mcp.tool()
def decompile_function(address: Annotated[str, Field(description='Address of the function to decompile')]) -> str:
    """Decompile a function at the given address"""
    return make_jsonrpc_request('decompile_function', address)

@mcp.tool()
def disassemble_function(start_address: Annotated[str, Field(description='Address of the function to disassemble')]) -> str:
    """Get assembly code (address: instruction; comment) for a function"""
    return make_jsonrpc_request('disassemble_function', start_address)

@mcp.tool()
def get_xrefs_to(address: Annotated[str, Field(description='Address to get cross references to')]) -> list[Xref]:
    """Get all cross references to the given address"""
    return make_jsonrpc_request('get_xrefs_to', address)

@mcp.tool()
def get_entry_points() -> list[Function]:
    """Get all entry points in the database"""
    return make_jsonrpc_request('get_entry_points')

@mcp.tool()
def set_comment(address: Annotated[str, Field(description='Address in the function to set the comment for')], comment: Annotated[str, Field(description='Comment text')]):
    """Set a comment for a given address in the function disassembly and pseudocode"""
    return make_jsonrpc_request('set_comment', address, comment)

@mcp.tool()
def rename_local_variable(function_address: Annotated[str, Field(description='Address of the function containing the variable')], old_name: Annotated[str, Field(description='Current name of the variable')], new_name: Annotated[str, Field(description='New name for the variable (empty for a default name)')]):
    """Rename a local variable in a function"""
    return make_jsonrpc_request('rename_local_variable', function_address, old_name, new_name)

@mcp.tool()
def rename_global_variable(old_name: Annotated[str, Field(description='Current name of the global variable')], new_name: Annotated[str, Field(description='New name for the global variable (empty for a default name)')]):
    """Rename a global variable"""
    return make_jsonrpc_request('rename_global_variable', old_name, new_name)

@mcp.tool()
def set_global_variable_type(variable_name: Annotated[str, Field(description='Name of the global variable')], new_type: Annotated[str, Field(description='New type for the variable')]):
    """Set a global variable's type"""
    return make_jsonrpc_request('set_global_variable_type', variable_name, new_type)

@mcp.tool()
def rename_function(function_address: Annotated[str, Field(description='Address of the function to rename')], new_name: Annotated[str, Field(description='New name for the function (empty for a default name)')]):
    """Rename a function"""
    return make_jsonrpc_request('rename_function', function_address, new_name)

@mcp.tool()
def set_function_prototype(function_address: Annotated[str, Field(description='Address of the function')], prototype: Annotated[str, Field(description='New function prototype')]) -> str:
    """Set a function's prototype"""
    return make_jsonrpc_request('set_function_prototype', function_address, prototype)

@mcp.tool()
def declare_c_type(c_declaration: Annotated[str, Field(description='C declaration of the type. Examples include: typedef int foo_t; struct bar { int a; bool b; };')]):
    """Create or update a local type from a C declaration"""
    return make_jsonrpc_request('declare_c_type', c_declaration)

@mcp.tool()
def set_local_variable_type(function_address: Annotated[str, Field(description='Address of the function containing the variable')], variable_name: Annotated[str, Field(description='Name of the variable')], new_type: Annotated[str, Field(description='New type for the variable')]):
    """Set a local variable's type"""
    return make_jsonrpc_request('set_local_variable_type', function_address, variable_name, new_type)

