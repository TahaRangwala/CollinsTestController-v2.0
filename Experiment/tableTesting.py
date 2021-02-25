from prettytable import PrettyTable
import plotly.graph_objects as go

# Specify the Column Names while initializing the Table 
myTable = PrettyTable(["Student Name", "Class", "Section", "Percentage"])

# Add rows 
myTable.add_row(["Leanord", "X", "B", "91.2 %"])
print(myTable)
myTable.add_row(["Penny", "X", "C", "63.5 %"])
print(myTable)
myTable.add_row(["Howard", "X", "A", "90.23 %"])
myTable.add_row(["Bernadette", "X", "D", "92.7 %"])
myTable.add_row(["Sheldon", "X", "A", "98.2 %"])
myTable.add_row(["Raj", "X", "B", "88.1 %"])
myTable.add_row(["Amy", "X", "B", "95.0 %"])

theString = "23MHZ"
theNum = ""
for i in range(len(theString)):
    
    currentVal = theString[i]
    if(str(currentVal).isdigit()):
        theNum = theNum + str(currentVal)
    else:
        break

print(int(theNum))