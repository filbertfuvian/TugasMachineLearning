# -*- coding: utf-8 -*-
"""Tubes2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MYYx3_hP4VBIoissxbBzMvm68HKJi7vE

# IF3070 Foundations of Artificial Intelligence | Tugas Besar 2

This notebook serves as a template for the assignment. Please create a copy of this notebook to complete your work. You can add more code blocks, markdown blocks, or new sections if needed.

Group Number: 04

Group Members:
- Rashid May (18222014)
- Lutfi Khairul Amal (18222018)
- Filbert Fuvian (18222024)
- Qady Zaka Raymaula (18222038)

## Import Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
# %pip install imbalanced-learn
from imblearn.over_sampling import SMOTE

"""## Import Dataset"""

df = pd.read_csv('https://drive.google.com/uc?id=14c4AEgg4ePy7ztmp1DapbNcjYvOKu7pq')

binary_features = ['IsDomainIP', 'HasObfuscation', 'IsHTTPS', 'HasTitle', 'HasFavicon',
                   'Robots', 'IsResponsive', 'HasDescription', 'HasExternalFormSubmit',
                   'HasSocialNet', 'HasSubmitButton', 'HasHiddenFields', 'HasPasswordField',
                   'Bank', 'Pay', 'Crypto', 'HasCopyrightInfo']

numerical_features = ['URLLength', 'DomainLength', 'CharContinuationRate', 'TLDLegitimateProb',
                      'URLCharProb', 'TLDLength', 'NoOfSubDomain', 'NoOfObfuscatedChar',
                      'ObfuscationRatio', 'NoOfLettersInURL', 'LetterRatioInURL', 'NoOfDegitsInURL',
                      'DegitRatioInURL', 'NoOfEqualsInURL', 'NoOfQMarkInURL', 'NoOfAmpersandInURL',
                      'NoOfOtherSpecialCharsInURL', 'SpacialCharRatioInURL', 'LineOfCode',
                      'LargestLineLength', 'DomainTitleMatchScore', 'URLTitleMatchScore',
                      'NoOfURLRedirect', 'NoOfSelfRedirect', 'NoOfPopup', 'NoOfiFrame',
                      'NoOfImage', 'NoOfCSS', 'NoOfJS', 'NoOfSelfRef', 'NoOfEmptyRef',
                      'NoOfExternalRef']

categorical_features = ['FILENAME', 'URL', 'Domain', 'TLD', 'Title']

"""# 1. Split Training Set and Validation Set

Splitting the training and validation set works as an early diagnostic towards the performance of the model we train. This is done before the preprocessing steps to **avoid data leakage inbetween the sets**. If you want to use k-fold cross-validation, split the data later and do the cleaning and preprocessing separately for each split.

Note: For training, you should use the data contained in the `train` folder given by the TA. The `test` data is only used for kaggle submission.
"""

train_set, val_set = train_test_split(df, test_size=0.2, random_state=42)

"""# 2. Data Cleaning and Preprocessing

This step is the first thing to be done once a Data Scientist have grasped a general knowledge of the data. Raw data is **seldom ready for training**, therefore steps need to be taken to clean and format the data for the Machine Learning model to interpret.

By performing data cleaning and preprocessing, you ensure that your dataset is ready for model training, leading to more accurate and reliable machine learning results. These steps are essential for transforming raw data into a format that machine learning algorithms can effectively learn from and make predictions.

We will give some common methods for you to try, but you only have to **at least implement one method for each process**. For each step that you will do, **please explain the reason why did you do that process. Write it in a markdown cell under the code cell you wrote.**

## A. Data Cleaning

**Data cleaning** is the crucial first step in preparing your dataset for machine learning. Raw data collected from various sources is often messy and may contain errors, missing values, and inconsistencies. Data cleaning involves the following steps:

1. **Handling Missing Data:** Identify and address missing values in the dataset. This can include imputing missing values, removing rows or columns with excessive missing data, or using more advanced techniques like interpolation.

2. **Dealing with Outliers:** Identify and handle outliers, which are data points significantly different from the rest of the dataset. Outliers can be removed or transformed to improve model performance.

3. **Data Validation:** Check for data integrity and consistency. Ensure that data types are correct, categorical variables have consistent labels, and numerical values fall within expected ranges.

4. **Removing Duplicates:** Identify and remove duplicate rows, as they can skew the model's training process and evaluation metrics.

5. **Feature Engineering**: Create new features or modify existing ones to extract relevant information. This step can involve scaling, normalizing, or encoding features for better model interpretability.

### I. Handling Missing Data

Missing data can adversely affect the performance and accuracy of machine learning models. There are several strategies to handle missing data in machine learning:

1. **Data Imputation:**

    a. **Mean, Median, or Mode Imputation:** For numerical features, you can replace missing values with the mean, median, or mode of the non-missing values in the same feature. This method is simple and often effective when data is missing at random.

    b. **Constant Value Imputation:** You can replace missing values with a predefined constant value (e.g., 0) if it makes sense for your dataset and problem.

    c. **Imputation Using Predictive Models:** More advanced techniques involve using predictive models to estimate missing values. For example, you can train a regression model to predict missing numerical values or a classification model to predict missing categorical values.

2. **Deletion of Missing Data:**

    a. **Listwise Deletion:** In cases where the amount of missing data is relatively small, you can simply remove rows with missing values from your dataset. However, this approach can lead to a loss of valuable information.

    b. **Column (Feature) Deletion:** If a feature has a large number of missing values and is not critical for your analysis, you can consider removing that feature altogether.

3. **Domain-Specific Strategies:**

    a. **Domain Knowledge:** In some cases, domain knowledge can guide the imputation process. For example, if you know that missing values are related to a specific condition, you can impute them accordingly.

4. **Imputation Libraries:**

    a. **Scikit-Learn:** Scikit-Learn provides a `SimpleImputer` class that can handle basic imputation strategies like mean, median, and mode imputation.

    b. **Fancyimpute:** Fancyimpute is a Python library that offers more advanced imputation techniques, including matrix factorization, k-nearest neighbors, and deep learning-based methods.

The choice of imputation method should be guided by the nature of your data, the amount of missing data, the problem you are trying to solve, and the assumptions you are willing to make.
"""

binary_imputer = SimpleImputer(strategy='constant', fill_value=0)
train_set[binary_features] = binary_imputer.fit_transform(train_set[binary_features])
val_set[binary_features] = binary_imputer.transform(val_set[binary_features])


numerical_imputer = SimpleImputer(strategy='median')
train_set[numerical_features] = numerical_imputer.fit_transform(train_set[numerical_features])
val_set[numerical_features] = numerical_imputer.transform(val_set[numerical_features])


train_set[categorical_features] = train_set[categorical_features].fillna('Unknown')
val_set[categorical_features] = val_set[categorical_features].fillna('Unknown')

"""### II. Dealing with Outliers

Outliers are data points that significantly differ from the majority of the data. They can be unusually high or low values that do not fit the pattern of the rest of the dataset. Outliers can significantly impact model performance, so it is important to handle them properly.

Some methods to handle outliers:
1. **Imputation**: Replace with mean, median, or a boundary value.
2. **Clipping**: Cap values to upper and lower limits.
3. **Transformation**: Use log, square root, or power transformations to reduce their influence.
4. **Model-Based**: Use algorithms robust to outliers (e.g., tree-based models, Huber regression).
"""

def winsorize(data, lower_percentile=1, upper_percentile=99):
    lower_bound = np.percentile(data, lower_percentile)
    upper_bound = np.percentile(data, upper_percentile)
    data = np.clip(data, lower_bound, upper_bound)
    return data

for feature in numerical_features:
    Q1 = train_set[feature].quantile(0.25)
    Q3 = train_set[feature].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    train_set[feature] = winsorize(train_set[feature].values)
    val_set[feature] = winsorize(val_set[feature].values)

"""### III. Remove Duplicates
Handling duplicate values is crucial because they can compromise data integrity, leading to inaccurate analysis and insights. Duplicate entries can bias machine learning models, causing overfitting and reducing their ability to generalize to new data. They also inflate the dataset size unnecessarily, increasing computational costs and processing times. Additionally, duplicates can distort statistical measures and lead to inconsistencies, ultimately affecting the reliability of data-driven decisions and reporting. Ensuring data quality by removing duplicates is essential for accurate, efficient, and consistent analysis.
"""

train_set.drop_duplicates(inplace=True)
val_set.drop_duplicates(inplace=True)

"""### IV. Feature Engineering

**Feature engineering** involves creating new features (input variables) or transforming existing ones to improve the performance of machine learning models. Feature engineering aims to enhance the model's ability to learn patterns and make accurate predictions from the data. It's often said that "good features make good models."

1. **Feature Selection:** Feature engineering can involve selecting the most relevant and informative features from the dataset. Removing irrelevant or redundant features not only simplifies the model but also reduces the risk of overfitting.

2. **Creating New Features:** Sometimes, the existing features may not capture the underlying patterns effectively. In such cases, engineers create new features that provide additional information. For example:
   
   - **Polynomial Features:** Engineers may create new features by taking the square, cube, or other higher-order terms of existing numerical features. This can help capture nonlinear relationships.
   
   - **Interaction Features:** Interaction features are created by combining two or more existing features. For example, if you have features "length" and "width," you can create an "area" feature by multiplying them.

3. **Binning or Discretization:** Continuous numerical features can be divided into bins or categories. For instance, age values can be grouped into bins like "child," "adult," and "senior."

4. **Domain-Specific Feature Engineering:** Depending on the domain and problem, engineers may create domain-specific features. For example, in fraud detection, features related to transaction history and user behavior may be engineered to identify anomalies.

Feature engineering is both a creative and iterative process. It requires a deep understanding of the data, domain knowledge, and experimentation to determine which features will enhance the model's predictive power.
"""

# Data Redundan (Ada feature yang merepresentasikan feature ini, contoh : URLLength, HasTitle)
# [ 'FILENAME','TLD', 'URL', 'Domain', 'Title']

# Data Jelek (Tidak make sense / tidak relevan)
# ['IsDomainIP', 'HasObfuscation', 'NoOfObfuscatedChar', 'ObfuscationRatio', 'NoOfDegitsInURL',
# 'DegitRatioInURL', 'NoOfEqualsInURL', 'NoOfQMarkInURL', 'NoOfAmpersandInURL', 'NoOfURLRedirect',
# 'NoOfSelfRedirect', 'NoOfPopup', 'NoOfiFrame', 'NoOfEmptyRef', 'DomainTitleMatchScore', 'URLTitleMatchScore']

dropped_features = ['FILENAME','TLD', 'URL', 'Domain', 'Title', 'IsDomainIP', 'HasObfuscation', 'NoOfObfuscatedChar', 'ObfuscationRatio', 'NoOfDegitsInURL',
                          'DegitRatioInURL', 'NoOfEqualsInURL', 'NoOfQMarkInURL', 'NoOfAmpersandInURL', 'NoOfURLRedirect',
                          'NoOfSelfRedirect', 'NoOfPopup', 'NoOfiFrame', 'NoOfEmptyRef', 'DomainTitleMatchScore', 'URLTitleMatchScore']


class DropFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, features_to_drop):
        self.features_to_drop = features_to_drop

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.drop(columns=self.features_to_drop, axis=1)


numerical_features = [
    'URLLength', 'DomainLength', 'CharContinuationRate', 'TLDLegitimateProb',
    'URLCharProb', 'TLDLength', 'NoOfSubDomain', 'NoOfLettersInURL',
    'LetterRatioInURL', 'NoOfOtherSpecialCharsInURL', 'SpacialCharRatioInURL',
    'LineOfCode', 'LargestLineLength', 'NoOfImage', 'NoOfCSS', 'NoOfJS',
    'NoOfSelfRef', 'NoOfExternalRef'
]

features_to_discretize = [
    'URLLength', 'DomainLength', 'LineOfCode', 'LargestLineLength',
    'NoOfLettersInURL', 'NoOfOtherSpecialCharsInURL', 'NoOfImage',
    'NoOfCSS', 'NoOfJS', 'NoOfSelfRef', 'NoOfExternalRef'
]

numerical_features = [feature for feature in numerical_features if feature not in features_to_discretize]

categorical_features = [feature + '_Category' for feature in features_to_discretize]

class Discretizer(BaseEstimator, TransformerMixin):
    def __init__(self, features_to_discretize, n_bins=3, labels=['Low', 'Medium', 'High']):
        self.features_to_discretize = features_to_discretize
        self.n_bins = n_bins
        self.labels = labels

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()
        for feature in self.features_to_discretize:
            X_copy[feature + '_Category'] = pd.cut(X_copy[feature], bins=self.n_bins, labels=self.labels)
        X_copy = X_copy.drop(columns=self.features_to_discretize)
        return X_copy

"""## B. Data Preprocessing

**Data preprocessing** is a broader step that encompasses both data cleaning and additional transformations to make the data suitable for machine learning algorithms. Its primary goals are:

1. **Feature Scaling:** Ensure that numerical features have similar scales. Common techniques include Min-Max scaling (scaling to a specific range) or standardization (mean-centered, unit variance).

2. **Encoding Categorical Variables:** Machine learning models typically work with numerical data, so categorical variables need to be encoded. This can be done using one-hot encoding, label encoding, or more advanced methods like target encoding.

3. **Handling Imbalanced Classes:** If dealing with imbalanced classes in a binary classification task, apply techniques such as oversampling, undersampling, or using different evaluation metrics to address class imbalance.

4. **Dimensionality Reduction:** Reduce the number of features using techniques like Principal Component Analysis (PCA) or feature selection to simplify the model and potentially improve its performance.

5. **Normalization:** Normalize data to achieve a standard distribution. This is particularly important for algorithms that assume normally distributed data.

### Notes on Preprocessing processes

It is advised to create functions or classes that have the same/similar type of inputs and outputs, so you can add, remove, or swap the order of the processes easily. You can implement the functions or classes by yourself

or

use `sklearn` library. To create a new preprocessing component in `sklearn`, implement a corresponding class that includes:
1. Inheritance to `BaseEstimator` and `TransformerMixin`
2. The method `fit`
3. The method `transform`

### I. Feature Scaling

**Feature scaling** is a preprocessing technique used in machine learning to standardize the range of independent variables or features of data. The primary goal of feature scaling is to ensure that all features contribute equally to the training process and that machine learning algorithms can work effectively with the data.

Here are the main reasons why feature scaling is important:

1. **Algorithm Sensitivity:** Many machine learning algorithms are sensitive to the scale of input features. If the scales of features are significantly different, some algorithms may perform poorly or take much longer to converge.

2. **Distance-Based Algorithms:** Algorithms that rely on distances or similarities between data points, such as k-nearest neighbors (KNN) and support vector machines (SVM), can be influenced by feature scales. Features with larger scales may dominate the distance calculations.

3. **Regularization:** Regularization techniques, like L1 (Lasso) and L2 (Ridge) regularization, add penalty terms based on feature coefficients. Scaling ensures that all features are treated equally in the regularization process.

Common methods for feature scaling include:

1. **Min-Max Scaling (Normalization):** This method scales features to a specific range, typically [0, 1]. It's done using the following formula:

   $$X' = \frac{X - X_{min}}{X_{max} - X_{min}}$$

   - Here, $X$ is the original feature value, $X_{min}$ is the minimum value of the feature, and $X_{max}$ is the maximum value of the feature.  
<br />
<br />
2. **Standardization (Z-score Scaling):** This method scales features to have a mean (average) of 0 and a standard deviation of 1. It's done using the following formula:

   $$X' = \frac{X - \mu}{\sigma}$$

   - $X$ is the original feature value, $\mu$ is the mean of the feature, and $\sigma$ is the standard deviation of the feature.  
<br />
<br />
3. **Robust Scaling:** Robust scaling is a method that scales features to the interquartile range (IQR) and is less affected by outliers. It's calculated as:

   $$X' = \frac{X - Q1}{Q3 - Q1}$$

   - $X$ is the original feature value, $Q1$ is the first quartile (25th percentile), and $Q3$ is the third quartile (75th percentile) of the feature.  
<br />
<br />
4. **Log Transformation:** In cases where data is highly skewed or has a heavy-tailed distribution, taking the logarithm of the feature values can help stabilize the variance and improve scaling.

The choice of scaling method depends on the characteristics of your data and the requirements of your machine learning algorithm. **Min-max scaling and standardization are the most commonly used techniques and work well for many datasets.**

Scaling should be applied separately to each training and test set to prevent data leakage from the test set into the training set. Additionally, **some algorithms may not require feature scaling, particularly tree-based models.**
"""

class FeatureScaler(BaseEstimator, TransformerMixin):
    def __init__(self, numerical_features):
        self.numerical_features = numerical_features
        self.scaler = StandardScaler()

    def fit(self, X, y=None):
        self.scaler.fit(X[self.numerical_features])
        return self

    def transform(self, X):
        X_scaled = X.copy()
        X_scaled[self.numerical_features] = self.scaler.transform(X_scaled[self.numerical_features])
        return X_scaled

"""### II. Feature Encoding

**Feature encoding**, also known as **categorical encoding**, is the process of converting categorical data (non-numeric data) into a numerical format so that it can be used as input for machine learning algorithms. Most machine learning models require numerical data for training and prediction, so feature encoding is a critical step in data preprocessing.

Categorical data can take various forms, including:

1. **Nominal Data:** Categories with no intrinsic order, like colors or country names.  

2. **Ordinal Data:** Categories with a meaningful order but not necessarily equidistant, like education levels (e.g., "high school," "bachelor's," "master's").

There are several common methods for encoding categorical data:

1. **Label Encoding:**

   - Label encoding assigns a unique integer to each category in a feature.
   - It's suitable for ordinal data where there's a clear order among categories.
   - For example, if you have an "education" feature with values "high school," "bachelor's," and "master's," you can encode them as 0, 1, and 2, respectively.
<br />
<br />
2. **One-Hot Encoding:**

   - One-hot encoding creates a binary (0 or 1) column for each category in a nominal feature.
   - It's suitable for nominal data where there's no inherent order among categories.
   - Each category becomes a new feature, and the presence (1) or absence (0) of a category is indicated for each row.
<br />
<br />
3. **Target Encoding (Mean Encoding):**

   - Target encoding replaces each category with the mean of the target variable for that category.
   - It's often used for classification problems.
"""

class FeatureEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, categorical_features):
        self.categorical_features = categorical_features
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

    def fit(self, X, y=None):
        self.encoder.fit(X[self.categorical_features])
        self.encoded_feature_names = self.encoder.get_feature_names_out(self.categorical_features)
        return self

    def transform(self, X):
        X_encoded = X.copy()
        encoded_data = self.encoder.transform(X_encoded[self.categorical_features])
        encoded_df = pd.DataFrame(encoded_data, columns=self.encoded_feature_names, index=X_encoded.index)
        X_encoded = X_encoded.drop(columns=self.categorical_features)
        X_encoded = pd.concat([X_encoded, encoded_df], axis=1)
        return X_encoded

"""### III. Handling Imbalanced Dataset

**Handling imbalanced datasets** is important because imbalanced data can lead to several issues that negatively impact the performance and reliability of machine learning models. Here are some key reasons:

1. **Biased Model Performance**:

 - Models trained on imbalanced data tend to be biased towards the majority class, leading to poor performance on the minority class. This can result in misleading accuracy metrics.

2. **Misleading Accuracy**:

 - High overall accuracy can be misleading in imbalanced datasets. For example, if 95% of the data belongs to one class, a model that always predicts the majority class will have 95% accuracy but will fail to identify the minority class.

3. **Poor Generalization**:

 - Models trained on imbalanced data may not generalize well to new, unseen data, especially if the minority class is underrepresented.


Some methods to handle imbalanced datasets:
1. **Resampling Methods**:

 - Oversampling: Increase the number of instances in the minority class by duplicating or generating synthetic samples (e.g., SMOTE).
 - Undersampling: Reduce the number of instances in the majority class to balance the dataset.

2. **Evaluation Metrics**:

 - Use appropriate evaluation metrics such as precision, recall, F1-score, ROC-AUC, and confusion matrix instead of accuracy to better assess model performance on imbalanced data.

3. **Algorithmic Approaches**:

 - Use algorithms that are designed to handle imbalanced data, such as decision trees, random forests, or ensemble methods.
 - Adjust class weights in algorithms to give more importance to the minority class.
"""

class ImbalanceHandler(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.smote = SMOTE(random_state=42)

    def fit(self, X, y):
        self.smote.fit_resample(X, y)
        return self

    def transform(self, X):
        return X

"""# 3. Compile Preprocessing Pipeline

All of the preprocessing classes or functions defined earlier will be compiled in this step.

If you use sklearn to create preprocessing classes, you can list your preprocessing classes in the Pipeline object sequentially, and then fit and transform your data.
"""

# pipe = Pipeline([("imputer", FeatureImputer()),
#                  ("featurecreator", FeatureCreator()),
#                  ("scaler", FeatureScaler()),
#                  ("encoder", FeatureEncoder())])

# train_set = pipe.fit_transform(train_set)
# val_set = pipe.transform(val_set)

preprocessing_pipeline = Pipeline([
    ('drop_features', DropFeatures(dropped_features)),
    ('discretizer', Discretizer(features_to_discretize)),
    ('scaler', FeatureScaler(numerical_features)),
    ('encoder', FeatureEncoder(categorical_features)),
    ('imbalance_handler', ImbalanceHandler()),
])

X_train = train_set.drop(columns=['id', 'label'])
y_train = train_set['label']

X_val = val_set.drop(columns=['id','label'])
y_val = val_set['label']

X_train = preprocessing_pipeline.fit_transform(X_train, y_train)
X_val = preprocessing_pipeline.transform(X_val)

"""# 4. Modeling and Validation

Modelling is the process of building your own machine learning models to solve specific problems, or in this assignment context, predicting the target feature `label`. Validation is the process of evaluating your trained model using the validation set or cross-validation method and providing some metrics that can help you decide what to do in the next iteration of development.
"""

# Model membutuhkan numpy array sebagai input
X_train = X_train.to_numpy()
y_train = y_train.to_numpy()
X_val = X_val.to_numpy()
y_val = y_val.to_numpy()

"""## A. KNN"""

class KNN:
    def __init__(self, k=3, distance_metric='euclidean', p=3):
        self.k = k
        self.distance_metric = distance_metric
        self.p = p

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        predictions = [self._predict(x) for x in X]
        return predictions

    def _predict(self, x):
        distances = [self._compute_distance(x, x_train) for x_train in self.X_train]
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        most_common = np.bincount(k_nearest_labels).argmax()
        return most_common

    def _compute_distance(self, x1, x2):
        if self.distance_metric == 'euclidean':
            return np.sqrt(np.sum((x1 - x2) ** 2))
        elif self.distance_metric == 'manhattan':
            return np.sum(np.abs(x1 - x2))
        elif self.distance_metric == 'minkowski':
            return np.sum(np.abs(x1 - x2) ** self.p) ** (1 / self.p)
        else:
            raise ValueError(f"Distance metric salah: {self.distance_metric}")

# Inisialisasi model KNN
knn_model = KNN(k=3, distance_metric='euclidean')

knn_model.fit(X_train, y_train)

# Lakukan Save model KNN (Opsional)
with open('knn_model.pkl', 'wb') as file:
    pickle.dump(knn_model, file)

# Lakukan Load model KNN (Opsional)
with open('knn_model.pkl', 'rb') as file:
    knn_model_loaded = pickle.load(file)

# Predict X_val
knn_predictions = knn_model.predict(X_val)

# Hitung akurasi dari prediction
accuracy = accuracy_score(y_val, knn_predictions)
print(f"Akurasi KNN: {accuracy}")

from sklearn.neighbors import KNeighborsClassifier

knn_sckit_model = KNeighborsClassifier(n_neighbors=10)
knn_sckit_model.fit(X_train, y_train)
knn_sckit_predictions = knn_sckit_model.predict(X_val)
accuracy = accuracy_score(y_val, knn_sckit_predictions)

print(f"Akurasi KNN SCKit: {accuracy}")

"""## B. Naive Bayes"""

class NaiveBayes:
    def __init__(self):
        self.class_priors = {}
        self.feature_likelihoods = {}
        self.num_features = 0

    def fit(self, X, y):
        self.num_features = X.shape[1]
        self.class_priors = self._calculate_class_priors(y)
        self.feature_likelihoods = self._calculate_feature_likelihoods(X, y)

    def _calculate_class_priors(self, y):
        class_priors = {}
        total_samples = len(y)
        for label in set(y):
            class_priors[label] = sum(y == label) / total_samples
        return class_priors

    def _calculate_feature_likelihoods(self, X, y):
        likelihoods = {}
        for label in set(y):
            X_label = X[y == label]
            likelihoods[label] = {
                feature_index: (X_label[:, feature_index].mean(), X_label[:, feature_index].std())
                for feature_index in range(self.num_features)
            }
        return likelihoods

    def predict(self, X):
        predictions = []
        for x in X:
            posteriors = {}
            for label in self.class_priors:
                prior = self.class_priors[label]
                likelihood = self._calculate_likelihood(x, label)
                posteriors[label] = prior * likelihood
            predictions.append(int(max(posteriors, key=posteriors.get)))
        return predictions

    def _calculate_likelihood(self, x, label):
        likelihood = 1
        for feature_index in range(self.num_features):
            mean, std = self.feature_likelihoods[label][feature_index]
            likelihood *= self._gaussian_probability(x[feature_index], mean, std)
        return likelihood

    def _gaussian_probability(self, x, mean, std):
        if std == 0:
            return 1 if x == mean else 0
        exponent = np.exp(-((x - mean) ** 2 / (2 * std ** 2)))
        return (1 / (np.sqrt(2 * np.pi) * std)) * exponent

# Inisialisasi model Naive Bayes
nb_model = NaiveBayes()

nb_model.fit(X_train, y_train)

# Save model Naive Bayes (Opsional)
with open('naive_bayes_model.pkl', 'wb') as file:
    pickle.dump(nb_model, file)

# Load model Naive Bayes (Opsional)
with open('naive_bayes_model.pkl', 'rb') as file:
    nb_model_loaded = pickle.load(file)

# Predict X_val
nb_predictions = nb_model.predict(X_val)

# Akurasi nb_predictions
accuracy = accuracy_score(y_val, nb_predictions)
print(f"Akurasi Naive Bayes: {accuracy}")

# Gaussian Naive Bayes with Scikit-learn
from sklearn.naive_bayes import GaussianNB

nb_sckit_model = GaussianNB()
nb_sckit_model.fit(X_train, y_train)
nb_sckit_predictions = nb_sckit_model.predict(X_val)
accuracy = accuracy_score(y_val, nb_sckit_predictions)

print(f"Akurasi Naive Bayes SCKit: {accuracy}")

"""## C. Improvements (Optional)

- **Visualize the model evaluation result**

This will help you to understand the details more clearly about your model's performance. From the visualization, you can see clearly if your model is leaning towards a class than the others. (Hint: confusion matrix, ROC-AUC curve, etc.)

- **Explore the hyperparameters of your models**

Each models have their own hyperparameters. And each of the hyperparameter have different effects on the model behaviour. You can optimize the model performance by finding the good set of hyperparameters through a process called **hyperparameter tuning**. (Hint: Grid search, random search, bayesian optimization)

- **Cross-validation**

Cross-validation is a critical technique in machine learning and data science for evaluating and validating the performance of predictive models. It provides a more **robust** and **reliable** evaluation method compared to a hold-out (single train-test set) validation. Though, it requires more time and computing power because of how cross-validation works. (Hint: k-fold cross-validation, stratified k-fold cross-validation, etc.)
"""

# Type your code here

"""## D. Submission
To predict the test set target feature and submit the results to the kaggle competition platform, do the following:
1. Create a new pipeline instance identical to the first in Data Preprocessing
2. With the pipeline, apply `fit_transform` to the original training set before splitting, then only apply `transform` to the test set.
3. Retrain the model on the preprocessed training set
4. Predict the test set
5. Make sure the submission contains the `id` and `label` column.

Note: Adjust step 1 and 2 to your implementation of the preprocessing step if you don't use pipeline API from `sklearn`.
"""

pipe = Pipeline([
    ('drop_features', DropFeatures(dropped_features)),
    ('discretizer', Discretizer(features_to_discretize)),
    ('scaler', FeatureScaler(numerical_features)),
    ('encoder', FeatureEncoder(categorical_features)),
    ('imbalance_handler', ImbalanceHandler()),
])

X_train = train_set.drop(columns=['id', 'label'])
y_train = train_set['label']

test_df = pd.read_csv('test.csv') # Ambil test.csv

test = test_df.drop(columns=['id'])
test_id = test_df['id']

X_train = pipe.fit_transform(X_train, y_train)
test = pipe.transform(test)

X_train = X_train.to_numpy()
y_train = y_train.to_numpy()
test = test.to_numpy()

knn_predict = knn_model.predict(test)
nb_predict = nb_model.predict(test)

predictions_set = pd.DataFrame({
    'id': test_id,
    'label': knn_predict
})

predictions_set.to_csv('submissions_knn.csv', index=False)

predictions_set = pd.DataFrame({
    'id': test_id,
    'label': nb_predict
})

predictions_set.to_csv('submissions_nb.csv', index=False)

"""# 6. Error Analysis

Based on all the process you have done until the modeling and evaluation step, write an analysis to support each steps you have taken to solve this problem. Write the analysis using the markdown block. Some questions that may help you in writing the analysis:

- Does my model perform better in predicting one class than the other? If so, why is that?
- To each models I have tried, which performs the best and what could be the reason?
- Is it better for me to impute or drop the missing data? Why?
- Does feature scaling help improve my model performance?
- etc...

Menggunakan X_val kecil (0.001 dari dataset)

### KNN
- Hasil prediksi X_val menggunnakan model KNN scratch
  * Akurasi KNN: 0.9716312056737588
  * Waktu yang dibutuhkan: 2 menit

- Hasil prediksi X_val menggunnakan model KNN SCKit
  * Akurasi KNN SCKit: 0.96453900709219
  * Waktu yang dibutuhkan: < 1 detik

### Naive Bayes
- Hasil prediksi X_val menggunnakan model nb scratch
  * Akurasi Naive Bayes: 0.8794326241134752
  * Waktu yang dibutuhkan: < 1 detik

- Hasil prediksi X_val menggunnakan model nb SCKit
  * Akurasi KNN SCKit: 0.9645390070921985
  * Waktu yang dibutuhkan: < 1 detik


Algoritma KNN meghasilkan akurasi yang lebih baik, namun memakan waktu yang jauh lebih lama dibanding algoritma Gaussian Naive Bayes
"""