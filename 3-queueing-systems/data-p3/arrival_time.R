df <- read.csv("./3-queueing-systems/data-p3/comp_data.csv")

library(lubridate)
library(dplyr)

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
    '# of Hours' = n_distinct(Day_of_Week) * (21.8*4),  # Adjust for the number of unique days times 4 hours
    Count = n(),
    'Avg Arrival Rate' = Count / `# of Hours`
  )
print(summary_table_1)

df <- df %>%
  mutate(S2_minutes = hour(S2) * 60 + minute(S2))

df <- df %>%
  mutate(S1 = S2_minutes - Wait_Time)
df$S1

df <- df %>%
  mutate(S1_time = S1/60)
df$S1_time

df <- df%>%
  mutate(S1_hstime = hm(S1_time))
df$S1_hstime

df <- df %>%
  group_by(Wait_Time, Period_of_Week) %>%
  mutate(S2_date = as.Date(S2),
  S1_datetime = S2_date + S1_hstime)
df$S1_datetime

library(ggplot2)

# Plot the density of S1 as a numeric variable
ggplot(df, aes(x = S1_time)) +
  geom_density(fill = "lightblue", color = "darkblue", alpha = 0.5) +
  labs(
    title = "Density Plot of S1 (Numeric Arrival Time)",
    x = "Arrival Time (S1) as Numeric Value",
    y = "Density"
  ) +
  theme_minimal()


