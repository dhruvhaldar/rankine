def luminance(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def adjust(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

def contrast(c1, c2):
    l1 = luminance(c1)
    l2 = luminance(c2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

print("Contrast #28a745 vs #ffffff:", contrast('28a745', 'ffffff'))
print("Contrast #6c757d vs #ffffff:", contrast('6c757d', 'ffffff'))
print("Contrast #005bb5 vs #ffffff:", contrast('005bb5', 'ffffff'))
print("Contrast #d32f2f vs #ffffff:", contrast('d32f2f', 'ffffff'))
