import os
from PIL import Image

def get_date_taken(path):
    return Image.open(path)._getexif()[36867]

def main():
    base_path = '/Volumes/My Passport for Mac/ty_saguaro_project/saguaro_photos'
    for saguaro_folder in os.listdir(base_path):
        if saguaro_folder.startswith('Saguaro'):
            saguaro_num = saguaro_folder.split()[1]
            saguaro_path = os.path.join(base_path, saguaro_folder)
            for year_folder in os.listdir(saguaro_path):
                if os.path.isdir(os.path.join(saguaro_path, year_folder)):
                    year = year_folder.split('_')[1]
                    year_path = os.path.join(saguaro_path, year_folder)
                    counter = {}
                    for file_name in sorted(os.listdir(year_path)):
                        if (file_name.endswith('.jpg') or file_name.endswith('.JPG')) and not file_name.startswith('._'):
                            file_path = os.path.join(year_path, file_name)
                            try:
                                img_date = get_date_taken(file_path)
                                date = '_'.join(img_date.split(':')[:3]).replace(' ', '_')
                                if date not in counter:
                                    counter[date] = 1
                                else:
                                    counter[date] += 1
                                new_name = f'{saguaro_num}_{year}_{date}_{counter[date]}.jpg'
                                os.rename(file_path, os.path.join(year_path, new_name))
                            except Exception as e:
                                print(f'Failed to process file {file_path}: {str(e)}')

if __name__ == "__main__":
    main()

print('done')
