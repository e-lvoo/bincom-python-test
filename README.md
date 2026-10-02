# Bincom Python Basic Developer Test

Python 3 program analyzing weekly dress-color data from the supplied HTML page. It answers the analysis questions and demonstrates PostgreSQL storage, recursive search, binary-to-decimal conversion, and Fibonacci summation.

## Requirements

- Python 3.9 or newer
- PostgreSQL and `psycopg2-binary` for Question 6 (optional for the other questions)

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install psycopg2-binary
python bincom_python_test.py
```

The script reads `python_class_question.html` by default. Pass a different HTML file as an argument if needed.

## PostgreSQL setup (Question 6)

Start PostgreSQL, create a database named `bincom`, and set `PG_DSN` to your local connection settings. For Homebrew PostgreSQL where your database role matches your macOS username:

```bash
createdb bincom
PG_DSN="dbname=bincom user=$(whoami) host=localhost" python bincom_python_test.py
```

The script creates or updates the `colour_frequencies` table. PostgreSQL is optional for the other questions.

## Analysis notes

- `BLEW` is normalized to `BLUE`; ambiguous `ARSH` is preserved as written.
- Since colors are categories, the program defines the mean-color result as the color whose count is closest to the average count across colors.
- The median is calculated over per-color frequencies; Question 4 reports population and sample variance.
- Question 7 uses recursive binary search on a sorted sample list.
- Question 8 generates four binary digits and converts them to base 10.
- Question 9 sums the first 50 Fibonacci values starting with 0 and 1.
