import tkinter as tk  # For creating the GUI
import pyautogui  # For performing mouse clicks
import keyboard  # For handling keybindings
import threading  # For running the clicking function in a separate thread
import time  # For sleep functionality

class AutoClicker:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("500x200")
        
        self.default_key = "f6"

        # Label to give instructions to the user
        self.label = tk.Label(root, text="Press the key to start/stop clicking or click the button", font=("Arial", 12))
        self.label.pack(pady=10)

        # Variable to track whether the autoclicker is active
        self.clicking = False

        # Label and entry field for click interval
        self.click_interval_label = tk.Label(root, text="Click interval (seconds):")
        self.click_interval_label.pack()
        self.click_interval_entry = tk.Entry(root)
        self.click_interval_entry.pack()
        self.click_interval_entry.insert(0, "0.001")  # Default click interval

        # Label and entry field for the toggle key
        self.toggle_key_label = tk.Label(root, text="Toggle key:")
        self.toggle_key_label.pack()
        self.toggle_key_entry = tk.Entry(root)
        self.toggle_key_entry.pack()
        self.toggle_key_entry.insert(0, self.default_key)  # Default toggle key
        self.toggle_key_entry.bind("<KeyRelease>", self.update_key)  # Bind the key release event to update the key

        # Button to start/stop the autoclicker
        self.toggle_button = tk.Button(root, text="Start", command=self.toggle_clicking)
        self.toggle_button.pack(pady=10)

        # Set the initial toggle key and add the hotkey binding
        self.toggle_key = self.default_key
        keyboard.add_hotkey(self.toggle_key, self.toggle_clicking)

    def update_key(self, event):
        # Update the toggle key based on user input
        new_toggle_key = self.toggle_key_entry.get()

        if new_toggle_key:
            try:
                # Remove the previous hotkey binding
                keyboard.remove_hotkey(self.toggle_key)
            except KeyError:
                pass  # The key was not set before

            # Set the new toggle key and add the new hotkey binding
            self.toggle_key = new_toggle_key
            keyboard.add_hotkey(self.toggle_key, self.toggle_clicking)
            self.label.config(text="Key updated successfully.", fg="green")
        else:
            self.label.config(text="Invalid key value. Please enter a valid key.", fg="red")

    def toggle_clicking(self):
        # Toggle between starting and stopping the autoclicker
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self):
        # Start the autoclicker
        if not self.clicking:
            try:
                # Get the click interval from the entry field
                self.click_interval = float(self.click_interval_entry.get())
                self.clicking = True
                self.toggle_button.config(text="Stop")
                self.label.config(text="Clicking... Press the key or button to stop.", fg="black")
                # Start the clicking in a separate thread
                self.click_thread = threading.Thread(target=self.click)
                self.click_thread.start()
            except ValueError:
                self.label.config(text="Invalid interval value. Please enter a number.", fg="red")

    def stop_clicking(self):
        # Stop the autoclicker
        self.clicking = False
        if hasattr(self, 'click_thread'):
            self.click_thread.join()  # Ensure the thread is finished
        self.toggle_button.config(text="Start")
        self.label.config(text="Press the key to start/stop clicking or click the button", fg="black")

    def click(self):
        # Perform the clicking at the specified interval
        while self.clicking:
            pyautogui.click()
            time.sleep(self.click_interval)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
