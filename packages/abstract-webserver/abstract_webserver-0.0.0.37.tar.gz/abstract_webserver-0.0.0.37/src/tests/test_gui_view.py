import ast
import os
import importlib.util
import pkgutil
import sys
import traceback
import PySimpleGUI as sg
from abstract_gui import AbstractBrowser

# Global variables
module = None
functions = {}

# Specify the custom path for module loading
CUSTOM_MODULE_PATH = "/home/computron/miniconda/lib/python3.12/site-packages/"

def file_events(event, values, window):
    global module, functions
    print("Event:", event)

    # Load from a file
    if event == 'Load File':
        directory = values.get('-DIR-')
        basename = values.get('-FILES_LIST-')[0]
        file_path = os.path.join(directory, basename)
        filename, ext = os.path.splitext(basename)
        if file_path and os.path.isfile(file_path) and ext == '.py':
            try:
                functions = parse_functions_from_file(file_path)
                module = load_module_from_file(file_path)
                window['-FUNCTION-'].update(values=list(functions.keys()))
                window['-OUTPUT-'].update("Loaded functions:\n" + "\n".join(functions.keys()) + "\n")
                update_argument_fields(window, [])
            except Exception as e:
                sg.popup_error("Error loading file", e, traceback.format_exc())
        else:
            sg.popup_error("Please select a valid Python file.")

    # Load from an installed module in the custom path
    elif event == 'Load Module':
        selected_module = values.get('-MODULE-')
        if selected_module:
            try:
                # Temporarily add the custom path to sys.path if not already present
                if CUSTOM_MODULE_PATH not in sys.path:
                    sys.path.insert(0, CUSTOM_MODULE_PATH)
                module = importlib.import_module(selected_module)
                functions = parse_functions_from_module(module)
                window['-FUNCTION-'].update(values=list(functions.keys()))
                window['-OUTPUT-'].update(f"Loaded functions from module '{selected_module}':\n" + "\n".join(functions.keys()) + "\n")
                update_argument_fields(window, [])
                # Remove the custom path after loading (optional, keeps sys.path clean)
                if CUSTOM_MODULE_PATH in sys.path:
                    sys.path.remove(CUSTOM_MODULE_PATH)
            except Exception as e:
                sg.popup_error("Error loading module", e, traceback.format_exc())
        else:
            sg.popup_error("Please select a module.")

    # When a function is selected, show relevant input fields
    elif event == '-FUNCTION-':
        selected_function = values['-FUNCTION-']
        if selected_function and selected_function in functions:
            arg_names = functions[selected_function]
            update_argument_fields(window, arg_names)
        else:
            update_argument_fields(window, [])  # Hide all if no valid function

    # Run the selected function with provided arguments
    elif event == 'Run Function':
        selected_function = values.get('-FUNCTION-')
        if not selected_function:
            sg.popup_error("No function selected.")
            return
        if module is None:
            sg.popup_error("No module loaded.")
            return
        try:
            args = []
            for arg in functions[selected_function]:
                arg_value = values.get(f'-ARG_{arg}-', '')
                args.append(arg_value if arg_value != '' else None)
            func = getattr(module, selected_function)
            result = func(*args)
            output_str = f"Result from {selected_function}({', '.join(map(str, args))}):\n{result}\n"
            window['-OUTPUT-'].update(window['-OUTPUT-'].get() + output_str)
        except Exception as e:
            error_str = f"Error running function {selected_function}: {e}\n{traceback.format_exc()}\n"
            window['-OUTPUT-'].update(window['-OUTPUT-'].get() + error_str)

def parse_functions_from_file(filepath):
    """Parse functions from a file using AST."""
    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=filepath)
    funcs = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            arg_names = [arg.arg for arg in node.args.args]
            funcs[node.name] = arg_names
    return funcs

def parse_functions_from_module(module):
    """Parse functions from an imported module."""
    funcs = {}
    for name, obj in vars(module).items():
        if callable(obj) and not name.startswith('_'):
            try:
                import inspect
                sig = inspect.signature(obj)
                arg_names = [param.name for param in sig.parameters.values()]
                funcs[name] = arg_names
            except (ValueError, TypeError):
                continue
    return funcs

def load_module_from_file(filepath):
    """Dynamically load a module from a file path."""
    module_name = os.path.splitext(os.path.basename(filepath))[0]
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def get_installed_modules():
    """Get a list of installed module names from the custom path."""
    # Ensure the custom path is scanned
    modules = []
    for finder, name, ispkg in pkgutil.iter_modules([CUSTOM_MODULE_PATH]):
        if not ispkg:  # Only include modules, not packages (optional: remove this check for packages)
            modules.append(name)
    return sorted(modules)

def update_argument_fields(window, arg_names):
    """Show/hide and label input fields based on the function's arguments."""
    max_args = 10
    for i in range(max_args):
        text_key = f'-ARG_TEXT_{i}-'
        input_key = f'-ARG_{i}-'
        if i < len(arg_names):
            window[text_key].update(value=f"{arg_names[i]}:", visible=True)
            window[input_key].update(value='', visible=True)
            window[input_key].Key = f'-ARG_{arg_names[i]}-'
        else:
            window[text_key].update(visible=False)
            window[input_key].update(visible=False)

# Define the layout with both file and module selection options
layout = [
    [sg.Text('Load from File:'), sg.Button('Load File')],
    [sg.Text('Load from Module:'), sg.Combo(get_installed_modules(), key='-MODULE-', readonly=True, enable_events=False), sg.Button('Load Module')],
    [sg.Text('Select Function:'), sg.Combo([], key='-FUNCTION-', readonly=True, enable_events=True)],
    *[[sg.Text('', key=f'-ARG_TEXT_{i}-', visible=False),
       sg.Input('', key=f'-ARG_{i}-', visible=False, size=(30, 1))] for i in range(10)],
    [sg.Button('Run Function')],
    [sg.Frame('Output', [[sg.Multiline(size=(80, 20), key='-OUTPUT-', autoscroll=True)]])]
]

# Start the browser
AbstractBrowser().initiate_browser_window(
    window_name="MyBrowser",
    title="File/Folder Browser",
    extra_buttons=layout,
    event_handlers=[file_events]
)
