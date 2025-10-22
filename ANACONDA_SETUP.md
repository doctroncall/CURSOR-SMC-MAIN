# 🐍 MT5 Sentiment Bot - Anaconda Setup Guide

This guide explains how to run the MT5 Sentiment Analysis Bot using Anaconda or Miniconda.

## Why Use Anaconda?

- **Easier TA-Lib Installation**: TA-Lib is automatically installed via conda-forge (no manual compilation needed!)
- **Better Package Management**: Conda handles complex dependencies more reliably
- **Isolated Environments**: Keep your bot dependencies separate from other Python projects
- **Cross-Platform**: Works consistently on Windows, macOS, and Linux

## Prerequisites

1. **Install Anaconda or Miniconda**
   - **Anaconda** (Full distribution with many pre-installed packages): 
     - Download from: https://www.anaconda.com/products/distribution
   - **Miniconda** (Minimal installer, recommended for smaller footprint):
     - Download from: https://docs.conda.io/en/latest/miniconda.html

2. **MetaTrader 5** (Windows) or MT5 account access
3. **Git** (optional, for cloning the repository)

## Quick Start

### Step 1: Clone or Download the Repository

```bash
git clone <repository-url>
cd mt5-sentiment-bot
```

Or download and extract the ZIP file.

### Step 2: Run the Bot

**On Linux/macOS:**
```bash
chmod +x start_bot_conda.sh
./start_bot_conda.sh
```

**On Windows:**
```cmd
start_bot_conda.bat
```

That's it! The startup script will:
- ✅ Check if conda is installed
- ✅ Create the conda environment from `environment.yml`
- ✅ Install all dependencies (including TA-Lib)
- ✅ Set up the database
- ✅ Launch the Streamlit dashboard

### Step 3: Configure Your MT5 Credentials

On first run, you'll be prompted to edit the `.env` file with your MT5 credentials:

```env
MT5_LOGIN=your_account_number
MT5_PASSWORD=your_password
MT5_SERVER=your_broker_server
```

After editing, run the startup script again.

## Manual Setup (Alternative Method)

If you prefer to set up manually:

### 1. Create the Conda Environment

```bash
conda env create -f environment.yml
```

This creates an environment named `mt5-sentiment-bot` with all dependencies.

### 2. Activate the Environment

**Linux/macOS:**
```bash
conda activate mt5-sentiment-bot
```

**Windows:**
```cmd
conda activate mt5-sentiment-bot
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your MT5 credentials
```

### 4. Run the Application

```bash
streamlit run app.py
```

## Managing the Environment

### Update Dependencies

When `environment.yml` is updated:

```bash
conda env update -f environment.yml --prune
```

### List Installed Packages

```bash
conda list
```

### Export Your Environment

To create a snapshot of your exact package versions:

```bash
conda env export > environment-snapshot.yml
```

### Remove the Environment

If you need to start fresh:

```bash
conda deactivate
conda env remove -n mt5-sentiment-bot
```

## Advantages Over Regular Python Virtual Environment

| Feature | Conda | Venv (pip) |
|---------|-------|------------|
| TA-Lib installation | ✅ Automatic via conda-forge | ❌ Manual compilation required |
| Dependency resolution | ✅ Advanced solver | ⚠️ Basic |
| Binary packages | ✅ Pre-compiled | ⚠️ Sometimes needs compilation |
| Cross-platform | ✅ Consistent | ⚠️ Platform-specific issues |
| Package management | ✅ Conda + pip | pip only |

## Troubleshooting

### "conda: command not found"

**Solution:** Ensure Anaconda/Miniconda is installed and added to your PATH.

**On Linux/macOS:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/anaconda3/bin:$PATH"
# or for Miniconda
export PATH="$HOME/miniconda3/bin:$PATH"
```

Then restart your terminal or run:
```bash
source ~/.bashrc
```

**On Windows:** Reinstall Anaconda and check "Add Anaconda to PATH" during installation.

### Environment creation fails

**Solution 1:** Try creating with a specific Python version:
```bash
conda create -n mt5-sentiment-bot python=3.10
conda activate mt5-sentiment-bot
conda env update -f environment.yml
```

**Solution 2:** Install packages step by step:
```bash
conda create -n mt5-sentiment-bot python=3.10
conda activate mt5-sentiment-bot
conda install -c conda-forge ta-lib numpy pandas scikit-learn matplotlib
pip install -r requirements.txt
```

### TA-Lib still not working

Try installing from conda-forge explicitly:
```bash
conda activate mt5-sentiment-bot
conda install -c conda-forge ta-lib
```

### Slow package installation

**Solution:** Use mamba (faster conda alternative):
```bash
conda install -c conda-forge mamba
mamba env create -f environment.yml
```

### MT5 Connection Issues

These are usually not conda-related. See `TROUBLESHOOTING.md` for MT5-specific issues.

## Switching from Venv to Conda

If you were previously using the regular virtual environment:

1. **Backup your .env file** (if you have one)
2. **Remove old venv**: `rm -rf venv` (Linux/Mac) or `rmdir /s venv` (Windows)
3. **Follow the Quick Start steps above**
4. **Restore your .env file**

Your data, models, and logs will remain intact.

## Using with IDEs

### VSCode

1. Install the Python extension
2. Press `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Choose the conda environment: `mt5-sentiment-bot`

### PyCharm

1. File → Settings → Project → Python Interpreter
2. Click the gear icon → Add
3. Select "Conda Environment" → Existing environment
4. Choose the `mt5-sentiment-bot` environment

### Jupyter Notebook

To use the bot's environment in Jupyter:

```bash
conda activate mt5-sentiment-bot
conda install ipykernel
python -m ipykernel install --user --name=mt5-sentiment-bot
```

Then select "mt5-sentiment-bot" as the kernel in Jupyter.

## Development Workflow

### Activating for Development

```bash
conda activate mt5-sentiment-bot
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/ gui/ app.py
```

### Type Checking

```bash
mypy src/
```

## Additional Resources

- [Conda User Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/)
- [Managing Environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [Conda Cheat Sheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)

## Support

For issues specific to:
- **Bot functionality**: See `README.md` and `TROUBLESHOOTING.md`
- **MT5 connection**: See `CONNECTION_GUIDE.md`
- **Conda installation**: Visit https://docs.conda.io/

---

**Ready to trade smarter with Anaconda? Run the bot and let's go! 🚀**
