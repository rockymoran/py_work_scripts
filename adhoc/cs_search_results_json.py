import requests
import pandas as pd
from pandas.io.json import json_normalize
import json
import plotly as py
import plotly.figure_factory as ff
import config
import plotly.graph_objs as go

username = config.username
password = config.password

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

columns = ['Schedule_ID', 'Course', 'Rm',  'Dates', 'DualListPrimary', 'Dual']
gantt_columns = ['Schedule_ID', 'Start', 'Finish', 'Room', 'Days']

login_url = 'https://api.haas.berkeley.edu/Account/Login'
search_url = 'https://api.haas.berkeley.edu/Search/JsonRefreshSearchGrid'
search_results = 'https://api.haas.berkeley.edu/Account/GetSecurityLevel?strCtrlID=CourseSchedGrid'

with requests.Session() as s:
    p = s.post(login_url, payload)
    r = json_normalize(json.loads(s.get(url=search_url, params=search_model_params).text))
    df = pd.DataFrame.from_dict(r, orient='columns')[columns]
    df = df.drop(df[(df['Dual']) & (~df['DualListPrimary'])].index)
    df['Schedule_ID'] = df['Schedule_ID'].apply(str)
    Rm_split = df['Rm'].str.split(n=0, expand=True)
    time_split = Rm_split[1].str.split('-', n=0, expand=True)
    df['Days'] = Rm_split[0]
    df['Start'] = time_split[0]
    df['Finish'] = time_split[1]
    df['Room'] = Rm_split[2]
    df['Start'] = pd.to_datetime(df['Start'])
    df['Finish'] = pd.to_datetime(df['Finish'])
    df_gantt = df[gantt_columns]
    df_gantt.rename(columns={'Schedule_ID': 'Task'}, inplace=True)
    df_gantt.rename(columns={'Room': 'Resource'}, inplace=True)
    df_gantt.drop_duplicates(inplace=True)
    df_gantt.dropna(inplace=True)
    df_mini = df_gantt.loc[(df_gantt['Resource'] == 'C125') & (df_gantt['Days'] == 'T')]
    fig = ff.create_gantt(df_mini.reset_index(drop=True), index_col='Resource', title='Dog Chart Woof',
                          showgrid_x=True, showgrid_y=True)
    py.offline.plot(fig, auto_open=True)
