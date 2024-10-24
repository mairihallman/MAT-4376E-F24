#Q3

# Load necessary library
library(tidyverse)

# Function to update beta distribution parameters based on data
update_beta <- function(prior_alpha, prior_beta, successes, failures) {
  posterior_alpha <- prior_alpha + successes
  posterior_beta <- prior_beta + failures
  return(list(alpha = posterior_alpha, beta = posterior_beta))
}

# Function to compute the posterior probability
compute_prob_new_higher <- function(posterior_old, posterior_new, n_samples = 10000) {
  # Draw random samples from the posterior distributions
  samples_old <- rbeta(n_samples, posterior_old$alpha, posterior_old$beta)
  samples_new <- rbeta(n_samples, posterior_new$alpha, posterior_new$beta)
  
  # Estimate the probability that the new page conversion rate is higher than the old one
  prob_new_higher <- mean(samples_new > samples_old)
  return(prob_new_higher)
}

# Example data subset of 100 points (Assuming we have the data already)
set.seed(123)  # for reproducibility
data <- tibble(
  group = sample(c("control", "treatment"), size = 100, replace = TRUE),
  conversion = sample(c(0, 1), size = 100, replace = TRUE)
)


# Split the data into control (old page) and treatment (new page)
data_control <- data %>% filter(group == "control")
data_treatment <- data %>% filter(group == "treatment")

# Count successes (conversion=1) and failures (conversion=0) for both old and new page
success_old <- sum(data_control$conversion == 1)
failure_old <- sum(data_control$conversion == 0)
success_new <- sum(data_treatment$conversion == 1)
failure_new <- sum(data_treatment$conversion == 0)

# Priors for old and new page conversion rates
prior_old <- list(alpha = 2, beta = 20)
prior_new <- list(alpha = 2, beta = 20)

# Update posteriors with the first 100 data points
posterior_old <- update_beta(prior_old$alpha, prior_old$beta, success_old, failure_old)
posterior_new <- update_beta(prior_new$alpha, prior_new$beta, success_new, failure_new)

# Compute posterior probability that new page has higher conversion rate
prob_new_higher <- compute_prob_new_higher(posterior_old, posterior_new)
cat("Posterior probability that the new page has a higher conversion rate:", prob_new_higher, "\n")

# Now, update with another 100 data points and observe posterior changes

# Simulate the next 100 points (Assuming more data becomes available)
new_data <- tibble(
  group = sample(c("control", "treatment"), size = 100, replace = TRUE),
  conversion = sample(c(0, 1), size = 100, replace = TRUE)
)

# Split the new data into control (old page) and treatment (new page)
new_data_control <- new_data %>% filter(group == "control")
new_data_treatment <- new_data %>% filter(group == "treatment")

# Count successes and failures for the additional data
new_success_old <- sum(new_data_control$conversion == 1)
new_failure_old <- sum(new_data_control$conversion == 0)
new_success_new <- sum(new_data_treatment$conversion == 1)
new_failure_new <- sum(new_data_treatment$conversion == 0)

# Update the posteriors again with the new data points
posterior_old_updated <- update_beta(posterior_old$alpha, posterior_old$beta, new_success_old, new_failure_old)
posterior_new_updated <- update_beta(posterior_new$alpha, posterior_new$beta, new_success_new, new_failure_new)

# Compute the updated posterior probability
prob_new_higher_updated <- compute_prob_new_higher(posterior_old_updated, posterior_new_updated)
cat("Updated posterior probability that the new page has a higher conversion rate:", prob_new_higher_updated, "\n")

# Investigating when the priors become irrelevant
# As we increase the data size, the influence of priors diminishes. You can check by running
# the above steps with more data and comparing the probabilities with larger datasets.

# Function to simulate AB test and update posteriors with increasing data size
simulate_ab_test <- function(prior_old, prior_new, initial_data_size, step_size, max_data_size, n_samples = 10000) {
  
  data_sizes <- seq(initial_data_size, max_data_size, by = step_size)
  prob_diff <- numeric(length(data_sizes))  # To store probability differences between iterations
  
  # Initial random dataset (simulate control and treatment group conversion data)
  set.seed(123)  # for reproducibility
  
  for (i in seq_along(data_sizes)) {
    
    # Simulate data for current size
    data <- tibble(
      group = sample(c("control", "treatment"), size = data_sizes[i], replace = TRUE),
      conversion = sample(c(0, 1), size = data_sizes[i], replace = TRUE)
    )
    
    # Split the data into control (old page) and treatment (new page)
    data_control <- data %>% filter(group == "control")
    data_treatment <- data %>% filter(group == "treatment")
    
    # Count successes (conversion=1) and failures (conversion=0) for both old and new page
    success_old <- sum(data_control$conversion == 1)
    failure_old <- sum(data_control$conversion == 0)
    success_new <- sum(data_treatment$conversion == 1)
    failure_new <- sum(data_treatment$conversion == 0)
    
    # Update posteriors
    posterior_old <- update_beta(prior_old$alpha, prior_old$beta, success_old, failure_old)
    posterior_new <- update_beta(prior_new$alpha, prior_new$beta, success_new, failure_new)
    
    # Compute the posterior probability that the new page has a higher conversion rate
    prob_new_higher <- compute_prob_new_higher(posterior_old, posterior_new, n_samples)
    
    # Store the probability
    prob_diff[i] <- prob_new_higher
    
    # Print current data size and posterior probability
    cat("Data size:", data_sizes[i], " - Probability new page is better:", prob_new_higher, "\n")
    
    # Check convergence
    if (i > 1) {
      if (abs(prob_diff[i] - prob_diff[i - 1]) < 0.01) {
        cat("Convergence reached at data size:", data_sizes[i], "\n")
        break
      }
    }
  }
  
  return(prob_diff)
}

# Set priors
prior_old <- list(alpha = 2, beta = 20)
prior_new <- list(alpha = 2, beta = 20)

# Run simulation to determine at what data size priors become irrelevant
# Start with an initial dataset of 100, increase by 100 up to 5000 data points
probabilities <- simulate_ab_test(prior_old, prior_new, initial_data_size = 100, step_size = 100, max_data_size = 5000)

