from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Encode function
def encode_image(input_image_path, message, output_image_path):
    image = Image.open(input_image_path)
    encoded = image.copy()
    width, height = image.size
    index = 0

    binary_message = ''.join([format(ord(i), "08b") for i in message]) + '1111111111111110'

    for row in range(height):
        for col in range(width):
            if index < len(binary_message):
                pixel = list(image.getpixel((col, row)))
                for n in range(3):
                    if index < len(binary_message):
                        pixel[n] = pixel[n] & ~1 | int(binary_message[index])
                        index += 1
                encoded.putpixel((col, row), tuple(pixel))

    encoded.save(output_image_path)
    return output_image_path

# Decode function
def decode_image(image_path):
    image = Image.open(image_path)
    width, height = image.size
    binary_data = ""
    for row in range(height):
        for col in range(width):
            pixel = image.getpixel((col, row))
            for n in range(3):
                binary_data += str(pixel[n] & 1)
    bytes_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ""
    for byte in bytes_data:
        if byte == '11111110':
            break
        message += chr(int(byte, 2))
    return message

# GUI Setup
class StegApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Cybersecurity Steganography Tool")
        self.root.geometry("1080x720")
        self.root.configure(bg="white")

        self.image_path = None

        # Header
        Label(root, text="Cybersecurity Steganography", font=("Helvetica", 26, "bold"), fg="blue", bg="white").pack(pady=20)

        # Frame
        frame = Frame(root, bg="white", bd=3, relief=RIDGE)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Left - Image Section
        left = Frame(frame, bg="white")
        left.pack(side=LEFT, padx=30, pady=30)

        Button(left, text="Choose Image", font=("Helvetica", 12), command=self.choose_image, bg="#d0f0c0", fg="black", width=20).pack()
        self.image_label = Label(left, text="No image selected", fg="black", bg="white", wraplength=200, justify=LEFT)
        self.image_label.pack(pady=10)
        self.preview_label = Label(left, bg="white")
        self.preview_label.pack()

        # Right - Message Section
        right = Frame(frame, bg="white")
        right.pack(side=LEFT, padx=30, pady=30, fill=BOTH, expand=True)

        Label(right, text="Enter Secret Message:", fg="black", bg="white", font=("Helvetica", 14)).pack(anchor=W)
        self.message_text = Text(right, height=10, font=("Consolas", 12), wrap=WORD, bg="#f4f4f4", fg="black", insertbackground="black")
        self.message_text.pack(fill=X, pady=10)

        btn_frame = Frame(right, bg="white")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="Encode and Save", font=("Helvetica", 12), command=self.encode, bg="#3a86ff", fg="white", width=18).grid(row=0, column=0, padx=10)
        Button(btn_frame, text="Decode Message", font=("Helvetica", 12), command=self.decode, bg="#ff006e", fg="white", width=18).grid(row=0, column=1, padx=10)

        self.output_label = Label(right, text="", fg="black", bg="white", wraplength=500, font=("Helvetica", 12))
        self.output_label.pack(pady=20)

    def choose_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if self.image_path:
            self.image_label.config(text=os.path.basename(self.image_path))
            img = Image.open(self.image_path)
            img.thumbnail((250, 250))
            photo = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo
        else:
            self.image_label.config(text="No image selected")

    def encode(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return
        message = self.message_text.get("1.0", END).strip()
        if not message:
            messagebox.showerror("Error", "Message cannot be empty.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            encode_image(self.image_path, message, save_path)
            self.output_label.config(text="✅ Message successfully encoded and saved.")

    def decode(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return
        message = decode_image(self.image_path)
        self.output_label.config(text="🔓 Decoded Message:\n" + message)


if __name__ == "__main__":
    root = Tk()
    app = StegApp(root)
    root.mainloop()
