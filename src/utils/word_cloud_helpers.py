import json
from datetime import datetime
import random

import stylecloud as sc

from config import Settings

list_style_pallete_color = [
    "Blues_3",
    "Blues_4",
    "Blues_5",
    "Blues_6",
    "Blues_7",
    "Blues_8",
    "Blues_9",
    "BuGn_3",
    "BuGn_4",
    "BuGn_5",
    "BuGn_6",
    "BuGn_7",
    "BuGn_8",
    "BuGn_9",
    "BuPu_3",
    "BuPu_4",
    "BuPu_5",
    "BuPu_6",
    "BuPu_7",
    "BuPu_8",
    "BuPu_9",
    "GnBu_3",
    "GnBu_4",
    "GnBu_5",
    "GnBu_6",
    "GnBu_7",
    "GnBu_8",
    "GnBu_9",
    "Greens_3",
    "Greens_4",
    "Greens_5",
    "Greens_6",
    "Greens_7",
    "Greens_8",
    "Greens_9",
    "Greys_3",
    "Greys_4",
    "Greys_5",
    "Greys_6",
    "Greys_7",
    "Greys_8",
    "Greys_9",
    "OrRd_3",
    "OrRd_4",
    "OrRd_5",
    "OrRd_6",
    "OrRd_7",
    "OrRd_8",
    "OrRd_9",
    "Oranges_3",
    "Oranges_4",
    "Oranges_5",
    "Oranges_6",
    "Oranges_7",
    "Oranges_8",
    "Oranges_9",
    "PuBu_3",
    "PuBu_4",
    "PuBu_5",
    "PuBu_6",
    "PuBu_7",
    "PuBu_8",
    "PuBu_9",
    "PuBuGn_3",
    "PuBuGn_4",
    "PuBuGn_5",
    "PuBuGn_6",
    "PuBuGn_7",
    "PuBuGn_8",
    "PuBuGn_9",
    "PuRd_3",
    "PuRd_4",
    "PuRd_5",
    "PuRd_6",
    "PuRd_7",
    "PuRd_8",
    "PuRd_9",
    "Purples_3",
    "Purples_4",
    "Purples_5",
    "Purples_6",
    "Purples_7",
    "Purples_8",
    "Purples_9",
    "RdPu_3",
    "RdPu_4",
    "RdPu_5",
    "RdPu_6",
    "RdPu_7",
    "RdPu_8",
    "RdPu_9",
    "Reds_3",
    "Reds_4",
    "Reds_5",
    "Reds_6",
    "Reds_7",
    "Reds_8",
    "Reds_9",
    "YlGn_3",
    "YlGn_4",
    "YlGn_5",
    "YlGn_6",
    "YlGn_7",
    "YlGn_8",
    "YlGn_9",
    "YlGnBu_3",
    "YlGnBu_4",
    "YlGnBu_5",
    "YlGnBu_6",
    "YlGnBu_7",
    "YlGnBu_8",
    "YlGnBu_9",
    "YlOrBr_3",
    "YlOrBr_4",
    "YlOrBr_5",
    "YlOrBr_6",
    "YlOrBr_7",
    "YlOrBr_8",
    "YlOrBr_9",
    "YlOrRd_3",
    "YlOrRd_4",
    "YlOrRd_5",
    "YlOrRd_6",
    "YlOrRd_7",
    "YlOrRd_8",
    "YlOrRd_9",
]

def get_random_icon_name():
    # read the assets, and get random icon name
    file = f'{Settings.ROOT_DIR}/assets/fontawesome-icons-with-categories.json'

    with open(file) as json_file:
        data = json.load(json_file)

        category_index = random.randint(0, len(data) - 1)
        list_key = [k for k in data.keys()]
        icon_list_name = data[list_key[category_index]]
        icon_index = random.randint(0, len(icon_list_name) - 1)

        return data[list_key[category_index]][icon_index]


def generate_word_cloud(text_format: str):
    # generated word clouds
    suffix = datetime.now().strftime("%y%m%d_%H%M%S")
    filename = f"cloud_word_{suffix}"
    output_name = f'{Settings.ROOT_DIR}/assets/{filename}.png'
    gradient_list = ['horizontal', 'vertical']

    # generate sc
    sc.gen_stylecloud(
        text=text_format,
        palette=f'colorbrewer.sequential.{list_style_pallete_color[random.randint(0, len(list_style_pallete_color)-1)]}',
        font_path=f'{Settings.ROOT_DIR}/assets/OpenSans-SemiBold.ttf',
        icon_name=get_random_icon_name(),  # with random icon name
        output_name=output_name,
        gradient=gradient_list[random.randint(0, 1)],
        custom_stopwords=['UV', 'Currently', 'location', 'h', 'C', 'km', 'weather', 'also', 'are', 'and'],
    )

    return output_name
