
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

## Read data
polls_data=pd.read_csv("./data-p1/polls_us_election_2016.csv")

polls_data2=pd.read_csv('./data-p1/agg_polls_by_day.csv')

polls_data_by_day=pd.read_csv('./data-p1/agg_polls_by_day.csv')

####################  weighted average (Mairi) #########################
dff = polls_data2[polls_data2["state"] == 'U.S.']

def weighted_average(group, value_column):
    sqrt_sample_sizes = group['samplesizeadj'] ** 0.5
    median_sqrt_sample_size = group['samplesizeadj'].median() ** 0.5
    weights = sqrt_sample_sizes / median_sqrt_sample_size
    return (group[value_column] * weights).sum() / weights.sum()

df_agg = dff.groupby(['day', 'population']).apply(
    lambda group: pd.Series({
        'c_minus_t_raw': weighted_average(group, 'c_minus_t_raw'),
        'c_minus_t_adj': weighted_average(group, 'c_minus_t_adj')
    })
).reset_index()

# Reset the index to make 'day' a regular column again
df_agg = df_agg.reset_index()

# Display the new aggregated DataFrame
print("Aggregated DataFrame (df_agg):")
print(df_agg)

polls_data2=df_agg

df_agg.to_csv("./data-p1/agg_polls_by_day_weightedaverage.csv")

print(polls_data2)

####################################################
## Convert dates
polls_data["startdate"] = pd.to_datetime(polls_data["startdate"])
polls_data["enddate"] = pd.to_datetime(polls_data["enddate"])

## Get period of end date
polls_data["enddate_period"]=polls_data["enddate"].dt.to_period('M')
polls_data["enddate_period"]=polls_data["enddate_period"].dt.to_timestamp()

## Calculate clinton minus trump
polls_data["c-minus-t"]=polls_data["rawpoll_clinton"]-polls_data["rawpoll_trump"]

polls_data.dtypes
print(polls_data)

## Grades and Counts of Pollsters
pollsters=pd.DataFrame(polls_data.groupby("pollster").agg({"grade":lambda x: x.mode(),"pollster":"size"}))
print(pollsters)

## Adjusted poll values by grade and count
grades2=polls_data.groupby("grade").agg({"adjpoll_clinton":"mean","adjpoll_trump":"mean","grade":"size"})
grades2=grades2.rename(columns={"grade":"grade","grade":"count"})
grades2=grades2.reset_index()
print(grades2)

####################################################
## Bar Graph Grade Distribution
plt.bar(grades2["grade"],grades2["count"])
plt.xlabel("Grade of Pollster")
plt.ylabel("Number of Polls")
plt.title("Count of Polls by Grade")
plt.show()

####################################################
## Boxplot From Mairi
polls_data.boxplot(column="c-minus-t",by="grade")
plt.show()

## Changing Grade to Numeric
grade_mapping = {"A+": 10, "A": 9, "A-": 8 ,"B+":7, "B": 6, "B-": 5, "C+": 4, "C": 3, "C-": 2, "D": 1}
polls_data["grade_numeric"] = polls_data["grade"].map(grade_mapping)

####################################################
## Scatter Plot
plt.scatter(polls_data["grade_numeric"],polls_data["c-minus-t"])
plt.xlabel("Grade as Number")
plt.ylabel("Clinton Minus Trump Raw Polls")
plt.show()

####################################################
### Stacked Bar Chart
grouped_data = polls_data.groupby(['grade', 'population']).size().unstack(fill_value=0)

# Plotting
grouped_data.plot(kind='bar', stacked=True)

# Adding labels and title
plt.xlabel('Grade')
plt.ylabel('Number of Polls')
plt.title('Stacked Bar Chart of Election Polls by Grade and Population, Original Data')
plt.xticks(rotation=0)
plt.show()
####################################################

## Line graph: Clinton minus Trump over time by grade

averaged_data_Aplus=polls_data[polls_data["grade"]=="A+"].groupby("enddate_period")["c-minus-t"].mean().reset_index()
plt.plot(averaged_data_Aplus["enddate_period"],averaged_data_Aplus["c-minus-t"], label="Grade A+")

averaged_data_A=polls_data[polls_data["grade"]=="A"].groupby("enddate_period")["c-minus-t"].mean().reset_index()
plt.plot(averaged_data_A["enddate_period"],averaged_data_A["c-minus-t"], label="Grade A")

averaged_data_Aminus=polls_data[polls_data["grade"]=="A-"].groupby("enddate_period")["c-minus-t"].mean().reset_index()
plt.plot(averaged_data_Aminus["enddate_period"],averaged_data_Aminus["c-minus-t"], label="Grade A-")

averaged_data_Bplus=polls_data[polls_data["grade"]=="B+"].groupby("enddate_period")["c-minus-t"].mean().reset_index()
plt.plot(averaged_data_Bplus["enddate_period"],averaged_data_Bplus["c-minus-t"], label="Grade B+")

averaged_data_B=polls_data[polls_data["grade"]=="B"].groupby("enddate_period")["c-minus-t"].mean().reset_index()
plt.plot(averaged_data_B["enddate_period"],averaged_data_B["c-minus-t"], label="Grade B")

averaged_data_Bminus=polls_data[polls_data["grade"]=="B-"].groupby("enddate_period")["c-minus-t"].mean().reset_index()
plt.plot(averaged_data_Bminus["enddate_period"],averaged_data_Bminus["c-minus-t"], label="Grade B-")

averaged_data_Cplus=polls_data[polls_data["grade"]=="C+"].groupby("enddate_period")["c-minus-t"].mean().reset_index()
plt.plot(averaged_data_Cplus["enddate_period"],averaged_data_Cplus["c-minus-t"], label="Grade C+")

averaged_data_C=polls_data[polls_data["grade"]=="C"].groupby("enddate_period")["c-minus-t"].mean().reset_index()
plt.plot(averaged_data_C["enddate_period"],averaged_data_C["c-minus-t"], label="Grade C")

averaged_data_Cminus=polls_data[polls_data["grade"]=="C-"].groupby("enddate_period")["c-minus-t"].mean().reset_index()
plt.plot(averaged_data_Cminus["enddate_period"],averaged_data_Cminus["c-minus-t"], label="Grade C-")

averaged_data_D=polls_data[polls_data["grade"]=="D"].groupby("enddate_period")["c-minus-t"].mean().reset_index()
plt.plot(averaged_data_D["enddate_period"],averaged_data_D["c-minus-t"], label="Grade D")

plt.xlabel("Reference Month")
plt.ylabel("Clinton minus Trump")
plt.legend()
plt.title("Clinton Minus Trump (Raw) by Pollster Grade (Sep-Nov 2016), Monthly")
plt.show()


############ With weighted average data ##############

polls_data2["day"] = pd.to_datetime(polls_data2["day"])
polls_data2 = polls_data2[polls_data2["day"] >= dt.datetime(2016, 9, 1)]

averaged_data_Aplus=polls_data2[polls_data2["grade"]=="A+"].groupby("day")["c_minus_t_adj"].mean().reset_index()
plt.plot(averaged_data_Aplus["day"],averaged_data_Aplus["c_minus_t_adj"], label="Grade A+")

averaged_data_A=polls_data2[polls_data2["grade"]=="A"].groupby("day")["c_minus_t_adj"].mean().reset_index()
plt.plot(averaged_data_A["day"],averaged_data_A["c_minus_t_adj"], label="Grade A")

averaged_data_Aminus=polls_data2[polls_data2["grade"]=="A-"].groupby("day")["c_minus_t_adj"].mean().reset_index()
plt.plot(averaged_data_Aminus["day"],averaged_data_Aminus["c_minus_t_adj"], label="Grade A-")

averaged_data_Bplus=polls_data2[polls_data2["grade"]=="B+"].groupby("day")["c_minus_t_adj"].mean().reset_index()
plt.plot(averaged_data_Bplus["day"],averaged_data_Bplus["c_minus_t_adj"], label="Grade B+")

averaged_data_B=polls_data2[polls_data2["grade"]=="B"].groupby("day")["c_minus_t_adj"].mean().reset_index()
plt.plot(averaged_data_B["day"],averaged_data_B["c_minus_t_adj"], label="Grade B")

averaged_data_Bminus=polls_data2[polls_data2["grade"]=="B-"].groupby("day")["c_minus_t_adj"].mean().reset_index()
plt.plot(averaged_data_Bminus["day"],averaged_data_Bminus["c_minus_t_adj"], label="Grade B-")

averaged_data_Cplus=polls_data2[polls_data2["grade"]=="C+"].groupby("day")["c_minus_t_adj"].mean().reset_index()
plt.plot(averaged_data_Cplus["day"],averaged_data_Cplus["c_minus_t_adj"], label="Grade C+")

averaged_data_C=polls_data2[polls_data2["grade"]=="C"].groupby("day")["c_minus_t_adj"].mean().reset_index()
plt.plot(averaged_data_C["day"],averaged_data_C["c_minus_t_adj"], label="Grade C")

averaged_data_Cminus=polls_data2[polls_data2["grade"]=="C-"].groupby("day")["c_minus_t_adj"].mean().reset_index()
plt.plot(averaged_data_Cminus["day"],averaged_data_Cminus["c_minus_t_adj"], label="Grade C-")

averaged_data_D=polls_data2[polls_data2["grade"]=="D"].groupby("day")["c_minus_t_adj"].mean().reset_index()
plt.plot(averaged_data_D["day"],averaged_data_D["c_minus_t_adj"], label="Grade D")

plt.xlabel("Date")
plt.ylabel("Clinton minus Trump")
plt.title("Clinton Minus Trump (Adjusted) by Pollster Grade (Sep-Nov 2016), Weighted Average")
plt.legend()
plt.show()

####################################################
### Stacked Bar Chart
grouped_data = polls_data_by_day.groupby(['grade', 'population']).size().unstack(fill_value=0)

# Plotting
grouped_data.plot(kind='bar', stacked=True)

# Adding labels and title
plt.xlabel('Grade')
plt.ylabel('Number of Polls')
plt.title('Stacked Bar Chart of Election Polls by Grade and Population, Day Aggregated Data')
plt.xticks(rotation=0)
plt.show()

####################################################
### Stacked Bar Chart
grouped_data = polls_data2.groupby(['grade', 'population']).size().unstack(fill_value=0)

# Plotting
grouped_data.plot(kind='bar', stacked=True)

# Adding labels and title
plt.xlabel('Grade')
plt.ylabel('Number of Polls')
plt.title('Stacked Bar Chart of Election Polls by Grade and Population, Weighted Averaged Data')
plt.xticks(rotation=0)
plt.show()
