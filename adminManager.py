import json
from pathlib import Path

adminDataFile = Path('adminData.json')

with open(adminDataFile, encoding="UTF-8") as f:
    adminData = json.load(f)

def getAdminUserIDs():
    return adminData['user-ids']