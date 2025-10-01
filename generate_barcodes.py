import pandas as pd

CODE128B_CHAR_MAP = {
    ' ': 0, '!': 1, '"': 2, '#': 3, '$': 4, '%': 5, '&': 6, "'": 7,
    '(': 8, ')': 9, '*': 10, '+': 11, ',': 12, '-': 13, '.': 14, '/': 15,
    '0': 16, '1': 17, '2': 18, '3': 19, '4': 20, '5': 21, '6': 22, '7': 23,
    '8': 24, '9': 25, ':': 26, ';': 27, '<': 28, '=': 29, '>': 30, '?': 31,
    '@': 32, 'A': 33, 'B': 34, 'C': 35, 'D': 36, 'E': 37, 'F': 38, 'G': 39,
    'H': 40, 'I': 41, 'J': 42, 'K': 43, 'L': 44, 'M': 45, 'N': 46, 'O': 47,
    'P': 48, 'Q': 49, 'R': 50, 'S': 51, 'T': 52, 'U': 53, 'V': 54, 'W': 55,
    'X': 56, 'Y': 57, 'Z': 58, '[': 59, '\\': 60, ']': 61, '^': 62, '_': 63,
    '`': 64, 'a': 65, 'b': 66, 'c': 67, 'd': 68, 'e': 69, 'f': 70, 'g': 71,
    'h': 72, 'i': 73, 'j': 74, 'k': 75, 'l': 76, 'm': 77, 'n': 78, 'o': 79,
    'p': 80, 'q': 81, 'r': 82, 's': 83, 't': 84, 'u': 85, 'v': 86, 'w': 87,
    'x': 88, 'y': 89, 'z': 90, '{': 91, '|': 92, '}': 93, '~': 94,
}

CODE128_PATTERNS = [
    "212222", "222122", "222221", "121223", "121322", "131222", "122213",
    "122312", "132212", "221213", "221312", "231212", "112232", "122132",
    "122231", "113222", "123122", "123221", "223211", "221132", "221231",
    "213212", "223112", "312131", "311222", "321122", "321221", "312212",
    "322112", "322211", "212123", "212321", "232121", "111323", "131123",
    "131321", "112313", "132113", "132311", "211313", "231113", "231311",
    "112133", "112331", "132131", "113123", "113321", "133121", "313121",
    "211331", "231131", "213113", "213311", "213131", "311123", "311321",
    "331121", "312113", "312311", "332111", "314111", "221411", "431111",
    "111224", "111422", "121124", "121421", "141122", "141221", "112214",
    "112412", "122114", "122411", "142112", "142211", "241211", "221114",
    "413111", "241112", "134111", "111242", "121142", "121241", "114212",
    "124112", "124211", "411212", "421112", "421211", "212141", "214121",
    "412121", "111143", "111341", "131141", "114113", "114311", "411113",
    "411311", "113141", "114131", "311141", "411131", "211412", "211214",
    "211232", "2331112"
]

START_B_VAL = 104
STOP_VAL = 106

def generate_pure_code128b(data, filename="barcode.svg"):
    """
    Generates a Code128 barcode using only the B subset and saves it as an SVG.

    Args:
        data (str): The string data to encode. Must contain only Code128B chars.
        filename (str): The name of the output SVG file.
    """
    # Encode data to Code128B values
    char_values = []
    for char in data:
        if char not in CODE128B_CHAR_MAP:
            raise ValueError(f"Character '{char}' is not valid in Code128B.")
        char_values.append(CODE128B_CHAR_MAP[char.lower() if char in '`abcdefghijklmnopqrstuvwxyz' else char])

    checksum_sum = START_B_VAL
    for i, value in enumerate(char_values):
        checksum_sum += value * (i + 1)
    
    checksum_val = checksum_sum % 103
    all_values = [START_B_VAL] + char_values + [checksum_val]
    all_patterns = [CODE128_PATTERNS[val] for val in all_values]
    full_pattern_str = "".join(all_patterns) + CODE128_PATTERNS[STOP_VAL]
    
    # Generate the SVG
    bar_unit_width = 3  # Width of the narrowest bar/space in pixels
    height = 100        # Height of the barcode in pixels
    
    svg_parts = []
    current_x = 0
    is_bar = True  # The first digit always represents a bar

    for width_char in full_pattern_str:
        width = int(width_char) * bar_unit_width
        if is_bar:
            svg_parts.append(
                f'<rect x="{current_x}" y="0" width="{width}" height="{height}" fill="#000000" />'
            )
        current_x += width
        is_bar = not is_bar

    total_width = current_x
    
    # Add a quiet zone (padding) on the left and right
    quiet_zone = 10 * bar_unit_width
    final_width = total_width + (2 * quiet_zone)

    svg_content = f'''
<svg xmlns="http://www.w3.org/2000/svg" width="{final_width}" height="{height}" version="1.1">
    <rect x="0" y="0" width="{final_width}" height="{height}" fill="#FFFFFF"/>
    <g transform="translate({quiet_zone}, 0)">
        {''.join(svg_parts)}
    </g>
</svg>
    '''.strip()

    # Write to file
    try:
        with open(filename, 'w') as f:
            f.write(svg_content)
    except IOError as e:
        print(f"Error writing to {filename}: {e}")


card_df = pd.read_csv('card_info.csv')

for index, row in card_df.iterrows():
    id = row['Card Number']
    card_name = row['Card Name'].replace(' ', '_').replace(':', '_').replace('(', '').replace(')', '')
    barcode_data = row['Barcode Data']
    target_image = './barcode_images/%03d_%s_%s.svg' % (id, card_name, barcode_data)
    generate_pure_code128b(barcode_data, target_image)
