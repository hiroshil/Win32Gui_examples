from ctypes import windll, wintypes, POINTER, pointer, cast, c_int, c_void_p, c_wchar_p, c_char_p
# code generated by AI and edited by me

# https://github.com/usermicrodevices/pywingui/blob/master/winuser.py#L17
UNICODE = True

if UNICODE:
	def MAKEINTRESOURCE(i):#MAKEINTRESOURCEW
		return cast(c_void_p(i&0xFFFF), c_wchar_p)
else:
	def MAKEINTRESOURCE(i):#MAKEINTRESOURCEA
		return cast(c_void_p(i&0xFFFF), c_char_p)

MAKEINTRESOURCEW = MAKEINTRESOURCE

# Define constants (replace with actual values if needed)
TDCBF_OK_BUTTON = 0x1
TDCBF_YES_BUTTON = 0x2
TDCBF_NO_BUTTON = 0x4
TDCBF_CANCEL_BUTTON = 0x8
TDCBF_RETRY_BUTTON = 0x10
TDCBF_CLOSE_BUTTON = 0x20
TD_WARNING_ICON = MAKEINTRESOURCEW(-1)
TD_ERROR_ICON = MAKEINTRESOURCEW(-2)
TD_INFORMATION_ICON = MAKEINTRESOURCEW(-3)
TD_SHIELD_ICON = MAKEINTRESOURCEW(-4)

# Define the TaskDialog function signature
TaskDialog = windll.comctl32.TaskDialog

# Define argument types
TaskDialog.argtypes = [
    wintypes.HWND,
    wintypes.HINSTANCE,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.LPCWSTR,
    POINTER(c_int)
]

# Define return type
HRESULT = wintypes.LONG
TaskDialog.restype = HRESULT


def show_task_dialog(title, message, buttons=TDCBF_OK_BUTTON, icon=None):
    """
    Displays a Task Dialog with specified title and message.

    Args:
      title: The title of the task dialog window
      message: The message to display
      buttons: The buttons to show (default is only OK)

    Returns:
        The selected button.
    """
    # Create a buffer for the selected button result
    selected_button = c_int()
    button_ptr = pointer(selected_button)

    # Call TaskDialog
    result = TaskDialog(
        None,  # hwndOwner
        None,  # hInstance
        title,
        None,  # pszMainInstruction (use title as instruction)
        message,
        buttons,
        icon,  # pszIcon
        button_ptr
    )


    if result == 0: #S_OK
        return selected_button.value
    else:
        return None

# Example usage:
selected_button = show_task_dialog("My Task Dialog", "This is a test message", TDCBF_YES_BUTTON | TDCBF_NO_BUTTON, TD_INFORMATION_ICON)
# https://stackoverflow.com/questions/67525257/capture-makes-remaining-patterns-unreachable/79106921#79106921
match selected_button:
    case int(TDCBF_YES_BUTTON):
        print("Yes button clicked")
    case int(TDCBF_NO_BUTTON):
        print("No button clicked")
    case int(TDCBF_OK_BUTTON):
        print("OK button clicked")