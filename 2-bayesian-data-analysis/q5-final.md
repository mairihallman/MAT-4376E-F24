Next, we aim to perform Bayesian linear regression on the patient data provided. The original data has 28 variables. Note that, at this point, we are using the entire patient dataset and have not filtered for the patients in patients.csv. We take LOSdays as our target, and all other variables except hadm_id and LOSgroupNum as predictors, but leave hadm_id in the dataframe for now to facilitate splitting the dataset laters. Religion and ethnicity are dropped as we don’t believe them to be significant. ExpiredHospital is also dropped because predicting how long a patient will stay at the hospital after their death seems unhelpful. To reduce the risk of multicollinearity and high VIF when computing pairwise interactions, numeric variables are centered. High-cardinality categorical variables are encoded using binary encoding, and low-cardinality categorical variables are one-hot encoded. After encoding, we have 56 predictors.

Next, we compute pairwise interactions. The addition of pairwise interactions increases the number of predictors from 56 to 1596. The next task is feature selection, for which we use mltxend’s SequentialFeatureSelector. We initially tried a number of other feature selection techniques, including assessing mutual information scores, random forest models, assessing correlation coefficients, inspecting covariance matrix visualizations, computing VIF, and stepwise selection on subsets of variables. These proved to be prescriptive rather than descriptive, adding an extra layer of complexity to the task by necessitating decision making and a lot of trial and error. Using a sequential feature selector allowed us to outsource some of the decision-making without compromising the quality of our feature selection. We ran deterministic linear regression to compare the quality of the features selected by different methods, and the sequential feature selector yielded the highest R2 score. It is worth noting that the R2 was still not particularly high (0.1631), but we attribute this to the constraint on the number of features and the general trend of lower R2 values in social science research compared to other domains. The five features selected are'NumTransfers', 'NumCallouts admit_type_EMERGENCY', 'NumDiagnosis NumTransfers', 'NumChartEvents admit_type_NEWBORN', 'admit_type_NEWBORN admit_location_CLINIC REFERRAL/PREMATURE'.

Our dataset is then split into two subsets: the data on which we will perform Bayesian inference (patients in patients.csv) and the rest of the data. We perform deterministic linear regression on the latter, using our five selected features as predictors and LOSdays as the target. The purpose of this is to use the intercept and coefficients to inform the means of our normal priors when we perform Bayesian linear regression. This approach falls under the larger umbrella of empirical Bayesial methods (Casella 1992). As stated previously, it is important to note that here we are not using the data on which we will be performing Bayesian inference. Below is a summary of the results.

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

We are now ready to perform Bayesian linear regression. For this, we use Python's `pymc` library. For the intercept and coefficients, we use normal priors with the above coefficient estimations for the means. To reflect uncertainty about our previous computations, we set variances to 100 to make the priors less informative. We use an exponential prior for the standard deviation. The likelihood is defined as a normal distribution with mean computed by our regression formula. Below are the plots of our posterior distributions and sampling chains.

![ ]("trace_plot.png")
*Figure X: Kernel density estimates and sampling chains for posterior distributions.*

For the following, we will use “coefficient” to represent the overall posterior distribution. The negative coefficient for number of transfers suggests that more transfers is correlated with a shorter overall stay. This seems surprising at first, but perhaps patients who are frequently transferred are less likely to stay in one place. The interaction between NumCallouts and admit_type_EMERGENCY has a large negative coefficient relative to the other variables. This indicates that, when a patient enters the hospital via emergency admission, more callouts is correlated with a shorter hospital stay. We hypothesize that this could be for two reasons. Firstly, that more callouts indicates that a patient receives more immediate care, or that patients with more callouts are more likely to die shortly after reaching the hospital. The slightly positive coefficient for the interaction between NumDiagnosis and NumTransfers is interesting, as transfers alone had a negative coefficient. The small positive coefficient for the interaction between NumChartEvents and admit_type_NEWBORN suggests that, for newborn admissions, more chart events is correlated with a slightly longer stay. This makes sense, as more chart events could be indicative of premature births or other complications requiring a longer stay. The interaction between admit_type_NEWBORN and admit_location_CLINIC REFERRAL/PREMATURE also has a higher positive coefficient, supporting our hypothesis that premature births lead to longer hospital stays.

By sampling from the posterior distributions, we compute the probability of a patient staying in the hospital for more than two days to be 73.7%.  


