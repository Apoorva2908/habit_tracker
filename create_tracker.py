import xlsxwriter
import pandas as pd
from datetime import datetime, timedelta

start = datetime.today()
end = datetime(2026,5,31)

dates=[]
d=start
while d<=end:
    dates.append(d)
    d+=timedelta(days=1)

df=pd.DataFrame({
"Date":dates,
"Study":[0]*len(dates),
"Workout":[0]*len(dates),
"Medicine":[0]*len(dates)
})

workbook=xlsxwriter.Workbook("Life_Tracker.xlsx")
sheet=workbook.add_worksheet("Daily Tracker")
dash=workbook.add_worksheet("Dashboard")

header=workbook.add_format({'bold':True,'align':'center','bg_color':'#D9E1F2'})
percent=workbook.add_format({'num_format':'0%'})
center=workbook.add_format({'align':'center'})

headers=["Date","Study","Workout","Medicine","Score","Streak"]

for i,h in enumerate(headers):
    sheet.write(0,i,h,header)

for r,row in enumerate(df.itertuples(),1):
    sheet.write(r,0,row.Date.strftime("%Y-%m-%d"))

    sheet.write_boolean(r,1,False)
    sheet.write_boolean(r,2,False)
    sheet.write_boolean(r,3,False)

    sheet.write_formula(r,4,f"=COUNTIF(B{r+1}:D{r+1},TRUE)/3",percent)

    if r==1:
        sheet.write_formula(r,5,f"=IF(E{r+1}=1,1,0)")
    else:
        sheet.write_formula(r,5,f"=IF(E{r+1}=1,F{r}+1,0)")

sheet.set_column("A:A",15)
sheet.set_column("B:D",10)
sheet.set_column("E:F",12)

sheet.conditional_format(f"E2:E{len(df)+1}",{
'type':'3_color_scale',
'min_color':"#F8696B",
'mid_color':"#FFEB84",
'max_color':"#63BE7B"
})

sheet.conditional_format(f"F2:F{len(df)+1}",{
'type':'data_bar',
'bar_color':'#4CAF50'
})

dash.write("A1","Life Progress Dashboard",header)

dash.write("A3","Overall Progress")
dash.write_formula("B3",f"=AVERAGE('Daily Tracker'!E2:E{len(df)+1})",percent)

dash.write("A5","Days Remaining")

dash.write_formula("B5","=DATE(2026,5,31)-TODAY()")

dash.write("A7","Best Streak")
dash.write_formula("B7",f"=MAX('Daily Tracker'!F2:F{len(df)+1})")

chart=workbook.add_chart({'type':'line'})

chart.add_series({
'name':'Daily Score',
'categories':f"'Daily Tracker'!A2:A{len(df)+1}",
'values':f"'Daily Tracker'!E2:E{len(df)+1}",
})

chart.set_title({'name':'Daily Progress'})
chart.set_x_axis({'name':'Date'})
chart.set_y_axis({'name':'Score'})

dash.insert_chart("D2",chart)

workbook.close()

print("Tracker created: Life_Tracker.xlsx")