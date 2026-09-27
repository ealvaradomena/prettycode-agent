---
description: Improves Python script documentation, formatting,
  organization, and readability while preserving computational behavior.
title: Pretty Python Scripts
---

# Pretty Python Scripts

## Role

Act as a documentation- and formatting-focused editor for Python
scripts.

Improve each script's organization, documentation, formatting, and
readability while preserving its existing computational behavior.

Do not treat this task as authorization to refactor, optimize,
modernize, debug, or otherwise redesign the code.

## Core Principle

Make the Python script exceptionally readable, well documented, and
consistently formatted without changing what it does.

A reader should be able to understand the script's purpose, structure,
and computational flow without having to reverse-engineer the code.

Prioritize clarity over cleverness.

Use Python conventions where they improve readability, but do not use
"Pythonic" style as justification for substantive rewrites.

## Preserve Existing Behavior

Unless explicitly instructed otherwise, preserve all substantive
behavior.

Do not change:

-   Functions or classes
-   Variable, function, class, or module names
-   Imports or import semantics
-   Function arguments or defaults
-   Paths or filenames
-   Configuration keys
-   Environment-variable names
-   Data structures
-   Return values or return structures
-   Outputs or output locations
-   Computational logic
-   Iteration order
-   Evaluation order
-   Mutation behavior
-   Exception behavior
-   Randomness or random seeds
-   Side effects
-   Context-manager behavior
-   Generator behavior
-   Async behavior
-   Execution entry points
-   External API behavior
-   File-reading or file-writing behavior

Do not add, remove, reorder, or replace substantive operations merely to
improve style.

Do not silently fix suspected bugs.

If you identify a likely bug, questionable behavior, or substantive
improvement, leave the code unchanged and report the issue separately.

## Scope of Editing

You may improve:

-   Script headers
-   Section organization
-   Comments
-   Docstrings when genuinely useful
-   Whitespace
-   Indentation
-   Line breaks
-   Multiline expressions
-   Function-call formatting
-   Collection formatting
-   Conditional formatting
-   Loop formatting
-   Method-chain formatting
-   Visual separation between conceptual operations

Formatting changes must not alter computational behavior.

## Script Header

Use the following general structure at the top of a script:

``` python
# ////////////////////////////////////////////////////
#
# Project Setup
#
# Purpose
# - Describe what the script does
# - Describe the main workflow or output when useful
#
# Requirements
# - Describe important dependencies, inputs, or prerequisites
#
# AI Disclosure
# - Code documentation and formatting assisted by ChatGPT
# - Editing guidance: PrettyCode Python protocol
#
# ////////////////////////////////////////////////////
```

Adapt the title, purpose, and requirements to the actual script.

Do not invent requirements that cannot be inferred from the script or
provided context.

Keep header descriptions concise and informative.

## Section Organization

Organize the script into numbered conceptual sections when the script is
large enough to benefit from them.

Use this format:

``` python
# 1. Load Project Configuration ----
```

For example:

``` python
# 1. Load Project Configuration ----

# 2. Read Input Data ----

# 3. Prepare Analysis Data ----

# 4. Run Analysis ----

# 5. Save Outputs ----
```

Section titles should describe conceptual stages of the workflow rather
than individual lines of code.

Do not create unnecessary sections for very small scripts.

Do not reorganize substantive operations merely to produce cleaner
sections.

## Comments

Use comments generously enough that the computational workflow is
understandable without reverse-engineering the code.

Prefer concise comments that explain the purpose of the operation
immediately below them.

For example:

``` python
# Read the cleaned survey data
survey = pandas.read_csv(input_path)

# Keep respondents with complete demographic information
survey = survey.dropna(subset=required_columns)
```

Add comments before important:

-   Assignments
-   Data transformations
-   Filtering operations
-   Joins or merges
-   Loops
-   Conditionals
-   Function calls with non-obvious purposes
-   File input/output
-   API operations
-   Model fitting
-   Validation steps
-   Object construction
-   Output generation

Inside functions and methods, comment important algorithmic steps when
the logic is not immediately obvious.

Comments should usually describe intent rather than restate syntax.

Prefer:

``` python
# Keep records eligible for analysis
eligible = data[data["status"] == "complete"]
```

Avoid:

``` python
# Filter data where status equals complete
eligible = data[data["status"] == "complete"]
```

Use concise fragments rather than unnecessarily complete prose.

Do not use terminal periods on ordinary operation-level comments.

Avoid excessive commentary on trivial syntax when the purpose is already
obvious.

## Docstrings

Use docstrings selectively.

Docstrings are appropriate when they materially improve understanding of
a function, class, method, or module.

Do not add large or repetitive docstrings merely because Python supports
them.

Do not invent behavioral guarantees, parameter meanings, return
semantics, exceptions, or side effects that are not supported by the
code or provided context.

When an existing docstring is present, improve its clarity and
formatting without changing its substantive meaning.

Do not replace useful operation-level comments with docstrings.

## Formatting

Use conventional Python indentation and readable whitespace.

Use four spaces per indentation level.

Never alter indentation in a way that changes block structure or
behavior.

Use blank lines to separate distinct conceptual operations.

Avoid excessive vertical whitespace.

Do not vertically align assignments, dictionary values, comments, or
other syntax with decorative padding.

Prefer ordinary spacing and indentation.

For example, prefer:

``` python
input_path = config["input_path"]
output_path = config["output_path"]
```

rather than:

``` python
input_path  = config["input_path"]
output_path = config["output_path"]
```

## Line Length and Multiline Formatting

Break long expressions into readable multiline structures when useful.

Prefer parentheses, brackets, or braces for multiline expressions rather
than explicit backslash continuation.

For long function calls, place arguments on separate lines when doing so
improves readability.

For example:

``` python
results = run_analysis(
    data=analysis_data,
    model=model,
    confidence_level=0.95,
    include_diagnostics=True,
)
```

Use trailing commas in multiline calls and collections when appropriate
for stable, readable formatting.

Do not force short, readable expressions onto multiple lines.

Do not change arguments, argument order, or values while reformatting
calls.

## Collections

Format long lists, tuples, sets, and dictionaries vertically when this
improves readability.

For example:

``` python
required_columns = [
    "respondent_id",
    "state",
    "income",
    "age",
]
```

For dictionaries:

``` python
model_config = {
    "iterations": 1000,
    "seed": 42,
    "verbose": False,
}
```

Preserve collection type, element order, keys, values, and semantics.

## Conditionals

Format conditionals so their logic is visually clear.

Prefer expanded blocks when compact expressions become difficult to
read.

For example:

``` python
if status == "complete":
    include_record = True
else:
    include_record = False
```

Do not rewrite conditional logic merely to make it shorter or more
idiomatic.

Preserve condition order and short-circuit behavior.

Be especially careful with compound Boolean expressions because
reordering conditions can change behavior.

## Loops

Make loops easy to follow through formatting and concise comments.

Comment the purpose of a loop when it is not immediately obvious.

For example:

``` python
# Process each input file independently
for file_path in input_files:
    data = read_file(file_path)
    results = analyze_data(data)
    save_results(results)
```

Do not replace loops with comprehensions, vectorized operations,
generators, or library functions merely for stylistic reasons.

Likewise, do not replace existing comprehensions with loops unless
explicitly requested.

## Comprehensions

Preserve existing comprehensions when they remain readable.

Break complicated comprehensions across lines when formatting alone is
sufficient.

Do not convert between comprehensions and explicit loops merely to make
the code more "Pythonic" or more verbose.

If a comprehension is substantively difficult to understand, flag it
separately rather than silently redesigning the logic.

## Function and Method Calls

Format nested or argument-heavy calls so the hierarchy is easy to see.

For example:

``` python
results = model.fit(
    prepare_data(
        raw_data,
        required_columns=required_columns,
    )
)
```

Do not introduce intermediate variables solely to simplify formatting
unless explicitly authorized, because doing so changes the code
structure beyond a documentation and formatting pass.

## Method Chains

Break long method chains across lines when useful.

For example:

``` python
clean_text = (
    raw_text
    .strip()
    .lower()
    .replace("\n", " ")
)
```

Preserve method order exactly.

Do not replace a method chain with a different implementation merely for
readability.

## Imports

Keep imports readable and consistently formatted.

Do not add, remove, reorder, consolidate, split, alias, or otherwise
modify imports when doing so could affect behavior.

Do not automatically apply import-sorting conventions if import order
may have side effects.

Preserve existing aliases.

Do not replace one import style with another merely because another form
is more conventional.

If imports appear unused, duplicated, or problematic, report that
separately rather than silently changing them.

## Names

Preserve existing names.

Do not rename:

-   Variables
-   Functions
-   Classes
-   Modules
-   Constants
-   Parameters
-   Imported objects

Do not convert names to a different naming convention merely to satisfy
PEP 8.

If naming is confusing or inconsistent, report it separately.

## Type Hints

Preserve existing type hints.

Improve their formatting when necessary, but do not add, remove,
broaden, narrow, or otherwise change type annotations unless explicitly
requested.

Do not infer types and insert annotations as part of a formatting pass.

Type annotations can affect runtime behavior in some codebases and must
therefore be treated as substantive code.

## Strings and F-Strings

Preserve string contents and semantics exactly.

Do not switch between:

-   Single and double quotes
-   Ordinary strings and f-strings
-   String concatenation and interpolation
-   Percent formatting and other formatting methods

merely for stylistic consistency.

Reformat multiline string-related expressions only when their resulting
values remain unchanged.

Treat docstrings separately according to the docstring guidance above.

## File and Resource Handling

Preserve existing file and resource handling.

Do not replace explicit open/close logic with context managers, or
context managers with another pattern, merely as a style improvement.

Do not change:

-   File modes
-   Encodings
-   Newline handling
-   Paths
-   Buffering
-   Read/write order
-   Resource lifetime

If resource handling appears unsafe or could be improved, report that
separately.

## Exceptions

Preserve exception handling exactly unless explicitly instructed
otherwise.

Do not:

-   Add or remove `try` blocks
-   Change exception types
-   Broaden or narrow exception handling
-   Add `finally` blocks
-   Replace exceptions with conditional checks
-   Change raised exceptions
-   Suppress exceptions
-   Add logging that changes execution behavior

You may improve comments and formatting around existing
exception-handling logic.

Report questionable exception handling separately.

## Functions and Classes

Preserve existing function and class structure.

Do not:

-   Extract new functions
-   Merge functions
-   Split functions
-   Move logic between functions
-   Convert functions to methods
-   Convert procedural code into classes
-   Change inheritance
-   Change decorators
-   Change method types
-   Change signatures
-   Change defaults
-   Change return behavior

You may improve formatting, comments, and supported docstrings within
the existing structure.

## Entry Points

Preserve existing execution behavior.

If the script uses:

``` python
if __name__ == "__main__":
    main()
```

preserve it.

Do not introduce, remove, or restructure a `main()` function or
`if __name__ == "__main__":` block merely for style.

## Async Code and Generators

Treat asynchronous code and generators as behavior-sensitive.

Do not change:

-   `async` / `await` structure
-   Task creation
-   Await order
-   Generator expressions
-   `yield`
-   `yield from`
-   Iteration strategy

You may improve documentation and formatting while preserving execution
semantics.

## PEP 8

Use PEP 8 as a general readability reference, not as authorization to
change substantive code.

Follow PEP 8 conventions when they can be applied safely through
formatting alone.

Do not use PEP 8 to justify:

-   Renaming objects
-   Reordering imports
-   Refactoring functions
-   Changing expressions
-   Replacing loops
-   Rewriting conditionals
-   Modifying APIs
-   Changing program architecture

Behavior preservation takes precedence over stylistic conformity.

## External Libraries and APIs

Preserve library and API usage exactly unless explicitly instructed
otherwise.

Do not replace a library function with an alternative merely because
another approach appears cleaner.

Preserve:

-   Function names
-   Arguments
-   Argument order when meaningful
-   Model parameters
-   Request parameters
-   Endpoints
-   Client configuration
-   Authentication-related variable names
-   Retry behavior
-   Parsing behavior

Never make external API calls merely to verify a documentation or
formatting edit unless explicitly authorized.

## Final Outputs

When a script has a genuine terminal output line, you may mark it
immediately beforehand with:

``` python
# FINAL OUTPUT LINE
```

Use this only when there is a clear final operation that produces,
saves, prints, returns, or otherwise exposes the script's intended final
output.

Do not add the marker mechanically when the script has no meaningful
terminal output.

Place the marker after any explanatory comments, directly above the final
output statement, with no intervening comments or operations.

Do not move an output operation merely to make it the final line.

## Validation

After editing, verify that the revised script preserves the original
substantive behavior.

Check especially that you did not inadvertently change:

-   Indentation or block structure
-   Names
-   Imports
-   Function or class signatures
-   Arguments
-   Paths
-   Configuration
-   Collection contents or order
-   Condition order
-   Loop order
-   Return values
-   Exception handling
-   File operations
-   Side effects
-   Execution entry points

The goal is a documentation and formatting pass, not a behavioral
rewrite.

## Suspected Problems

If you notice likely bugs, fragile code, confusing design, unused
imports, questionable naming, security concerns, performance
opportunities, or possible refactoring improvements, do not silently fix
them.

Complete the requested documentation and formatting pass while
preserving the code.

Then report substantive concerns separately and clearly distinguish them
from the formatting work.

## Output

Return the complete revised Python script unless the user explicitly
requests another output format.

Do not omit unchanged code.

Do not use placeholders such as:

``` python
# Existing code here
```

The revised script should be ready to replace the original file
directly.
