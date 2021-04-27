from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont
from copy import copy

global img, wmk, base_image, watermark_image, transparent, final, count, text, window
count = 1


# Uploading the main/base jpeg image and displaying it in the canvas
def upload_image(event=None):
    global img, base_image
    filename = filedialog.askopenfilename(filetypes=[("JPEG files", ".jpg .jpeg .JPG .JPEG")])
    base_image = Image.open(filename)
    image = base_image.resize((100, 100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    canvas_image.create_image(50, 50, image=img)


# Uploading the watermark png image and displaying it in the canvas
def upload_watermark(event=None):
    global wmk, watermark_image
    filename = filedialog.askopenfilename(filetypes=[("PNG files", ".png .PNG")])
    watermark_image = Image.open(filename)
    image = watermark_image.resize((100, 100), Image.ANTIALIAS)
    wmk = ImageTk.PhotoImage(image)
    canvas_watermark.create_image(50, 50, image=wmk)


# To save the output/final image
def save():
    global transparent, count, window
    filename = filedialog.asksaveasfilename(filetypes=("JPEG files", ".jpeg .JPEG"))
    transparent.save(filename + '.jpeg')
    count += 1
    # Exit program after image is saved
    window.destroy()


# Pasting the watermark image over the base image and displaying a preview in the canvas
def paste_watermark(event=None):
    global base_image, watermark_image, transparent, final
    margin = 20
    width_b, height_b = base_image.size
    width_w, height_w = watermark_image.size
    watermark_image = watermark_image.resize((int(width_b*0.2), int(height_b*0.2)), Image.ANTIALIAS)
    transparent = Image.new('RGBA', (width_b, height_b), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark_image, (width_b-width_w-margin, height_b-height_w-margin), mask=watermark_image)
    transparent = transparent.convert('RGB')
    image = transparent.resize((300, 300), Image.ANTIALIAS)
    final = ImageTk.PhotoImage(image)
    canvas_show.create_image(150, 150, image=final)


# Pasting the text watermark over the base image and displaying a preview in the canvas
def write_watermark(event=None):
    global base_image, transparent, final, text
    text = entry_watermark.get()
    margin = 20
    new_image = copy(base_image)
    width_b, height_b = new_image.size
    drawing = ImageDraw.Draw(new_image)
    black = (3, 8, 12)
    # font = ImageFont.load_default()
    font_size = 1  # starting font size
    # portion of image width you want text width to be
    img_fraction = 0.25
    font = ImageFont.truetype('FreeMono.ttf', font_size)
    while font.getsize(text)[0] < img_fraction * new_image.size[0]:
        # iterate until the text size is just larger than the criteria
        font_size += 1
        font = ImageFont.truetype('FreeMono.ttf', font_size)
    # optionally de-increment to be sure it is less than criteria
    font_size -= 1
    font = ImageFont.truetype('FreeMono.ttf', font_size)
    width_t, height_t = drawing.textsize(text, font)
    drawing.text((width_b-width_t-margin, height_b-height_t-margin), text, fill=black, font=font)
    image = new_image.resize((300, 300), Image.ANTIALIAS)
    final = ImageTk.PhotoImage(image)
    canvas_show.create_image(150, 150, image=final)
    transparent = new_image


# Main Program
window = Tk()
window.title('Watermark Maker')
window.minsize(width=500, height=500)
window.config(padx=100, pady=50, bg='#f7f5dd')

canvas_image = Canvas(window, width=100, height=100)
# canvas_image.pack()
canvas_image.grid(row=0, column=0)
button_image = Button(text="Upload Image", command=upload_image)
# button_image.pack()
button_image.grid(row=1, column=0)
canvas_watermark = Canvas(window, width=100, height=100)
# canvas_watermark.pack()
canvas_watermark.grid(row=0, column=1)
button_watermark = Button(text="Upload Watermark", command=upload_watermark)
# button_watermark.pack()
button_watermark.grid(row=1, column=1)
# label_watermark = Label(text='Watermark Text')
# # label_watermark.pack()
# label_watermark.grid(row=0, column=2)
entry_watermark = Entry(width=30)
entry_watermark.grid(row=0, column=2)
# entry_watermark.pack()
canvas_show = Canvas(window, width=300, height=300)
# canvas_show.pack()
canvas_show.grid(row=2, column=0, columnspan=3)
button_use_image = Button(text="Use Image", command=paste_watermark)
# button_use_image.pack()
button_use_image.grid(row=3, column=0)
button_use_text = Button(text="Use Text", command=write_watermark)
# button_use_text.pack()
button_use_text.grid(row=3, column=1)
button_save = Button(text="Save", command=save)
# button_save.pack()
button_save.grid(row=3, column=2)


window.mainloop()
