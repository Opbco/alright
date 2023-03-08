import os
from alright import WhatsApp
from datetime import date


today = date.today()
pdf_folder_path = os.path.join(os.getcwd(), 'pdf_files')

files_name = os.listdir(pdf_folder_path)

messenger = WhatsApp()
numbers = ['237677979923', '237675469030', '237679117011']
i = 0
for file_name in files_name:
    file_path = f'{pdf_folder_path}/{file_name}'
    messenger.find_user(numbers[i])
    if messenger.send_file(file_path):
        os.remove(file_path)
        messenger.send_message(f'{file_name[9:-4]} send to {file_name[:8]} on the {today}')
    i+=1