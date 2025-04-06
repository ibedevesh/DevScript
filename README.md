# DevScript

**DevScript** is an AI-powered coding language.
---

## Features

- Write code in plain English  
- Auto-converts to Python behind the scenes  
- Built-in CSV/data analysis support  
- Works locally with API key authentication  
- Simple CLI interface

---

## Installation

DevScript isn't on PyPI yet, so install it from GitHub:

### Option 1: Clone & Install

```
git clone https://github.com/ibedevesh/DevScript.git
cd DevScript
pip install -e .
```

### Option 2: Install Direct from GitHub

```
pip install git+https://github.com/ibedevesh/DevScript.git
```

---

## Setup

After installation, run:

```
devscript setup
```

You’ll be asked to enter your API key for authentication.

---

## Writing DevScript Files

DevScript files use the `.ds` extension.

### Example: hello.ds

```
print "Hello from DevScript!"

name = input "What's your name?"
print "Nice to meet you, " + name
```

---

## Usage

### Run a DevScript file:

```
devscript run hello.ds
```

### Convert to Python:

```
devscript convert hello.ds
```

Python code is saved in the `generated_py` folder.

### Convert and Run:

```
devscript convert hello.ds --run
```

### Check API usage:

```
devscript usage
```

---

## Example: Math and Loops

```
# Print numbers from 1 to 5
for i from 1 to 5:
    print "Number: " + i

# Create a list of values
numbers = [100, 200, 300]

# Perform operations
calculate the average of numbers
calculate the sum of numbers
print "Total is: " + total
```

---

## Example: CSV Analysis

```
analyze "customers.csv"

group by Country
Count how many customers are from each Country

save it to "country_count.csv"
```

---

## Troubleshooting

**API Key Issues:**

- Make sure you’ve run `devscript setup`
- Check API status: `devscript usage`
- Config is stored in: `~/.devscript/config.json`

**Connection Issues:**

- Check internet connection  
- Ensure nothing is blocking the network  
- Debug with:
```
DEVSCRIPT_DEBUG=1 devscript run file.ds
```

---

## License

Licensed under the MIT License. See LICENSE file.

---

## Created by Devesh

DevScript is in early access. Be part of the journey. 🚀

---

You can now select all, copy, and paste into your README.md. Need badges, GitHub actions, or a landing site? Let's gooo!
