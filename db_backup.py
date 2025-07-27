import dropbox
import os
from datetime import datetime
from dotenv import load_dotenv
from dropbox.exceptions import ApiError

load_dotenv()

def upload_backup():
    db_file_name = "fluency_progress.db"
    db_file_path = os.path.join(os.path.dirname(__file__), db_file_name)
    
    if not os.path.exists(db_file_path):
        raise FileNotFoundError(f"Database file '{db_file_path}' not found!")

    DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
    if not DROPBOX_TOKEN:
        raise ValueError("Dropbox token not set!")

    dbx = dropbox.Dropbox(DROPBOX_TOKEN)

    backup_filename = datetime.now().strftime('fluency_progress_%Y%m%d_%H%M%S.db')

    try:
        with open(db_file_path, "rb") as f:
            dbx.files_upload(
                f.read(),
                f"/FluencyEngineBackups/{backup_filename}",
                mode=dropbox.files.WriteMode.add
            )
        print(f"✅ Database backed up successfully as '{backup_filename}'.")
    except ApiError as e:
        print(f"❌ Dropbox API error: {e}")

if __name__ == "__main__":
    upload_backup()
