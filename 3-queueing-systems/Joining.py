# Load necessary libraries
import pandas as pd
import duckdb as ddb

# import data to join
df1 = pd.read_csv("./data-p3/BASA_AUC_2028_912.csv")
df2 = pd.read_csv("./data-p3/dat_P_sub_c.csv")

# create database to use
con = ddb.connect("./data_p3.db")

# add data to database
con.sql("CREATE OR REPLACE TABLE DF1 AS SELECT * FROM df1")
con.sql("CREATE OR REPLACE TABLE DF2 AS SELECT * FROM df2")

# checking out the data 
con.sql("Select PASS_ID, Act_Departure from DF1 except select PASS_ID, Act_Departure from DF2")
con.sql("""with cte as (Select t1.PASS_ID, t1.Act_Departure as d1, t2.act_departure as d2 from DF1 
        as t1 left join df2 as t2 on t1.pass_id=t2.pass_id) select * from cte where d1=date_add(d2,INTERVAL 10 MINUTE)""")

con.sql("""with cte as (Select t1.PASS_ID, t1.S2 as d1, t2.S2 as d2 from DF1 
        as t1 left join df2 as t2 on t1.pass_id=t2.pass_id) select * from cte""")

con.sql("""with cte as (Select t1.PASS_ID, t1.C_avg as d1, t2.C_avg as d2 from DF1 
        as t1 left join df2 as t2 on t1.pass_id=t2.pass_id) select * from cte where d1!=d2""")

# noticed there was a 10 minute time difference (we end up taking the average of both)
con.sql("""with cte as (SELECT 
    t1.pass_id,
    t1.sch_departure,
    t2.sch_departure,
    date_diff('minutes', 
        STRPTIME(t1.sch_departure, '%Y-%m-%d %H:%M:%S'), 
        STRPTIME(t2.sch_departure, '%Y-%m-%d %H:%M')
    ) AS time_difference_in_seconds
FROM 
    df1 AS t1
LEFT JOIN 
    df2 AS t2 
ON 
    t1.pass_id = t2.pass_id)
        select * from cte where time_difference_in_seconds != (-10)""")

# creating the joined data
con.sql("""CREATE OR REPLACE TABLE JOINED AS select t1.pass_id
        , (STRPTIME(t1.sch_departure, '%Y-%m-%d %H:%M:%S')-INTERVAL 5 MINUTE) as Sch_Departure
        , (STRPTIME(t1.act_departure, '%Y-%m-%d %H:%M:%S')-INTERVAL 5 MINUTE) as Act_Departure
        , CASE WHEN t1.Month='08-Aug' THEN t1.C0 ELSE COALESCE(t2.C0, t1.C0) END as C0
        , CASE WHEN t1.Month='08-Aug' THEN t1.C_Start ELSE COALESCE(t2.C_Start,t1.C_Start) END as C_Start
        , CASE WHEN t1.Month='08-Aug' THEN t1.C_Avg ELSE COALESCE(t2.C_Avg,t1.C_Avg) END as C_Avg
        , t1.S2 as S2
        , t1.Wait_Time as Wait_Time
        , t1.Day_of_Week as Day_of_Week
        , CASE WHEN t1.Day_of_Week='1 - MON' or t1.Day_of_Week='2 - TUE'
        OR t1.Day_of_Week='3 - WED' OR t1.Day_of_Week='4 - THU' 
        OR t1.Day_of_Week='5 - FRI' THEN '1 - WEEKDAY' ELSE '2 - WEEKEND' END 
         as Period_of_Week
        , t1.Airfield as Airfield
        , t1.Season as Season
        from DF1 t1
        left join DF2 t2
        on CAST(t1.pass_id AS INTEGER) = CAST(t2.pass_id AS INTEGER)""")

# exporting joined data
con.sql("""COPY JOINED TO './joined.csv' (HEADER, DELIMITER ',')""")

# creating the cu report (maximum number of simultaneously active servers during 15-minute block)
con.sql("""
CREATE OR REPLACE TABLE cu_report AS
        SELECT 
        date_part('day', CAST(S2 as TIMESTAMP)) AS day,
        DATE_TRUNC('hour', CAST(S2 AS TIMESTAMP)) 
            + INTERVAL '1 minute' * (FLOOR(EXTRACT(MINUTE FROM CAST(S2 AS TIMESTAMP)) / 15) * 15)::int AS interval_start,
        MAX(C0) as max_Servers
FROM 
    joined
GROUP BY 
    interval_start,
        day
ORDER BY 
    interval_start;
""")
# exporting cu report
con.sql("""COPY CU_REPORT TO './cu_report.csv' (HEADER, DELIMITER ',')""")

# creating wait time report
con.sql("""
CREATE OR REPLACE TABLE wt_report AS
        SELECT * FROM JOINED
        WHERE WAIT_TIME IS NOT NULL
""")
# exporting wait time report
con.sql("""COPY WT_REPORT TO './wt_report.csv' (HEADER, DELIMITER ',')""")

# creating clusters on period of the week and time of day
con.sql("""
CREATE OR REPLACE TABLE clustered AS SELECT *
        , period_of_week
        , CASE 
        WHEN 0 <= DATE_PART('HOUR', CAST(S2 as TIMESTAMP)) AND DATE_PART('HOUR', CAST(S2 as TIMESTAMP)) < 4 THEN '0:00 - 4:00'
        WHEN 4 <= DATE_PART('HOUR', CAST(S2 as TIMESTAMP)) AND DATE_PART('HOUR', CAST(S2 as TIMESTAMP)) < 8 THEN '4:00 - 8:00'
        WHEN 8 <= DATE_PART('HOUR', CAST(S2 as TIMESTAMP)) AND DATE_PART('HOUR', CAST(S2 as TIMESTAMP)) < 12 THEN '8:00 - 12:00'
        WHEN 12 <= DATE_PART('HOUR', CAST(S2 as TIMESTAMP)) AND DATE_PART('HOUR', CAST(S2 as TIMESTAMP)) < 16 THEN '12:00 - 16:00'
        WHEN 16 <= DATE_PART('HOUR', CAST(S2 as TIMESTAMP)) AND DATE_PART('HOUR', CAST(S2 as TIMESTAMP)) < 20 THEN '16:00 - 20:00'
        WHEN 20 <= DATE_PART('HOUR', CAST(S2 as TIMESTAMP)) AND DATE_PART('HOUR', CAST(S2 as TIMESTAMP)) < 24 THEN '20:00 - 0:00'
        END AS hour_cluster
        , CASE
        WHEN Period_of_week = '1 - WEEKDAY' THEN 436 ELSE 176 END AS week_cluster
        FROM JOINED
""")
# calculating the mean wait time for each cluster and imputing the nulls as such
con.sql("""
WITH mean_wait_time AS (
    SELECT
        Period_of_Week,
        hour_cluster,
        AVG(Wait_Time) AS avg_wait_time
    FROM clustered
    WHERE Wait_Time IS NOT NULL
    GROUP BY Period_of_Week, hour_cluster
)
UPDATE clustered
SET Wait_Time = mw.avg_wait_time
FROM mean_wait_time mw
WHERE clustered.Period_of_Week = mw.Period_of_Week
  AND clustered.hour_cluster = mw.hour_cluster
  AND clustered.Wait_Time IS NULL
""")
# exporting clustered 
con.sql("COPY CLUSTERED TO './clustered.csv' (HEADER, DELIMITER ',')")

# Creating the arrivals table (avg arrival rate per cluster)
con.sql("""
CREATE OR REPLACE TABLE cluster_arrivals AS
        SELECT max(period_of_week) as cluster_name,
        week_cluster, hour_cluster, count(*) as count
        , ROUND(count/(week_cluster), 2) as Avg_Arrival_Rate
        from clustered
        group by week_cluster, hour_cluster
        order by cluster_name, CAST(SPLIT_PART(hour_cluster, ':', 1) AS INTEGER)
""")
# exporting arrivals table
con.sql("COPY cluster_arrivals TO './cluster_arrivals.csv' (HEADER, DELIMITER ',')")

# Creating servers table (average servers and distribution)
con.sql(""" create or replace table avg_servers as
with cte as (select *
        , CASE 
        WHEN 0 <= DATE_PART('HOUR', CAST(interval_start as TIMESTAMP)) AND DATE_PART('HOUR', CAST(interval_start as TIMESTAMP)) < 4 THEN '0:00 - 4:00'
        WHEN 4 <= DATE_PART('HOUR', CAST(interval_start as TIMESTAMP)) AND DATE_PART('HOUR', CAST(interval_start as TIMESTAMP)) < 8 THEN '4:00 - 8:00'
        WHEN 8 <= DATE_PART('HOUR', CAST(interval_start as TIMESTAMP)) AND DATE_PART('HOUR', CAST(interval_start as TIMESTAMP)) < 12 THEN '8:00 - 12:00'
        WHEN 12 <= DATE_PART('HOUR', CAST(interval_start as TIMESTAMP)) AND DATE_PART('HOUR', CAST(interval_start as TIMESTAMP)) < 16 THEN '12:00 - 16:00'
        WHEN 16 <= DATE_PART('HOUR', CAST(interval_start as TIMESTAMP)) AND DATE_PART('HOUR', CAST(interval_start as TIMESTAMP)) < 20 THEN '16:00 - 20:00'
        WHEN 20 <= DATE_PART('HOUR', CAST(interval_start as TIMESTAMP)) AND DATE_PART('HOUR', CAST(interval_start as TIMESTAMP)) < 24 THEN '20:00 - 0:00'
        END AS hour_cluster
        , CASE
        WHEN DATE_PART('dayofweek', CAST(interval_start as TIMESTAMP)) = 0 
        or DATE_PART('dayofweek', CAST(interval_start as TIMESTAMP)) = 6 THEN 104 ELSE 260 END AS week_cluster
        , CASE
        WHEN DATE_PART('dayofweek', CAST(interval_start as TIMESTAMP)) = 0 
        or DATE_PART('dayofweek', CAST(interval_start as TIMESTAMP)) = 6 THEN '2 - WEEKEND' ELSE '1 - WEEKDAY' END AS cluster
        from cu_report )

    select max(cluster) as cluster, hour_cluster, 
        ROUND(avg(max_servers),2) as Avg_Servers,
        FROM cte 
        GROUP BY cluster, hour_cluster
        order by cluster, CAST(SPLIT_PART(hour_cluster, ':', 1) AS INTEGER)
""")

con.sql(""" create or replace table servers as
with num_by_cluster_c0 as (select period_of_week, hour_cluster, count(*) as sum_c0, c0 from clustered group by period_of_week, hour_cluster, c0
        having c0 is not null and c0 !=0),
num_by_cluster as (select period_of_week, hour_cluster, count(*) as sum from clustered where c0 is not null and c0 !=0
        group by period_of_week, hour_cluster
        )
        select t1.*, t2.sum from num_by_cluster_c0 as t1 left join num_by_cluster as t2 on t1.hour_cluster=t2.hour_cluster and t1.period_of_week=t2.period_of_week
""")
# Creating table for distribution of number of servers
con.sql(
""" create or replace table percentage_servers as
with cte as (
SELECT 
    Period_of_Week,
    hour_cluster,
    SUM(CASE WHEN C0 = 0 THEN sum_c0 ELSE 0 END) AS "0_servers",
    SUM(CASE WHEN C0 = 1 THEN sum_c0 ELSE 0 END) AS "1_server",
    SUM(CASE WHEN C0 = 2 THEN sum_c0 ELSE 0 END) AS "2_servers",
    SUM(CASE WHEN C0 = 3 THEN sum_c0 ELSE 0 END) AS "3_servers",
    SUM(sum_c0) AS "Total_count",
    ROUND(100.0 * SUM(CASE WHEN C0 = 0 THEN sum_c0 ELSE 0 END) / SUM(sum_c0), 2) AS "0_servers_percentage",
    ROUND(100.0 * SUM(CASE WHEN C0 = 1 THEN sum_c0 ELSE 0 END) / SUM(sum_c0), 2) AS "1_server_percentage",
    ROUND(100.0 * SUM(CASE WHEN C0 = 2 THEN sum_c0 ELSE 0 END) / SUM(sum_c0), 2) AS "2_servers_percentage",
    ROUND(100.0 * SUM(CASE WHEN C0 = 3 THEN sum_c0 ELSE 0 END) / SUM(sum_c0), 2) AS "3_servers_percentage"
FROM 
    servers
GROUP BY 
    Period_of_Week, 
    hour_cluster
    )
    select period_of_week, hour_cluster, "1_server_percentage", "2_servers_percentage", "3_servers_percentage"
    from cte
ORDER BY 
    Period_of_Week, CAST(SPLIT_PART(hour_cluster, ':', 1) AS INTEGER)
"""
)
# joining the two tables and exporting
con.sql(
""" CREATE OR REPLACE TABLE avg_servers_final AS
select t1.*, t2."1_server_percentage", t2."2_servers_percentage", t2."3_servers_percentage" from avg_servers t1
left join percentage_servers as t2 on t1.cluster=t2.Period_of_Week and t1.hour_cluster=t2.hour_cluster
"""
)
con.sql("COPY avg_servers_final TO './avg_servers_final.csv' (HEADER, DELIMITER ',')")

# creating average wait time and performance levels table
con.sql(""" CREATE OR REPLACE TABLE times as
WITH cumulative_percentage AS (
    SELECT
        Period_of_Week,
        hour_cluster,
        COUNT(*) AS total_count,
        AVG(wait_time) as Avg_Wait,
        SUM(CASE WHEN Wait_Time <= 5 THEN 1 END) AS count_5mins,
        SUM(CASE WHEN Wait_Time <= 10 THEN 1 END) AS count_10mins,
        SUM(CASE WHEN Wait_Time <= 15 THEN 1 END) AS count_15mins,
        SUM(CASE WHEN Wait_Time <= 20 THEN 1 END) AS count_20mins,
        SUM(CASE WHEN Wait_Time <= 25 THEN 1 END) AS count_25mins,
        SUM(CASE WHEN Wait_Time <= 30 THEN 1 END) AS count_30mins
    FROM clustered
        WHERE Wait_time is not null
    GROUP BY Period_of_Week, hour_cluster
),
cte2 as (
SELECT
    Period_of_Week,
    hour_cluster,
        total_count,
        Avg_Wait,
    -- Calculate the cumulative percentages
    ROUND(100.0 * count_5mins / total_count, 6) AS "<=5 mins",
    ROUND(100.0 * count_10mins / total_count, 6) AS "<=10 mins",
    ROUND(100.0 * count_15mins / total_count, 6) AS "<=15 mins",
    ROUND(100.0 * count_20mins / total_count, 6) AS "<=20 mins",
    ROUND(100.0 * count_25mins / total_count, 6) AS "<=25 mins",
    ROUND(100.0 * count_30mins / total_count, 6) AS "<=30 mins"
FROM cumulative_percentage
)
select * from cte2 ORDER BY Period_of_Week, hour_cluster
""")
# exporting times table
con.sql("COPY times TO './times.csv' (HEADER, DELIMITER ',')")

# creating the quality of service estimates table
con.sql(""" create or replace table qos_estimates as
        with cte as (
select t1.cluster,t1.hour_cluster, t2.avg_wait, t3.avg_arrival_rate,
        ((t2.avg_wait*t3.avg_arrival_rate)+SQRT((t2.avg_wait*t3.avg_arrival_rate)*(t2.avg_wait*t3.avg_arrival_rate)+(4*t2.avg_wait*t3.avg_arrival_rate)))/(2*t2.avg_wait) AS serv_rate,
        t3.avg_arrival_rate/serv_rate as rho,
        CAST(ROUND((1-((t3.avg_arrival_rate)/(serv_rate))*EXP(-((serv_rate)-(t3.avg_arrival_rate))*5))*100,2) AS VARCHAR)|| '%' as "5m",
        CAST(ROUND((1-((t3.avg_arrival_rate)/(serv_rate))*EXP(-((serv_rate)-(t3.avg_arrival_rate))*10))*100,2) AS VARCHAR)|| '%' as "10m",
        CAST(ROUND((1-((t3.avg_arrival_rate)/(serv_rate))*EXP(-((serv_rate)-(t3.avg_arrival_rate))*15))*100,2) AS VARCHAR)|| '%' as "15m",
        CAST(ROUND((1-((t3.avg_arrival_rate)/(serv_rate))*EXP(-((serv_rate)-(t3.avg_arrival_rate))*20))*100,2) AS VARCHAR)|| '%' as "20m",
        CAST(ROUND((1-((t3.avg_arrival_rate)/(serv_rate))*EXP(-((serv_rate)-(t3.avg_arrival_rate))*25))*100,2) AS VARCHAR)|| '%' as "25m",
        CAST(ROUND((1-((t3.avg_arrival_rate)/(serv_rate))*EXP(-((serv_rate)-(t3.avg_arrival_rate))*30))*100,2) AS VARCHAR)|| '%' as "30m"
        from avg_servers_final t1
        left join times t2
        on t1.cluster = t2.Period_of_Week
        and t1.hour_cluster=t2.hour_cluster
        left join cluster_arrivals as t3
        on t1.cluster = t3.cluster_name
        and t1.hour_cluster=t3.hour_cluster)
        select cluster
        , hour_cluster
        , ROUND(serv_rate,3) as Est_Service_Rate
        , ROUND(rho,3) as Traffic_Intensity
        , "5m" as "5_minutes", 
        "10m" as "10_minutes", "15m" as "15_minutes", "20m" as "20_minutes", "25m" as "25_minutes", "30m" as "30_minutes"
        from cte
        order by cluster, CAST(SPLIT_PART(hour_cluster, ':', 1) AS INTEGER)
""")
# exporting qos table
con.sql("COPY qos_estimates TO './qos_estimates.csv' (HEADER, DELIMITER ',')")

# Creating a table to use for linear regression
con.sql(""" create or replace table reg as 
select t2.cluster, t2.hour_cluster
        , t3.Avg_servers as avg_servers
        , t4.avg_arrival_rate as arrival_rate
        , t2.est_service_rate as est_serv_rate
        , round(arrival_rate/avg_servers, 3) as "arr_rate/server"
        , round(est_serv_rate/avg_servers,3) as "serv_rate/server"
        from qos_estimates t2
        left join avg_servers_final t3
        on t2.cluster=t3.cluster and t2.hour_cluster=t3.hour_cluster
        left join cluster_arrivals t4 
        on t2.cluster=t4.cluster_name and t2.hour_cluster=t4.hour_cluster
""")
# exporting data to be used for linear regression
con.sql("COPY reg TO './reg.csv' (HEADER, DELIMITER ',')")

# Regerssion is done in R using reg.csv, 
# a and b come from the regression done in R

a=0.308737
b=0.996213

# creating table with regression qos estimates, one formatted and one with raw data for c estimates
Q_reg_est_Formatted=f""" create or replace table reg_ests_formatted as 
select cluster, hour_cluster
, round("arr_rate/server",1) as class
, round(({a}*avg_servers)+({b}*arrival_rate),3) as reg_serv_rate
, round(arrival_rate/reg_serv_rate,3) as reg_rho
, CAST(ROUND((1-((arrival_rate)/(reg_serv_rate))*EXP(-(reg_serv_rate-arrival_rate)*5))*100,2) AS VARCHAR)|| '%' as "5m"
, CAST(ROUND((1-((arrival_rate)/(reg_serv_rate))*EXP(-(reg_serv_rate-arrival_rate)*10))*100,2) AS VARCHAR)|| '%' as "10m"
, CAST(ROUND((1-((arrival_rate)/(reg_serv_rate))*EXP(-(reg_serv_rate-arrival_rate)*15))*100,2) AS VARCHAR)|| '%' as "15m"
, CAST(ROUND((1-((arrival_rate)/(reg_serv_rate))*EXP(-(reg_serv_rate-arrival_rate)*20))*100,2) AS VARCHAR)|| '%' as "20m"
, CAST(ROUND((1-((arrival_rate)/(reg_serv_rate))*EXP(-(reg_serv_rate-arrival_rate)*25))*100,2) AS VARCHAR)|| '%' as "25m"
, CAST(ROUND((1-((arrival_rate)/(reg_serv_rate))*EXP(-(reg_serv_rate-arrival_rate)*30))*100,2) AS VARCHAR)|| '%' as "30m"
 from reg
"""
Q_reg_est=f""" create or replace table reg_ests as
select cluster, hour_cluster
, round("arr_rate/server",1) as class
, arrival_rate
, ({a}*avg_servers)+({b}*arrival_rate) as reg_serv_rate
, round(arrival_rate/reg_serv_rate,3) as reg_rho
, (1-((arrival_rate)/(reg_serv_rate))*EXP(-(reg_serv_rate-arrival_rate)*5)) as "5m"
, (1-((arrival_rate)/(reg_serv_rate))*EXP(-(reg_serv_rate-arrival_rate)*10)) as "10m"
, (1-((arrival_rate)/(reg_serv_rate))*EXP(-(reg_serv_rate-arrival_rate)*15)) as "15m"
, (1-((arrival_rate)/(reg_serv_rate))*EXP(-(reg_serv_rate-arrival_rate)*20)) as "20m"
, (1-((arrival_rate)/(reg_serv_rate))*EXP(-(reg_serv_rate-arrival_rate)*25)) as "25m"
, (1-((arrival_rate)/(reg_serv_rate))*EXP(-(reg_serv_rate-arrival_rate)*30)) as "30m"
 from reg
"""
con.sql(Q_reg_est)
con.sql("COPY reg_ests TO './reg_ests.csv' (HEADER, DELIMITER ',')")

con.sql(Q_reg_est_Formatted)
con.sql("COPY reg_ests_formatted TO './reg_ests_formatted.csv' (HEADER, DELIMITER ',')")

# the rest is done in R
