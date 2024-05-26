import cv2
import easyocr
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        process_image(img, file_path)

def process_image(img, file_path):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(img)

    detected_texts = []
    for text in result:
        position1 = tuple(map(int, text[0][0]))  # x1, y1
        position2 = tuple(map(int, text[0][2]))  # x2, y2
        detectText = text[1]
        detected_texts.append(detectText)

        # Draw a rectangle around the text
        cv2.rectangle(img, position1, position2, (0, 255, 0), 3)
        cv2.putText(img, detectText, position1, cv2.FONT_HERSHEY_COMPLEX, 1, (200, 10, 0), 2)

    show_image(img)
    copy_text(detected_texts)
    save_image_option(img, file_path)

def show_image(img):
    # Convert BGR image to RGB format
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert RGB image to PhotoImage format
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    # Create a tkinter window and display the image
    img_label = tk.Label(root, image=img_tk)
    img_label.image = img_tk
    img_label.pack()


# def show_image(img):
#     cv2.imshow('Image', img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

def copy_text(detected_texts):
    text = "\n".join(detected_texts)
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Text Copied", "Detected text has been copied to clipboard.")

def save_image_option(img, original_path):
    save = messagebox.askyesno("Save Image", "Do you want to save the image with highlighted text?")
    if save:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                            ("All files", "*.*")],
                                                 initialfile="highlighted_text.png")
        if save_path:
            cv2.imwrite(save_path, img)
            messagebox.showinfo("Image Saved", f"Image saved at {save_path}")

root = tk.Tk()
root.title("Text Detection from Image")
root.geometry("800x600")

btn_select = tk.Button(root, text="Select Image", command=select_image)
btn_select.pack()

root.mainloop()
