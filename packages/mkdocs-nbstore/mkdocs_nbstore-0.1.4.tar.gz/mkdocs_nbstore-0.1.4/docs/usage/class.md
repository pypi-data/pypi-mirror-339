# Class Options

mkdocs-nbstore provides several class options that
allow you to control how Jupyter notebook content is
displayed in your documentation. These options can be
specified using standard Markdown attribute syntax.

## Default Behavior (No Class Options)

When no class options are specified, mkdocs-nbstore
displays only the figure output from the referenced
Jupyter notebook cell.

**Example:**

```markdown
![alt text](class.ipynb){#image}
```

This produces the following output:

![alt](class.ipynb){#image}

This default behavior is ideal for when you only want
to show visualizations without the accompanying code.

## Source Code Only: `.source` Option

The `.source` option instructs mkdocs-nbstore to
display only the source code of the cell, without
its output.

**Example:**

```markdown
![alt text](){#image .source}
```

This produces the following output:

![alt](){#image .source}

This option is useful when:

- You want to explain the code that generates a visualization
- The code itself is the primary focus
- You're creating tutorials where readers should focus on implementation

!!! note
    Here we use an empty parentheses `()` to tell the plugin
    to use the active notebook `class.ipynb`.

## Complete Cell: `.cell` Option

The `.cell` option displays both the source code and
the output of the cell, similar to how it appears in
Jupyter notebooks.

**Example:**

```markdown
![alt text](){#image .cell}
```

This produces the following output:

![alt](){#image .cell}

This option provides a comprehensive view and is ideal for:

- Educational content where both code and result are important
- Detailed explanations of data processing and visualization techniques
- Demonstrating how code changes affect output

## Combining Options

While `.source` and `.cell` cannot be meaningfully
combined (`.source` takes precedence), you can combine
them with other standard Markdown attributes:

**Example:**

```markdown
![alt](){#image .source title="My title" hl_lines="3 4"}
```

This produces the following output:

![alt](){#image .source title="My title" hl_lines="3 4"}

Here, we use two additional attributes:

- `title="My title"` to add a title to the image
- `hl_lines="3 4"` to highlight lines 3 and 4 in the source code

For more information on how to use the `title` and `hl_lines` attributes,
see the [Adding a title][title] and [Highlighting specific lines][hl_lines]
from the MkDocs Material documentation.

[title]: https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#adding-a-title
[hl_lines]: https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#highlighting-specific-lines

## Best Practices

- Use the default (no options) when you want a clean document focused on results
- Use `.source` for code-focused explanations or tutorials
- Use `.cell` for comprehensive educational material
- Be consistent with your choice of options throughout your documentation

These class options give you flexibility in how you
present Jupyter notebook content while maintaining a
clean, readable document structure.
