Steganography Tool
Program created by: Benjamin Barish

Description _________________________________________________________________________
This Steganography Tool allows users to encode and decode secret messages in image files using the least significant bit (LSB) 
technique. The program provides a simple and interactive interface to encode a message into an image and later decode it back.

The tool supports multiple image formats like PNG, JPG, JPEG, and BMP, and provides the option to either manually enter file 
paths or select files through a graphical popup dialog.

Features ____________________________________________________________________________
Encoding: Allows you to encode a secret message into an image file.
Decoding: Allows you to extract the hidden message from an image.
File Dialogs: Option to select input and output image files using popup dialogs or by manually entering file paths.
ASCII Art Welcome Screen: Displays a custom ASCII art message on startup.
Delimiter: Appends an "EOF" delimiter at the end of the encoded message to mark its end.

Requirements__________________________________________________________________________
Python 3.x
Pillow (PIL) library for image manipulation
Tkinter for file dialog
Installing Dependencies
To install the required dependencies, run the following command: pip install pillow

Usage _______________________________________________________________________________
Step 1: Run the Program
To run the program, execute the Python script steganography.py: python steganography.py

Step 2: Main Menu Options
You will be presented with the following options in the main menu:

(E)ncode a message: This option lets you encode a message into an image.
(D)ecode a message: This option lets you decode a hidden message from an image.
(X) Exit: Exit the program.

Step 3: Encoding a Message
To encode a message:
Select or enter the input image path where you want to embed the secret message.
Select or enter the output image path where the encoded image will be saved.
Enter the secret message you want to hide in the image.
The tool will embed the message in the image and save it to the chosen output file.

Step 4: Decoding a Message
To decode a message:
Select or enter the path of the encoded image.
The program will extract and display the hidden message, stopping at the "EOF" delimiter.
