from PIL import Image, ImageTk
import random
from stegano import lsb
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import wave
import struct

def login():
    if username_entry.get() == "root" and password_entry.get() == "root" and verification_entry.get()== verification_code:
        login_window.destroy()
        show_gui()
    else:
        error_label.config(text="Error: Incorrect username or password")

def text_to_image():
    texttoimage = tk.Tk()
    texttoimage.title("text to Image Stegano")
    texttoimage.geometry("800x600")
    image_path_label = tk.Label(texttoimage, text="Choose an  file:",font = ("Lucida Console", 14, "italic"))
    image_path_label.pack()
    image_path_textbox = tk.Text(texttoimage, height=1)
    image_path_textbox.pack()
    def browse_image_file():
        image_file_path = filedialog.askopenfilename()
        image_path_textbox.delete("1.0", tk.END)
        image_path_textbox.insert(tk.END, image_file_path)
    browse_image_file_button = tk.Button(texttoimage, text="Browse...", command=browse_image_file)
    browse_image_file_button.pack()
    text_to_hide_label = tk.Label(texttoimage, text="Enter the text to be hidden:", font = ("Lucida Console", 14, "italic"))
    text_to_hide_label.pack()
    text_to_hide_textbox = tk.Text(texttoimage, height=5)
    text_to_hide_textbox.pack()

    def hide_text_in_image():
        image_file_path = image_path_textbox.get("1.0", tk.END).strip()
        text_to_hide = text_to_hide_textbox.get("1.0", tk.END).strip()
        secret_image = lsb.hide(image_file_path, text_to_hide)
        secret_image.save("secret.png")
        tk.messagebox.showinfo("ALERT!!!", "The text has been hidden in the image file.")
    def decrept_text_in_image():
        secret_image_path = "secret.png"
        secret_image = Image.open(secret_image_path)
        hidden_text = lsb.reveal(secret_image)
        tk.messagebox.showinfo("Decrypted Text", hidden_text)
        
    hide_text_button = tk.Button(texttoimage, text="Hide Text", command=hide_text_in_image)
    hide_text_button.pack()
    decrept_text_button = tk.Button(texttoimage, text="Decrypt Text", command=decrept_text_in_image)
    decrept_text_button.pack()
    texttoimage.mainloop()

def encrypt(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            for l in range(3):
                v1 = format(img1[i][j][l], '08b')
                v2 = format(img2[i][j][l], '08b')
                v3 = v1[:4] + v2[:4] 
                img1[i][j][l] = int(v3, 2)

    cv2.imwrite("encrypted_image.png", img1)

def decrypt(img_path):
    img = cv2.imread(img_path)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for l in range(3):
                v1 = format(img[i][j][l], '08b')
                v2 = v1[4:] + '0000'
                img[i][j][l] = int(v2, 2)

    cv2.imwrite("decrypted_image.png", img)
def image_to_image():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Image to Image Steganography")
    image1_path_label = ttk.Label(root, text="Choose the first image:")
    image1_path_label.pack(pady=10)
    image1_path_textbox = tk.Text(root, height=1)
    image1_path_textbox.pack()
    def browse_image1_file():
        image_file_path = filedialog.askopenfilename()
        image1_path_textbox.delete("1.0", tk.END)
        image1_path_textbox.insert(tk.END, image_file_path)
    browse_image1_button = ttk.Button(root, text="Browse...", command=browse_image1_file)
    browse_image1_button.pack(pady=10)
    image2_path_label = ttk.Label(root, text="Choose the second image:")
    image2_path_label.pack(pady=10)
    image2_path_textbox = tk.Text(root, height=1)
    image2_path_textbox.pack()
    def browse_image2_file():
        image_file_path = filedialog.askopenfilename()
        image2_path_textbox.delete("1.0", tk.END)
        image2_path_textbox.insert(tk.END, image_file_path)
    browse_image2_button = ttk.Button(root, text="Browse...", command=browse_image2_file)
    browse_image2_button.pack(pady=10)
    def encrypt_images():
        img1_path = image1_path_textbox.get("1.0", tk.END).strip()
        img2_path = image2_path_textbox.get("1.0", tk.END).strip()
        if img1_path == "" or img2_path == "":
            messagebox.showwarning("Warning", "Please choose both images.")
        else:
            try:
                encrypt(img1_path, img2_path)
                messagebox.showinfo("Success", "The images have been encrypted successfully.")
            except:
                messagebox.showerror("Error", "An error occurred during encryption, please select image of same size")

    encrypt_button = ttk.Button(root, text="Encrypt", command=encrypt_images)
    encrypt_button.pack(pady=10)

    def decrypt_image():
        img_path = filedialog.askopenfilename()
        if img_path == "":
            messagebox.showwarning("Warning", "Please choose an image.")
        else:
            try:
                decrypt(img_path)
                messagebox.showinfo("Success", "The image has been decrypted successfully.")
            except:
                messagebox.showerror("Error", "An error occurred during decryption.")

    decrypt_button = ttk.Button(root, text="Decrypt", command=decrypt_image)
    decrypt_button.pack(pady=10)

    # create the "Quit" button
    quit_button = ttk.Button(root, text="Quit", command=root.quit)
    quit_button.pack(pady=10)

    root.mainloop()

def text_to_audio():
    audio_window = tk.Tk()
    audio_window.geometry("400x400")
    audio_window.title("Text to Audio Steganography")
    def select_audio():
        global audio_filename
        audio_filename = filedialog.askopenfilename()
        print("Selected audio file:", audio_filename)
        selected_file_label.config(text="Selected Audio File: " + audio_filename)

    def hide_text():
        global audio_filename
        text = str(text_input.get())
        audio_file= wave.open(audio_filename, 'rb')
        frame_bytes = bytearray(list(audio_file.readframes(audio_file.getnframes())))
        text = text + int((len(frame_bytes)-(len(text)*8*8))/8) *'#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in text])))
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        frame_modified = bytes(frame_bytes)
        with wave.open('hidden_audio.wav', 'wb') as output_file:
            output_file.setparams(audio_file.getparams())
            output_file.writeframes(frame_modified)
        audio_file.close()
        messagebox.showinfo("Text hidden in audio file successfully.")

    def extract_text():
            global audio_filename
            audio_file = wave.open(audio_filename, mode='rb')
            frame_bytes = bytearray(list(audio_file.readframes(audio_file.getnframes())))
            extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
            string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
            decoded = string.split("###")[0]
            print("Sucessfully decoded: "+str(decoded))
            
            extracted_text_label.config(text="Extracted Text: " + str(decoded))
        

    select_audio_button = tk.Button(audio_window,text="Select Audio", command=select_audio)
    select_audio_button.pack()
    selected_file_label = tk.Label(audio_window, text="")
    selected_file_label.pack()
    text_input = tk.Entry(audio_window)
    text_input.pack()
    hide_button = tk.Button(audio_window, text="Hide", command=hide_text)
    hide_button.pack()
    extract_text_button = tk.Button(audio_window, text="Extract Text", command=extract_text)
    extract_text_button.pack()
    extracted_text_label = tk.Label(audio_window, text="")
    extracted_text_label.pack()


    audio_window.mainloop()
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2

def text_to_video():
    video_window = tk.Tk()
    video_window.geometry("400x400")
    video_window.title("Text to Video Steganography")

    def select_video():
        global video_filename
        video_filename = filedialog.askopenfilename()
        print("Selected video file:", video_filename)
        selected_file_label.config(text="Selected Video File: " + video_filename)

    def hide_text():
        global video_filename
        text = str(text_input.get())
        video_capture = cv2.VideoCapture(video_filename)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        frames = []
        for i in range(frame_count):
            ret, frame = video_capture.read()
            if not ret:
                break
            frames.append(frame)
        video_capture.release()
        text = text + int((len(frames)*fps - len(text)*8*8)/8) *'#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in text])))
        bit_count = 0
        for i in range(frame_count):
            for j in range(frames[i].shape[0]):
                for k in range(frames[i].shape[1]):
                    if bit_count < len(bits):
                        pixel = list(frames[i][j][k])
                        for l in range(3):
                            if bit_count < len(bits):
                                pixel[l] = (pixel[l] & 254) | bits[bit_count]
                                bit_count += 1
                        frames[i][j][k] = tuple(pixel)
                    else:
                        break
            if bit_count >= len(bits):
                break
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_file = cv2.VideoWriter('hidden_video.avi', fourcc, fps, frames[0].shape[:2])
        for i in range(len(frames)):
            output_file.write(frames[i])
        output_file.release()
        messagebox.showinfo("Text hidden in video file successfully.")

    def extract_text():
        global video_filename
        video_capture = cv2.VideoCapture(video_filename)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        bits = []
        bit_count = 0
        for i in range(frame_count):
            ret, frame = video_capture.read()
            if not ret:
                break
            for j in range(frame.shape[0]):
                for k in range(frame.shape[1]):
                    if bit_count < 8*8:
                        pixel = list(frame[j][k])
                        for l in range(3):
                            bits.append(pixel[l] & 1)
                        bit_count += 3
            if bit_count >= 8*8:
                break
        video_capture.release()
        string = "".join(chr(int("".join(map(str,bits[i:i+8])),2)) for i in range(0,len(bits),8))
        decoded = string.split("###")[0]
        print("Successfully decoded: "+str(decoded))
        extracted_text_label.config(text="Extracted Text: " + str(decoded))

    select_video_button = tk.Button(video_window, text="Select Video", command=select_video)
    select_video_button.pack()
    selected_file_label = tk.Label(video_window,text="")
    text_input_label = tk.Label(video_window, text="Enter text to hide:")
    text_input_label.pack()
    text_input = tk.Entry(video_window)
    text_input.pack()

    hide_text_button = tk.Button(video_window, text="Hide Text", command=hide_text)
    hide_text_button.pack()

    extract_text_button = tk.Button(video_window, text="Extract Text", command=extract_text)
    extract_text_button.pack()
    extracted_text_label = tk.Label(video_window)

    video_window.mainloop()




def show_gui():
    root = tk.Tk()
    root.geometry("400x400")
    label = tk.Label(root, text="Select an option:")
    label.pack(pady=10)
    button1 = tk.Button(root, text="Text to image", command=text_to_image)
    button1.pack(pady=10)
    button2 = tk.Button(root, text="Image to image", command=image_to_image)
    button2.pack(pady=10)

    button3 = tk.Button(root, text="Text to Video", command=text_to_video)
    button3.pack(pady=10)

    button4 = tk.Button(root, text="Text to Audio", command=text_to_audio)
    button4.pack(pady=10)

    root.mainloop()

login_window = tk.Tk()
login_window.geometry("800x600")
def generate_code():
    code = ""
    for i in range(6):
        code += str(random.randint(0,9))
    return code

verification_code = generate_code()

username_label = tk.Label(login_window, text="Username:")
username_entry = tk.Entry(login_window)
password_label = tk.Label(login_window, text="Password:")
password_entry = tk.Entry(login_window, show="*")
verification_label = tk.Label(login_window, text="Enter the code shown below:")
verification_code_label = tk.Label(login_window, text=verification_code, font=("Courier", 20))
verification_entry = tk.Entry(login_window)
login_button = tk.Button(login_window, text="Login", command=login)
error_label = tk.Label(login_window, text="")
username_label.pack(pady=10)
username_label.config(font=("TkDefaultFont", 20))
username_entry.pack(pady=10)
password_label.pack(pady=10)
password_label.config(font=("TkDefaultFont", 20))
password_entry.pack(pady=10)
verification_label.pack(pady=10)
verification_code_label.pack(pady=10)
verification_entry.pack(pady=10)
login_button.pack(pady=10)
error_label.pack(pady=10)
login_window.mainloop()