# Task 4

The next area of analysis is in regards to data collected from the hospital. First we will be defining the data, and explaining what some of the values mean. In the second portion we wil be analyzing. We have divided up the dataset into three distinct sections; Precursor Data, Geographical Data, Variable Data. These are divisions make by the type of the data provided (Category vs Numeric) as well as the type of actional markers we can recommend.

## Data Dictionary

### Precursor Data

Each patients arrives to the hospital in a given state. Each patient is assigned a gender, age, marital status, etc. These are data points which cannot be controlled by the hospital. Below is the data dictionary for this section.


| Name | Variable Type | Description |
| --- | --- | --- |
| gender | char | Gender expressed as M or F |
| age | integer | Age of patient expressed at integer |
| insurance | string | Self paid, Private, Medicaid or Medicare |
| religion | string | Self identified religion of patient |
| marital_status | string | Self identified stats (Divorced, Single, Married, etc) |
| ethnicity | string | Reorganized to Categories White, Black, Asian, Hispanic, Other and Unavailable |


 !!! Notes Originally ethnicity was expressed as subcategories ( eg. ASIAN - Chinese ). Little insight could be drawn from such small subdivision so it was oped to categorize them into broader categories. Unavailable has remained the same. 


### Positional Data

Each hospital is located in different parts of the United States, and will be pushed by different factors due to that location. Further more each patient will be inducted into different parts of the hospital. A patient entering emerge will have a different experience to those entering newborn. 

| Name | Variable Type | Description |
| --- | --- | --- |
| hadm_id | integer | Identifier for particular visit to hospital |
| admit_type | string | Categorized admission as - Emergency, Elective, Newborn Urgent |
| admit_location | string | Physical location the patient was admitted to (Ex. Transfer from HOSP/Extram) |

With this section of data we will look into patients records across time, and throughout different parts of the hospital. 


### Variable Data

This is data that in some way could change via workflow changes within the hospital, and as mistakes are made by staff. The number of labs for instance. It is possible that every hospital currently operates with the utmost efficiency with no wasted lab results. This is incredibly unlikely however, especially when excessive lab assessment's lengthen the stay of the patient. What will be shown later in this report is a statistical approach to which variables may be of higher importance to the length of each patients stay.

| Name | Variable Type | Description |
| --- | --- | --- |
| AdmitDiagnosis | string | Diagnosis upon admission |
| NumCallouts | integer | Number of clinicians *called out* of their working hours |
| NumDiagnosis| float | ICD-9 Code Diagnosis |
| NumProcs         | float | ICD-9 Code Procedures|
| AdmitProcedure   | string | Procedure performed upon admission |
| NumCPTevents     | float | CPT Code labeled events |
| NumInput         | float| ICD-9 Code of inputs (e.g., fluids) |
| NumLabs          | float |ICD-9 Code of lab tests performed |
| NumMicroLabs     | float| ICD-9 of microbiology lab tests |
| NumNotes         | float| Number of clinical notes  |
| NumOutput        | float | ICD-9 Code of outputs (e.g., urine) |
| NumRx            | float | Number of prescribed medications |
| NumProcEvents    | float | ICD-9 Procedure Code |
| NumTransfers     | float | ### Transfer code |
| NumChartEvents   | float | #### |
| ExpiredHospital  | boolean | Whether the patient died in hospital |
| TotalNumInteract | float | number of interactions |

You will note the use of coding systems such as ICD-9. These codes are standardized by organization bodies such as the NIH and are used across hospitals.
For more information see [PubMed](https://pmc.ncbi.nlm.nih.gov/articles/PMC3865615/#:~:text=The%20ICD%2D9%2DCM%20system,Diseases%20(ICD%2D9).)


## Analytics

### Precursor Data

Due to the fact that this data is prior to the patients arrival at the hospital, there is little that can be said for actionable results. Instead we will seek to understand more about the patient base.

**Gender**

The key not is the greater proportion of men making up 55% of the patient base. 

| Men | Women |
| --- | --- |
| 32950 | 26026 |

This proportion is interesting as it is 5% offset from the national average. 

**Age**

!!! Add histogram that looks nice

For ages strictly greater than 0 we have a skewed distribution shown in figure ## with mean equal to 61 and standard deviation equal to 16; comparing this to the average age in the United States being 38. This is not unexpected as people of more age are more likely to posses ailments requiring hospital visitation. 

Once we incorporate the data for ages less than 1 ( eg newborn / infant ), we can see age no longer follows a normal distribution. Over 8000 newborns or infants were admitted though the duration of the study. 

**Insurance**

The most common form of insurance at 48% is Medicare, followed closely by Private insurance at 38%. Below is a pie-chart breaking down the insurance categories.

FIGURE

**Religion**

Along the trend of trying to determine patient data, we compare the distribution of religious secs compared to the national average. We see that compared to the national average, 3% less patients are Catholic. This falls below statistical significant range. We can say then that the religious distribution of patient data follows that of national averages.

**Marital Status**

As shown in the pie-charts below, 50% of patients are married. This is similar to 53% national average of married individuals. 

**Ethnicity**

As mentioned above, the ethnicity was simplified to 6 categories. According to the pie-chart below, 70% of patients identify as white. This is 10% higher than the national average. This leads us to believe that this hospital operates is a predominantly white area. This idea is supported by the difference between patient ethnicity percentage and the national average. 


### Positional Data

**Admit Type**

Admission types will follow one of four choices, Emergency, Newborn, Elective, and Urgent. The pie-chart can be found below.

The vast majority of patients enter as emergency (71%). 

**Admit Location**

Within the Hospital there are 8 known locations a patient can be admitted to. It follow from the previous section that the majority of patients will be entering via the Emergency Room, this corroborates that theory, in total 38% of patients.


### Variable Data

It is important to note that any correlational data will be done in the next section as a precursor to the Bayesian Linear Regression Analysis.

Until then we will look into the frequences of some key data points withing the Variable Data.

**NumDiagnosis**

- most common diagnosis


**NumProcedure**

- most common procedure && what different approaches are compared to the NUMDiagnosis


**NumInputs & Num OutPuts**

- Comparing the Inputs to Outputs


**Num Transfers**

- This becomes the biggest correlation with Lenghth of Stay, go over the average length of stay in diagnosis. 


**Expired in Hospital**

- Age of people who pass, most common procedures being done. This provides the customer with a list of things that are risk
- They may not be able to do anything but its good to flag it








Insights can be extracted from this dataset from a comparison to the average. Because this hospital operates in the United States, we compare the precursor data to data released by the United States Census Bueraum and [US Religion Census](https://www.usreligioncensus.org/sites/default/files/2023-10/2020_US_Religion_Census.pdf) [PEW](https://www.pewresearch.org/social-trends/2021/10/05/rising-share-of-u-s-adults-are-living-without-a-spouse-or-partner/) [USAFACTS](https://usafacts.org/articles/the-diverse-demographics-of-asian-americans/)

# GO OFF OF [MIMIC Website](https://mimic.mit.edu/docs/iii/tables/admissions/)
EXTRAM - Expanded trauma