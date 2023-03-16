import pathlib
import re

# mdns-name, numPanels, dmx universe (unused, manually set for now)
import shutil

from data import *

panelBGLength = 235
LEDS_PER_PANEL = 360

MODELS_GENERATED_PATH = 'generated/models.xml'
PANEL_TEMPLATE_PATH = 'templates/layout_model_strip_template.xml'
MINIS_FILE_PATH = 'templates/MINIS_models.xml'
FINAL_PATH_FILE = '../../../../xlights/xlights_rgbeffects.xml'
BACKUP_PATH_FILE = '../../../../xlights/xlights_rgbeffects.xbkp'

t_pos = (float, float, float)


# panelSize_UnscaledX = 0.5
# panelSize_UnscaledY = 1
#
# Hpanel_ScaleX = 0.145
# Hpanel_ScaleY =
# HpanelSize_ScaledX = panelSize_UnscaledX * Hpanel_ScaleX
# HpanelSize_ScaledY = panelSize_UnscaledY * Hpanel_ScaleY
#
# Vpanel_ScaleX = 0.145
# Vpanel_ScaleY =

def main():
    generate_models_template_file()
    print('generated models')
    update_rgbeffects_file()


def update_rgbeffects_file():
    print('test')
    final_path_obj = pathlib.Path(FINAL_PATH_FILE)

    # create backup just in case
    shutil.copyfile(FINAL_PATH_FILE, BACKUP_PATH_FILE)

    with open(MODELS_GENERATED_PATH, 'r') as gen_file:
        generated = gen_file.read()

    allText = final_path_obj.read_text()
    newText = re.sub('<models>.*</models>', f'<models>{generated}</models>', allText, flags=re.DOTALL)
    final_path_obj.write_text(newText, 'utf-8')


def generate_models_template_file():
    model_template = pathlib.Path(PANEL_TEMPLATE_PATH).read_text()
    minis_text = pathlib.Path(MINIS_FILE_PATH).read_text()

    with open(MODELS_GENERATED_PATH, 'w') as file:
        # start with minis
        file.write(minis_text)

        for mdns, num_panels, universe in controller_data_OLD:
            for i in range(num_panels):
                direction, x, y, z = panelData_OLD[mdns][i]
                pos1 = (x, y, z)
                pos2 = get_pos2(direction, *pos1)
                light_num = i + 1

                model_str = generate_model_str(model_template, mdns, light_num, pos1, pos2)
                file.write(model_str)
                file.write('\r\n')


def get_pos2(direction, x1, y1, z1) -> t_pos:
    # lines 2nd coord is relative, so disregard pos1
    delta = panelBGLength
    if direction == L: return -delta, 0, 0
    if direction == R: return +delta, 0, 0
    if direction == U: return 0, +delta, 0
    if direction == D: return 0, -delta, 0

    raise ValueError(f"Unknown direction! ({direction})")


def generate_model_str(template, mdns, light_num, pos1: t_pos, pos2: t_pos):
    start_channel = LEDS_PER_PANEL * 3 * (light_num - 1) + 1  # 1, 1081, 2061, 3240

    replacements = [('<MDNS>', mdns),
                    ('<LIGHTNUM>', light_num),
                    ('<StartChannel>', start_channel),

                    ('<PosX>', pos1[0]),
                    ('<PosY>', pos1[1]),
                    ('<PosZ>', pos1[2]),

                    ('<PosX2>', pos2[0]),
                    ('<PosY2>', pos2[1]),
                    ('<PosZ2>', pos2[2]),
                    ]

    for orig, new in replacements:
        template = template.replace(orig, str(new))
    return template


if __name__ == "__main__":
    main()
