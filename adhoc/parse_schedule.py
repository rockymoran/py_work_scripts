import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox


def parse_schedule(schedule):
    try:
        # Handle empty or NaN values
        if pd.isna(schedule) or not isinstance(schedule, str):
            return 'N/A', 'N/A', 'N/A', 'N/A'

        # Split by spaces
        parts = schedule.strip().split()
        if len(parts) < 2:  # Need at least days and time
            return schedule, 'N/A', 'N/A', 'N/A'

        # First part is Days
        days = parts[0]

        # Second part should be the time
        if len(parts) > 1:
            # Check if second part contains a hyphen for time range
            if '-' in parts[1]:
                times = parts[1].split('-')
                start_t = times[0]
                end_t = times[1]
            else:
                start_t = parts[1]
                end_t = 'N/A'
        else:
            start_t = 'N/A'
            end_t = 'N/A'

        # Third part is Room if it exists
        room = parts[2] if len(parts) > 2 else 'N/A'

        return days, start_t, end_t, room

    except Exception as e:
        print(f"Error processing schedule entry: {schedule}")
        return schedule, 'N/A', 'N/A', 'N/A'


def process_instructor_file(df):
    try:
        # Create new dataframe with just CCN and Instructor columns
        instructor_df = pd.DataFrame({
            'CCN': df['CCN'],
            'Instructor': df['Instructor']
        })

        instructor_df = instructor_df.sort_values('Instructor')

        # Ask user for save location
        output_file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialdir="C:/Work",
            filetypes=[
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ],
            title="Save Instructor File"
        )

        if output_file:
            # Save to tab-delimited file
            instructor_df.to_csv(output_file, sep='\t', index=False)
            messagebox.showinfo("Success", f"Instructor file saved successfully to:\n{output_file}")
        else:
            messagebox.showwarning("Warning", "Instructor file save operation cancelled.")

    except Exception as e:
        messagebox.showerror("Error", f"Error processing instructor file:\n{str(e)}")


def select_file():
    # Create and hide the main tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        initialdir="C:/Users/Downloads",  # Specify your default directory here
        filetypes=[
            ("Excel files", "*.xlsx *.xls"),
            ("All files", "*.*")
        ]
    )

    return file_path


def process_excel():
    # Get input file from user
    input_file = select_file()

    if not input_file:
        messagebox.showwarning("Warning", "No file selected. Operation cancelled.")
        return

    try:
        # Read the Excel file
        df = pd.read_excel(input_file)

        if 'Schedule' not in df.columns or 'CCN' not in df.columns:
            messagebox.showerror("Error", "Required columns 'Schedule' and 'CCN' not found in Excel file.")
            return

        # Create empty lists for new columns
        days_list = []
        start_t_list = []
        end_t_list = []
        room_list = []

        # Process each schedule entry
        for schedule in df['Schedule']:
            days, start_t, end_t, room = parse_schedule(schedule)
            days_list.append(days)
            start_t_list.append(start_t)
            end_t_list.append(end_t)
            room_list.append(room)

        # Create new dataframe with required columns
        new_df = pd.DataFrame({
            'CCN': df['CCN'],
            'Days': days_list,
            'StartT': start_t_list,
            'EndT': end_t_list,
            'Room': room_list
        })

        # Ask user for save location
        output_file = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialdir="C:/Work",
            filetypes=[
                ("Text files", "*.csv"),
                ("All files", "*.*")
            ],
            title="Save Output File"
        )

        if output_file:
            # Save to tab-delimited file
            new_df.to_csv(output_file, sep='\t', index=False)
            messagebox.showinfo("Success", f"File saved successfully to:\n{output_file}")
        else:
            messagebox.showwarning("Warning", "Save operation cancelled.")

        process_instructor_file(df)

    except Exception as e:
        messagebox.showerror("Error", f"Error processing file:\n{str(e)}")


if __name__ == "__main__":
    process_excel()
