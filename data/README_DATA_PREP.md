# Vertex AI Data Preparation Pipeline

## 📊 **What `vertex_ai_data_prep.py` Does**

The `vertex_ai_data_prep.py` script is a **comprehensive data preparation pipeline** designed specifically for Vertex AI machine learning workflows. It transforms raw customer churn data into a format ready for training and deployment in Google Cloud's Vertex AI platform.

## 🔄 **Pipeline Overview**

### **1. Data Loading & Acquisition**
```python
# Downloads Telco Customer Churn dataset from public URL
url = "https://raw.githubusercontent.com/dphi-official/Datasets/master/Telco-Customer-Churn.csv"
df = pd.read_csv(url)
```
- **Source**: Public Telco Customer Churn dataset
- **Fallback**: Local file if URL is unavailable
- **Output**: Raw pandas DataFrame

### **2. Data Cleaning & Preprocessing**
```python
# Remove duplicates and missing values
df = df.drop_duplicates()
df = df.dropna()

# Convert data types
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')

# Encode target variable
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
```
- **Duplicate Removal**: Eliminates duplicate records
- **Missing Value Handling**: Removes rows with null values
- **Data Type Conversion**: Ensures proper numeric types
- **Target Encoding**: Converts categorical target to binary

### **3. Feature Engineering**
```python
# Create new features
df['TotalChargesPerMonth'] = df['TotalCharges'] / df['tenure']
df['MonthlyChargesRatio'] = df['MonthlyCharges'] / df['TotalCharges']

# Encode categorical variables
df_encoded = pd.get_dummies(df, columns=categorical_columns, drop_first=True)
```
- **New Features**: Creates derived features for better model performance
- **Categorical Encoding**: One-hot encoding for all categorical variables
- **Feature Selection**: Prepares features for ML algorithms

### **4. Data Validation & Quality Checks**
```python
validation_report = {
    "total_rows": len(df),
    "total_columns": len(df.columns),
    "missing_values": df.isnull().sum().sum(),
    "duplicate_rows": df.duplicated().sum(),
    "target_distribution": df["Churn"].value_counts().to_dict()
}
```
- **Quality Metrics**: Comprehensive data quality assessment
- **Issue Detection**: Identifies potential problems
- **Validation Report**: Detailed summary of data characteristics

### **5. Cloud Storage Upload**
```python
# Upload to Google Cloud Storage
blob = bucket.blob(gcs_data_path)
blob.upload_from_filename(cleaned_data_path)
gcs_uri = f"gs://{bucket_name}/{gcs_data_path}"
```
- **GCS Integration**: Uploads cleaned data to Google Cloud Storage
- **Versioned Storage**: Timestamped files for tracking
- **Cloud Accessibility**: Makes data available for Vertex AI services

### **6. Feature Store Ingestion**
```python
# Ingest into Vertex AI Feature Store
entity_type.ingest_from_df(
    feature_ids=feature_columns,
    feature_time=datetime.now(),
    feature_values=df,
    entity_id_column="customerID"
)
```
- **Feature Store**: Centralized feature management
- **Real-time Serving**: Enables online feature serving
- **Entity Management**: Organizes features by customer entities

## 🏗️ **Architecture & Design**

### **Class-Based Design**
```python
class DataPreparationPipeline:
    def __init__(self):
        # Initialize with configuration
        self.config = get_config()
        self.secrets = self.config.secrets
    
    def load_data(self) -> pd.DataFrame:
        # Data loading logic
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # Data cleaning logic
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        # Feature engineering logic
    
    def run_pipeline(self) -> Dict[str, Any]:
        # Complete pipeline execution
```

### **Configuration Integration**
- **Centralized Config**: Uses project's configuration system
- **Environment Support**: Works across dev/staging/prod
- **Secret Management**: Secure handling of GCP credentials

### **Error Handling & Logging**
```python
# Comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_prep.log'),
        logging.StreamHandler()
    ]
)
```

## 📈 **Data Transformations**

### **Input Data Structure**
```csv
customerID,gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges,Churn
7590-VHVEG,Female,0,Yes,No,1,Yes,No phone service,DSL,No,Yes,No,No,No,No,Month-to-month,Yes,Electronic check,29.85,29.85,No
```

### **Output Data Structure**
```csv
customerID,tenure,MonthlyCharges,TotalCharges,TotalChargesPerMonth,MonthlyChargesRatio,gender_Male,Partner_Yes,Dependents_Yes,PhoneService_Yes,MultipleLines_Yes,InternetService_Fiber optic,OnlineSecurity_Yes,OnlineBackup_Yes,DeviceProtection_Yes,TechSupport_Yes,StreamingTV_Yes,StreamingMovies_Yes,Contract_One year,Contract_Two year,PaperlessBilling_Yes,PaymentMethod_Credit card (automatic),PaymentMethod_Electronic check,PaymentMethod_Mailed check,Churn
7590-VHVEG,1,29.85,29.85,29.85,1.0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0
```

### **Feature Engineering Details**
- **TotalChargesPerMonth**: Average monthly charges
- **MonthlyChargesRatio**: Ratio of monthly to total charges
- **Categorical Encoding**: One-hot encoding for all categorical variables
- **Feature Count**: ~50+ features after encoding

## 🚀 **Usage Examples**

### **Basic Usage**
```bash
# Run the complete pipeline
python data/vertex_ai_data_prep.py
```

### **Programmatic Usage**
```python
from data.vertex_ai_data_prep import DataPreparationPipeline

# Initialize pipeline
pipeline = DataPreparationPipeline()

# Run complete pipeline
results = pipeline.run_pipeline()

# Check results
if results["success"]:
    print(f"Data shape: {results['data_shape']}")
    print(f"GCS URI: {results['gcs_uri']}")
```

### **Step-by-Step Usage**
```python
# Run individual steps
df = pipeline.load_data()
df_cleaned = pipeline.clean_data(df)
df_engineered = pipeline.engineer_features(df_cleaned)
validation = pipeline.validate_data(df_engineered)
gcs_uri = pipeline.upload_to_gcs(df_engineered)
success = pipeline.ingest_to_feature_store(df_engineered)
```

## 📊 **Output & Results**

### **Files Generated**
- `data/raw_telco_data.csv`: Raw downloaded data
- `data/cleaned_telco_data.csv`: Cleaned and processed data
- `data_prep.log`: Detailed execution logs
- `gs://bucket/data/churn/cleaned_telco_data_YYYYMMDD_HHMMSS.csv`: Cloud storage file

### **Feature Store Results**
- **Entity Type**: `customers`
- **Features**: 50+ engineered features
- **Entity ID**: `customerID`
- **Timestamp**: Current ingestion time

### **Validation Report**
```json
{
    "total_rows": 7043,
    "total_columns": 52,
    "missing_values": 0,
    "duplicate_rows": 0,
    "target_distribution": {"0": 5174, "1": 1869},
    "numeric_features": 5,
    "categorical_features": 0,
    "issues": []
}
```

## 🔧 **Configuration Requirements**

### **Environment Variables**
```bash
# Required for GCP integration
export GCP_PROJECT_ID="your-project-id"
export GCP_LOCATION="us-central1"
export GCS_BUCKET_NAME="your-bucket-name"
export FEATURE_STORE_ID="churn_featurestore"
export ENTITY_TYPE_ID="customers"
```

### **Dependencies**
```bash
pip install pandas numpy google-cloud-storage google-cloud-aiplatform
```

## 🛡️ **Security & Best Practices**

### **Data Privacy**
- **No PII Exposure**: Customer IDs are preserved but not sensitive
- **Secure Upload**: Data uploaded via authenticated GCP clients
- **Access Control**: Uses project's IAM permissions

### **Error Handling**
- **Graceful Failures**: Handles network issues and missing data
- **Fallback Mechanisms**: Local file backup if URL fails
- **Detailed Logging**: Comprehensive error tracking

### **Data Quality**
- **Validation Checks**: Multiple quality assessments
- **Issue Detection**: Identifies data problems
- **Quality Reports**: Detailed quality metrics

## 📈 **Performance & Scalability**

### **Current Performance**
- **Dataset Size**: ~7,000 records, ~50 features
- **Processing Time**: ~30-60 seconds
- **Memory Usage**: ~50-100 MB

### **Scalability Considerations**
- **Larger Datasets**: Can handle 100K+ records
- **Parallel Processing**: Can be extended for batch processing
- **Cloud Resources**: Leverages GCP's scalable infrastructure

## 🔍 **Monitoring & Debugging**

### **Log Files**
- `data_prep.log`: Detailed execution logs
- Console output: Real-time progress updates
- Error tracking: Comprehensive error reporting

### **Debugging Tips**
```python
# Enable debug logging
logging.getLogger().setLevel(logging.DEBUG)

# Check intermediate results
df = pipeline.load_data()
print(f"Loaded {len(df)} records")

# Validate specific steps
validation = pipeline.validate_data(df)
print(f"Validation issues: {validation['issues']}")
```

## 🎯 **Integration with Vertex AI**

### **Training Pipeline Integration**
```python
# Use prepared data for training
gcs_uri = "gs://bucket/data/churn/cleaned_telco_data_20231201_143022.csv"
training_data = aiplatform.TabularDataset.create(
    display_name="churn_training_data",
    gcs_source=[gcs_uri]
)
```

### **Feature Store Integration**
```python
# Use features for online serving
featurestore = aiplatform.Featurestore("churn_featurestore")
entity_type = featurestore.get_entity_type("customers")
features = entity_type.read(entity_ids=["customer123"])
```

## 📚 **Next Steps**

### **Customization**
- **Different Datasets**: Modify data URL and schema
- **Feature Engineering**: Add custom feature calculations
- **Validation Rules**: Implement domain-specific checks

### **Production Deployment**
- **Scheduled Runs**: Set up automated data refresh
- **Monitoring**: Implement data quality alerts
- **Versioning**: Add data version management

### **Advanced Features**
- **Incremental Updates**: Handle new data additions
- **Data Lineage**: Track data transformations
- **Performance Optimization**: Optimize for large datasets

---

**This pipeline transforms raw customer data into ML-ready features, making it the foundation for your Vertex AI churn prediction system!** 