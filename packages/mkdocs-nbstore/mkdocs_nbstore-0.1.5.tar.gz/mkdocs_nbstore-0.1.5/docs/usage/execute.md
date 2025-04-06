# Execute Option

The `.execute` class option allows you to dynamically execute
notebooks when building your documentation. This powerful feature
ensures your documentation always displays the most up-to-date
results without requiring manual notebook execution.

## Basic Usage

To execute a notebook when referenced in your documentation,
simply add the `.execute` class option:

```markdown
![Cell output](notebook.ipynb){#data-visualization .execute}
```

This will execute the entire notebook before extracting and
displaying the specified cell's output.

## Requirements

To use the `.execute` option, you need to have nbconvert
installed:

```bash
pip install nbconvert
```

## Key Benefits

### 1. Automated Workflow

The `.execute` option streamlines your documentation workflow:

- **No manual execution required** - notebooks are automatically
  executed during documentation build
- **Apply once, execute completely** - adding `.execute` to one
  reference executes the entire notebook
- **State preservation** - executed notebook states are preserved
  during development server sessions

### 2. Smart Execution Management

mkdocs-nbstore intelligently manages notebook execution:

- **Execution caching** - notebooks are only re-executed when
  necessary
- **Change detection** - automatically re-executes when notebook
  content changes
- **No duplication needed** - apply `.execute` to just one cell
  reference per notebook

### 3. Documentation Consistency

Using `.execute` ensures documentation consistency:

- **Fresh results** - visualizations and outputs always reflect
  the current code
- **No stale outputs** - eliminates inconsistencies from partial
  manual executions
- **Clean notebook states** - entire notebooks are executed,
  preventing internal state conflicts

## Usage Patterns

### Single Execution Point

You only need to add `.execute` to one cell reference per
notebook, typically the first one:

```markdown
![First visualization](analysis.ipynb){#first-chart .execute}

More explanation here...

![Second visualization](analysis.ipynb){#second-chart}
```

### Combining with Other Options

The `.execute` option can be combined with other display options:

```markdown
![Execute and show full cell](notebook.ipynb){#setup .execute .cell}
![Execute and show only source](notebook.ipynb){#helper-function .execute .source}
```

## Behavior Notes

- Executed notebooks are **not saved back** to disk - your
  original notebooks remain unchanged
- Once executed in a serve session, notebooks won't be re-executed
  when markdown files change
- Notebooks will automatically re-execute when their content
  changes
- The entire notebook is always executed, ensuring all cells have
  consistent state

This execution model provides a perfect balance between
performance and up-to-date documentation.
