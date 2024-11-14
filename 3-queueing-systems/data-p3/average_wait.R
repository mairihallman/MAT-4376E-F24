df <- read.csv("./3-queueing-systems/data-p3/comp_data.csv")
library(dplyr)
library(lubridate)
df$S2 <- ymd_hm(df$S2)
#Creating 4-hour windows
df <- df %>% 
  mutate(Date = as.Date(S2), 
  Hour = hour(S2), 
  Time_Window = cut (Hour, breaks = seq(0, 24, by = 4),
  right = FALSE, labels = paste(seq(0, 20, by = 4), 
  seq(4, 24, by = 4), sep = "-")))

average_wait_time <- df %>%
  group_by(Day_of_Week, Time_Window) %>%
  summarise(Average_Wait_Time = round(mean(Wait_Time, na.rm = TRUE),1))

print(average_wait_time)

#filling in the extra wait times using the averages
df <- df %>%
  left_join(average_wait_time, by = c("Day_of_Week", "Time_Window")) %>%
  mutate(Wait_Time = ifelse(is.na(Wait_Time), Average_Wait_Time, Wait_Time)) %>%
  select(-Average_Wait_Time) 

#check that values arent missing
sum(is.na(df$Wait_Time)) #since 0, they were all filled

write.csv(df, "./3-queueing-systems/data-p3/joined_all.csv", row.names = FALSE)
df$Wait_Time

#creating clusters by hour and by period of week
df <- df %>% 
  mutate(Date = as.Date(S2), 
  Hour = hour(S2), 
  Time_Window = cut (Hour, breaks = seq(0, 24, by = 4),
  right = FALSE, labels = paste(seq(0, 20, by = 4), 
  seq(4, 24, by = 4), sep = "-")))

summary_table_1 <- df %>%
  group_by(Period_of_Week, Time_Window) %>%
  summarise(
    '# of Hours' = n_distinct(Day_of_Week) * 52,  # Adjust for the number of unique days times 4 hours
    Count = n(),
    'Avg Arrival Rate' = Count / `# of Hours`
  )
print(summary_table_1)

#FIND POISSON DISTRIBUTION GRAPH (LOOK AT MAIRIS CODE)
 
  