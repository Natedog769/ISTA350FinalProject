'''
    Nate Mendoza
    Ista350
    SL Stephen

    For my final project I am making 4 images 
    one of unemployment data web scrape
    one of min wages web scape
    one of average wages csv
    one of the housing data csv data


'''
import pandas as pd, numpy as np, matplotlib.pyplot as plt, math
import statsmodels.api as sm, datetime as dt

min_income_csv = 'MinimumWageData.csv'

unEmUrl1 = 'https://www.ncsl.org/research/labor-and-employment/national-employment-monthly-update.aspx#:~:text=The%20national%20unemployment%20rate%20decreased,rates%20can%20be%20found%20here.'


def get_and_display_Unemployement_data():
    
    #we are getting data about un employment
    data = pd.read_html(unEmUrl1, index_col=0, na_values=0)[0]

    # need to fix the NaNs with 0
    for i in data.index:
        for j in data.columns:
            if math.isnan(data.loc[i][j]):
                data.loc[i][j] = 0
    #lets grab the columns
    months = data.columns

    #here we build the figure this displays all years with x as the month
    plt.figure(figsize=(18,10))
    for year in data.index:
        if year > 2011:
            plt.plot(data.loc[year])
    plt.xticks(size=15)
    plt.yticks(size=15)
    plt.xlabel("Year", size=20)
    plt.title("US Unemployment Monlthy Data", size=25)
    plt.ylabel("Unemployment (%)", size=20)
    plt.legend(data.index)
    plt.show()


    #lets get yearly averages from the months
    yearAverages = pd.Series(index=data.index, dtype=np.float64)

    #for each year in the new series lets get that years data and get the average
    for year in data.index:
        sum = 0
        average = 0
        for month in data.columns:
            sum += data.loc[year][month]
        average = sum / len(data.columns)
        print(year, ' average :',average)
        yearAverages.loc[year] = average

    plt.figure(figsize=(15,10))
    plt.plot(yearAverages[1:])
    plt.title("US Unemployement Averages", size = 30)
    plt.xlabel("Year", size=20)
    plt.xticks(size=15)
    plt.ylabel("Unemployement Rate (%)", size=20)
    plt.yticks(size=15)
    plt.show()    



def get_and_show_minWage():
    
    wageData = pd.read_csv(min_income_csv, encoding = "ISO-8859-1", header=0, index_col=0)

    milIndex = wageData.index
    milState = wageData['State']
    milWage = wageData['State.Minimum.Wage']


    milData = pd.DataFrame(index=milIndex, columns=['State','State.Minimum.Wage'])
    milData['State'] = milState
    milData['State.Minimum.Wage'] = milWage

    #this will get an index of the state
    stateIndex = []

    for state in milData['State']:
        if state not in stateIndex:
            stateIndex.append(state)
            
    #ok here we have the states in an list, now we need to get the year for the column labels
    yearCols = [y for y in range(2008, 2021)]


    newStateWageDF = pd.DataFrame(data = 0, index=stateIndex, columns=yearCols, dtype=np.float64)

    
    #this block of code fills the data frame with wages from the initial dataframe
    #we will go thru each row which is a year for a state
    for year in wageData.index:
        #if we find the years we want
        if year > 2007:
            #we will extract the years minwage based on the year        
            #then we add it to the year column in the other df with list comprehension
            newStateWageDF[year] = [wage for wage in wageData['State.Minimum.Wage'].loc[year]]#this loc will get a series 
            

    #plotting the data
    keys = ['Arizona','California', 'Colorado', 'Nevada', 'New Mexico', 'Utah']

    x = newStateWageDF.columns

    plt.figure(figsize=(15,8))

    for key in keys:
        plt.plot(x, newStateWageDF.loc[key])

    plt.legend(keys, loc='upper left', prop={'size':10})
    plt.title("States Min Wages(2008-2020)", size=30)
    plt.ylabel("Min Wage (Dollars)", size=20)
    plt.yticks(size=15)
    plt.xlabel("Year", size=20)
    plt.xticks(size=15)
    plt.show()

    #this data should be used with the average
    minWageSalary = pd.Series(index=keys, data=newStateWageDF[2020])
    for state in minWageSalary.keys():    
        minWageSalary.loc[state] *= (40*50)





def get_and_show_average_wages():


    #gonna try something esle now gonna scape another site this is average wages and salary
    averageSalaryURL="https://www.statsamerica.org/sip/rank_list.aspx?rank_label=bea&item_in=0035&ct=S09"
    aveSal = pd.read_html(averageSalaryURL, index_col=1)[0]
    type(aveSal.index[0])

    neighborSal=pd.DataFrame(columns = aveSal.columns)

    neighborState = ['Arizona', 'California', 'Colorado', 'Nevada', 'New Mexico', 'Utah' ]

    for state in neighborState:
        neighborSal.loc[state] = (aveSal.loc[state])

    #here we will build an hbar graph
    plt.figure(figsize=(15,10))

    
    plt.barh(neighborSal.index, neighborSal['Average Earnings'] , color=['red','cyan','green','blue','orange','yellow'])



    for index, value in enumerate(neighborSal['Average Earnings']):
        plt.text(value, index, str(value),size=15)

    plt.title("Earnings by place of work: Average Earnings Per Job in 2021", size=20)
    plt.xlabel('Salary in US Dollars', size=15)
    plt.ylabel("Average Salary", size=20)
    plt.yticks(size=15)

    plt.xticks(rotation=45, size= 15)

    plt.show()



def get_and_show_housing_data():
    housefile = 'ZHVI.csv'
    houseData = pd.read_csv(housefile, index_col=0, header=0)

    #need to turn the index into datetimeobjects
    indexDT = []

    for date in houseData.index:
        dateItems = date.split('-')
        #print(dt.datetime(int(dateItems[0]), int(dateItems[1]), int(dateItems[2])))
        indexDT.append(dt.datetime(int(dateItems[0]), int(dateItems[1]), int(dateItems[2])))
        
    houseData.reindex(index=indexDT)

    #clean the data of nans
    for row in houseData.index:
        
        
        for state in houseData.columns:
            if math.isnan(houseData.loc[row][state]):
                houseData.loc[row][state] = 0

    #now lets get the states we want to know
    neighborState = ['Arizona', 'California', 'Colorado', 'Nevada', 'New Mexico', 'Utah' ]

    neighborDF = pd.DataFrame(index=houseData.index, columns=neighborState)


    for state in houseData.columns:
        if state in neighborState:
            
            neighborDF[state] = houseData[state]


    #now we need to change the data a bit to get the averages for each year so we arent dealing with monthly data
    yearAverages = pd.DataFrame(data=0, index=range(2000,2023), columns=neighborDF.columns)


    for date in neighborDF.index:
        for state in neighborDF.columns:
            #print(type(neighborDF.loc[date][state]))
            year = date[:4]
            yearAverages.loc[int(year)][state] += neighborDF.loc[date][state]
            
    totalAves = pd.Series(data= 0, index=yearAverages.index, dtype=np.float64)     

    for year in yearAverages.index:
        for state in yearAverages.columns:
            yearAverages.loc[year][state] /= 12

            totalAves.loc[year] += yearAverages.loc[year][state] 
            
            
    yearAverages=yearAverages.drop(2022)


    totalAves /=6
    totalAves = totalAves.drop(2022)

    # we have our final form of data now we get the best fit line with ols
    x = sm.add_constant(range(len(totalAves.index)))


    result = sm.OLS(totalAves, x).fit()

    print(result.params)
    #right here is the best fit line 
    xs = range(len(totalAves.index))
    ys = result.params[1] * xs + result.params[0]

    plt.figure(figsize=(15,10))

    plt.title('Average Housing Prices 2000-2021', size=30)
    plt.xticks(ticks=xs,labels=totalAves.index, size=15, rotation=45)
    plt.plot(xs, yearAverages,'o', markersize=12)
    plt.legend(yearAverages.columns, prop={'size': 15})

    plt.yticks(size=15)

    plt.plot(xs, ys, linewidth=4,)

    plt.show()


print("     Final Project")
print("     Final Project")
print("     Final Project")
print("     Nate Mendoza")


get_and_display_Unemployement_data()

get_and_show_minWage()

get_and_show_average_wages()

get_and_show_housing_data()