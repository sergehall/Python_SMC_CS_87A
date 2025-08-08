# CS 87A – Python Programming

_Santa Monica College, Fall 2020_

---

Welcome! This repository contains my completed coursework for **CS 87A – Python Programming** at **Santa Monica College**.  
It includes six programming assignments covering Python fundamentals, data structures, file I/O, classes, and GUI development with Tkinter.

---

## Course Overview

> _“CS 87A – Introduction to Computer Programming in Python”_  
> [View Assignments (PDF)](./Assignment/)  

- **Instructor**: _(Instructor name not specified)_
- **Term**: Fall 2020
- **Format**: Online via Canvas
- **Language**: Python 3

---

## Project Structure

```text
/
├── Assignment/                  # Original assignment PDFs
│   ├── CS87A_FA2020_A01.pdf
│   ├── CS87A_FA2020_A02.pdf
│   ├── CS87A_FA2020_A03.pdf
│   ├── CS87A_FA2020_A04.pdf
│   ├── CS87A_FA2020_A05.pdf
│   └── CS87A_FA2020_A06.pdf
│
├── Home work/                   # Python solutions + data files
│   ├── A01.py                    # Assignment 1 solution
│   ├── A02.py                    # Assignment 2 solution
│   ├── A03.py                    # Assignment 3 solution
│   ├── A04.py                    # Assignment 4 solution
│   ├── A05.py                    # Assignment 5 solution
│   ├── A05ClassPrH.py            # Helper class definitions for A05
│   ├── A06.py                    # Assignment 6 Tkinter GUI app
│   ├── house.tab                  # Dataset for House election results
│   └── president.tab              # Dataset for Presidential election results
│
├── .gitignore
└── README.md
```

---

## Assignment Highlights

| Assignment | Topics Covered                                                                                       | Status      |
| ---------- | --------------------------------------------------------------------------------------------------- | ----------- |
| **A01**    | Python syntax basics, variables, loops, conditionals                                                | ✅ complete |
| **A02**    | Functions, input/output, error handling                                                              | ✅ complete |
| **A03**    | Lists, tuples, dictionaries, and basic algorithms                                                   | ✅ complete |
| **A04**    | Classes and objects, encapsulation, and methods                                                      | ✅ complete |
| **A05**    | File I/O, custom classes, dictionaries with tuple keys, election data parsing and aggregation logic | ✅ complete |
| **A06**    | Tkinter GUI programming, Canvas drawing, visualization of processed election data                   | ✅ complete |

---

## Getting Started

<details>
<summary>Expand to view setup instructions</summary>

### 1. **Clone the repository**

```bash
git clone https://github.com/sergehall/Python_SMC_CS_87A
cd Python_SMC_CS_87A
```

### 2. **Install Python**

Ensure you have Python **3.10+** installed.

```bash
python3 --version
```

If not installed (macOS via Homebrew):

```bash
brew install python
```

### 3. **Run assignments**

Each assignment can be run individually.  
Some require data files (`house.tab` and `president.tab`) to be present in the same directory.

Example:

```bash
cd "Home work"
python3 A05.py
python3 A06.py
```

> **Note:** Tkinter is required for `A06.py`.  
> On macOS, install with:
> ```bash
> brew install python-tk
> ```

</details>

---

## A06 – Tkinter GUI Demo

The final assignment (`A06.py`) creates a desktop application that:

- Loads parsed election data from `A05`’s helper functions
- Lets the user select year/state and type of chart
- Draws bar charts on a Tkinter `Canvas`
- Includes **Draw**, **Clear**, and **Quit** buttons

---

## Data Files

Two `.tab` files are included for assignments 5 and 6:

- **house.tab** – House of Representatives election results
- **president.tab** – Presidential election results

These are tab-delimited text files used by the parsing functions.

---

## Author

**Serge Hall**  
GitHub: [@SergeHall](https://github.com/SergeHall)  
Email: `serge.hall.dev@gmail.com`

---

## License

This repository is for **educational purposes only**, as part of coursework at **Santa Monica College**.  
Not intended for production or commercial use.
