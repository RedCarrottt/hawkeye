def textwidth(text, fontsize=14):
    try:
        import cairo
        import os
    except Exception as e:
        return len(text) * fontsize
    temp_filename = '.temp.svg'
    surface = cairo.SVGSurface(temp_filename, 1280, 200)
    cr = cairo.Context(surface)
    cr.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(fontsize)
    xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
    os.remove(temp_filename)
    return width
