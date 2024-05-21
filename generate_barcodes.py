import pandas as pd
import code128

card_df = pd.read_csv('card_info.csv')

for index, row in card_df.iterrows():
    id = row['Card Number']
    card_name = row['Card Name'].replace(' ', '_').replace(':', '_').replace('(', '').replace(')', '')
    barcode_data = row['Barcode Data']
    target_image = './barcode_images/%03d_%s_%s.png' % (id, card_name, barcode_data)
    code128.image(barcode_data).save(target_image)
