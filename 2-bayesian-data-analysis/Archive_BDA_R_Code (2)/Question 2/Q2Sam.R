# Calculate number of conversions
control_conversions <- sum(ab_data.cleaned$converted[ab_data.cleaned$group == "control"])
treatment_conversions <- sum(ab_data.cleaned$converted[ab_data.cleaned$group == "treatment"])

# Total observations by group
control_total <- sum(ab_data.cleaned$group == "control")
treatment_total <- sum(ab_data.cleaned$group == "treatment")

# Set seed for replicability
set.seed(1111) 
n.draws <- 300000

# Define the prior
prior <- data.frame(
  p.A = rbeta(n.draws, shape1 = 2 + control_conversions, shape2 = 20 + (control_total - control_conversions)), 
  p.B = rbeta(n.draws, shape1 = 2 + treatment_conversions, shape2 = 20 + (treatment_total - treatment_conversions))
)

#prior <- data.frame(
# p.A = rbeta(n.draws, shape1 = 5 + control_conversions, shape2 = 15 + (control_total - control_conversions)), 
#p.B = rbeta(n.draws, shape1 = 5 + treatment_conversions, shape2 = 15 + (treatment_total - treatment_conversions))
#)

#prior <- data.frame(
# p.A = rbeta(n.draws, shape1 = 12 + control_conversions, shape2 = 88 + (control_total - control_conversions)),
#p.B = rbeta(n.draws, shape1 = 12 + treatment_conversions, shape2 = 88 + (treatment_total - treatment_conversions))
#)

#prior <- data.frame(
#p.A = rbeta(n.draws, shape1 = 5 + control_conversions, shape2 = 15 + (control_total - control_conversions)), 
#p.B = rbeta(n.draws, shape1 = 5 + treatment_conversions, shape2 = 15 + (treatment_total - treatment_conversions))
#)

# Define the generative model
generative.model <- function(p.A, p.B, control_total, treatment_total) {
  conversions.A <- rbinom(1, control_total, p.A)
  conversions.B <- rbinom(1, treatment_total, p.B)
  c(conversions.A = conversions.A, conversions.B = conversions.B)
}

# Get simulation data
sim.data <- as.data.frame( t(sapply(1:n.draws, function(i) {
  generative.model(prior$p.A[i], prior$p.B[i], control_total, treatment_total)}
)))

# Use likelihood as opposed to exact match to calculate posterior
likelihood.A <- dbinom(control_conversions, size = control_total, prob = prior$p.A)
likelihood.B <- dbinom(treatment_conversions, size = treatment_total, prob = prior$p.B)

posterior_weights <- likelihood.A * likelihood.B

posterior <- prior[posterior_weights > 0, ] 

# Calculate posterior means
mean_A <- mean(posterior$p.A)
mean_B <- mean(posterior$p.B)

# Visualize the results, two ways
par(mfrow = c(1,1))

hist(posterior$p.A, main = "Posterior: Control Group", xlab = "Conversion Rate (Control)", col=c("#F1F2F4"))
abline(v = mean_A, col = "#63AFD3", lwd = 2)

hist(posterior$p.B, main = "Posterior: Treatment Group", xlab = "Conversion Rate (Treatment)", col=c("#F1F2F4"))
abline(v = mean_B, col = "#41825D", lwd = 2) 

plot(posterior,main = "Success for Control & Treatment",
     xlab="Conversion Rate (Control)", ylab="Conversion Rate (Treatment)")

hist(posterior$p.A - posterior$p.B, main="Posterior --
converted A - converted B")
(expected.avg.mean.diff <- mean_A - mean_B)
abline(v = expected.avg.mean.diff , col = "purple", lwd =2)

# Get credible interval
credible_interval_A <- quantile(posterior$p.A, probs = c(0.025, 0.975))
credible_interval_B <- quantile(posterior$p.B, probs = c(0.025, 0.975))

print(credible_interval_A)
print(credible_interval_B)

# Calculate posterior means
mean_A <- mean(posterior$p.A)
mean_B <- mean(posterior$p.B)

# Print the means
cat("Mean conversion rate for Control:", mean_A, "\n")
cat("Mean conversion rate for Treatment:", mean_B, "\n")

library(ggplot2)

# Create a data frame to store the posterior probabilities and group labels
posterior_df <- data.frame(
  Probability = c(posterior$p.A, posterior$p.B),
  Group = c(rep("Control", nrow(posterior)), rep("Treatment", nrow(posterior)))
)



# Create the histogram plot with ggplot
ggplot(posterior_df, aes(x = Probability, fill = Group)) +
  geom_histogram(position = "identity", alpha = 0.8, bins = 30) +  
  labs(title = "Posterior Distributions of Conversion Rates",
       x = "Conversion Probability",
       y = "Density") +
  scale_fill_manual(values = c("Control" = "#63AFD3", "Treatment" = "#41825D")) +  
  theme_minimal()

