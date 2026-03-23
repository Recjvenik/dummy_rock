"""Seed 6 new foundation modules for Class 8-10 students."""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from modules.models import Module, Section, Concept, QuizQuestion, PracticalExercise

FOUNDATION_MODULES = [
    {
        'order': 8, 'title': 'How Computers Think',
        'subtitle': 'Discover how machines process information using binary, logic gates, and basic algorithms.',
        'description': 'Binary numbers, logic gates (AND/OR/NOT), flowcharts, how CPUs work, and what makes a computer "smart".',
        'difficulty': 'beginner', 'tag': 'foundation', 'icon': '💻', 'color': '#00ff88',
        'estimated_time': 40, 'grade_level': '8',
        'prerequisites': 'Basic math (addition, multiplication)',
        'learning_objectives': 'Understand binary numbers\nLearn how logic gates work\nDraw simple flowcharts\nExplain how a CPU processes instructions',
        'sections': [
            {'order': 1, 'title': 'The Language of Computers: Binary',
             'content_md': """# Binary: The Language of 0s and 1s

Computers don't understand English or Hindi — they only understand **two things**: **0** and **1**. This is called **binary**.

## Why Binary?

Computers are electronic machines. Inside them, tiny switches called **transistors** can be either:
- **OFF** = 0
- **ON** = 1

Think of it like a light switch — it's either on or off. There's no "half on"!

## How Binary Works

In our normal number system (decimal), we use digits 0-9 and multiply by powers of 10:
- 253 = 2×100 + 5×10 + 3×1

In binary, we only use 0 and 1, and multiply by powers of 2:
- 1011 in binary = 1×8 + 0×4 + 1×2 + 1×1 = **11** in decimal

## Binary Counting

| Decimal | Binary |
|---------|--------|
| 0       | 0000   |
| 1       | 0001   |
| 2       | 0010   |
| 3       | 0011   |
| 4       | 0100   |
| 5       | 0101   |
| 6       | 0110   |
| 7       | 0111   |
| 8       | 1000   |

## Real-World Example

When you type the letter "A" on your keyboard, the computer sees it as the binary number **01000001** (which is 65 in decimal). Every character, image, and video you see is just a huge collection of 0s and 1s!

## Try It Yourself
Convert these decimal numbers to binary:
1. 6 = ?
2. 10 = ?
3. 15 = ?

**Answers:** 110, 1010, 1111""",
             'key_insight': 'Everything in a computer — text, images, videos, games — is stored as patterns of 0s and 1s.',
             'has_visualizer': False},

            {'order': 2, 'title': 'Logic Gates: The Building Blocks',
             'content_md': """# Logic Gates

Logic gates are tiny electronic circuits that make decisions based on simple rules. They are the **building blocks** of all computers!

## The Three Basic Gates

### AND Gate
Both inputs must be 1 (ON) for the output to be 1.

| Input A | Input B | Output |
|---------|---------|--------|
| 0       | 0       | 0      |
| 0       | 1       | 0      |
| 1       | 0       | 0      |
| 1       | 1       | **1**  |

**Real-world example:** A bank locker needs TWO keys to open. Both Key A AND Key B must be present.

### OR Gate
At least one input must be 1 for the output to be 1.

| Input A | Input B | Output |
|---------|---------|--------|
| 0       | 0       | 0      |
| 0       | 1       | **1**  |
| 1       | 0       | **1**  |
| 1       | 1       | **1**  |

**Real-world example:** A doorbell rings if Person A OR Person B presses the button.

### NOT Gate
Flips the input — 0 becomes 1, and 1 becomes 0.

| Input | Output |
|-------|--------|
| 0     | **1**  |
| 1     | **0**  |

**Real-world example:** A light switch — if the light is ON, pressing the switch turns it OFF.

## Combining Gates

By combining these simple gates, we can build circuits that:
- **Add numbers** (adder circuit)
- **Compare values** (comparator)
- **Store data** (memory)
- **Make decisions** (processor)

Your computer's processor has **billions** of these tiny gates working together!""",
             'key_insight': 'Just three simple logic gates (AND, OR, NOT) combined billions of times = the entire computer!',
             'has_visualizer': True, 'visualizer_type': 'logic_gates'},

            {'order': 3, 'title': 'Flowcharts: Thinking Step by Step',
             'content_md': """# Flowcharts: Teaching Computers to Think

Before we can tell a computer what to do, we need to break down problems into clear steps. A **flowchart** is a visual diagram that shows these steps.

## Flowchart Symbols

- **Oval** → Start / End
- **Rectangle** → Process (do something)
- **Diamond** → Decision (yes/no question)
- **Arrow** → Flow direction

## Example: Making Tea ☕

1. **Start**
2. Boil water
3. Add tea leaves
4. Wait 3 minutes
5. **Decision:** Do you want sugar?
   - **Yes** → Add sugar
   - **No** → Skip
6. Pour into cup
7. **End**

## Example: Is a Number Even or Odd?

1. **Start**
2. Input a number N
3. **Decision:** Is N ÷ 2 remainder = 0?
   - **Yes** → Print "Even"
   - **No** → Print "Odd"
4. **End**

## Why Flowcharts Matter for AI

AI systems follow similar step-by-step logic, but with one big difference: they can **learn** which steps to take by looking at data, instead of being told every step manually.

## Practice Activity
Draw a flowchart for: "Decide what to wear based on weather"
- If raining → take umbrella + raincoat
- If sunny → wear light clothes + sunglasses
- If cold → wear jacket""",
             'key_insight': 'Every computer program — and every AI system — is ultimately a series of step-by-step instructions.',
             'has_visualizer': False},

            {'order': 4, 'title': 'How Does a CPU Work?',
             'content_md': """# The CPU: The Brain of the Computer

The **CPU** (Central Processing Unit) is the "brain" of every computer. But unlike our brain, it can only do very simple things — it just does them incredibly fast!

## The Fetch-Execute Cycle

The CPU repeats these steps billions of times per second:

1. **FETCH** — Get the next instruction from memory
2. **DECODE** — Figure out what the instruction means
3. **EXECUTE** — Do the operation (add, compare, move data)
4. **STORE** — Save the result

This is called the **Fetch-Decode-Execute cycle**.

## How Fast is a CPU?

A modern CPU runs at about 4 GHz — that means it performs **4 billion cycles per second**!

| Year | CPU Speed | Example |
|------|-----------|---------|
| 1971 | 740 KHz   | Intel 4004 (first CPU) |
| 1993 | 66 MHz    | Pentium |
| 2006 | 2.93 GHz  | Core 2 Duo |
| 2024 | 5.8 GHz   | Latest processors |

## From CPU to AI

AI needs massive amounts of computation. That's why modern AI uses:
- **GPUs** (Graphics Processing Units) — originally for games, now for AI
- **TPUs** (Tensor Processing Units) — Google's AI-specific chips
- **NPUs** (Neural Processing Units) — AI chips in your phone!

The reason AI became practical in the 2010s: computers finally got fast enough to process the huge calculations needed.""",
             'key_insight': 'A CPU does only simple operations (add, compare, move) but does them 4 BILLION times per second.',
             'has_visualizer': False},
        ],
        'concepts': ['Binary', 'Logic Gates', 'Algorithm', 'Flowchart', 'CPU'],
        'quiz': [
            {'question': 'What is the binary representation of decimal 5?', 'option_a': '1010', 'option_b': '0101', 'option_c': '0011', 'option_d': '1100', 'correct_answer': 'b', 'explanation': '5 = 4+1 = 0101 in binary.', 'difficulty': 'beginner'},
            {'question': 'An AND gate gives output 1 only when:', 'option_a': 'Any input is 1', 'option_b': 'All inputs are 0', 'option_c': 'All inputs are 1', 'option_d': 'No inputs are given', 'correct_answer': 'c', 'explanation': 'AND gate requires ALL inputs to be 1 for output 1.', 'difficulty': 'beginner'},
            {'question': 'What does a NOT gate do?', 'option_a': 'Adds two numbers', 'option_b': 'Flips the input (0→1, 1→0)', 'option_c': 'Multiplies inputs', 'option_d': 'Stores data', 'correct_answer': 'b', 'explanation': 'NOT gate inverts: 0 becomes 1, 1 becomes 0.', 'difficulty': 'beginner'},
            {'question': 'How many logic gates are in a modern CPU?', 'option_a': 'Hundreds', 'option_b': 'Thousands', 'option_c': 'Millions', 'option_d': 'Billions', 'correct_answer': 'd', 'explanation': 'Modern CPUs contain billions of transistors forming logic gates.', 'difficulty': 'beginner'},
        ],
    },
    {
        'order': 9, 'title': 'Data & Patterns',
        'subtitle': 'Learn how data is collected, organized, and how to spot patterns — the foundation of all AI.',
        'description': 'Data types, tables, charts, statistics basics, pattern recognition, and why data is the fuel for AI.',
        'difficulty': 'beginner', 'tag': 'foundation', 'icon': '📊', 'color': '#ffd700',
        'estimated_time': 45, 'grade_level': '9',
        'prerequisites': 'How Computers Think (Module 8)',
        'learning_objectives': 'Understand different types of data\nCreate and read charts and graphs\nCalculate mean, median, mode\nRecognize patterns in data\nUnderstand why AI needs data',
        'sections': [
            {'order': 1, 'title': 'What is Data?',
             'content_md': """# Understanding Data

**Data** is raw information — facts, numbers, measurements, or observations. It's the fuel that powers all AI systems.

## Types of Data

### Numerical Data (Numbers)
- **Temperature**: 32°C
- **Height**: 165 cm
- **Test score**: 85 marks

### Categorical Data (Groups)
- **Color**: Red, Blue, Green
- **Subject**: Math, Science, English
- **Animal type**: Dog, Cat, Bird

### Text Data
- Messages, essays, books, websites

### Image Data
- Photos, drawings, medical scans

### Audio Data
- Music, speech, sound effects

## Structured vs Unstructured Data

| Type | Description | Example |
|------|-------------|---------|
| **Structured** | Organized in rows/columns | Excel spreadsheet, database |
| **Unstructured** | No fixed format | Social media posts, images, videos |

**Fun fact:** Over 80% of the world's data is unstructured! AI helps us make sense of it.

## Why Does AI Need Data?

Think of it this way:
- A child learns to recognize a dog by seeing **thousands** of dogs
- An AI learns to recognize a dog by seeing **millions** of dog photos
- More data + better data = smarter AI""",
             'key_insight': 'AI systems are only as good as the data they learn from. Garbage in = garbage out!',
             'has_visualizer': False},

            {'order': 2, 'title': 'Reading Charts & Graphs',
             'content_md': """# Visualizing Data

Charts and graphs help us understand data at a glance. AI scientists use them all the time!

## Types of Charts

### Bar Chart
Best for comparing categories.
- Example: Comparing test scores of students

### Line Chart
Best for showing trends over time.
- Example: Temperature changes throughout a week

### Pie Chart
Best for showing parts of a whole.
- Example: How students spend their day (study, play, sleep)

### Scatter Plot
Best for finding relationships between two things.
- Example: Height vs Weight of students

## Reading a Chart: Key Questions

When you see a chart, ask yourself:
1. **What** is being measured? (look at labels)
2. **What's the trend?** (going up, down, or flat?)
3. **Are there outliers?** (unusual data points)
4. **What's the story?** (what does the data tell us?)

## Correlation: Finding Connections

When two things change together, we say they are **correlated**:

- **Positive correlation**: As one goes UP, the other goes UP
  - Example: Study hours ↑ → Test scores ↑
- **Negative correlation**: As one goes UP, the other goes DOWN
  - Example: Screen time ↑ → Sleep hours ↓
- **No correlation**: No clear pattern
  - Example: Shoe size vs Test scores

> **Important:** Correlation ≠ Causation!
> Ice cream sales and drowning incidents both go up in summer, but ice cream doesn't cause drowning. Summer heat is the real cause!""",
             'key_insight': 'Correlation does NOT mean causation — this is one of the most important rules in data science.',
             'has_visualizer': False},

            {'order': 3, 'title': 'Basic Statistics for AI',
             'content_md': """# Statistics: Making Sense of Numbers

Statistics helps us summarize and understand data. Every AI system uses statistics!

## The Three Averages

Given test scores: 72, 85, 85, 90, 65, 85, 92

### Mean (Average)
Add all numbers ÷ count
- (72+85+85+90+65+85+92) ÷ 7 = **82**

### Median (Middle Value)
Arrange in order, pick the middle
- 65, 72, 85, **85**, 85, 90, 92 → Median = **85**

### Mode (Most Frequent)
The number that appears most often
- 85 appears 3 times → Mode = **85**

## When to Use Which?

| Measure | Best When | Watch Out |
|---------|-----------|-----------|
| Mean    | Data is evenly spread | Affected by extreme values |
| Median  | Data has extremes/outliers | Ignores actual values |
| Mode    | Finding most common category | May not exist |

## Standard Deviation

Tells you how **spread out** the data is:
- Small SD → data points are close together (consistent)
- Large SD → data points are spread far apart (variable)

## Why AI Needs Statistics

AI models use statistics to:
- **Find patterns** in messy data
- **Predict** future outcomes
- **Measure accuracy** of predictions
- **Handle uncertainty** (nothing is 100% certain!)""",
             'key_insight': 'Mean, median, and mode are the foundation of all data analysis — and therefore all AI.',
             'has_visualizer': False},

            {'order': 4, 'title': 'Pattern Recognition',
             'content_md': """# Pattern Recognition: How AI Sees the World

**Pattern recognition** is the ability to find regularities in data. It's the MOST important skill in AI!

## Patterns Are Everywhere

- **Number patterns**: 2, 4, 6, 8, ? → **10** (add 2 each time)
- **Visual patterns**: 🔴🔵🔴🔵🔴? → **🔵** (alternating colors)
- **Weather patterns**: Usually rains in July-August in India (monsoon)
- **Behavior patterns**: You usually eat lunch at 1 PM

## How Humans Recognize Patterns

Your brain is a pattern recognition machine:
- You recognize your friend's face in a crowd (face pattern)
- You know a song from just the first few notes (audio pattern)
- You can read messy handwriting (letter pattern)

## How AI Recognizes Patterns

AI uses the same idea, but with math:

1. **Collect thousands of examples**
2. **Find what's common** (features)
3. **Build a rule** (model)
4. **Test on new examples**

### Example: Spam Email Detection
The AI noticed patterns:
- Spam emails often contain: "FREE", "WINNER", "CLICK HERE"
- Spam emails often come from unknown senders
- Spam emails often have many exclamation marks!!!

By learning these patterns from millions of emails, AI can predict if a new email is spam.

## Activity: Find the Pattern!

Look at this data of students:

| Study Hours | Score |
|-------------|-------|
| 1           | 40    |
| 2           | 55    |
| 3           | 65    |
| 4           | 78    |
| 5           | 88    |

**Pattern:** More study hours → higher scores! This is a positive correlation, and AI can learn to predict your score based on study hours.""",
             'key_insight': 'AI is essentially a pattern-finding machine — it finds patterns that humans might miss in huge datasets.',
             'has_visualizer': True, 'visualizer_type': 'pattern_recognition'},
        ],
        'concepts': ['Data', 'Statistics', 'Pattern Recognition', 'Correlation', 'Mean', 'Median', 'Mode'],
        'quiz': [
            {'question': 'What is the mean of 10, 20, 30?', 'option_a': '10', 'option_b': '20', 'option_c': '30', 'option_d': '60', 'correct_answer': 'b', 'explanation': 'Mean = (10+20+30)/3 = 60/3 = 20.', 'difficulty': 'beginner'},
            {'question': 'When two things increase together, it is called:', 'option_a': 'Negative correlation', 'option_b': 'No correlation', 'option_c': 'Positive correlation', 'option_d': 'Causation', 'correct_answer': 'c', 'explanation': 'When both variables increase together, it is positive correlation.', 'difficulty': 'beginner'},
            {'question': 'Which type of data is a photo?', 'option_a': 'Numerical', 'option_b': 'Categorical', 'option_c': 'Structured', 'option_d': 'Unstructured', 'correct_answer': 'd', 'explanation': 'Images are unstructured data — they don\'t fit neatly into rows and columns.', 'difficulty': 'beginner'},
        ],
    },
]

FOUNDATION_MODULES_2 = [
    {
        'order': 10, 'title': 'Introduction to Programming Logic',
        'subtitle': 'Learn the building blocks of programming — variables, loops, conditions — using simple pseudocode.',
        'description': 'Variables, data types, if-else conditions, loops, functions, and pseudocode — no coding language needed!',
        'difficulty': 'beginner', 'tag': 'foundation', 'icon': '🧩', 'color': '#4d96ff',
        'estimated_time': 50, 'grade_level': '9',
        'prerequisites': 'How Computers Think, Data & Patterns',
        'learning_objectives': 'Understand variables and data types\nWrite if-else conditions\nUnderstand loops (for, while)\nWrite simple pseudocode algorithms',
        'sections': [
            {'order': 1, 'title': 'Variables: Storing Information',
             'content_md': """# Variables: Giving Names to Data

A **variable** is like a labeled box where you store information.

## Creating Variables (Pseudocode)

```
name = "Ravi"
age = 15
height = 5.6
is_student = True
```

## Data Types

| Type | Example | Description |
|------|---------|-------------|
| **Integer** | 42 | Whole numbers |
| **Float** | 3.14 | Decimal numbers |
| **String** | "Hello" | Text (in quotes) |
| **Boolean** | True/False | Yes or No |

## Operations

```
x = 10
y = 3
sum = x + y       → 13
difference = x - y → 7
product = x * y    → 30
quotient = x / y   → 3.33
```

Variables can change:
```
score = 0
score = score + 10  → score is now 10
score = score + 5   → score is now 15
```""",
             'key_insight': 'Variables are the memory of a program — they store values that can change as the program runs.',
             'has_visualizer': False},
            {'order': 2, 'title': 'Conditions: Making Decisions',
             'content_md': """# If-Else: Teaching Computers to Decide

Conditions let programs make decisions — just like how you decide what to do.

## Basic If-Else

```
IF temperature > 35:
    PRINT "It's very hot! Stay hydrated."
ELSE IF temperature > 25:
    PRINT "Nice weather!"
ELSE:
    PRINT "It's cold. Wear a jacket."
```

## Comparison Operators

| Operator | Meaning |
|----------|---------|
| ==       | Equal to |
| !=       | Not equal to |
| >        | Greater than |
| <        | Less than |
| >=       | Greater than or equal |
| <=       | Less than or equal |

## Combining Conditions

```
IF age >= 18 AND has_license == True:
    PRINT "You can drive!"
ELSE:
    PRINT "You cannot drive yet."
```

## Real-World Example: Grading System

```
IF marks >= 90:
    grade = "A+"
ELSE IF marks >= 80:
    grade = "A"
ELSE IF marks >= 70:
    grade = "B"
ELSE IF marks >= 60:
    grade = "C"
ELSE:
    grade = "Need Improvement"
```

This is EXACTLY how AI makes decisions — but with thousands of conditions learned from data!""",
             'key_insight': 'AI decision-making is built on the same if-else logic, but with millions of conditions learned automatically.',
             'has_visualizer': False},
            {'order': 3, 'title': 'Loops: Repeating Actions',
             'content_md': """# Loops: Doing Things Again and Again

Loops let you repeat actions without writing the same code over and over.

## For Loop (Known Repetitions)

```
FOR i = 1 TO 5:
    PRINT "Hello! This is message number " + i
```
Output: Prints "Hello!" 5 times with numbers 1 through 5.

## While Loop (Unknown Repetitions)

```
password = ""
WHILE password != "secret123":
    password = INPUT("Enter password: ")
PRINT "Access granted!"
```

## Loop Example: Finding Sum

```
total = 0
FOR i = 1 TO 100:
    total = total + i
PRINT total  → 5050
```

The great mathematician Gauss figured this out in seconds at age 7!

## Why Loops Matter for AI

AI training is essentially a giant loop:
```
FOR epoch = 1 TO 1000:
    prediction = model.predict(data)
    error = actual - prediction
    model.update_weights(error)
PRINT "Training complete!"
```

Every AI model is trained by repeating this process thousands or millions of times!""",
             'key_insight': 'AI training = a giant loop that runs millions of times, getting a tiny bit smarter each time.',
             'has_visualizer': False},
        ],
        'concepts': ['Variable', 'Data Type', 'Condition', 'Loop', 'Algorithm', 'Pseudocode'],
        'quiz': [
            {'question': 'What is the value of x after: x = 5; x = x + 3?', 'option_a': '5', 'option_b': '3', 'option_c': '8', 'option_d': '15', 'correct_answer': 'c', 'explanation': 'x starts at 5, then 5+3=8.', 'difficulty': 'beginner'},
            {'question': 'Which loop type is best when you know exactly how many times to repeat?', 'option_a': 'While loop', 'option_b': 'For loop', 'option_c': 'If-else', 'option_d': 'Function', 'correct_answer': 'b', 'explanation': 'FOR loops are used when the number of iterations is known.', 'difficulty': 'beginner'},
        ],
    },
    {
        'order': 11, 'title': 'Math for AI',
        'subtitle': 'The essential math concepts that power AI — from basic algebra to probability and matrices.',
        'description': 'Linear equations, coordinate geometry, probability, statistics, matrices, and how they connect to AI.',
        'difficulty': 'intermediate', 'tag': 'foundation', 'icon': '🔢', 'color': '#ff6bca',
        'estimated_time': 60, 'grade_level': '10',
        'prerequisites': 'Data & Patterns, Introduction to Programming Logic',
        'learning_objectives': 'Understand linear equations and graphs\nCalculate basic probability\nWork with simple matrices\nConnect math concepts to AI applications',
        'sections': [
            {'order': 1, 'title': 'Linear Equations & Graphs',
             'content_md': """# Linear Equations: The Foundation of ML

The equation **y = mx + b** is the most important equation in machine learning!

## What is a Linear Equation?

A straight line on a graph: `y = mx + b`
- **m** = slope (how steep the line is)
- **b** = y-intercept (where the line crosses the y-axis)
- **x** = input
- **y** = output/prediction

## Examples

| Equation | Slope | Y-intercept | Meaning |
|----------|-------|-------------|---------|
| y = 2x + 1 | 2 | 1 | For every +1 in x, y increases by 2 |
| y = -0.5x + 10 | -0.5 | 10 | For every +1 in x, y decreases by 0.5 |
| y = 3x | 3 | 0 | Passes through origin |

## Connection to AI

**Linear Regression** (the simplest ML algorithm) finds the best values of m and b to fit your data!

```
# AI finds: Study hours → Test score
# y = 12x + 30
# If you study 5 hours: score = 12(5) + 30 = 90!
```""",
             'key_insight': 'Linear regression — the first ML algorithm — is just finding the best y = mx + b for your data.',
             'has_visualizer': True, 'visualizer_type': 'gradient_descent'},
            {'order': 2, 'title': 'Probability: Handling Uncertainty',
             'content_md': """# Probability: How AI Handles Uncertainty

AI doesn't give yes/no answers — it gives **probabilities** (how likely something is).

## Basic Probability

**Probability = Favorable outcomes ÷ Total outcomes**

### Coin Flip
- P(Heads) = 1/2 = 0.5 = 50%

### Die Roll
- P(getting 6) = 1/6 = 16.7%
- P(even number) = 3/6 = 50%

## Probability Rules

- P(something) is always between 0 and 1
- P(sure thing) = 1 (100%)
- P(impossible) = 0 (0%)
- P(A or B) = P(A) + P(B) - P(A and B)

## How AI Uses Probability

When you ask ChatGPT a question, it doesn't "know" the answer — it calculates the **probability of each possible next word**:

```
"The capital of India is ___"

P("New") = 0.85
P("Old") = 0.05
P("Mumbai") = 0.03
...

AI picks "New" → then "Delhi" → highest probability!
```

## Bayes' Theorem (The AI Favorite)

Bayes' theorem updates beliefs based on new evidence:

**P(A|B) = P(B|A) × P(A) / P(B)**

Example: If a medical test is 95% accurate, and the disease affects 1% of people, what's the chance you actually have the disease if you test positive? (Answer: only ~16%! This surprises most people.)""",
             'key_insight': 'Every AI prediction is really a probability — AI doesn\'t "know" things, it calculates how likely they are.',
             'has_visualizer': False},
        ],
        'concepts': ['Linear Equation', 'Slope', 'Probability', 'Matrix', 'Bayes Theorem'],
        'quiz': [
            {'question': 'In y = mx + b, what does m represent?', 'option_a': 'Y-intercept', 'option_b': 'Slope', 'option_c': 'Input', 'option_d': 'Output', 'correct_answer': 'b', 'explanation': 'm is the slope — how steep the line is.', 'difficulty': 'beginner'},
            {'question': 'What is the probability of rolling an even number on a die?', 'option_a': '1/6', 'option_b': '1/3', 'option_c': '1/2', 'option_d': '2/3', 'correct_answer': 'c', 'explanation': 'Even numbers are 2,4,6 = 3 out of 6 = 1/2.', 'difficulty': 'beginner'},
        ],
    },
    {
        'order': 12, 'title': 'Building Your First Model',
        'subtitle': 'Step-by-step guide to building, training, and testing your first AI model with visuals.',
        'description': 'The ML pipeline: collect data, prepare it, choose a model, train, evaluate, and improve.',
        'difficulty': 'intermediate', 'tag': 'practical', 'icon': '🏗️', 'color': '#00e5ff',
        'estimated_time': 55, 'grade_level': '10',
        'prerequisites': 'Math for AI, Data & Patterns',
        'learning_objectives': 'Understand the ML pipeline end-to-end\nPrepare data for training\nTrain a simple classification model\nEvaluate model accuracy\nUnderstand overfitting and underfitting',
        'sections': [
            {'order': 1, 'title': 'The Machine Learning Pipeline',
             'content_md': """# Building AI: A Step-by-Step Process

Building an AI model follows a clear pipeline. Let's learn each step!

## The 6 Steps

### Step 1: Define the Problem
What do you want to predict?
- "Is this email spam or not?" (Classification)
- "What will tomorrow's temperature be?" (Regression)
- "Which students might need extra help?" (Prediction)

### Step 2: Collect Data
Gather examples (the more, the better!):
- At least 100 examples for simple problems
- Thousands for complex problems
- Millions for deep learning

### Step 3: Prepare Data
- Clean: Remove errors and missing values
- Split: Training set (80%) + Test set (20%)
- Normalize: Scale numbers to similar ranges

### Step 4: Choose & Train a Model
Start simple:
- Linear Regression (for numbers)
- Decision Tree (for categories)
- Neural Network (for complex patterns)

### Step 5: Evaluate
How good is your model?
- **Accuracy**: % of correct predictions
- **Precision**: Of all "yes" predictions, how many were right?
- **Recall**: Of all actual "yes" cases, how many did we catch?

### Step 6: Improve
- Add more data
- Try different models
- Tune parameters
- Fix errors in data""",
             'key_insight': 'The ML pipeline is: Problem → Data → Prepare → Train → Evaluate → Improve. Then repeat!',
             'has_visualizer': False},
            {'order': 2, 'title': 'Training: How AI Learns',
             'content_md': """# Training: How the AI Gets Smarter

Training is the process where an AI model learns from examples.

## Analogy: Learning to Shoot Baskets 🏀

1. **First attempt**: Throw the ball (probably miss)
2. **See the error**: Ball went too far left
3. **Adjust**: Throw a little to the right
4. **Repeat**: Each throw gets closer
5. **After 1000 throws**: You're quite accurate!

AI training works EXACTLY the same way:

## The Training Loop

```
REPEAT 1000 times:
    1. Model makes a PREDICTION
    2. Compare with ACTUAL answer
    3. Calculate ERROR (how wrong?)
    4. ADJUST model weights slightly
    5. Go back to step 1
```

## What are Weights?

Weights are numbers that the model adjusts during training:

```
Initial: score = 0.5 × study_hours + 0.3 × sleep_hours
After training: score = 12 × study_hours + 5 × sleep_hours
```

The model learned that study_hours matters much more than sleep_hours!

## When to Stop Training?

- **Underfitting**: Model is too simple, hasn't learned enough (train MORE)
- **Just Right**: Model works well on both training and test data ✓
- **Overfitting**: Model memorized training data but fails on new data (STOP!)""",
             'key_insight': 'Training is just a loop: predict → check error → adjust weights → repeat thousands of times.',
             'has_visualizer': True, 'visualizer_type': 'gradient_descent'},
        ],
        'concepts': ['Training', 'Testing', 'Accuracy', 'Overfitting', 'Underfitting', 'ML Pipeline'],
        'quiz': [
            {'question': 'What percentage of data is typically used for training?', 'option_a': '50%', 'option_b': '80%', 'option_c': '95%', 'option_d': '100%', 'correct_answer': 'b', 'explanation': 'Usually 80% for training and 20% for testing.', 'difficulty': 'beginner'},
            {'question': 'If your model works perfectly on training data but poorly on new data, it is:', 'option_a': 'Underfitting', 'option_b': 'Just right', 'option_c': 'Overfitting', 'option_d': 'Broken', 'correct_answer': 'c', 'explanation': 'Overfitting means the model memorized training data instead of learning general patterns.', 'difficulty': 'intermediate'},
        ],
    },
    {
        'order': 13, 'title': 'AI in the Real World',
        'subtitle': 'Explore how AI is used in healthcare, self-driving cars, chatbots, gaming, and more!',
        'description': 'Real-world AI applications, ethics, bias, careers in AI, and the future of artificial intelligence.',
        'difficulty': 'beginner', 'tag': 'knowledge', 'icon': '🌍', 'color': '#ff8c00',
        'estimated_time': 40, 'grade_level': '10',
        'prerequisites': 'AI Basics',
        'learning_objectives': 'Know real-world AI applications\nUnderstand AI ethics and bias\nExplore AI career paths\nThink critically about AI impact',
        'sections': [
            {'order': 1, 'title': 'AI Applications Around You',
             'content_md': """# AI Is Already Everywhere!

You interact with AI dozens of times every day without realizing it!

## AI in Your Daily Life

### 📱 Your Phone
- **Face unlock** — facial recognition AI
- **Autocorrect** — language model that predicts words
- **Camera** — AI enhances photos automatically
- **Voice assistant** — Siri, Google Assistant use NLP

### 🎮 Gaming
- **Game NPCs** — AI-controlled characters that adapt
- **Matchmaking** — AI pairs players of similar skill
- **Procedural generation** — AI creates game worlds

### 🏥 Healthcare
- **Disease detection** — AI reads X-rays and MRIs
- **Drug discovery** — AI predicts which molecules could be medicines
- **Personalized treatment** — AI recommends treatments based on genes

### 🚗 Self-Driving Cars
- **Computer vision** — seeing roads, pedestrians, signs
- **Path planning** — deciding where to drive
- **Decision making** — when to brake, accelerate, turn

### 💬 Chatbots & Assistants
- **ChatGPT, Claude** — conversation AI
- **Customer service bots** — answer common questions
- **Translation** — Google Translate uses neural networks

## AI in India 🇮🇳
- **Farming**: AI predicts crop diseases from leaf photos
- **Education**: Personalized learning platforms
- **Banking**: Fraud detection in UPI transactions
- **Healthcare**: AI-powered diagnostics in rural areas""",
             'key_insight': 'AI isn\'t just for tech companies — it\'s transforming healthcare, farming, education, and every industry.',
             'has_visualizer': False},
            {'order': 2, 'title': 'AI Ethics & Responsibility',
             'content_md': """# AI Ethics: Using AI Responsibly

With great power comes great responsibility. AI can help OR harm — depending on how we build it.

## Key Ethical Issues

### 1. Bias in AI
AI learns from data. If the data is biased, the AI will be biased too.

**Example:** An AI hiring tool trained mostly on male resumes started rejecting female candidates — not because women were less qualified, but because the training data was biased.

### 2. Privacy
AI needs data to learn. But whose data? And who consented?

- Facial recognition can identify you in public
- AI can predict your behavior from browsing history
- Voice assistants record what you say

### 3. Deepfakes
AI can create fake videos and audio that look real.
- Used for misinformation
- Can damage reputations
- Hard to detect

### 4. Job Displacement
AI automates many jobs — but also creates new ones.

**Jobs at risk:** Data entry, simple customer service, routine analysis
**New jobs:** AI trainers, ethics officers, prompt engineers, AI researchers

## The Responsible AI Checklist
✅ Is the training data fair and diverse?
✅ Can the AI explain its decisions?
✅ Is the AI being used to help people?
✅ Has potential harm been considered?
✅ Are humans still in control?

## Careers in AI

| Career | What You Do | Education |
|--------|-------------|-----------|
| ML Engineer | Build and deploy models | B.Tech + practice |
| Data Scientist | Analyze data, find insights | Statistics + coding |
| AI Researcher | Invent new AI methods | PhD (usually) |
| AI Ethics Officer | Ensure AI is fair | Multi-disciplinary |
| Prompt Engineer | Design AI instructions | Creative + technical |
| Robotics Engineer | Build AI-powered robots | Engineering + AI |""",
             'key_insight': 'AI is a tool — like fire or electricity. It can help or harm. We must build it responsibly.',
             'has_visualizer': False},
        ],
        'concepts': ['AI Ethics', 'Bias', 'Privacy', 'Deepfakes', 'AI Applications', 'Responsible AI'],
        'quiz': [
            {'question': 'AI bias usually comes from:', 'option_a': 'The computer hardware', 'option_b': 'Biased training data', 'option_c': 'The programming language used', 'option_d': 'The internet speed', 'correct_answer': 'b', 'explanation': 'AI learns from data — biased data leads to biased AI.', 'difficulty': 'beginner'},
            {'question': 'Which is NOT a real-world use of AI?', 'option_a': 'Disease detection from X-rays', 'option_b': 'Self-driving cars', 'option_c': 'Creating new physical objects from thin air', 'option_d': 'Language translation', 'correct_answer': 'c', 'explanation': 'AI cannot create physical objects — it works with digital information.', 'difficulty': 'beginner'},
        ],
    },
]

ADDITIONAL_CONCEPTS = [
    'Binary', 'Logic Gates', 'Flowchart', 'CPU', 'GPU', 'Data', 'Statistics',
    'Pattern Recognition', 'Correlation', 'Mean', 'Median', 'Mode',
    'Variable', 'Data Type', 'Condition', 'Loop', 'Pseudocode',
    'Linear Equation', 'Slope', 'Probability', 'Matrix', 'Bayes Theorem',
    'ML Pipeline', 'AI Ethics', 'Bias', 'Privacy', 'Deepfakes', 'Responsible AI',
    'AI Applications', 'Training', 'Testing', 'Accuracy',
]


class Command(BaseCommand):
    help = 'Seed foundation modules for Class 8-10 students'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding Foundation Modules (Class 8-10)...')

        # Create additional concepts
        concept_objs = {}
        for c in ADDITIONAL_CONCEPTS:
            obj, _ = Concept.objects.get_or_create(name=c)
            concept_objs[c] = obj
        self.stdout.write(f'  ✓ {len(ADDITIONAL_CONCEPTS)} concepts ensured')

        all_modules = FOUNDATION_MODULES + FOUNDATION_MODULES_2
        for mod_data in all_modules:
            slug = slugify(mod_data['title'])
            module, created = Module.objects.update_or_create(
                slug=slug,
                defaults={
                    'order': mod_data['order'],
                    'title': mod_data['title'],
                    'subtitle': mod_data['subtitle'],
                    'description': mod_data['description'],
                    'difficulty': mod_data['difficulty'],
                    'tag': mod_data['tag'],
                    'icon': mod_data['icon'],
                    'color': mod_data['color'],
                    'estimated_time': mod_data['estimated_time'],
                    'grade_level': mod_data.get('grade_level', 'all'),
                    'prerequisites': mod_data.get('prerequisites', ''),
                    'learning_objectives': mod_data.get('learning_objectives', ''),
                    'is_published': True,
                }
            )
            action = 'Created' if created else 'Updated'

            for s in mod_data.get('sections', []):
                Section.objects.update_or_create(
                    module=module, order=s['order'],
                    defaults={
                        'title': s['title'],
                        'content_md': s['content_md'],
                        'key_insight': s.get('key_insight', ''),
                        'has_visualizer': s.get('has_visualizer', False),
                        'visualizer_type': s.get('visualizer_type', ''),
                    }
                )

            for c_name in mod_data.get('concepts', []):
                if c_name in concept_objs:
                    module.concepts.add(concept_objs[c_name])

            for i, q in enumerate(mod_data.get('quiz', [])):
                QuizQuestion.objects.update_or_create(
                    module=module, order=i,
                    defaults={
                        'question_type': 'mcq',
                        'question': q['question'],
                        'option_a': q['option_a'],
                        'option_b': q['option_b'],
                        'option_c': q.get('option_c', ''),
                        'option_d': q.get('option_d', ''),
                        'correct_answer': q['correct_answer'],
                        'explanation': q.get('explanation', ''),
                        'difficulty': q.get('difficulty', 'beginner'),
                    }
                )

            section_count = len(mod_data.get('sections', []))
            self.stdout.write(f'  ✓ {action} Module {mod_data["order"]}: {mod_data["title"]} ({section_count} sections)')

        self.stdout.write(self.style.SUCCESS('\n✅ Foundation modules seeded successfully!'))
