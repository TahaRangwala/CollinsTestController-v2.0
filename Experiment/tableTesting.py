
"""
import plotly.graph_objects as go 
 
headerColor = 'grey' 
rowEvenColor = 'lightgrey' 
rowOddColor = 'white' 
 
fig = go.Figure(data=[go.Table( 
  header=dict( 
    values=['<b> </b>','<b>1</b>','<b>2</b>','<b>3</b>','<b>4</b>', '<b>5</b>'], 
    line_color='darkslategray', 
    fill_color=headerColor, 
    align=['left','center'], 
    font=dict(color='white', size=12) 
  ), 
  cells=dict( 
    values=[ 
      ['<b>1</b>','<b>2</b>','<b>3</b>','<b>4</b>', '<b>5</b>'], 
      [1200000, 20000, 80000, 2000, 12120000], 
      [1300000, 20000, 70000, 2000, 130902000], 
      [1300000, 20000, 120000, 2000, 131222000], 
      [1400000, 20000, 90000, 2000, 14102000],
      [1,1,1,1,1]], 
    line_color='darkslategray', 
    fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5], 
    align = ['left', 'center'], 
    font = dict(color = 'darkslategray', size = 11) 
    )) 
]) 
 
fig.show()"""
def closest(lst, K):        
    return int(lst.index(lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]))
       
# Driver code  
lst = [150030000, 150020000, 150001000, 150020000, 150100000, 150000001]  
K = 150000000
print(closest(lst, K)) 