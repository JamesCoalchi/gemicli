# Gemicli

**Gemicli** is a Python package designed for executing simple tasks in the terminal using **Gemini AI**.

# Beta

Gemicli is currently in **beta**. While the core functionality is available, please be aware that it may contain bugs, incomplete features, or unexpected behavior. Use it with caution and feel free to report any issues or improvements on GitHub.

# Showcase

[![asciicast](https://asciinema.org/a/696070.svg)](https://asciinema.org/a/696070)

## Installation

### Prerequisites  
- Python 3.7 or higher. 

To install **Gemicli**, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/JamesCoalchi/gemicli.git
   ```

2. Navigate to the project directory:
   ```
   cd gemicli
   ```
   
3. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv  
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate  
   ```

4. Install the package:
   ```
   pip install .
   ```
## Testing the Installation

Run the following command to verify the installation:
```
gemicli -v
```
or
```
gemicli --version
```

## Usage

### Step 1: Configure the Gemini API Key

Before using the package, you need to configure your Gemini API key. Use the `-config` or `--configure` flag followed by your API key:

```
gemicli -config YOURAPIKEY
```

### Step 2: Use the Package with a Prompt

You can now use the package by providing a prompt with the `-p` or `--prompt` flag:

```
gemicli -p "a calendar for year 2025"
```

### Optional: Toggle Code Preview

You can switch the **Code Preview** feature on or off using the `-debug` or `--switch_debug` flag. By default, it is enabled. If disabled, it will only give the code output.

```
gemicli -debug
```

## Contributing

If you'd like to contribute to **Gemicli**, feel free to fork the repository, make changes, and submit a pull request.
