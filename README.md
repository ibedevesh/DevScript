# DevScript

DevScript is an AI-powered coding language that lets users describe logic naturally. The AI converts it into real executable Python code.

## Installation

### Option 1: Install from the repository

1. Clone this repository:
```bash
git clone https://github.com/yourusername/devscript.git
cd devscript
```

2. Install DevScript as a CLI tool:
```bash
pip install -e .
```

This will install the `devscript` command globally, allowing you to run DevScript files from anywhere.

### Option 2: Manual setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/devscript.git
cd devscript
```

2. Install the required dependencies:
```bash
pip install google-generativeai python-dotenv pandas matplotlib
```

3. Set up your Google Gemini API key in the `.env` file:
```
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_MODEL=gemini-2.0-flash
```

## Usage

1. Create a `.ds` file with your DevScript code. For example, `example.ds`:
```
load "data.csv"
filter rows where age > 25
sort by salary descending
print first 5 rows
```

2. Run the DevScript CLI:
```bash
# If installed as a CLI tool:
devscript example.ds

# Or run directly:
python main.py example.ds
```

3. Command-line options:
```bash
# Show the generated Python code:
devscript example.ds --show-python

# Convert to Python without executing:
devscript example.ds --dry-run
```

4. The tool will:
   - 🔁 Convert your DevScript to Python using Google Gemini
   - 📦 Detect and install any required packages
   - 🚀 Execute the Python code
   - Display the results

## Writing DevScript Code

DevScript is designed to be intuitive. Here are some examples:

### Data Analysis
```
load "data.csv"
filter rows where age > 25
sort by salary descending
print first 5 rows
```

### Data Visualization
```
load "data.csv"
plot a line chart of salary by age
save the chart as "salary_by_age.png"
```

### Simple Operations
```
create a list of numbers from 1 to 5
plot a bar chart of these numbers
title the chart "Simple Bar Chart"
save the chart as "simple_bar_chart.png"
```

## Example Output

🔁 Converting DevScript to Python...

✅ Generated Python:

import pandas as pd

# Load the CSV file
data = pd.read_csv("data.csv")

# Filter rows where age > 25
filtered_data = data[data['age'] > 25]

# Sort by salary in descending order
sorted_data = filtered_data.sort_values(by='salary', ascending=False)

# Print the first 5 rows
print(sorted_data.head(5))

📦 Required packages: pandas
✅ All required packages already installed.

🚀 Running Python Code:

   name  age  salary department
2  Jane   30   85000         HR
1   Bob   28   75000     Sales
0  John   26   65000         IT

## Next Steps

- Add VS Code extension for syntax highlighting
- Create a hosted AI backend for improved scale and speed
- Add more language targets beyond Python
- Create a web playground
