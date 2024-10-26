Next, we performed Bayesian linear regression on the patient data provided. The original data had 28 variables. Note that, at this point, we were using the entire patient dataset and had not filtered for the patients in patients.csv. We took LOSdays as our target, and all other variables except hadm_id and LOSgroupNum as predictors, but left hadm_id in the dataframe for now to facilitate splitting the dataset later. Religion and ethnicity were dropped because we did not believe them to be significant. ExpiredHospital was also dropped because predicting how long a patient will stay at the hospital after their death seemed irrelevant. To reduce the risk of multicollinearity and high variance inflation factor when computing pairwise interactions, numeric variables were centered. High-cardinality categorical variables were encoded using binary encoding, and low-cardinality categorical variables were one-hot encoded. After encoding, we had 56 predictors.

Next, we computed pairwise interactions. The addition of pairwise interactions increased the number of predictors from 56 to 1596. The next task was feature selection, for which we used mltxend’s SequentialFeatureSelector. We initially tried a number of other feature selection techniques, including assessing mutual information scores, random forest models, assessing correlation coefficients, inspecting covariance matrix visualizations, computing VIF, and stepwise selection on subsets of variables. This added an extra layer of complexity to the task by necessitating decision making and a lot of trial and error. Using a sequential feature selector allowed us to outsource some of the decision-making without compromising the quality of our feature selection. We ran deterministic linear regression to compare the quality of the features selected by different methods, and the sequential feature selector yielded the highest R2 score. It is worth noting that the R2 was still not particularly high (0.1631), but we attribute this to the constraint on the number of features and the general trend of lower R2 values in social science research compared to other domains. The five features selected were 'NumTransfers', 'NumCallouts admit_type_EMERGENCY', 'NumDiagnosis NumTransfers', 'NumChartEvents admit_type_NEWBORN', 'admit_type_NEWBORN admit_location_CLINIC, and REFERRAL/PREMATURE'.

Our dataset was then split into two subsets: the data on which we performed Bayesian inference (patients in patients.csv) and the rest of the data. We performed deterministic linear regression on the latter, using our five selected features as predictors and LOSdays as the target. The purpose of this was to use the intercept and coefficients to inform the means of our normal priors when we perform Bayesian linear regression. This approach falls under the larger umbrella of empirical Bayesian methods (Casella 1992). As stated previously, it is important to note that here we did not use the data on which we then performed Bayesian inference. Below is a summary of the results.

#### Table 1: Coefficients for Empirical Bayesian Analysis


| Coefficients | Estimate    | Pr(>\|t\|) |
|--------------|-------------|------------|
| (Intercept)  | 1.016e+01   | < 2e-16    |
| x1           | -1.469e+00  | < 2e-16    |
| x2           | -1.424e+01  | < 2e-16    |
| x3           | 6.560e-03   | < 2e-16    |
| x4           | 1.465e-02   | < 2e-16    |
| x5           | 1.421e+01   | < 2e-16    |

**Residual standard error:** 11.4 on 55994 degrees of freedom  
**Multiple R-squared:** 0.1632, **Adjusted R-squared:** 0.1631 

--- 
&NewLine;

We performed Bayesian linear regression using Python's `pymc` library. For the intercept and coefficients, we used normal priors with the above coefficient estimations for the means. To reflect uncertainty about our previous computations, we set variances to 100 to make the priors less informative. An exponential prior was selected for the standard deviation. The likelihood is defined as a normal distribution with mean computed by our regression formula. Below are the plots of our posterior distributions and sampling chains. The red lines indicate the high density intervals.


![ ]("trace_plot.png")
*Figure X: Kernel density estimates and sampling chains for posterior distributions.*

For the following, we use "coefficient” to represent the overall posterior distribution. The negative coefficient for number of transfers suggests that more transfers was correlated with a shorter overall stay. This seemeds surprising at first, but perhaps patients who were frequently transferred were less likely to stay in one place for a long period of time. The interaction between NumCallouts and admit_type_EMERGENCY had a large negative coefficient relative to the other variables. This indicates that, when a patient entered the hospital via emergency admission, more callouts was correlated with a shorter hospital stay. We hypothesize that this could be for two reasons. Firstly, that more callouts indicated that a patient received more immediate care, or that patients with more callouts were more likely to die shortly after reaching the hospital. The slightly positive coefficient for the interaction between NumDiagnosis and NumTransfers was interesting, as transfers alone had a negative coefficient. Perhaps transfers due to new diagnoses had an inverse effect compared to transfers alone. The small positive coefficient for the interaction between NumChartEvents and admit_type_NEWBORN suggested that, for newborn admissions, more chart events were correlated with a slightly longer stay. This makes sense, as more chart events could be indicative of premature births or other complications.. The interaction between admit_type_NEWBORN and admit_location_CLINIC REFERRAL/PREMATURE also had a higher positive coefficient, supporting our hypothesis that premature births led to longer hospital stays.

By sampling from the posterior distributions, we computed the probability of a patient staying in the hospital for more than two days to be 73.7%.  



