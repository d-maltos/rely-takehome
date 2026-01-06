"""
space_missions_functions.py
Author: Dylan Maltos
Last Updated: 2026-01-05

Rely Health Takehome - Space Missions Functions
This module contains all required functions for programmatic testing
"""

import pandas as pd
from typing import List, Tuple, Dict
from datetime import datetime

# Load data once when module is imported
def _load_data():
    """Load space missions data from CSV file"""
    try:
        df = pd.read_csv('space_missions.csv')
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
        return df
    except FileNotFoundError:
        raise FileNotFoundError("space_missions.csv not found in the current directory")

# Cache the loaded dataframe
_dataframe = None

def _get_dataframe():
    """Get or load the dataframe"""
    global _dataframe
    if _dataframe is None:
        _dataframe = _load_data()
    return _dataframe.copy()

def getMissionCountByCompany(companyName: str) -> int:
    """
    Returns the total number of missions for a given company
    
    Args:
        companyName: Name of the company (ex, "SpaceX", "NASA", "RVSN USSR")
    
    Returns:
        Integer representing the total number of missions
    """
    if not isinstance(companyName, str):
        return 0
    
    df = _get_dataframe()
    count = len(df[df['Company'] == companyName])
    return int(count)

def getSuccessRate(companyName: str) -> float:
    """
    Calculates the success rate for a given company as a percentage
    
    Args:
        companyName: Name of the company
    
    Returns:
        Float representing success rate as a percentage (0-100), rounded to 2 decimal places
        Only "Success" missions count as successful
        Returns 0.0 if company has no missions
    """
    if not isinstance(companyName, str):
        return 0.0
    
    df = _get_dataframe()
    company_missions = df[df['Company'] == companyName]
    
    if len(company_missions) == 0:
        return 0.0
    
    success_count = len(company_missions[company_missions['MissionStatus'] == 'Success'])
    total_count = len(company_missions)
    
    if total_count == 0:
        return 0.0
    
    success_rate = (success_count / total_count) * 100
    return round(success_rate, 2)

def getMissionsByDateRange(startDate: str, endDate: str) -> list:
    """
    Returns a list of all mission names launched between startDate and endDate (inclusive)
    
    Args:
        startDate: Start date in "YYYY-MM-DD" format
        endDate: End date in "YYYY-MM-DD" format
    
    Returns:
        List of strings containing mission names, sorted chronologically
    """
    if not isinstance(startDate, str) or not isinstance(endDate, str):
        return []
    
    try:
        start = pd.to_datetime(startDate, format='%Y-%m-%d')
        end = pd.to_datetime(endDate, format='%Y-%m-%d')
    except (ValueError, TypeError):
        return []
    
    df = _get_dataframe()
    df = df[(df['Date'] >= start) & (df['Date'] <= end)]
    # Sort by Date, then Time, then Mission for deterministic ordering
    # Time is string format "HH:MM:SS" which sorts correctly as string
    df = df.sort_values(['Date', 'Time', 'Mission'], na_position='last')
    
    missions = df['Mission'].dropna().tolist()
    return [str(m) for m in missions]

def getTopCompaniesByMissionCount(n: int) -> list:
    """
    Returns the top N companies ranked by total number of missions
    
    Args:
        n: Number of top companies to return
    
    Returns:
        List of tuples: [(companyName, missionCount), ...]
        Sorted by mission count in descending order
        If companies have the same count, sort alphabetically by company name
    """
    if not isinstance(n, int) or n <= 0:
        return []
    
    df = _get_dataframe()
    company_counts = df['Company'].value_counts().reset_index()
    company_counts.columns = ['Company', 'Count']
    
    # Sort by count descending, then by company name ascending
    company_counts = company_counts.sort_values(['Count', 'Company'], ascending=[False, True])
    
    # Get top n
    top_n = company_counts.head(n)
    
    # Convert to list of tuples
    result = [(row['Company'], int(row['Count'])) for _, row in top_n.iterrows()]
    return result

def getMissionStatusCount() -> dict:
    """
    Returns the count of missions for each mission status
    
    Returns:
        Dictionary with status as key and count as value
        Keys: "Success", "Failure", "Partial Failure", "Prelaunch Failure"
    """
    df = _get_dataframe()
    status_counts = df['MissionStatus'].value_counts().to_dict()
    
    # Ensure all expected keys are present
    result = {
        "Success": int(status_counts.get("Success", 0)),
        "Failure": int(status_counts.get("Failure", 0)),
        "Partial Failure": int(status_counts.get("Partial Failure", 0)),
        "Prelaunch Failure": int(status_counts.get("Prelaunch Failure", 0))
    }
    
    return result

def getMissionsByYear(year: int) -> int:
    """
    Returns the total number of missions launched in a specific year
    
    Args:
        year: Year (ex, 2020)
    
    Returns:
        Integer representing the total number of missions in that year
    """
    if not isinstance(year, int):
        return 0
    
    df = _get_dataframe()
    df['Year'] = df['Date'].dt.year
    count = len(df[df['Year'] == year])
    return int(count)

def getMostUsedRocket() -> str:
    """
    Returns the name of the rocket that has been used the most times
    
    Returns:
        String containing the rocket name
        If multiple rockets have the same count, return the first one alphabetically
    """
    df = _get_dataframe()
    rocket_counts = df['Rocket'].value_counts().reset_index()
    rocket_counts.columns = ['Rocket', 'Count']
    
    # Find the maximum count
    max_count = rocket_counts['Count'].max()
    
    # Get all rockets with max count
    top_rockets = rocket_counts[rocket_counts['Count'] == max_count]
    
    # Sort alphabetically and return the first one
    top_rockets = top_rockets.sort_values('Rocket')
    
    if len(top_rockets) > 0:
        return str(top_rockets.iloc[0]['Rocket'])
    else:
        return ""

def getAverageMissionsPerYear(startYear: int, endYear: int) -> float:
    """
    Calculates the average number of missions per year over a given range
    
    Args:
        startYear: Starting year (inclusive)
        endYear: Ending year (inclusive)
    
    Returns:
        Float representing average missions per year, rounded to 2 decimal places
    """
    if not isinstance(startYear, int) or not isinstance(endYear, int):
        return 0.0
    
    if startYear > endYear:
        return 0.0
    
    df = _get_dataframe()
    df['Year'] = df['Date'].dt.year
    
    # Filter by year range
    filtered_df = df[(df['Year'] >= startYear) & (df['Year'] <= endYear)]
    
    if len(filtered_df) == 0:
        return 0.0
    
    # Calculate average
    total_missions = len(filtered_df)
    num_years = endYear - startYear + 1
    
    if num_years == 0:
        return 0.0
    
    average = total_missions / num_years
    return round(average, 2)