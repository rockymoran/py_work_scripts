import requests
import getpass
import pandas as pd
from pandas.io.json import json_normalize
import json

# in order for getpass to work, pycharm MUST be set up as follows:
# Run -> Edit Configurations -> Execution -> Emulate terminal in output console
# password = getpass.getpass()
username = 'rocky_moran'
password = ''

sem = 'Fall'
year = '2019'
sem_year = 'Fall 2019'

search_model_params = {
    'searchModel.selectedSemester': sem,
    'searchModel.selectedYear': year,
    'searchModel.selectedInstructorName': '',
    'searchModel.selectedRoomName': '',
    'searchModel.bExcel': False,
    'searchModel.SortBy': '',
    'searchModel.selectedTerm_input': sem_year,
    'searchModel.selectedTerm': sem_year,
    'searchModel.CCN': '',
    'searchModel.selectedCourseTitle_input': '',
    'searchModel.selectedCourseTitle': '',
    'searchModel.selectedCourseNo_input': '',
    'searchModel.selectedCourseNo': '',
    'searchModel.selectedInstructor_input': '',
    'searchModel.selectedInstructor': '',
    'searchModel.Topics': 'false',
    'searchModel.selectedProgram_input': '',
    'searchModel.selectedProgram': '',
    'searchModel.selectedClassroom_input': '',
    'searchModel.selectedClassroom': '',
    'searchModel.DualListPrimary': 'false',
    'searchModel.selectedGroup_input': '',
    'searchModel.selectedGroup': '',
    'searchModel.Schedule_ID': '',
    'searchModel.Cancelled': 'false',
    'searchModel.selectedType_input': '',
    'searchModel.selectedType': '',
    'searchModel.StartDateFrom': '',
    'searchModel.StartDateTo': '',
    'searchModel.selectedDay_input': '',
    'searchModel.selectedDay': '',
    'searchModel.EndDateFrom': '',
    'searchModel.EndDateTo': ''
}

payload = {
    'UserName': username,
    'Password': password
}

login_url = 'https://api.haas.berkeley.edu/Account/Login'
search_url = 'https://api.haas.berkeley.edu/Search/JsonRefreshSearchGrid'
search_results = 'https://api.haas.berkeley.edu/Account/GetSecurityLevel?strCtrlID=CourseSchedGrid'

with requests.Session() as s:
    p = s.post(login_url, payload)
    r = s.get(url = search_url, params = search_model_params)
    r = json.loads(r.text)
    df = pd.DataFrame.from_dict(json_normalize(r), orient='columns')
    print(df.head())
    print(list(df))
    print(df['Rm'])
