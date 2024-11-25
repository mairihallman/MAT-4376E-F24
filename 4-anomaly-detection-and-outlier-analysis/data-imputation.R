df <- read.csv("./4-anomaly-detection-and-outlier-analysis/Data/Original Flights Data.csv")

library(lubridate)
library(dplyr)

#First go around of filling in Average Arrival Delay
average_delay <- df %>%
    group_by(ORIGIN_AIRPORT_ID, DEST_AIRPORT_ID, DAY_OF_WEEK) %>%
    summarise(Average_Delay = round(median(ARR_DELAY, na.rm = TRUE),0))
print(average_delay)

df <- df %>%
    left_join(average_delay, by = c("ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DAY_OF_WEEK")) %>%
    mutate(ARR_DELAY = ifelse(is.na(ARR_DELAY), Average_Delay, ARR_DELAY)) %>%
    select(-Average_Delay)

sum(is.na(df$ARR_DELAY))

#Need a second time with less granular groupings to fill in Average Arrival Delay
average_delay <- df %>%
    group_by(ORIGIN_AIRPORT_ID, DEST_AIRPORT_ID) %>%
    summarise(Average_Delay = round(median(ARR_DELAY, na.rm = TRUE),0))
print(average_delay)

df <- df %>%
    left_join(average_delay, by = c("ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID")) %>%
    mutate(ARR_DELAY = ifelse(is.na(ARR_DELAY), Average_Delay, ARR_DELAY)) %>%
    select(-Average_Delay)

sum(is.na(df$ARR_DELAY))

#First Time with Departure Delays
departure_delay <- df %>%
    group_by(ORIGIN_AIRPORT_ID, DEST_AIRPORT_ID, DAY_OF_WEEK) %>%
    summarise(Departure_Delay = round(median(DEP_DELAY, na.rm = TRUE),0))
print(departure_delay)

df <- df %>%
    left_join(departure_delay, by = c("ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DAY_OF_WEEK")) %>%
    mutate(DEP_DELAY = ifelse(is.na(DEP_DELAY), Departure_Delay, DEP_DELAY)) %>%
    select(-Departure_Delay)

sum(is.na(df$DEP_DELAY))

#Second Time with Departure Delays
departure_delay <- df %>%
    group_by(ORIGIN_AIRPORT_ID, DEST_AIRPORT_ID) %>%
    summarise(Departure_Delay = round(median(DEP_DELAY, na.rm = TRUE),0))
print(departure_delay)

df <- df %>%
    left_join(departure_delay, by = c("ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID")) %>%
    mutate(DEP_DELAY = ifelse(is.na(DEP_DELAY), Departure_Delay, DEP_DELAY)) %>%
    select(-Departure_Delay)

sum(is.na(df$DEP_DELAY))

write.csv(df, "./4-anomaly-detection-and-outlier-analysis/Data/reduced_flights.csv")
