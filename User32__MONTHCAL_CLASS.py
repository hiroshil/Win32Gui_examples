import win32gui
import win32con
import win32api
import commctrl
import struct
from ctypes import Structure, c_long, c_ushort, sizeof, create_unicode_buffer
# data class and utils function generated by AI

class RECT(Structure):
    _fields_ = [("left", c_long),
                ("top", c_long),
                ("right", c_long),
                ("bottom", c_long)]
class SYSTEMTIME(Structure):
    _fields_ = [
        ('wYear', c_ushort),
        ('wMonth', c_ushort),
        ('wDayOfWeek', c_ushort),
        ('wDay', c_ushort),
        ('wHour', c_ushort),
        ('wMinute', c_ushort),
        ('wSecond', c_ushort),
        ('wMilliseconds', c_ushort),
    ]
MCMV_MONTH = 0
MCMV_YEAR = 1
MCMV_DECADE = 2
MCMV_CENTURY = 3
MCM_SETCURRENTVIEW = (commctrl.MCM_FIRST + 32)

msc_hwnd = int()
LEFT = 35
TOP = 40

def buffer_from_type(data_type):
    return create_unicode_buffer(sizeof(data_type))
def buffer_into_type(buff, data_class):
    buff  = bytes(buff)[:sizeof(data_class)]
    # Create a new instance of the data class
    new_data = data_class()

    offset = 0
    for i, field_name in enumerate(data_class._fields_):

      # Extract the field data from the buffer based on its size
      field_size = sizeof(field_name[1])
      field_data = buff[offset:offset + field_size]

      # Unpack using the correct format string based on field type
      if field_name[1] == c_ushort:
          format_string = '<H'
      elif field_name[1] == c_long:
          format_string = '<l'  # Little-endian long integer
      else:
          raise ValueError('not a ctypes value')
      unpacked_value = struct.unpack(format_string, field_data)[0]
      # Add more format strings for other field types if needed 
      # e.g., for c_int: format_string = '<i'

      #Set the field value
      setattr(new_data, field_name[0], unpacked_value)
      offset += field_size
    return new_data

def WndProc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_COMMAND and wParam == 102: # Assuming 102 is the ID of the submit button
        buf = buffer_from_type(SYSTEMTIME)
        win32gui.SendMessage(msc_hwnd, commctrl.MCM_GETCURSEL, 0, buf)
        st = buffer_into_type(buf, SYSTEMTIME)
        date_str = f"{st.wYear}-{st.wMonth}-{st.wDay}"
        print(date_str)
        
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "MyWindowClass"
    wc.lpfnWndProc = WndProc
    class_atom = win32gui.RegisterClass(wc)

    hwnd = win32gui.CreateWindow(class_atom, "My Window", win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE,
                                 100, 100, 400, 350, 0, 0, 0, None)
    
    # Create an edit text control
    global msc_hwnd
    msc_hwnd = win32gui.CreateWindow(commctrl.MONTHCAL_CLASS, "", win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_BORDER | commctrl.MCS_DAYSTATE,
                                        20, 20, 200, 20, hwnd, 101, 0, None) # 101 is the ID for the edit control

    # Get the size required to show an entire month.
    buf = buffer_from_type(RECT)
    win32gui.SendMessage(msc_hwnd, commctrl.MCM_GETMINREQRECT, 0, buf)
    rc = buffer_into_type(buf, RECT)
    win32gui.SetWindowPos(msc_hwnd, 0, LEFT, TOP, rc.right, rc.bottom, win32con.SWP_NOZORDER)
    
    # Set the calendar to the annual view.
    win32gui.SendMessage(msc_hwnd, MCM_SETCURRENTVIEW, 0, MCMV_YEAR)
    
    # Create a button
    button_hwnd = win32gui.CreateWindow("BUTTON", "Submit", win32con.WS_VISIBLE | win32con.WS_CHILD,
                                       20, 250, 80, 25, hwnd, 102, 0, None) # 102 is the ID for the button


    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)
    win32gui.PumpMessages()

if __name__ == "__main__":
    main()