# Process Capability Metrics

***A simple utility to calculate Process Capability (Cpk) metrics.***

## Installation

### Standard Installation [Recommended]

Execute the following command in the terminal:

```bash
pip install cpkmetrics
```

NOTE: For macOS/Linux, use `pip3` if needed.

The other options for installation are:

### Installation/Run with uv

<details>
<summary>Click to expand</summary>

Install with the uv package manager (modern python tooling standard):

```bash
uv pip install cpkmetrics
```

</details>

### Install From Source

<details>
<summary>Click to expand</summary>
Clone this repo and install:

```bash
git clone https://github.com/your-username/cpkmetrics.git  # Replace with actual repo URL
cd cpkmetrics
python -m venv venv # Optically create virtual environment - not necessary given the lack of dependencies in this package
source venv/bin/activate # On Windows: .\venv\Scripts\activate (Ignore if you dont create a venv)
pip install -e .
```

</details>

------

Alternatively, you can also forgo installation and run directly by using the `uv` package manager's `--with` feature.

```bash
uv run --with cpkmetrics my_python_code.py 
```

## Usage

A basic example calculating process capability metrics for a given mean, standard deviation and spec limits:

```python
from cpkmetrics.process_capability import ProcessCapability

# Example values for mean, stddev, USL, and LSL
mean = 10
stddev = 1
USL = 14
LSL = 6

# Create an instance of the ProcessCapability class with the provided parameters. Instantiation also automatically prints results to the terminal (unless you pass print_results=False arg)
pc = ProcessCapability(mean, stddev, USL, LSL)

# You can also access individual items directly through the corrresponding property
cpk = pc.process_capability_index

print(f"The Cpk is {round(cpk, 2)}")
#OUTPUT: The Cpk is 1.33
```

Further examples can be found [here](examples) including compatability with dataframes.

## Roadmap

- Skewness and Kurtosis metrics
- Allow setting threshold values for Cpk and Cpa Ratings
- Natural language results

## Contributing

Contributions are encouraged and welcome. Please note that the intent of this package is to remain very light weight, with no dependencies. Bug fixes, refactors and raising issues are highly encouraged. Please align to the design and engineering practices below and create a PR for contributions.

## Design and Engineering Practices

This project intends to have the smallest amount of code possible without sacrificing good design, structure and robust engineering practices that will allow future functionality, extensibility and forkability.

Documentation is copious - to maximize accessibility to AI/ML/SW engineers unfamiliar with statistical process control and for manufacturing/process/hardware engineers unfamiliar with python. Docstrings are detailed to allow for clarity as well as learning. In-line comments document code logic and design notes/decisions.

Project uses a modern toolchain to assist in this:

- **Project Management and Build:** pyproject.toml compliant to PEP 751 though `uv`
- **Testing:** `pytest` and `coverage`
- **Code Quality:** Linting, Formatting through `ruff` Static Analysis through `mypy`. Enforced through pre-commmit and GitHub Actions
- **Documentation:** Docstrings are enforced with `interrogate` at 90% threshold
