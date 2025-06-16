import os
from datetime import datetime
from dotenv import load_dotenv
import subprocess

load_dotenv()

BACKUP_PATH = os.getenv('BACKUP_PATH', '/backup/')
SERVER = os.getenv('SQL_SERVER', 'MAHSRV')
DATABASE = os.getenv('SQL_DATABASE', 'factorydb')
USER = os.getenv('SQL_USER', 'sa')
PASSWORD = os.getenv('SQL_PASSWORD', '')

os.makedirs(BACKUP_PATH, exist_ok=True)
filename = os.path.join(BACKUP_PATH, f"{DATABASE}_{datetime.now():%Y%m%d}.bak")
cmd = [
    'sqlcmd',
    '-S', SERVER,
    '-U', USER,
    '-P', PASSWORD,
    '-Q', f"BACKUP DATABASE [{DATABASE}] TO DISK='{filename}'"
]
try:
    subprocess.run(cmd, check=True)
except Exception as e:
    print('Backup failed:', e)
