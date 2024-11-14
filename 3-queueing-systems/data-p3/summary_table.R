df <- read.csv("./3-queueing-systems/data-p3/comp_data.csv")
library(lubridate)
library(dplyr)
library(tidyr)
df$Wait_Time

#creating clusters by hour and by period of week
df <- df %>% 
  mutate(Date = as.Date(S2), 
  Hour = hour(S2), 
  Time_Window = cut (Hour, breaks = seq(0, 24, by = 4),
  right = FALSE, labels = paste(seq(0, 20, by = 4), 
  seq(4, 24, by = 4), sep = "-")))

df <- df %>%
  mutate(
    cluster = case_when(
        Period_of_Week == "1 - WEEKDAY" & Time_Window == "0-4" ~ "1 - WEEKDAY 00-04",
        Period_of_Week == "1 - WEEKDAY" & Time_Window == "4-8" ~ "1 - WEEKDAY 04-08",
        Period_of_Week == "1 - WEEKDAY" & Time_Window == "8-12" ~ "1 - WEEKDAY 08-12",
        Period_of_Week == "1 - WEEKDAY" & Time_Window == "12-16" ~ "1 - WEEKDAY 12-16",
        Period_of_Week == "1 - WEEKDAY" & Time_Window == "16-20" ~ "1 - WEEKDAY 16-20",
        Period_of_Week == "1 - WEEKDAY" & Time_Window == "20-24" ~ "1 - WEEKDAY 20-24",
        Period_of_Week == "2 - WEEKEND" & Time_Window == "0-4" ~ "2 - WEEKEND 00-04",
        Period_of_Week == "2 - WEEKEND" & Time_Window == "4-8" ~ "2 - WEEKEND 04-08",
        Period_of_Week == "2 - WEEKEND" & Time_Window == "8-12" ~ "2 - WEEKEND 08-12",
        Period_of_Week == "2 - WEEKEND" & Time_Window == "12-16" ~ "2 - WEEKEND 12-16",
        Period_of_Week == "2 - WEEKEND" & Time_Window == "16-20" ~ "2 - WEEKEND 16-20",
        Period_of_Week == "2 - WEEKEND" & Time_Window == "20-24" ~ "2 - WEEKEND 20-24",
        )
  )

#Arrival Rates
summary_table_1 <- df %>%
  group_by(cluster) %>%
  summarise(
    `# of Hours` = if (first(Period_of_Week) == "1 - WEEKDAY") 436 else 176,
    Count = n(),
    `Avg Arrival Rate` = Count / `# of Hours`,
    .groups = "keep"  
  )
print(summary_table_1)

summary_table_2.1 <- df %>%
  group_by(cluster) %>%
  summarise(
   'Avg Number of Servers' = mean(C_Avg, na.rm = TRUE),
   .groups = "keep"
  )
print(summary_table_2.1)

distribution_C0 <- df %>%
  group_by(cluster) %>%
  count(C0...S2) %>%
  mutate(percent = n / sum(n) * 100) %>%
  pivot_wider(names_from = C0...S2, values_from = percent, values_fill = list(percent = 0))

#Average # and Distribution Table
summary_table_2 <- summary_table_2.1 %>%
  left_join(distribution_C0, by = 'cluster') %>%
  group_by(cluster) %>%
  summarise(`Avg Number of Servers` = mean(`Avg Number of Servers`),
    n = sum(n),
    `1` = sum(`1`),
    `2` = sum(`2`),
    `3` = sum(`3`),
  )
print(summary_table_2)

