def textwidth(text, fontsize=14):
    try:
        import cairo
    except Exception as e:
        return len(text) * fontsize
    surface = cairo.SVGSurface('temp.svg', 1280, 200)
    cr = cairo.Context(surface)
    cr.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(fontsize)
    xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
    return width
