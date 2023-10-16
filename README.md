# Expense Tracker
## Description
An expense tracker app built using Esmerald and Saffier.

The application serves as a showcase for the Esmerald ecosystem.
 
  
## Requirements

- Python 3.9+
- Esmerald 2.0+
- Saffier 0.18+


## Instructions
### 1. Installation

Install esmerald and saffier

```pip install esmerald```

and

```pip install saffier```


### 2. Create migrations

Set the environment variables for Saffier migration

```export SAFFIER_DATABASE_URL=<Your DB connection string>```

Initialize migration objects (inside project directory)

```saffier init```

Generate migration files

```saffier nakemigration```

Generate the data model in DB

```saffier migrate```

### 3. Running the app

Just type

```make run```
