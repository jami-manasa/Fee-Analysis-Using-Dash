import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.4) pip install plotly==4.5.4
import plotly.express as px

import dash             #(version 1.9.1) pip install dash==1.9.1
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()
app
df= pd.read_excel("WorkingMasterdata.xlsx")
dff = df.groupby('Programme', as_index=False)[['Amount Paid','Amount Pending']].sum()
print(dff)
PAGE_SIZE = 5

app.layout =html.Div([



html.Div([dash_table.DataTable(
    id='datatable-paging',
    columns=[
        {"name": i, "id": i} for i in sorted(df.columns)
    ],
    page_current=0,
    page_size=PAGE_SIZE,
    page_action='custom'
)],className='six columns'),



    html.Div([
    html.Div([
    html.Div([
        dcc.Dropdown(id='campusdropdown',
            options=[
                     {'label': 'PKD', 'value': 'PKD'},
                     {'label': 'BBSR', 'value': 'BBSR'},
                     {'label': 'VSKP', 'value': 'VSKP'}
                     
            ],
             placeholder="Select The Campus",
            value=["PKD","BBSR","VSKP"],
            multi=True,
                     style={
    'height': '10%', 
    'width': '60%', 
    'font-size': "100%",
    'display': 'inline-block', 'padding': '10px',
   
    
    },
        ),
        ],className='six columns'),

         html.Div([
        dcc.Dropdown(id='semdropdown',
            options=[
                     {'label': 'starting semister', 'value': 'During Start of Academics'},
                     {'label': 'end semister', 'value': 'During start of odd Semester'}
            ],
             placeholder="Select any Semister",
            value=['During Start of Academics', 'During start of odd Semester'],
            multi=True,
            clearable=False,
                     style={
    'height': '10%', 
    'width': '60%', 
    'font-size': "100%",
    'display': 'inline-block', 'padding': '10px',
     'float': 'right','margin': '-40px',"marginRight": "20px"
    
    },
        ),
        ],className='six columns'),


    html.Div([
        dcc.Dropdown(id='schdropdown',
            options=[
                     {'label': 'SCHOOL OF MANAGEMENT', 'value': 'SoM'},
                     {'label': 'SCHOOL OF AGRICULTURE & BIO-ENGINEERING', 'value': 'SOABE'}
            ],
             placeholder="Select any School",
            value=["SoM","SOABE"],
            multi=True,
            clearable=False,
                     style={
    'height': '10%', 
    'width': '60%', 
    'font-size': "100%",
    'display': 'inline-block', 'padding': '10px'
    
    },
        ),
        ],className='six columns'),


    html.Div([
        dcc.Dropdown(id='Progdropdown',
            options=[
                     {'label': 'BBA', 'value': 'BBA'},
                     {'label': 'B.TECH. AG.', 'value': 'B.TECH. AG.'},
                     {'label': 'B.TECH.Dairy', 'value': 'B.TECH.Dairy'}],
             placeholder="Select any Programme",
            value=["BBA","B.TECH. AG.","B.TECH.Dairy"],
            multi=True,
            clearable=False,style={
    'height': '10%', 
    'width': '60%', 
    'font-size': "100%",
    'display': 'inline-block', 'padding': '10px',
    'display': 'inline-block', 'padding': '10px',
     'float': 'right','margin': '-40px',"marginRight": "20px"
    
    },
        ),
        ],className='six columns'),

    html.Div([
        dcc.Dropdown(id='amountdropdown',
            options=[
                     {'label': 'Amount Paid', 'value': 'Amount Paid'},
                     {'label': 'Amount Pending', 'value': 'Amount Pending'}],
            placeholder="Select your Requirement",
            value='Amount Paid',
            multi=False,
            clearable=False,
                     style={
    'height': '10%', 
    'width': '60%', 
    'font-size': "100%",
    'display': 'inline-block', 'padding': '10px',
    
    },
        ),
        ],className='six columns'),






    

    ],className='row'),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='barchart'),
        ],className='six columns'),

    ],className='row')


])
######################################################################
@app.callback(
   Output('barchart', 'figure'),
    [Input('campusdropdown', 'value'),
     Input('semdropdown', 'value'),
     Input('schdropdown', 'value'),
     Input('Progdropdown', 'value'),
     Input('amountdropdown', 'value')]
)
def update_data(campusdropval,semdropval,schdropval,Progdropval,amountdropval):
    print(campusdropval)
    df_filterd = df[df["Campus"].isin(campusdropval)]
    df_filterd = df_filterd[df_filterd["Fee Collection Checkpoint"].isin(semdropval)]
    print( df_filterd)
    df_filterd = df_filterd[df_filterd["School"].isin(schdropval)]
    df_filterd = df_filterd[df_filterd["Programme"].isin(Progdropval)]

##    df = px.data.tips()
##    pie_chart=px.pie(df, values='tip', names='day')
    bar_chart=px.bar(
            data_frame=df_filterd,
            x="Programme",
            y=amountdropval,
            labels={'Programme':'Programme'}
            )
   
    
    return (bar_chart)
@app.callback(
    Output('datatable-paging', 'data'),
    [Input('datatable-paging', "page_current"),
     Input('datatable-paging', "page_size")])
def update_table(page_current,page_size):
    return df.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=False,use_reloader=False)












