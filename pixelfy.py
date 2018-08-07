import logging
import tkinter
import os
import sys
from tkinter import filedialog
from PIL import Image


# Log information
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
os.chdir(os.path.dirname(sys.argv[0]))

filename = ''
num_pixels = 8


def main():
    create_window()


def create_window():
    global img_panel
    # Create Tk window
    root = tkinter.Tk()

    # Create menu bar
    menu_bar = tkinter.Menu(root)
    root.config(menu=menu_bar)

    # Create the submenu
    submenu = tkinter.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=submenu)
    submenu.add_command(label="Open", command=browse_file)
    submenu.add_command(label="Exit", command=root.destroy)

    root.geometry('600x400')
    root.title('Pixelifier')
    root.iconbitmap(r'.\pix_icon.ico')

    img_panel = tkinter.Label(root)
    img_panel.pack()

    load_im_button = tkinter.Button(root, text="Load Image", command=browse_file)
    load_im_button.pack()

    pixelfy_button = tkinter.Button(root, text='Pixelify Image', command=lambda: pixelfy(num_pixels, filename))
    pixelfy_button.pack()

    scale = tkinter.Scale(root, from_=0, to=50, orient=tkinter.HORIZONTAL, command=set_pixels)
    scale.set(num_pixels)
    scale.pack()

    root.mainloop()


def browse_file():
    global filename
    filename = filedialog.askopenfilename(filetypes=(("Picture Files", ".jpg .png .jpeg"), ("All Files", "*.*")))
    logging.info(filename)
    return filename


def set_pixels(val):
    global num_pixels
    num_pixels = val


def pixelfy(num_horizontal_pixels, image_name):
    num_horizontal_pixels = int(num_horizontal_pixels)
    im = Image.open(image_name)
    im_x, im_y = im.size

    try:
        pixel_size = int(im_x / (num_horizontal_pixels * 3))
        num_vertical_pixels = int(im_y / (pixel_size * 3))
    except ZeroDivisionError:
        print('Too many pixels!')
        return

    small_im = Image.new(im.mode, (int((num_horizontal_pixels - 1) * (im_x / (num_horizontal_pixels * 3))), num_vertical_pixels * pixel_size))

    logging.info('File: ' + image_name)
    logging.info('Pixel Size: ' + str(pixel_size) + ' x ' + str(pixel_size))
    logging.info(str(num_horizontal_pixels) + ' horizontal pixels')
    logging.info(str(num_vertical_pixels) + ' vertical pixels')

    pix_num = 1
    x_ptr = y_ptr = pixel_size
    x_new_ptr = y_new_ptr = 0
    while y_ptr < im_y:
        while x_ptr < im_x:
            pixel_im = im.crop((x_ptr, y_ptr, x_ptr + pixel_size, y_ptr + pixel_size))
            small_im.paste(pixel_im, (x_new_ptr, y_new_ptr))
            logging.debug('Pixel #' + str(pix_num) + ': (' + str(x_ptr) + ', ' + str(y_ptr) + ')'
                  + ' onto (' + str(x_new_ptr) + ', ' + str(y_new_ptr) + ')')
            pix_num += 1
            x_ptr += pixel_size * 3
            x_new_ptr += pixel_size
        y_ptr += pixel_size * 3
        y_new_ptr += pixel_size
        x_ptr = pixel_size
        x_new_ptr = 0

    # Uncomment if you want to save this
    # small_im.save(os.path.dirname(image_name) + os.path.sep + 'pixel_' + os.path.basename(image_name))
    small_im.show()
    return small_im


if __name__ == '__main__':
    main()