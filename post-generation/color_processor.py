from PIL import Image
import os
import sys

def process_image(input_file, output_file):
    image = Image.open(input_file)
    image = image.convert('RGBA')

    width, height = image.size

    r_red = 0
    g_red = 160
    b_red = 100
    r_green = 0
    g_green = 160
    b_green = 100
    r_blue = 0
    g_blue = 160
    b_blue = 100

    for x in range(width):
        for y in range(height):
            r, g, b, a = image.getpixel((x, y))

            if r >r_red and g < g_red and b < b_red: 
                # Set the pixel to red
                image.putpixel((x, y), (255, 0, 0, 255))
            elif r <r_green and g > g_green and b < b_green: 
                # Set the pixel to green
                image.putpixel((x, y), (0, 255, 0, 255))
            elif r <r_blue and g < g_blue and b > b_blue: 
                # Set the pixel to blue
                image.putpixel((x, y), (0, 0, 255, 255))
            else:
                max_color = max(r, g, b)

                if max_color == r:
                    # Set the pixel to red
                    image.putpixel((x, y), (255, 0, 0, 255))
                elif max_color == g:
                    # Set the pixel to green
                    image.putpixel((x, y), (0, 255, 0, 255))
                else:
                    # Set the pixel to blue
                    image.putpixel((x, y), (0, 0, 255, 255))

    image.save(output_file)

# # gird search for thresholds

# def process_image(input_file, output_file, r_red, g_red, b_red, r_green, g_green, b_green, r_blue, g_blue, b_blue):
#     image = Image.open(input_file)
#     image = image.convert('RGBA')

#     width, height = image.size
#     for x in range(width):
#         for y in range(height):
#             r, g, b, a = image.getpixel((x, y))
#             if r >r_red and g < g_red and b < b_red: 
#                 image.putpixel((x, y), (255, 0, 0, 255))
#             elif r <r_green and g > g_green and b < b_green: 
#                 image.putpixel((x, y), (0, 255, 0, 255))
#             elif r <r_blue and g < g_blue and b > b_blue: 
#                 image.putpixel((x, y), (0, 0, 255, 255))
#             else:
#                 max_color = max(r, g, b)
#                 if max_color == r:
#                     image.putpixel((x, y), (255, 0, 0, 255))
#                 elif max_color == g:
#                     image.putpixel((x, y), (0, 255, 0, 255))
#                 else:
#                     image.putpixel((x, y), (0, 0, 255, 255))

#     # save the image with threshold values in the filename
#     image.save(f'{output_file}_r{r_red}_g{g_red}_b{b_red}_rg{r_green}_gg{g_green}_bg{b_green}_rb{r_blue}_gb{g_blue}_bb{b_blue}.png')


# def grid_search(input_file, output_file):
#     r_range = range(0, 255, 40)
#     g_range = range(0, 255, 40)
#     b_range = range(0, 255, 40)

#     for r in r_range:
#         for g in g_range:
#             for b in b_range:
#                 params = (r, g, b, r, g, b, r, g, b)
#                 process_image(input_file, output_file, *params)




org_dir = '../data/generated_imgs/'
counter = 0
for i in os.listdir(org_dir):
    if 'png' in i:
        input_file = '../data/generated_imgs/' + i
        output_file = '../data/color_processed_generated_imgs/' + i
        process_image(input_file, output_file)
        counter +=1

# optimal:
#amazon_1.png_r0_g160_b120_rg0_gg160_bg120_rb0_gb160_bb120.png
#amazon_1.png_r0_g160_b80_rg0_gg160_bg80_rb0_gb160_bb80.png
#r0_g160_b100_rg0_gg160_bg100_rb0_gb160_bb100
