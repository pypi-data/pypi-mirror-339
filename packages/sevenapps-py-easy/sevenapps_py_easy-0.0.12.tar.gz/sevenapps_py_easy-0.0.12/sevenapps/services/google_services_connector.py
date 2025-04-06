from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import gspread
from sevenapps.utils.file_manager import *


class GoogleServicesConnector:

    def __init__(self, config, credentials_file_path):
        self.credentials_file_path = credentials_file_path
        self.gspread_client = None
        self.drive_client = None
        self.config = config
        self.init_connection()
    def init_connection(self):
        path_credentials_file = os.path.join(os.getcwd(), self.credentials_file_path)
        scopes = ["https://www.googleapis.com/auth/drive", 'https://spreadsheets.google.com/feeds']
        creds = Credentials.from_service_account_file(path_credentials_file, scopes=scopes)
        self.drive_client = build("drive", "v3", credentials=creds)
        self.gspread_client = gspread.authorize(creds)

    def upload_file_result_to_drive(self, file_path, new_file_name, file_type):
        folder_id = self.config['google_configuration']['drive_folder_id']

        media = MediaFileUpload(file_path, mimetype=file_type)
        file = self.drive_client.files().create(
            body={"name": new_file_name, "parents": [folder_id]},
            media_body=media,
            fields="id"
        ).execute()

        return f"https://drive.google.com/file/d/{file.get('id')}"

    def create_google_spreadsheet_file(self, generated_file_datetime_name):
        folder_id = self.config['google_configuration']['drive_folder_id']
        spreadsheet = self.gspread_client.create(generated_file_datetime_name, folder_id)
        return spreadsheet.id

    def create_google_spreadsheet_file_by_file_template(self, spreadsheet_template_id, file_name):
        target_folder_id = self.config['google_configuration']['drive_folder_id']

        copied_file = self.drive_client.files().copy(
            fileId=spreadsheet_template_id,
            body={'parents': [target_folder_id]}
        ).execute()

        self.drive_client.files().update(fileId=copied_file['id'], body={'name': file_name}).execute()

        return copied_file['id']

    def add_data_to_gsheets(self, spreadsheet_id, data):
        spreadsheet = self.gspread_client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.get_worksheet(0)

        rows = []
        for item in data:
            row = [item["operator"], item["game"], item["isWorking"], item["date"], item["operatorDomain"],
                   item["gameUrl"]]
            rows.append(row)

        range_name = 'A2:F' + str(len(data) + 1)
        worksheet.update(values=rows, range_name=range_name)


