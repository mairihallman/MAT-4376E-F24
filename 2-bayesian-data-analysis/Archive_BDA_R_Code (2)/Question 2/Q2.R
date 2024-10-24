# Load necessary libraries
library(dplyr)
library(bayesAB)


# Summarize data to count total users and conversions for each group
summary_data <- ab_data.cleaned %>%
  group_by(group) %>%
  summarise(
    converted = sum(converted),     # Total number of conversions
    users = n()                        # Total number of users
  )

# Print the summarized data
print(summary_data)

# Filter the data for the two groups: control and treatment
control_data <- data %>% filter(group == "control") %>% pull(converted)
treatment_data <- data %>% filter(group == "treatment") %>% pull(converted)

# Perform Bayesian A/B Test using bayesAB (binomial model with individual-level data)
ab_test <- bayesTest(
  A_data = control_data,  # Control group conversion outcomes (0 or 1 for each user)
  B_data = treatment_data,  # Treatment group conversion outcomes (0 or 1 for each user)
  priors = c('alpha' = 2, 'beta' = 20),
  distribution = 'bernoulli'  # Use Bernoulli for individual 0/1 data
)

# Print the summary of the Bayesian A/B test
summary(ab_test)

# Plot the posterior distributions for group A and B
plot(ab_test)

c_mean <- mean(control_data)
t_mean <- mean(treatment_data)


