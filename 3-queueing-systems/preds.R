
library(gsl)

# Running Linear Regression
df <- 
  read.csv("/3-queueing-systems/reg.csv")
model= lm(serv_rate.server~arr_rate.server, data = df) 
summary(model)

plot(df$arr_rate.server,df$serv_rate.server, pch = 16, col = "blue"
       , main="a=0.308737 \n 
b=0.996213", ylab="Servers Rate", xlab = "Arrival Rate") 
abline(model)


# Using Lambert W function to get c estimate 
df2 <- 
  read.csv("/3-queueing-systems/reg_ests.csv")

a=0.308737
b=0.996213

df2$c_5 = (1/(a*5))*(lambert_W0(((df2$arrival_rate*5)/(1-df2$X5m))*exp(df2$arrival_rate*5))-(b*df2$arrival_rate*5))


print(df2)

write.csv(df2, "/3-queueing-systems/c_pred.csv", row.names=FALSE)

