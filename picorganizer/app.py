import datetime
from os import listdir
import os.path
import shutil
import sys
import piexif

def main():
    if len(sys.argv) !=3:
        print('This programs needs exactly two args. Please, provide origin and destination folder.')
        exit(1)
    origin = sys.argv[1]
    destination = sys.argv[2]
    print('Moving images from' + origin + ' to ' + destination)
    files = get_file_list(origin)
    move_files(files, destination)

def get_file_list(folder):
    files = []
    for file in listdir(folder):
        if os.path.isfile(os.path.join(folder, file)):
            files.append(os.path.join(folder, file))
    return files

def move_files(files, folder):  
    for file in files:
        extension = file.split('.')[-1].lower()
        if extension in ['jpg', 'tiff']:
            try:
                exif_dict = piexif.load(file)
            except:
                print("Can't read exif data from %s" % file)
            else:
                for ifd in ("0th", "Exif", "GPS", "1st"):
                    for tag in exif_dict[ifd]:
                        if piexif.TAGS[ifd][tag]["name"] == 'DateTimeOriginal':
                            image_datetime = datetime.datetime.strptime(exif_dict[ifd][tag].decode("utf-8"), "%Y:%m:%d %H:%M:%S")
                            year_folder = os.path.join(folder + os.sep + str(image_datetime.year))
                            month_folder = os.path.join(year_folder + os.sep + str(image_datetime.strftime('%m')))
                            if not os.path.exists(year_folder):
                                try:  
                                    os.mkdir(year_folder)
                                except OSError:  
                                    print ("Creation of the directory %s failed" % month_folder)
                                else:  
                                    print ("Successfully created the directory %s " % month_folder)
                            if not os.path.exists(month_folder):
                                try:  
                                    os.mkdir(month_folder)
                                except OSError:  
                                    print("Creation of the directory %s failed" % month_folder)
                                else:  
                                    print("Successfully created the directory %s " % month_folder)

                            if os.path.exists(month_folder):
                                file_name = os.path.basename(file)
                                try:
                                    shutil.move(file, os.path.join(month_folder, file_name))
                                except OSError:
                                    print("It is not possible to move %s" % file_name)
                                else:  
                                    print("Successfully moved %s " % file_name)

if __name__ == '__main__':
    main()