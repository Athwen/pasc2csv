import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import sys


def xml_to_csv(path):
    xml_list = []

    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for member in root.findall('object'):
            bbx = member.find('bndbox')
            xmin = int(bbx.find('xmin').text)
            ymin = int(bbx.find('ymin').text)
            xmax = int(bbx.find('xmax').text)
            ymax = int(bbx.find('ymax').text)
            label = member.find('name').text

            value = (root.find('filename').text,
                     xmin,
                     ymin,
                     xmax,
                     ymax,
                     label
                     )

            xml_list.append(value)
    column_name = ['filename', 'xmin', 'ymin', 'xmax', 'ymax', 'class']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main(path):
    xml_df = xml_to_csv(path)
    xml_df.to_csv('labels_csv.csv', index=None, header=False)
    print('Successfully converted xml to csv.')


folder_path = sys.argv[1]
print(folder_path)

if (os.path.isdir(folder_path)):
    main(folder_path)
else:
    print("Pass a valid directory")
