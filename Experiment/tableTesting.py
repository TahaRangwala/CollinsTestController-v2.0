import plotly.graph_objects as go 
 
fig = go.Figure(data=[go.Table( 
  header=dict( 
    values=['Frequency', 'Input Power 1dB Compression Point'], 
    line_color='darkslategray',
    fill_color='lightcyan', 
    align=['left','center'], 
    font=dict(color='black', size=12) 
  ), 
  cells=dict( 
    values=[ 
      [1200000, 20000, 80000, 2000, 12120000], 
      [1200000, 20000, 80000, 2000, 12120000]], 
    line_color='darkslategray',
    fill_color='lightcyan', 
    align = ['left', 'center'], 
    font = dict(color = 'darkslategray', size = 11) 
    )) 
]) 
 
fig.show()