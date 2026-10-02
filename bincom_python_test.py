"""
Bincom Python Basic Developer Test
Usage:
    python bincom_python_test.py path/to/page.html
Optional env var for Q6:
    PG_DSN="dbname=bincom user=postgres password=secret host=localhost"
"""
import os
import random
import re
import statistics
import sys
from collections import Counter


# ---------------------------------------------------------------- parsing
# The page contains obvious typos. BLEW is clearly BLUE; ARSH is ambiguous
# (ASH? a typo for something else?) so it is left as its own colour.
CORRECTIONS = {"BLEW": "BLUE"}

def load_colours(html_path):
    """Pull every colour out of the weekly table (one <tr> per day)."""
    with open(html_path, encoding="utf-8", errors="ignore") as f:
        html = f.read()

    colours = []
    for row in re.findall(r"<tr.*?>(.*?)</tr>", html, flags=re.S | re.I):
        cells = re.findall(r"<td.*?>(.*?)</td>", row, flags=re.S | re.I)
        cells = [re.sub(r"<.*?>", "", c).strip() for c in cells]
        if len(cells) < 2:
            continue  # header or junk row
        day, shirts = cells[0], cells[1]
        if not re.match(r"(?i)^(mon|tues|wednes|thurs|fri|satur|sun)day$", day):
            continue
        for c in shirts.split(","):
            c = c.strip().upper()
            if c:
                colours.append(CORRECTIONS.get(c, c))
    return colours


# ---------------------------------------------------------------- analysis
def analyse(colours):
    freq = Counter(colours)
    total = sum(freq.values())
    counts = list(freq.values())

    # Q1: "mean colour" is ill-defined, so: the colour whose frequency is
    # closest to the mean frequency.
    mean_freq = statistics.mean(counts)
    mean_colour = min(freq, key=lambda c: abs(freq[c] - mean_freq))

    # Q2: mode
    top = max(counts)
    mode_colours = [c for c, n in freq.items() if n == top]

    # Q3: median. Median of the frequencies; report the colour(s) sitting there.
    median_freq = statistics.median(counts)
    median_colours = [c for c, n in freq.items() if n == median_freq]
    if not median_colours:  # even number of colours -> median falls between two
        s = sorted(freq.items(), key=lambda kv: kv[1])
        mid = len(s) // 2
        median_colours = [s[mid - 1][0], s[mid][0]]

    # Q4: variance of the frequencies
    pvar = statistics.pvariance(counts)
    svar = statistics.variance(counts)

    # Q5: P(red) when picking a shirt at random
    p_red = freq.get("RED", 0) / total

    return freq, total, mean_freq, mean_colour, mode_colours, median_freq, median_colours, pvar, svar, p_red


# ---------------------------------------------------------------- Q6
def save_to_postgres(freq):
    import psycopg2  # pip install psycopg2-binary

    dsn = os.environ.get("PG_DSN", "dbname=bincom user=postgres host=localhost")
    conn = psycopg2.connect(dsn)
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS colour_frequencies (
                       colour    VARCHAR(50) PRIMARY KEY,
                       frequency INTEGER NOT NULL
                   )"""
            )
            for colour, n in freq.items():
                cur.execute(
                    """INSERT INTO colour_frequencies (colour, frequency)
                       VALUES (%s, %s)
                       ON CONFLICT (colour) DO UPDATE SET frequency = EXCLUDED.frequency""",
                    (colour, n),
                )
    finally:
        conn.close()


# ---------------------------------------------------------------- Q7
def recursive_search(nums, target, lo=0, hi=None):
    """Recursive binary search on a sorted list. Returns index or -1."""
    if hi is None:
        hi = len(nums) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if nums[mid] == target:
        return mid
    if nums[mid] < target:
        return recursive_search(nums, target, mid + 1, hi)
    return recursive_search(nums, target, lo, mid - 1)


# ---------------------------------------------------------------- Q8
def random_binary_to_decimal():
    bits = "".join(random.choice("01") for _ in range(4))
    return bits, int(bits, 2)


# ---------------------------------------------------------------- Q9
def fib_sum(n=50):
    """Sum of the first n Fibonacci numbers, starting 0, 1, 1, 2, ..."""
    a, b, total = 0, 1, 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    # Default: the HTML file sitting next to this script, so it works from any cwd.
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "python_class_question.html")
    colours = load_colours(path)
    (freq, total, mean_freq, mean_colour, mode_colours,
     median_freq, median_colours, pvar, svar, p_red) = analyse(colours)

    print("Frequencies:", dict(freq.most_common()))
    print(f"Total shirts: {total}")
    print(f"1. Mean frequency {mean_freq:.2f} -> mean colour: {mean_colour}")
    print(f"2. Most worn: {', '.join(mode_colours)}")
    print(f"3. Median frequency {median_freq} -> median colour: {', '.join(median_colours)}")
    print(f"4. Variance of frequencies: population={pvar:.4f}, sample={svar:.4f}")
    print(f"5. P(red) = {p_red:.4f}")

    try:
        save_to_postgres(freq)
        print("6. Saved to PostgreSQL table colour_frequencies")
    except Exception as e:
        print("6. PostgreSQL save failed:", e)

    raw = input("7. Enter a number to search for: ")
    nums = sorted([3, 7, 11, 15, 22, 28, 34, 41, 56, 63, 79, 90])
    try:
        idx = recursive_search(nums, int(raw))
        print(f"   Found at index {idx}" if idx >= 0 else "   Not found")
    except ValueError:
        print("   Please enter an integer.")

    bits, dec = random_binary_to_decimal()
    print(f"8. {bits} (base 2) = {dec} (base 10)")
    print(f"9. Sum of first 50 Fibonacci numbers: {fib_sum(50)}")
