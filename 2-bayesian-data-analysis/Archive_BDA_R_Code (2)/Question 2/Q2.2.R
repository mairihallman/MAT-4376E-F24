set.seed(1111) #for repolicability
n.draws <- 300000
 
summary_data <- ab_data.cleaned %>%
  group_by(group) %>%
  summarise(
    converted = sum(converted),     # Total number of conversions
    users = n()                        # Total number of users
  )

print(summary_data)

users.control <- summary_data$users[summary_data$group == 'control']
users.treatment <- summary_data$users[summary_data$group == 'treatment']

converted.A <- summary_data$converted[summary_data$group == 'control']
converted.B <- summary_data$converted[summary_data$group == 'treatment']

prior <- data.frame(
  p.A = rbeta(n.draws, shape1 = 2 + converted.A, shape2 = 20 + (users.control - converted.A )),
  p.B = rbeta(n.draws, shape1 = 2 + converted.A, shape2 = 20 + (users.treatment - converted.B ))
)

generative.model <- function(p.A, p.B, users.control, users.treatment) {
  control <- rbinom(1, users.control, p.A)
  treatment <- rbinom(1, users.treatment, p.B)
  return(c(control = control, treatment = treatment))
}

results <- apply(prior, 1, function(row) {
  p.A <- row["p.A"]
  p.B <- row["p.B"]
  generative.model(p.A, p.B, users.control, users.treatment)
})

results_df <- as.data.frame(t(results))
colnames(results_df) <- c("control", "treatment")

# Debugging output
print(paste("Converted A:", converted.A))
print(paste("Converted B:", converted.B))
print(head(results_df))

#Use likelihood as opposed to exact match to calculate posterior
likelihood.A <- dbinom(converted.A, size = users.control, prob = prior$p.A)
likelihood.B <- dbinom(converted.B, size = users.treatment, prob = prior$p.B)

posterior_weights <- likelihood.A * likelihood.B

posterior <- prior[posterior_weights > 0, ]

# Check the output
print(dim(posterior))  # Check dimensions of posterior
head(posterior)        # Show a few rows of posterior

meanA <- (mean(posterior$p.A))
meanB <- (mean(posterior$p.B))

#Graphing?

par(mfrow = c(1,1))
hist(posterior$p.A, main = "Posterior -- control converted",
     xlab="p.A")
abline(v=meanA, col = "darkgreen", lwd = 2)
hist(posterior$p.B, main = "Posterior -- treatment converted",
     xlab="p.B")
abline(v=meanB, col = "darkblue", lwd = 2)
plot(posterior,main = "Success for converted types control and treatment",
     xlab="p.A", ylab="p.B")

hist(posterior$p.A - posterior$p.B, main="Posterior --
converted A - converted B")
(expected.avg.mean.diff <- meanA - meanB)
abline(v = expected.avg.mean.diff , col = "purple", lwd =2)

library(ggplot2)
# Create a data frame to store the posterior probabilities and group labels
posterior_df <- data.frame(
  Probability = c(posterior$p.A, posterior$p.B),
  Group = c(rep("A", nrow(posterior)), rep("B", nrow(posterior)))
)

# Create the histogram plot with ggplot
#from Sam
ggplot(posterior_df, aes(x = Probability, fill = Group)) +
  geom_histogram(position = "identity", alpha = 0.8, bins = 30) +  
  labs(title = "Posterior Distributions of Conversion Rates",
       x = "Conversion Probability",
       y = "Density") +
  scale_fill_manual(values = c("A" = "#63AFD3", "B" = "#41825D")) +  
  theme_minimal()
