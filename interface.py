import tkinter as tk
import requests
from tkcalendar import Calendar
from datetime import date

def test_connection(school, token):
    try:
        request = requests.get(f"https://{school}.instructure.com/api/v1/users/self", headers={"Authorization": f"Bearer {token}"})
        request.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return "Success! Connection to Canvas established. ✅"
    except requests.exceptions.InvalidURL:
        return "Error: Invalid school name. Please check for typos. ❌"
    except requests.exceptions.HTTPError as err:
        return f"Error: HTTP Error {err.response.status_code}. Please check your token. ❌"
    except Exception as e:
        return f"An unexpected error occurred: {e} ❌"

def handle_test_connection_click(school, token, statusLabel):
    # Call the test_connection function and get the result
    result_message = test_connection(school, token)
    
    # Update the label with the result
    statusLabel.config(text=result_message)

def handle_calendar_selection(event, selectedCalendarLabel, calendarListBox, calendarKeyLabel):
    selected_index = calendarListBox.curselection()
    print(type(selected_index), selected_index)
    if selected_index:
        selected_calendar = calendarListBox.get(selected_index)
        selectedCalendarLabel.config(text=f"Selected Calendar: {selected_calendar}")
    else:
        selectedCalendarLabel.config(text="Selected Calendar: None")


    if selected_index == (0,):
        calendarKeyLabel.config(text="Google Calendar API Key:")
    elif selected_index == (1,):
        calendarKeyLabel.config(text="iCalendar API Key:")
    elif selected_index == (2,):
        calendarKeyLabel.config(text="Outlook Calendar API Key:")

    calendarKeyLabel.grid(column=0, row=6)
    apiKeyInput = tk.Entry(width=30)
    apiKeyInput.grid(column=1, row=6)

def update_date(toFrom, dateDict, date, fromLabel, toLabel):
    if toFrom == "from":
        dateDict["from"] = date
        fromLabel.config(text=f"From Date: {dateDict['from']}")
    else:
        dateDict["to"] = date
        toLabel.config(text=f"To Date: {dateDict['to']}") 

def open_calendar(toFrom, window, dateDict, fromLabel, toLabel):
    calendar_window = tk.Toplevel(window)
    calendar_window.title("Select Date")

    if toFrom == "from":
        date = dateDict["from"]
    else:
        date = dateDict["to"]

    calendar = Calendar(calendar_window, selectmode='day', year=date.year, month=date.month, day=date.day)
    calendar.grid(column=0, row=0)

    def on_select():
        selected_date = calendar.selection_get()
        print(f"Selected date: {selected_date}")
        update_date(toFrom, dateDict, selected_date, fromLabel, toLabel)
        calendar_window.destroy()

    selectButton = tk.Button(calendar_window, text="Select", command=on_select)
    selectButton.grid(column=0, row=1)

def main():
    window = tk.Tk()

    window.title("Canvas2Calendar")

    window.geometry('800x600')

    titleLabel = tk.Label(window, text="Canvas2Calendar:", font=("Arial Bold", 20))
    titleLabel.grid(column=0, row=0)

    schoolLabel = tk.Label(window, text="Subdomain:", font=("Arial", 12))
    schoolInput = tk.Entry(window, width=30)
    schoolInput.grid(column=1, row=1)
    schoolLabel.grid(column=0, row=1)


    canvasTokenLabel = tk.Label(window, text="Canvas Token:", font=("Arial", 12))
    canvasTokenInput = tk.Entry(window, width=30)
    canvasTokenLabel.grid(column=0, row=2)
    canvasTokenInput.grid(column=1, row=2)

    testConnectionButton = tk.Button(window, text="Test Connection", command=lambda: test_connection(schoolInput.get(), canvasTokenInput.get()))
    testConnectionButton.grid(column=1, row=3)

    testConnectionStatusLabel = tk.Label(window, text="", font=("Arial", 12))
    testConnectionStatusLabel.grid(column=1, row=4)

    testConnectionButton.config(command=lambda: handle_test_connection_click(schoolInput.get(), canvasTokenInput.get(), testConnectionStatusLabel))

    calendarListBox = tk.Listbox(window, selectmode="browse")
    calendarListBox.insert(0, "Google Calendar")
    calendarListBox.insert(1, "iCalendar")
    calendarListBox.insert(2, "Outlook Calendar")
    calendarListBox.grid(column=0, row=5)
    selectedCalendarLabel = tk.Label(window, text=f"Selected Calendar: None", font=("Arial", 12))
    selectedCalendarLabel.grid(column=0, row=4)
    calendarKeyLabel = tk.Label(text="")
    calendarListBox.bind('<<ListboxSelect>>', lambda event: handle_calendar_selection(event, selectedCalendarLabel, calendarListBox, calendarKeyLabel))

    dateDict = {}
    dateDict["from"] = date.today()
    dateDict["to"] = date(date.today().year, 12, 31)

    fromLabel = tk.Label(window, text=f"From Date: {dateDict['from']}", font=("Arial", 12))
    fromButton = tk.Button(window, text="Edit", command=lambda: open_calendar("from", window, dateDict, fromLabel, toLabel))
    fromLabel.grid(column=0, row=7)
    fromButton.grid(column=0, row=8)

    toLabel = tk.Label(window, text=f"To Date: {dateDict['to']}", font=("Arial", 12))
    toButton = tk.Button(window, text="Edit", command=lambda: open_calendar("to", window, dateDict, fromLabel, toLabel))
    toLabel.grid(column=0, row=9)
    toButton.grid(column=0, row=10)

    window.mainloop()

if __name__ == "__main__":
    main()