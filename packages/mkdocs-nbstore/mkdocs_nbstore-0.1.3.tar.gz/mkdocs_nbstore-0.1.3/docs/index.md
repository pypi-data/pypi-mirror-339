# mkdocs-nbstore

mkdocs-nbstore is a plugin for MkDocs that allows you
to embed figures from Jupyter notebooks into your documentation.

Data scientists, researchers, and technical writers often face the
challenge of incorporating visualizations from Jupyter notebooks
into their documentation.
Traditional approaches involve taking screenshots, exporting figures manually,
or using complex embedding techniques - all of which create maintenance
overhead and break the direct connection between code and documentation.

This plugin solves these challenges by providing a seamless bridge between
your Jupyter notebooks and MkDocs documentation.
With a simple markdown syntax, you can reference and embed specific
figures directly from your notebooks, ensuring your documentation always
displays the most current visualizations without manual intervention.

## Installation

```bash
pip install mkdocs-nbstore
```

## Configuration

In your `mkdocs.yml`, add the following:

```yaml
plugins:
  - mkdocs-nbstore:
      notebook_dir: ../notebooks
```

`notebook_dir` is the directory containing your Jupyter notebooks
relative to the `docs_dir`.

## Usage

In your markdown files, you can use the following syntax to embed
figures from Jupyter notebooks:

```markdown
![alt text](my-notebook.ipynb){#figure-identifier}
```

The figure will be embedded from the Jupyter notebook
located in the `notebook_dir` directory.

In your notebook's code cell,
you can use a comment to identify the figure
with a figure identifier that starts with `#`:

```python title="../notebooks/my-notebook.ipynb"
# #figure-identifier
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(3, 2))
ax.plot([1, 3, 2, 4])
```

![alt text](matplotlib.ipynb){#matplotlib}

## Why Use mkdocs-nbstore?

This plugin offers several compelling benefits for data scientists,
researchers, and technical documentation authors:

- **Seamless Integration**: Directly embed Jupyter notebook
  visualizations in your MkDocs documentation with minimal effort.

- **Separation of Concerns**: Keep your code in notebooks and
  your documentation in Markdown files, while maintaining a direct
  connection between them.

- **Simple Syntax**: Use familiar Markdown image syntax with a
  small extension to reference notebook figures.

- **Precise Figure Selection**: Target specific visualizations
  within notebooks using simple comments.

- **Automatic Updates**: When you update your notebooks, your
  documentation visuals update automatically in MkDocs serve mode.

- **Improved Documentation Workflow**: Create visualizations in
  the ideal environment (Jupyter) and use them in your documentation
  without screenshot workflows or manual exports.

- **Clean Documentation Source**: Your Markdown remains clean and
  readable, with no need for complex embedding code.

Whether you're documenting data science projects, research findings,
or technical implementations, mkdocs-nbstore streamlines the process
of including visualizations in your documentation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
