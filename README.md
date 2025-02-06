# cbatch - Codebase Batcher

A CLI tool to output your codebase into a structured Markdown file for AI context.

## Installation

```bash
pip install .
```

## Testing 

**4. Local Installation and Testing:**

Now you can install your `cbatch` tool locally to test it!

1.  **Open your terminal or command prompt.**
2.  **Navigate to the directory** where you have `setup.py` and `cbatch.py` (and `README.md` if you created it).
3.  **Run the following command:**

    ```bash
    pip install .
    ```

    (Make sure you have pip installed and are using the correct Python environment if you are using virtual environments.)

4.  **Test your `cbatch` command:** After successful installation, you should be able to run `cbatch` from your terminal from **any directory**!

    ```bash
    cbatch --help
    ```

    You should see the help message defined in your `argparse` setup. Try running other commands like `cbatch init` and `cbatch update` to make sure they work as expected.

**5.  (Optional) Create Distribution Packages (for sharing or uploading to PyPI):**

If you want to share your `cbatch` tool with others or upload it to PyPI (Python Package Index) so anyone can install it with `pip install cbatch` (after you upload to PyPI), you'll need to create distribution packages.

In the same directory as `setup.py`, run:

```bash
python setup.py sdist bdist_wheel
```