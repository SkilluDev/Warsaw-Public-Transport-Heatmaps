from collections import Counter
from genericpath import isfile
from ntpath import join
import os
import json
import matplotlib.pyplot as plt
import numpy as np

def sorttuple(e):
    return e[1]

def plottingStops(data, save=False, name=None):

    s = ""
    if (name):
        s=name

    plt.style.use('Solarize_Light2')

    # Separate the tuples into x and y values
    x_values = [y for x, y in data]

    value_counts = Counter(x_values)
    sumLines = 0;
    print("DATA FOR STOPS: "+s+"---------")
    for x, y in value_counts.items():
        sumLines+=x*y
    print(sumLines/len(data))
    

    newXVal = list(value_counts.keys())
    newYVal = list(value_counts.values())

    for i in range(len(newXVal)):
        print(str(newXVal[i])+" "+str(newYVal[i]))
    if(not save):

        func = lambda x: 2600*np.power(1.55,-(x-1))
        funcx = np.arange(1,21)
        funcy = func(funcx)
        plt.plot(funcx, funcy, color='rebeccapurple',alpha=0.5, zorder=5)
    # Plot the data
    plt.scatter(newXVal, newYVal, c=newXVal, cmap='viridis', edgecolors='black', zorder=10)  # Uses a colormap
    #plt.yscale('log')
    
    # Add labels and title
    plt.xlabel(f'# of {s} lines')
    plt.ylabel('# of stops')
    plt.title(f'Y stops have X {s} lines')
    plt.xticks(newXVal, labels=newXVal)
    #ylabels=[2500,1500,1000, 500, 400, 300, 200, 100, 20]
    #plt.yticks(ylabels, labels=ylabels)
    plt.grid(visible=True,which="both",axis='both')
    if(not save):
        plt.legend([r"$y = 2600 \cdot \left( 1.55^{-\left(x-1\right)} \right)$", 'Data points'])
    else:
        plt.legend(['Data points'])
    # Show the plot
    if(not save):
        plt.show()
    else:
        plt.savefig("docs/AutomatedGraphs/LinesWithZero/"+name+"AutomatedGraphLines.png")
        plt.close()
    return

def plottingSetsOfStops(data):
    plt.style.use('Solarize_Light2')

    # Separate the tuples into x and y values
    x_values = [y for x, y in data]

    value_counts = Counter(x_values)
    sumLines = 0;
    sumStops = 0;
    for x, y in value_counts.items():
        sumLines+=x*y
    print(sumLines/len(data))
    

    newXVal = list(value_counts.keys())
    newYVal = list(value_counts.values())
    
    total=0
    totalSets=0
    for i in range(len(newXVal)):
        print(str(newXVal[i])+" "+str(newYVal[i]))
        totalSets+=newYVal[i]
        total+=newXVal[i]*newYVal[i]
    print("Total stops:" +str(total))
    print("Total Sets of Stops:"+str(totalSets))
    func = lambda x: 1000*np.power(1.8,-(x-1))
    funcx = np.arange(0,22)
    funcy = func(funcx)
    

    # Plot the data
    plt.plot(funcx, funcy, color='rebeccapurple',alpha=0.5, zorder=5)
    plt.scatter(newXVal, newYVal, c=newXVal, cmap='viridis', edgecolors='black', zorder=10)  # Uses a colormap
    #plt.yscale('log')
    
    # Add labels and title
    plt.xlabel('# of stops')
    plt.ylabel('# of Sets of Stops')
    plt.title('Y Sets of Stops consist of X stops')
    plt.xticks(newXVal, labels=newXVal)
    ylabels=[2000, 1000, 500, 400, 300, 200, 100, 20]
    plt.yticks(ylabels, labels=ylabels)
    plt.grid(visible=True,which="both",axis='both')
    plt.legend([r"$y = 1000 \cdot \left( 1.8^{-\left(x-1\right)} \right)$", 'Data points'])
    # Show the plot
    plt.show()
    return

def plottingLinesForSOS(data, save=False, name=None):

    s = ""
    if (name):
        s=name
    plt.style.use('Solarize_Light2')

    # Separate the tuples into x and y values
    x_values = [y for x, y in data]

    value_counts = Counter(x_values)
    sumLines = 0;
    sumStops = 0;
    print("DATA FOR SOS: "+s+"---------")
    for x, y in value_counts.items():
        sumLines+=x*y
    print(sumLines/len(data))
    

    newXVal = list(value_counts.keys())
    newYVal = list(value_counts.values())

    for i in range(len(newXVal)):
        print(str(newXVal[i])+" "+str(newYVal[i]))
    if(not save):
        func = lambda x: 450*np.power(1.3,-(x-1))
        funcx = np.arange(0,61)
        funcy = func(funcx)
        plt.plot(funcx, funcy, color='rebeccapurple',alpha=0.5, zorder=5)
    # Plot the data
    plt.scatter(newXVal, newYVal, c=newXVal, cmap='viridis', edgecolors='black', zorder=10)  # Uses a colormap
    #plt.yscale('log')
    
    # Add labels and title
    plt.xlabel(f'# of {s} lines')
    plt.ylabel('# of Sets of Stops')
    
    plt.title(f'Y Sets of Stops have X {s} lines')
    plt.xticks(newXVal, labels=newXVal, fontsize="small")
    #ylabels=[1000, 500, 400, 300, 200, 100, 20]
    #plt.yticks(ylabels, labels=ylabels)
    plt.grid(visible=True,which="both",axis='both')
    # Show the plot
    if(not save):
        plt.legend([r"$y = 450 \cdot \left( 1.3^{-\left(x-1\right)} \right)$", 'Data points'])
    else:
        plt.legend(['Data points'])
    if(not save):
        plt.show()
    else:
        plt.savefig("docs/AutomatedGraphs/LinesForSOSWithZero/"+name+"AutomatedGraphLinesForSOS.png")
        plt.close()
    return

def plotStops():
    plottingStops(printData("allTypes"))
    return

def plotSetsOfStops():
    plottingSetsOfStops(countStops())
    return

def plotLinesForSOS():
    plottingLinesForSOS(printData("allTypes", complex=True))
    return

def automatePlotting(types):
    for t in types:
        plottingStops(printData(t), save=True, name=t)
        plottingLinesForSOS(printData(t, complex=True), save=True, name=t)
    return

def printData(dataType, complex=False):
    resultData = []
    mypath='jsons/'
    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    previousJ = ""
    currentLines = []
    for j in onlyfiles:
        if(complex and previousJ[6:10]!=j[6:10]):
            resultData.append((previousJ, len(set(currentLines))))
            currentLines=[]
        with open(mypath+j, 'r') as json_file:
            data = json.load(json_file)
        if type(data['result'])!=str:
            for i in data['result']:
                if(dataType=="allTypes"):
                    pass
                elif(dataType=="allD" and i['values'][0]['value'][0]!='N'):
                    pass
                elif(dataType=="tram" and len(i['values'][0]['value'])<3):
                    pass
                elif(dataType=="bus" and len(i['values'][0]['value'])>2):
                    pass
                elif(dataType=="lBus" and i['values'][0]['value'][0]=='L'):
                    pass
                elif(dataType=="exBus" and len(i['values'][0]['value'])>2 and (i['values'][0]['value'][0]=='5' or i['values'][0]['value'][0]=='4')):
                    pass
                elif(dataType=="outBus" and len(i['values'][0]['value'])>2 and (i['values'][0]['value'][0]=='7' or i['values'][0]['value'][0]=='8')):
                    pass
                elif(dataType=="nBus" and i['values'][0]['value'][0]=='N'):
                    pass
                elif(dataType=="dBus" and i['values'][0]['value'][0]!='N' and len(i['values'][0]['value'])>2):
                    pass
                else:
                    continue;
                currentLines.append(i['values'][0]['value'])
            if(not complex):
                resultData.append((j, len(currentLines)))
                currentLines=[]
        previousJ=j
    if(complex):
        resultData.append((previousJ, len(set(currentLines))))
        currentLines=[]
    resultData.sort(key=sorttuple)
    #print("Top 10 for type: "+dataType+" -----------------------------")
    #print(resultData[-10:])
    return resultData

def countStops():
    resultData = []
    mypath='jsons/'
    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    currentSum = 0
    previousJ = ""
    for j in onlyfiles:
        with open(mypath+j, 'r') as json_file:
            data = json.load(json_file)

        if previousJ[6:10]==j[6:10]:
            if type(data['result'])!=str:
                currentSum+=1
        else:
            if previousJ!="":
                resultData.append((previousJ, currentSum))
            currentSum = 1

        previousJ=j
    resultData.append((previousJ, currentSum))
    resultData.sort(key=sorttuple)
    print("Top 10 most stops: "+" -----------------------------")
    print(resultData[-10:])
    return resultData

types = ["allTypes", "bus", "allD", "dBus", "exBus", "lBus", "nBus", "outBus", "tram"]
automatePlotting(["allD"])