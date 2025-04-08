# Spreadsheet MCP

An MCP server for operating Google Spreadsheets (Google Sheets)

## Features

- Fetch data from Google Spreadsheets and display it in Markdown table format
- Get a list of column names (header row) from Google Spreadsheet sheets
- Identify the URL of a specified sheet name within a Google Spreadsheet
- Retrieve a list of all sheet names existing in a Google Spreadsheet
- Upload CSV files to Google Spreadsheets
- Copy the contents of one sheet to another sheet in Google Spreadsheets

This tool is designed for tabular sheets (with columns in the first row and no duplicate column names).

## Authentication

https://docs.gspread.org/en/latest/oauth2.html

## Configuration

```json
{
  "mcpServers": {
    "spreadsheet": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/yamitzky/spreadsheet-mcp.git",
        "spreadsheet-mcp"
      ]
    }
  }
}
```

## Development

### Setting up the development environment

```bash
# Clone the repository
git clone https://github.com/yamitzky/spreadsheet-mcp.git
cd spreadsheet-mcp

# Install development dependencies
uv sync
```

### Testing and Linting

```bash
# Run linting with ruff
ruff check .

# Run type checking with pyright
pyright
```
