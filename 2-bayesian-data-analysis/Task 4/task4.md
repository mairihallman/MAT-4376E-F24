## Section 4

The next area of analysis is in regards to data collected from the hospital. First we will be defining the data, and explaining what some of the values mean. In the second portion we wil be analyzing. We have divided up the dataset into three distinct sections; Precursor Data, Geographical Data, Variable Data. These are divisions make by the type of the data provided (Category vs Numeric) as well as the type of actionable markers we can recommend.

### Data Dictionary

#### Precursor Data

Each patients arrives to the hospital in a given state. Each patient is assigned a gender, age, marital status, etc. These are data points which cannot be controlled by the hospital. Below is the data dictionary for this section.


| Name | Variable Type | Description |
| --- | --- | --- |
| gender | char | Gender expressed as M or F |
| age | integer | Age of patient expressed at integer |
| insurance | string | Self paid, Private, Medicaid or Medicare |
| religion | string | Self identified religion of patient |
| marital_status | string | Self identified stats (Divorced, Single, Married, etc) |
| ethnicity | string | Reorganized to Categories White, Black, Asian, Hispanic, Other and Unavailable |


> Note: Originally ethnicity was expressed as subcategories ( eg. ASIAN - Chinese ). Little insight could be drawn from such small subdivision so it was oped to categorize them into broader categories. Unavailable has remained the same. 


#### Positional Data

Each hospital is located in different parts of the United States, and will be pushed by different factors due to that location. Further more each patient will be inducted into different parts of the hospital. A patient entering emerge will have a different experience to those entering newborn. 

| Name | Variable Type | Description |
| --- | --- | --- |
| hadm_id | integer | Identifier for particular visit to hospital |
| admit_type | string | Categorized admission as - Emergency, Elective, Newborn Urgent |
| admit_location | string | Physical location the patient was admitted to (Ex. Transfer from HOSP/Extram) |

With this section of data we will look into patients records across time, and throughout different parts of the hospital. 


#### Variable Data

This is data that in some way could change via workflow changes within the hospital, and as mistakes are made by staff. The number of labs for instance. It is possible that every hospital currently operates with the utmost efficiency with no wasted lab results. This is incredibly unlikely however, especially when excessive lab assessment's lengthen the stay of the patient. What will be shown later in this report is a statistical approach to which variables may be of higher importance to the length of each patients stay.

| Name | Variable Type | Description |
| --- | --- | --- |
| AdmitDiagnosis | string | Diagnosis upon admission |
| NumCallouts | integer | Number of clinicians *called out* of their working hours |
| NumDiagnosis| float | Aggregate Number of Procedures |
| NumProcs | float | Aggregate Number of Procedures |
| AdmitProcedure | string | Procedure performed upon admission |
| NumCPTevents | float | CPT Code labeled events |
| NumInput | float| Aggregate Number of Inputs ( eg Medication Administered ) |
| NumLabs | float | Aggregate Number of Labs|
| NumMicroLabs | float| Aggregate Number of Procedures Micro Labs|
| NumNotes | float| Aggregate Number of Clinical Notes |
| NumOutput | float | Aggregate Number of Procedures Outputs|
| NumRx | float | Number of prescribed medications |
| NumProcEvents | float | Aggregate Number of Procedures|
| NumTransfers | float | Aggregate Number of Transfers |
| NumChartEvents | float |Aggregate Number of Procedures |
| ExpiredHospital | boolean | Whether the patient died in hospital |
| TotalNumInteract | float | Aggregate Number of Procedures |


### Analytics

#### Precursor Data

Due to the fact that this data is prior to the patients arrival at the hospital, there is little that can be said for actionable results. Instead we will seek to understand more about the patient base.

**Gender**

The key not is the greater proportion of men making up 55% of the patient base. 

| Men | Women |
| --- | --- |
| 32950 | 26026 |

This proportion is interesting as it is 5% offset from the national average. 

**Age**

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

As mentioned above, the ethnicity was simplified to 6 categories. According to the pie-chart below, 70% of patients identify as white. This is 10% higher than the national average. This idea is supported by the difference between patient ethnicity percentage and the national average. 

!(Histogram)[precursor_histogram.png]
!(Pie Charts)[precursor_piechart.png]

#### Positional Data

**Admit Type**

Admission types will follow one of four choices, Emergency, Newborn, Elective, and Urgent. The pie-chart can be found below.

The vast majority of patients enter as emergency (71%). 

**Admit Location**

Within the Hospital there are 8 known locations a patient can be admitted to. It follow from the previous section that the majority of patients will be entering via the Emergency Room, this corroborates that theory, in total 38% of patients.


#### Variable Data

It is important to note that any correlational data will be done in the next section as a precursor to the Bayesian Linear Regression Analysis.

Until then we will look into the frequences of some key data points withing the Variable Data.

**AdmitDiagnosis**

Though the duration of the data over 15 thousand unique diagnosis's were found, nearly half of which were Newborn. Due to the nuances many diagnosis's entail, we will analysis the diagnosis further by filtering by keywords. If a keyword is detected, the entry will be flagged and categorized accordingly. 

In total this system flagged:

| Category | NumFlagged_Items | Keywords  |
| --- | --- | --- |
| Other | 43133 | N/A  |
| Diagnostic  |  3991 | scan, x-ray, ultrasound, mri, ct, imaging, biopsy, diagnostic  |
| Preventive | 2683 | vaccination, screening, check-up, preventive, immunization |
| Cardiovascular | 2587 | angioplasty, stent, bypass, pacemaker, cardiac, heart |
| Surgical | 2008 | surgery, operation, resection, excision, laparotomy, amputation, biopsy |
| Gastrointestinal | 1760 | endoscopy, colonoscopy, gastrectomy, biopsy, bowel, liver  |
| Renal | 1417 | dialysis, nephrectomy, catheter, kidney, bladder, renal  |
| Therapeutic |  1229 | therapy, treatment, chemotherapy, radiation, rehabilitation, transfusion |
| Respiratory  | 154 | ventilation, tracheotomy, bronchoscopy, thoracotomy, oxygen, pulmonary   |
| Musculoskeletal  | 14 | arthroscopy, joint, spine, orthopedic, tendon, ligament |

**AdmitProcedure**

We use a similar filter as above to analyze the procedures recorded.

| Category | NumFlagged_Items | Keywords |
| --- | --- | --- |
| Other | 43133 | N/A |
| Diagnostic| 3991 | scan, x-ray, ultrasound, mri, ct, imaging, biopsy, diagnostic |
| Preventive  | 2683 | vaccination, screening, check-up, preventive, immunization |
| Cardiovascular   | 2587 | angioplasty, stent, bypass, pacemaker, cardiac, heart |
| Surgical| 2008 | surgery, operation, resection, excision, laparotomy, amputation, biopsy  |
| Gastrointestinal |  1760 | endoscopy, colonoscopy, gastrectomy, biopsy, bowel, liver |
| Renal  |  1417 | dialysis, nephrectomy, catheter, kidney, bladder, renal  |
| Therapeutic |  1229 | therapy, treatment, chemotherapy, radiation, rehabilitation, transfusion |
| Respiratory  | 154 | ventilation, tracheotomy, bronchoscopy, thoracotomy, oxygen, pulmonary   |
| Musculoskeletal  |  14 | arthroscopy, joint, spine, orthopedic, tendon, ligament |

Although the majority of procedures could not be flagged, this tables still gives us an understanding how many of each type of procedure are completed and should be used to find proportions of categories, as opposed to the raw size. 

!(Admit & Procedure Piechart)[variable_piechart.png]


**Expired in Hospital**

Thanks in part to the categories we defined above, we can go through and analyses which groups of procedures and diagnosis have the highest mortality rate associated with them. It is important to note that this does not imply correlation. A particular ailment may have a high lethality despite the procedures complete not because of them. Below are two bar plots showing the number of occurrences than a particular diagnosis or procedure lead to expiry. However more importantly, as we establish above, the categories are designed to be a guideline for probabilities. As such the second bar graph shows the likelihood that given a particular diagnosis or procedure that you would expire within the hospital.

!(Num of Occurance)[variable_barplot.png]
!(Likelihood of Occurance)[variable_barplot_likelihood.png]







Insights can be extracted from this dataset from a comparison to the average. Because this hospital operates in the United States, we compare the precursor data to data released by the United States Census Bueraum and [US Religion Census](https://www.usreligioncensus.org/sites/default/files/2023-10/2020_US_Religion_Census.pdf) [PEW](https://www.pewresearch.org/social-trends/2021/10/05/rising-share-of-u-s-adults-are-living-without-a-spouse-or-partner/) [USAFACTS](https://usafacts.org/articles/the-diverse-demographics-of-asian-americans/)
