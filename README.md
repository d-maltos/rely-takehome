# Space Missions Dashboard - RelyHealth Takehome

An interactive dashboard for visualizing and analyzing historical space mission data from 1957 onwards.

## Features

- **Interactive Dashboard**: Built with Streamlit for a user-friendly interface
- **Data Visualization**: 5+ interactive charts showing various insights
- **Data Table**: Sortable and filterable table view of all missions
- **Advanced Filtering**: Filter by date range, company, mission status, and location
- **Summary Statistics**: Key metrics at a glance
- **Programmatic Functions**: 8 required functions for automated testing

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd rely-takehome
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Dashboard

To launch the interactive dashboard:

```bash
streamlit run dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Project Structure

```
rely-takehome/
├── space_missions.csv          # Dataset file
├── space_missions_functions.py  # Required functions for programmatic testing
├── dashboard.py                 # Streamlit dashboard application
├── requirements.txt             # Python dependencies
├── test_functions.py            # Test file
├── README.md                    # This file
```

## Required Functions

All functions are implemented in `space_missions_functions.py` with exact signatures as specified:

1. `getMissionCountByCompany(companyName: str) -> int`
2. `getSuccessRate(companyName: str) -> float`
3. `getMissionsByDateRange(startDate: str, endDate: str) -> list`
4. `getTopCompaniesByMissionCount(n: int) -> list`
5. `getMissionStatusCount() -> dict`
6. `getMissionsByYear(year: int) -> int`
7. `getMostUsedRocket() -> str`
8. `getAverageMissionsPerYear(startYear: int, endYear: int) -> float`

### Testing Functions

You can test the functions programmatically:

```python
from space_missions_functions import *

# Example usage (outputs depend on the provided CSV dataset)
print(getMissionCountByCompany("NASA"))
print(getSuccessRate("NASA"))
print(getMissionsByDateRange("1957-10-01", "1957-12-31"))
print(getTopCompaniesByMissionCount(3))
print(getMissionStatusCount())
print(getMissionsByYear(2020))
print(getMostUsedRocket())
print(getAverageMissionsPerYear(2010, 2020))
```

## Visualizations

The dashboard includes 5 interactive visualizations:

1. **Mission Success Rate Over Time**: Line chart showing how success rates have evolved
   - **Why**: Identifies trends in mission reliability and technological improvements
   - **Method**: Line chart with markers for clear temporal visualization

2. **Missions by Company (Top 10)**: Horizontal bar chart of most active companies
   - **Why**: Shows industry leaders and their contributions to space exploration
   - **Method**: Horizontal bar chart for easy company name readability

3. **Mission Status Distribution**: Pie chart of mission outcomes
   - **Why**: Provides quick overview of overall mission reliability
   - **Method**: Pie chart with percentage labels for intuitive understanding

4. **Mission Launch Timeline**: Bar chart of missions per year
   - **Why**: Reveals trends in space activity and identifies high-activity periods
   - **Method**: Bar chart showing temporal patterns clearly

5. **Top Launch Locations**: Bar chart of most active launch sites
   - **Why**: Shows geographic distribution of space activity
   - **Method**: Horizontal bar chart for easy location comparison

## Dashboard Features

- **Interactive Filters**: 
  - Date range picker
  - Multi-select for companies
  - Multi-select for mission statuses
  - Multi-select for launch locations
  
- **Data Table**:
  - Search functionality
  - Sortable columns
  - Configurable rows per page
  - Real-time filtering

- **Summary Statistics**:
  - Total missions count
  - Overall success rate
  - Number of unique companies
  - Number of unique launch locations

## Technology Stack

- **Python 3.8+**: Programming language
- **Streamlit**: Web framework for dashboard
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations

## Error Handling

All functions include:
- Input validation
- Edge case handling (empty data, invalid inputs)
- Graceful error returns (0, 0.0, [], "", {} as appropriate)

## Notes

- The CSV file (`space_missions.csv`) must be in the same directory as the Python files
- All functions handle missing or invalid data gracefully
- The dashboard uses caching for improved performance
- Functions are designed to be resilient to various edge cases