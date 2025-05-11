import warnings
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder  # Used for OneHotEncoding
from sklearn.metrics import mean_squared_error, precision_score, recall_score, f1_score, accuracy_score, roc_auc_score, confusion_matrix
from imblearn import under_sampling, over_sampling  # Used for data balancing
from imblearn.over_sampling import SMOTE  # Used for data balancing
from sklearn.preprocessing import MinMaxScaler  # Used for data normalization
from sklearn.metrics import r2_score  # Used to measure the accuracy of the predictive model
import pyodbc  # SQL connection

warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Creates the connection to the SQL Server passing the parameters (Server, User, Password, Database)
conexao = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\\SQLSERVER;'
    'DATABASE=SISTEMA_BANCO;'
    'UID=user_python;'
    'PWD=123456'
)

# Calls the database query passing the parameters from the created connection
df_origin = pd.read_sql_query('SELECT * FROM CONTRATOS_FINANCIAMENTOS', conexao)

# Closes the connection to the database
conexao.close()

# Dataset size.
df_origin.shape

# Overview of the dataset
df_origin.head(5)

# Analyzing missing data we found the following:
# Variable IDADE_DATA_ASSINATURA_CONTRATO has 1 missing record
# Variable VL_TOTAL_PC_PAGAS has 4 missing records
# Since we have a total of 10,415 observations, removing 5 will NOT affect our work
df_origin.isnull().sum()

# Basic information about variable types
df_origin.info(verbose=True)

# Evaluate the period of the collected data
start = pd.to_datetime(df_origin['DATA_ASSINATURA_CONTRATO']).dt.date.min()
end = pd.to_datetime(df_origin['DATA_ASSINATURA_CONTRATO']).dt.date.max()
print('Data period - From:', start, 'To:', end)

# Number of unique values for each variable
# The variable TIPO_FINANCIAMENTO has a single value, so it will be removed from our DataFrame
valores_unicos = []
for i in df_origin.columns[0:20].tolist():
    print(i, ':', len(df_origin[i].astype(str).value_counts()))
    valores_unicos.append(len(df_origin[i].astype(str).value_counts()))

# Viewing some statistical measures
df_origin.describe()

print('Highest financed amount:', df_origin['VALOR_FINANCIAMENTO'].max())
print('Lowest financed amount:', df_origin['VALOR_FINANCIAMENTO'].min())

# The target variable will need to be balanced in the preprocessing step
df_origin.groupby(['INADIMPLENTE_COBRANCA']).size()

# No changes are needed here
df_origin.groupby(['PZ_FINANCIAMENTO']).size()

# No treatment is needed here
df_origin.groupby(['RENDA_MENSAL_CLIENTE']).size()

# Note that we have a wide range of financed amounts; in this case we should create value ranges
df_origin.groupby(['VALOR_FINANCIAMENTO']).size()

df_origin.dropna(inplace=True)

# Creating financing term range
bins = [-100, 120, 180, 240]
labels = ['Up to 120 Months', '121 to 180 Months', '181 to 240 Months']
df_origin['FAIXA_PRAZO_FINANCIAMENTO'] = pd.cut(df_origin['PZ_FINANCIAMENTO'], bins=bins, labels=labels)
pd.value_counts(df_origin.FAIXA_PRAZO_FINANCIAMENTO)

# Creating financed amount range for the predictive model
bins = [-100, 100000, 200000, 300000, 400000, 500000, 750000, 1000000, 9000000000]
labels = ['Up to 100K', '101 to 200K', '201 to 300K', '301 to 400K', '401 to 500K', 
          '501 to 750K', '751K to 1M', 'Over 1M']
df_origin['FAIXA_VALOR_FINANCIADO'] = pd.cut(df_origin['VALOR_FINANCIAMENTO'], bins=bins, labels=labels)
pd.value_counts(df_origin.FAIXA_VALOR_FINANCIADO)

# We can drop the TIPO_FINANCIAMENTO variable as seen previously
# We should drop the VALOR_FINANCIAMENTO variable since we created a value range variable for it
# We should drop the PZ_FINANCIAMENTO variable since we created a month range variable for it
# We can drop the DATA_ASSINATURA_CONTRATO variable
# We can drop the NUMERO_CONTRATO variable
colunas = ['TAXA_AO_ANO', 'CIDADE_CLIENTE', 'ESTADO_CLIENTE','RENDA_MENSAL_CLIENTE', 
           'QT_PC_ATRASO', 'QT_DIAS_PRIM_PC_ATRASO','QT_TOTAL_PC_PAGAS',
           'VL_TOTAL_PC_PAGAS', 'QT_PC_PAGA_EM_DIA','QT_DIAS_MIN_ATRASO',
           'QT_DIAS_MAX_ATRASO', 'QT_DIAS_MEDIA_ATRASO','VALOR_PARCELA',
           'IDADE_DATA_ASSINATURA_CONTRATO', 'FAIXA_VALOR_FINANCIADO',
           'FAIXA_PRAZO_FINANCIAMENTO','INADIMPLENTE_COBRANCA']

df_data = pd.DataFrame(df_origin, columns=colunas)

df_data.head()

df_data.shape

df_data.info(verbose=True)

df_data.isnull().sum()

# Analyzing target distribution
# Here we can see there are many more defaults than non-defaults,
# so we will need to balance the dataset later.
df_data.INADIMPLENTE_COBRANCA.value_counts().plot(kind='bar', title='Defaults', color=['#1F77B4', '#FF7F0E'])

# Load variables for plotting
plt.rcParams["figure.figsize"] = [14.00, 3.50]
plt.rcParams["figure.autolayout"] = True
sns.countplot(data=df_data, x="FAIXA_VALOR_FINANCIADO", hue="INADIMPLENTE_COBRANCA")
plt.show()

plt.rcParams["figure.figsize"] = [12.00, 3.50]
plt.rcParams["figure.autolayout"] = True
sns.countplot(data=df_data, x="FAIXA_PRAZO_FINANCIAMENTO", hue="INADIMPLENTE_COBRANCA")
plt.show()

df_data.info()

# Identify numeric variables for boxplots
variaveis_numericas = []
for i in df_data.columns[0:17].tolist():
    if df_data.dtypes[i] in ['int64', 'float64']:
        variaveis_numericas.append(i)

# Visualizing numeric variables
variaveis_numericas

# We can observe in the boxplots below that the numeric variables show a large number of "possible" outliers
# We need to evaluate each of these variables in the context of the data to determine if we should treat them as outliers
plt.rcParams["figure.figsize"] = [14.00, 14.00]
plt.rcParams["figure.autolayout"] = True
f, axes = plt.subplots(4, 3)

linha = 0
coluna = 0
for i in variaveis_numericas:
    sns.boxplot(data=df_data, y=i, ax=axes[linha][coluna])
    coluna += 1
    if coluna == 3:
        linha += 1
        coluna = 0

plt.show()

# Identify categorical variables for OneHotEncoding (exclude the target)
variaveis_categoricas = []
for i in df_data.columns[0:16].tolist():
    if df_data.dtypes[i] in ['object', 'category']:
        variaveis_categoricas.append(i)

# Visualizing the categorical variables
variaveis_categoricas

# Create the encoder and apply OneHotEncoding
lb = LabelEncoder()
for var in variaveis_categoricas:
    df_data[var] = lb.fit_transform(df_data[var])

df_data.head()

df_data.info()

# Viewing the target class counts for balancing
variavel_target = df_data.INADIMPLENTE_COBRANCA.value_counts()
variavel_target

# Separate predictors and target
PREDITORAS = df_data.iloc[:, 0:15]
TARGET = df_data.iloc[:, 16]

PREDITORAS.head()
TARGET.head()

# Seed for reproducibility
seed = 2003

# Replace infinite values with NaN
PREDITORAS = PREDITORAS.replace([np.inf, -np.inf], np.nan)

# Drop any rows with NaN
PREDITORAS = PREDITORAS.dropna()
TARGET = TARGET.loc[PREDITORAS.index]

# Apply SMOTE for balancing
balanceador = SMOTE(random_state=seed)
PREDITORAS_RES, TARGET_RES = balanceador.fit_resample(PREDITORAS, TARGET)

# Visualize the balanced target classes
plt.rcParams["figure.figsize"] = [12.00, 5.00]
plt.rcParams["figure.autolayout"] = True
TARGET_RES.value_counts().plot(
    kind='bar',
    title='Defaults vs Non-Defaults',
    color=['#1F77B4', '#FF7F0E']
)

# Record sizes before and after balancing
PREDITORAS.shape
TARGET.shape
PREDITORAS_RES.shape
TARGET_RES.shape

# Split into training and test sets
X_train, X_test, Y_train, Y_test = train_test_split(
    PREDITORAS_RES, TARGET_RES, test_size=0.3, random_state=42
)

# Normalize features
scaler = MinMaxScaler()
X_train_norm = scaler.fit_transform(X_train)
X_test_norm = scaler.transform(X_test)

# Check training data dimensions
X_train_norm.shape

# Train Random Forest classifier
clf = RandomForestClassifier(n_estimators=300, random_state=seed)
clf.fit(X_train_norm, Y_train)

# Evaluate accuracy on test set
accuracy = clf.score(X_test_norm, Y_test)
print("Test set accuracy:", accuracy)

# Display feature importances
plt.rcParams["figure.figsize"] = [10.00, 10.00]
plt.rcParams["figure.autolayout"] = True
importances = pd.Series(data=clf.feature_importances_, index=PREDITORAS.columns)
importances = importances.sort_values(ascending=False)
sns.barplot(x=importances, y=importances.index, orient='h').set_title('Feature Importances')
plt.show()

# Save the trained model
joblib.dump(clf, 'trained_model.pkl')
