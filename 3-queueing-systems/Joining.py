import pandas as pd
import duckdb as ddb

df1 = pd.read_csv("./data-p3/BASA_AUC_2028_912.csv")
df2 = pd.read_csv("./data-p3/dat_P_sub_c.csv")

con = ddb.connect("./data_p3.db")

con.sql("CREATE OR REPLACE TABLE DF1 AS SELECT * FROM df1")
con.sql("CREATE OR REPLACE TABLE DF2 AS SELECT * FROM df2")

con.sql("Select PASS_ID, Act_Departure from DF1 except select PASS_ID, Act_Departure from DF2")
con.sql("""with cte as (Select t1.PASS_ID, t1.Act_Departure as d1, t2.act_departure as d2 from DF1 
        as t1 left join df2 as t2 on t1.pass_id=t2.pass_id) select * from cte where d1=date_add(d2,INTERVAL 10 MINUTE)""")

con.sql("""with cte as (Select t1.PASS_ID, t1.S2 as d1, t2.S2 as d2 from DF1 
        as t1 left join df2 as t2 on t1.pass_id=t2.pass_id) select * from cte""")

con.sql("""with cte as (Select t1.PASS_ID, t1.C_avg as d1, t2.C_avg as d2 from DF1 
        as t1 left join df2 as t2 on t1.pass_id=t2.pass_id) select * from cte where d1!=d2""")

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

con.sql("""CREATE OR REPLACE TABLE JOINED2 AS select t1.pass_id
        , (STRPTIME(t1.sch_departure, '%Y-%m-%d %H:%M:%S')-INTERVAL 5 MINUTE) as Sch_Departure
        , (STRPTIME(t1.act_departure, '%Y-%m-%d %H:%M:%S')-INTERVAL 5 MINUTE) as Act_Departure
        , COALESCE(t2.C0, t1.C0) END as C0
        , COALESCE(t2.C_Start,t1.C_Start) END as C_Start
        , COALESCE(t2.C_Avg,t1.C_Avg) END as C_Avg
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


con.sql("""COPY JOINED TO './joined.csv' (HEADER, DELIMITER ',')""")
