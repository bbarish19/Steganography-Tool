from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog

DELIMITER = "EOF"  # Unique marker to indicate end of the message

# ASCII Art to display at the start
ASCII_ART = """
8888888888888888888888888888888888888888888888888888888888888888888888
8888888888888888888888888888888888888888888888888888888888888888888888
888888888888888888888888888888P""  ""988888888888888888888888888888888
888888888888888888888P"88888P          988888"988888888888888888888888
888888888888888888888  "9888            888P"  88888888888888888888888
88888888888888888888888bo "9  d8o  o8b  P" od8888888888888888888888888
88888888888888888888888888bob 98"  "8P dod8888888888888888888888888888
88888888888888888888888888888    db    8888888888888888888888888888888
8888888888888888888888888888888      888888888888888888888888888888888
8888888888888888888888888888P"9bo  odP"9888888888888888888888888888888
8888888888888888888888888P" od88888888bo "9888888888888888888888888888
88888888888888888888888   d88888888888888b   8888888888888888888888888
888888888888888888888888oo8888888888888888oo88888888888888888888888888
8888888888888888888888888888888888888888888888888888888888888888888888
"""

def welcome_screen():
    """Displays a welcome screen with ASCII art and some nice formatting."""
    print("\n" + "="*70)
    print(" "*18 + "WELCOME TO THE STEGANOGRAPHY TOOL")
    print("-"*70)
    print(ASCII_ART)
    print("-"*70)
    print("This tool lets you encode and decode secret messages in image files!")
    print(" "*17 + "Program created by: Benjamin Barish")
    print("="*70)

def validate_file_path(file_path):
    """Validates if the file exists and is a valid image."""
    if not os.path.isfile(file_path):
        print(f"❌ The file {file_path} does not exist.")
        return False
    try:
        Image.open(file_path)  # Try opening the image to check if it's a valid image file
        return True
    except IOError:
        print(f"❌ The file {file_path} is not a valid image.")
        return False

def select_file_dialog(file_type="open"):
    """Opens a file dialog to select a file."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    if file_type == "open":
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    elif file_type == "save":
        file_path = filedialog.asksaveasfilename(title="Save file as", defaultextension=".png", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    return file_path

def encode_image():
    """Encodes a message into an image."""
    while True:
        choice = input("Would you like to manually enter the INPUT file path (M) or select it through a popup (P)? (M/P): ").strip().lower()

        if choice == 'm':
            input_image_path = input("Enter the path of the image to encode: ").strip()
        elif choice == 'p':
            input_image_path = select_file_dialog("open")
            print(f"\n" + "You selected the file: {input_image_path}" + "\n")  # Display the selected file
        else:
            print("❌ Invalid choice. Please enter 'M' for manual input or 'P' for popup selection.")
            continue

        if not validate_file_path(input_image_path):
            continue

        # Ask user to select the input file after choosing the popup method for encoding

        choice = input("Would you like to manually enter the OUTPUT file path (M) or select it through a popup (P)? (M/P): ").strip().lower()

        if choice == 'm':
            output_image_path = input("Enter the output image path: ").strip()
        elif choice == 'p':
            output_image_path = select_file_dialog("save")
            print(f"\n" + "You selected the output file: {output_image_path}" + "\n")  # Display the selected file
        else:
            print("❌ Invalid choice. Please enter 'M' for manual input or 'P' for popup selection.")
            continue
        
        if not output_image_path.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            print("❌ Please provide a valid image file extension for the output (e.g., .png, .jpg).")
            continue

        message = input("Enter the secret message: ").strip()

        img = Image.open(input_image_path)
        encoded_img = img.copy()
        width, height = img.size
        message += DELIMITER  # Append delimiter to mark the end of the message
        binary_message = ''.join(format(ord(char), '08b') for char in message)

        if len(binary_message) > width * height * 3:
            print("❌ Message is too large to encode in this image.")
            continue

        data_index = 0
        pixels = list(encoded_img.getdata())

        new_pixels = []
        for pixel in pixels:
            if data_index < len(binary_message):
                new_pixel = list(pixel)
                for i in range(3):  # Modify R, G, B values
                    if data_index < len(binary_message):
                        new_pixel[i] = (new_pixel[i] & ~1) | int(binary_message[data_index])
                        data_index += 1
                new_pixels.append(tuple(new_pixel))
            else:
                new_pixels.append(pixel)

        encoded_img.putdata(new_pixels)
        encoded_img.save(output_image_path)
        print("\n" + "Message successfully encoded into:", output_image_path)
        break


def decode_image():
    """Decodes a message from an image."""
    while True:
        choice = input("Would you like to manually enter the file path (M) or select it through a popup (P)? (M/P): ").strip().lower()

        if choice == 'm':
            image_path = input("Enter the path of the image to decode: ").strip()
        elif choice == 'p':
            image_path = select_file_dialog("open")
        else:
            print("❌ Invalid choice. Please enter 'M' for manual input or 'P' for popup selection.")
            continue

        if not validate_file_path(image_path):
            continue

        img = Image.open(image_path)
        pixels = list(img.getdata())

        binary_message = ""
        for pixel in pixels:
            for i in range(3):  # Extract LSB from R, G, B values
                binary_message += str(pixel[i] & 1)

        message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

        # Trim at the delimiter (EOF)
        if DELIMITER in message:
            message = message[:message.index(DELIMITER)]

        print("\nDecoded message:", message)
        break

def main_menu():
    """Displays the main menu and handles user selection."""
    welcome_screen()  # Display the welcome screen with ASCII art and description
    while True:
        print("\nChoose an option:")
        print("(E)ncode a message")
        print("(D)ecode a message")
        print("(X) Exit")

        choice = input("Enter your choice (E/D/X): ").strip().lower()

        if choice == 'e':
            encode_image()
        elif choice == 'd':
            decode_image()
        elif choice == 'x':
            
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 'E' to encode, 'D' to decode, or 'X' to exit.")

if __name__ == "__main__":
    print("Welcome to the Steganography Tool!\n")
    main_menu()
