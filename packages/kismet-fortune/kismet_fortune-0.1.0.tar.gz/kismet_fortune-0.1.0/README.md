# kismet

An evolutionary re-take on `fortune-mod`, Kismet is a modern Python command-line tool that delivers random quotations from llm generators, offering a touch of serendipity to your terminal. 

## Features

* **Curated Quotations:**  Kismet includes a diverse and regularly updated collection of thought-provoking, humorous, and inspiring quotes.
* **Extensible Database:** Easily add your own custom quotes to personalize your experience.  The format for adding new quotes will be documented separately.
* **Multiple Output Formats:**  Support for plain text, JSON, and potentially other formats for integration with various tools and workflows.
* **Filtering and Search:**  Find specific quotes or categories of quotes using flexible filtering options.
* **Modern Tooling:** Built with Python and Poetry for a smooth development and installation process.
* **Fast Performance:** Optimized for quick retrieval of random quotations.

## Installation

Kismet can be installed using `poetry`:

```bash
poetry install kismet-fortune
```

## Useage

kismet                      # Displays a random quote
kismet --help              # Shows help information
kismet --version           # Displays the version
kismet -f json             # Outputs a random quote in JSON format
kismet -s "keyword"       # Searches for quotes containing "keyword"
kismet -c "category"     # Displays a quote from a specific category (if implemented)
# More advanced usage examples forthcoming in the documentation...


## Acknowledgements

Inspired by the original `fortune-mod` utility and its contributors. 
