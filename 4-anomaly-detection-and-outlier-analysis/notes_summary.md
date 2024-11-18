# DUDADS Chapter 26 Summary

### 26.1 Overview

- **Importance of Anomaly Detection:**
  - Essential for identifying irregular values in large datasets.
  - Critical in fields like cybersecurity and quality control.
  - Anomalies can indicate fraud, attacks, or data errors.

- **Definitions:**
  - **Outlying Observations:** Data points that are atypical compared to others.
  - **Outliers:** Observations that are dissimilar or contradict known dependencies.

- **Challenges in Anomaly Detection:**
  - Anomalies are infrequent and often masked by noise.
  - The boundary between normal and anomalous is often unclear.
  - Removing outliers without analysis can lead to misleading results.

- **Detection Methods:**
  - **Supervised Learning:** Uses labeled data to build predictive models.
  - **Unsupervised Learning:** Identifies outliers based on behavior comparison without prior labels.

- **Common Outlier Detection Tests:**
  - Tukey’s boxplot test
  - Grubbs test
  - Mahalanobis distance
  - Chi-square test
  - Clustering-based methods (e.g., DBSCAN)

- **Statistical Learning Framework:**
  - Anomaly detection framed as a probability problem.
  - Requires understanding of normal behavior and potential anomalies.

- **Performance Evaluation:**
  - Metrics include precision, recall, and F1-score.
  - Confusion matrix used to assess true positives, true negatives, false positives, and false negatives.

- **Modern Approaches:**
  - Dimension reduction techniques (e.g., autoencoders) for anomaly detection.
  - Strategies for handling class imbalance (oversampling, undersampling).

- **Example Application:**
  - Illustrates concepts using a dataset with known outliers.
  - Visual inspection aids in identifying anomalies.

- **References and Further Reading:**
  - Cites various studies and resources for deeper understanding of methods and applications in anomaly detection.

### 26.2 Quantitative Approaches
  - **Anomaly Detection Methods**:
  - Two main types: 
    - Distance-based methods
    - Density-based methods

- **Distance-based Methods**:
  - Involves comparing observations based on distance metrics.
  - Common techniques include:
    - Distance to all observations
    - Distance to k-nearest neighbors (kNN)
    - Average and median distances to kNN
  - Anomaly detection function \( a: D \rightarrow \mathbb{R} \) ranks observations based on their anomaly score.
  - Threshold \( \alpha \) can be set to classify observations as anomalous.

- **Similarity Measures**:
  - Defined as a real-valued function to assess similarity between objects.
  - Common measures include:
    - Hellinger distance for probability distributions
    - Mahalanobis distance for assessing dissimilarity between observations.

- **Distance Methods Implementation**:
  - Mahalanobis distance used to identify anomalies in datasets.
  - Visualization techniques (histograms, boxplots) help in identifying outliers.

- **Density-based Methods**:
  - Focus on identifying anomalies in low-density regions.
  - Key algorithms include:
    - Local Outlier Factor (LOF)
    - DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
    - Isolation Forest

- **Local Outlier Factor (LOF)**:
  - Measures local deviation of an observation from its k-nearest neighbors.
  - Anomalies are identified based on local density comparisons.

- **DBSCAN**:
  - Groups nearby observations and labels those not in clusters as outliers.
  - Parameters include minimum number of points and radius for neighborhood.

- **Isolation Forest**:
  - Identifies anomalies by isolating observations through random partitioning.
  - Anomaly scores are derived from the depth of isolation in trees.

- **Strengths and Limitations**:
  - Distance-based methods may struggle with high-dimensional data.
  - Density-based methods are more effective with diverse patterns but less so with comparable densities.
  - Isolation Forest is efficient in terms of time and memory but can have high variance in scores.

### 26.3 Qualitative Approaches

  - **Qualitative Approaches Overview**
  - Non-numerical variables pose challenges for anomaly detection.
  - Categorical variables are measured on a nominal scale (e.g., color, language).
  - Central tendency is often represented by the mode; spread measures are less straightforward.

- **Categorical Variables**
  - Dichotomous features have two levels; polytomous variables have more than two.
  - Regression on categorical variables is termed multinomial logistic regression.
  - Common distance measures are not suitable for qualitative data.

- **Anomaly Detection Methods**
  - Two specific methods for categorical anomaly detection are introduced: 
    - Attribute Value Frequency (AVF) Algorithm
    - Greedy Algorithm

- **Attribute Value Frequency (AVF) Algorithm**
  - Fast and simple method for detecting outliers in categorical data.
  - Outliers are defined as infrequent observations in the dataset.
  - AVF score is calculated based on the frequency of feature levels.
  - A low AVF score indicates a higher likelihood of being an outlier.
  - The algorithm's complexity is O(n*p).

- **Greedy Algorithm**
  - Efficiently identifies candidate anomalous observations.
  - Works by minimizing the entropy of the dataset after removing potential outliers.
  - Steps include:
    1. Initialize the set of outliers as empty.
    2. Compute the entropy of the current dataset.
    3. Temporarily remove each normal observation to assess its impact on entropy.
    4. Add the observation that maximizes entropy reduction to the outlier set.
    5. Repeat until the desired number of outliers is identified.
  - Scalable for large datasets with appropriate frameworks.

### 26.4 Anomalies in High-Dimensional Data

- **High-Dimensional Data Challenges**
  - Real datasets often have hundreds or thousands of features.
  - Classical anomaly detection methods rely on proximity (distance), which becomes less effective as dimensions increase (curse of dimensionality).
  - In high-dimensional spaces, observations tend to be isolated and sparse, complicating outlier detection.

- **Key Challenges in Anomaly Detection**
  - Distance becomes irrelevant in high dimensions.
  - Most points in high-dimensional datasets can appear as outliers.
  - Effective methods must manage sparse data, provide interpretability, allow for comparison of anomalies, and consider local data behavior.

- **Projection Methods**
  - Dimension reduction techniques, such as Principal Component Analysis (PCA), help mitigate the curse of dimensionality.
  - PCA transforms data into a lower-dimensional space while preserving variance.
  - The quality of PCA results depends on the number of retained principal components.

- **Distance-Based Outlier Detection**
  - The Distance-Based Outlier Basis Using Neighbours (DOBIN) algorithm identifies outliers by examining distances between nearest neighbors.
  - It constructs a basis of vectors that highlight distant observations.

- **Subspace Methods**
  - Subspace methods focus on exploring lower-dimensional projections of high-dimensional data to identify anomalies.
  - Feature Bagging is an example that aggregates anomaly scores from various projections.

- **Ensemble Methods**
  - Ensemble methods combine results from multiple anomaly detection algorithms to improve robustness and accuracy.
  - Two types of ensemble methods are:
    - **Sequential Ensembles**: Apply algorithms sequentially, adjusting weights based on previous results.
    - **Independent Ensembles**: Apply different algorithms independently and combine results for final classification.

- **Conclusion**
  - Anomaly detection in high-dimensional data is complex and requires careful consideration of methods and their applicability to specific datasets.
  - There is no one-size-fits-all solution; various methods have strengths and weaknesses depending on the data characteristics.