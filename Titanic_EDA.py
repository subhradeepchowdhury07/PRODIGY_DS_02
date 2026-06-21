# ============================================
# CODSOFT TASK-02
# Data Cleaning & Exploratory Data Analysis
# ============================================

import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
df = pd.read_csv("train.csv")   # Change filename if needed

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# ============================================
# Dataset Information
# ============================================

print("=" * 50)
print("TITANIC DATASET INFORMATION")
print("=" * 50)

print("\nFirst 5 Rows:")
print(df.head())

print("\nShape of Dataset:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

# ============================================
# Data Cleaning
# ============================================

# Fill missing Age
if "Age" in df.columns:
    df["Age"] = df["Age"].fillna(df["Age"].median())

# Fill missing Embarked
if "Embarked" in df.columns:
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

# Drop Cabin
if "Cabin" in df.columns:
    df.drop(columns=["Cabin"], inplace=True)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# ============================================
# Survival Count
# ============================================

if "Survived" in df.columns:
    plt.figure(figsize=(6,4))
    df["Survived"].value_counts().plot(kind="bar")
    plt.title("Survival Count")
    plt.xlabel("Survived")
    plt.ylabel("Count")
    plt.show()

# ============================================
# Gender Distribution
# ============================================

if "Sex" in df.columns:
    plt.figure(figsize=(6,4))
    df["Sex"].value_counts().plot(kind="bar")
    plt.title("Gender Distribution")
    plt.xlabel("Gender")
    plt.ylabel("Count")
    plt.show()

# ============================================
# Survival by Gender
# ============================================

if "Survived" in df.columns and "Sex" in df.columns:
    pd.crosstab(df["Sex"], df["Survived"]).plot(kind="bar")
    plt.title("Survival by Gender")
    plt.xlabel("Gender")
    plt.ylabel("Count")
    plt.show()

# ============================================
# Survival by Passenger Class
# ============================================

if "Survived" in df.columns and "Pclass" in df.columns:
    pd.crosstab(df["Pclass"], df["Survived"]).plot(kind="bar")
    plt.title("Survival by Passenger Class")
    plt.xlabel("Passenger Class")
    plt.ylabel("Count")
    plt.show()

# ============================================
# Age Distribution
# ============================================

if "Age" in df.columns:
    plt.figure(figsize=(7,5))
    plt.hist(df["Age"], bins=20)
    plt.title("Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    plt.show()

# ============================================
# Fare Distribution
# ============================================

if "Fare" in df.columns:
    plt.figure(figsize=(7,5))
    plt.hist(df["Fare"], bins=20)
    plt.title("Fare Distribution")
    plt.xlabel("Fare")
    plt.ylabel("Frequency")
    plt.show()

# ============================================
# Embarked Distribution
# ============================================

if "Embarked" in df.columns:
    plt.figure(figsize=(6,4))
    df["Embarked"].value_counts().plot(kind="bar")
    plt.title("Embarked Distribution")
    plt.xlabel("Port")
    plt.ylabel("Passengers")
    plt.show()

# ============================================
# Correlation Matrix
# ============================================

numeric_df = df.select_dtypes(include="number")

plt.figure(figsize=(8,6))
plt.imshow(numeric_df.corr(), cmap="coolwarm")
plt.colorbar()

plt.xticks(range(len(numeric_df.columns)), numeric_df.columns, rotation=90)
plt.yticks(range(len(numeric_df.columns)), numeric_df.columns)

plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()

# ============================================
# Insights
# ============================================

print("\n" + "=" * 50)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 50)
