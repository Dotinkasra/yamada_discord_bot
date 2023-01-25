from tkinter import Image
from discord.ext import commands
import requests, os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class ImageCatcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gdrive = GoogleDriveFacade()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : ImageCatcher')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.attachments is None:
            return

        for a in message.attachments:
            locally_saved_file = self.save_img(
                name = a.filename, 
                url = a.url
            )
            self.gdrive.upload(
                local_file_path = locally_saved_file,
                save_folder_name = "サーバー"
            )
            os.remove(locally_saved_file)

    def save_img(self, name: str, url: str):
        with open(f'data/{name}', "wb") as f:
            f.write(requests.get(url).content)
        return f"data/{name}"

def setup(bot):
    return bot.add_cog(ImageCatcher(bot))

class GoogleDriveFacade:
    def __init__(self, setting_path: str = 'settings.yaml'):
        gauth = GoogleAuth(setting_path)
        gauth.LocalWebserverAuth()

        self.drive = GoogleDrive(gauth)

    def create_folder(self, folder_name):
        ret = self.check_files(folder_name)
        if ret:
            folder = ret
        else:
            folder = self.drive.CreateFile(
                {
                    'title': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                }
            )
            folder.Upload()
        return folder

    def check_files(self, folder_name):
        query = f'title = "{os.path.basename(folder_name)}"'

        list = self.drive.ListFile({'q': query}).GetList()
        if len(list)> 0:
            return list[0]
        return False

    def upload(self, 
               local_file_path: str,
               save_folder_name: str = 'sample'
        ):
        
        if save_folder_name:
            folder = self.create_folder(save_folder_name)
        file = self.drive.CreateFile(
            {
                'parents': [
                    {'id': folder["id"]}
                ]
            }
        )
        file.SetContentFile(local_file_path)
        file['title'] = os.path.basename(local_file_path)
        print(file)
        file.Upload()
        
        drive_url = f"https://drive.google.com/uc?id={str( file['id'] )}" 
        return drive_url
    
    def get_file_list(self):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
