
# eziql

🚀 **eziql** is a simple Python library that uses Groq's LLaMA model to convert natural language queries into SQL statements.

Whether you're a developer, data analyst, or a beginner working with databases, this package helps you quickly generate SQL queries just by describing what you want in plain English.

---

## ✨ Features

- ✅ Convert plain English to valid SQL queries  
- 🧠 Powered by Groq's LLaMA-3 model  
- 📝 Optional schema input for more accurate query generation  
- 🔐 Uses `.env` for API key management or accepts it directly in code  

---

## 📦 Installation

```bash
pip install eziql
```

---

## 🔧 Setup

You must provide your Groq API key to use this package. There are two ways:

### 1. Using Environment Variable (`.env` file)

Create a `.env` file in your project root and add:

```env
eziql_key=your_groq_api_key
```

### 2. Pass Key Directly in Code

```python
from eziql import GroqSQL  
sql_generator = GroqSQL(api_key="your_groq_api_key")
```

---

## 🧪 Usage Example

```python
from eziql import GroqSQL

sql_generator = GroqSQL()  # Loads key from .env

user_query = "write a query for showing all columns from table empTab"

table_schema = """
Tables:
    Car(id, name, color, type, sellDate)
"""

# Generate SQL  
sql_query = sql_generator.generate_sql(user_query, table_schema)  
print(sql_query)
```

You can also run it without schema:

```python
sql_query = sql_generator.generate_sql("Get all records from users table")
print(sql_query)
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributions

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📬 Contact

Created by Aman Prajapat — feel free to connect on LinkedIn or raise issues for support.