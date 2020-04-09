from PIL import Image, ImageDraw


def circle_in(longi, lat):
    im = Image.open('resources/mapwithgrid.png')
    #im = Image.open('draw.jpg')
    draw = ImageDraw.Draw(im)

    width, height = im.size
    w_factor = width/360
    h_factor = height/180

    print(width)
    print(height)

    print(f'w_factor {w_factor}')
    print(f'h_factor {h_factor}')

    longi = longi
    lat = lat * -1

    absXNull = 450
    absYNull = 222

    #absXNull = 641
    #absYNull = 362

    x = absXNull + (longi * w_factor)
    y = absYNull + (lat * h_factor)

    print(f'x; {x}')
    print(f'y; {y}')

    #draw.ellipse((636, 357, 646, 367), outline ='blue')
    draw.ellipse((x-5, y-5, x+5, y+5), outline ='red')

    im.save('mapwithdot.jpg', quality=95)
    return "mapwithdot.jpg"
