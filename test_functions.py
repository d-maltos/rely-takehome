"""
test_functions.py
Author: Dylan Maltos
Last Updated: 2026-01-05

Test script for space missions functions
Run this to verify all functions work correctly
"""

import pandas as pd
from space_missions_functions import (
    getMissionCountByCompany,
    getSuccessRate,
    getMissionsByDateRange,
    getTopCompaniesByMissionCount,
    getMissionStatusCount,
    getMissionsByYear,
    getMostUsedRocket,
    getAverageMissionsPerYear
)

def test_all_functions():
    """Test all required functions."""
    print("Testing Space Missions Functions\n")
    print("=" * 50)
    
    # Test 1: getMissionCountByCompany
    print("\n1. Testing getMissionCountByCompany('NASA')")
    result = getMissionCountByCompany("NASA")
    print(f"   Result: {result}")
    assert isinstance(result, int), "Should return an integer"
    
    # Test 1b: No missions case
    print("\n1b. Testing getMissionCountByCompany('DefinitelyNotACompany')")
    result = getMissionCountByCompany("DefinitelyNotACompany")
    print(f"   Result: {result}")
    assert result == 0, "Should return 0 for non-existent company"
    
    # Test 2: getSuccessRate
    print("\n2. Testing getSuccessRate('NASA')")
    result = getSuccessRate("NASA")
    print(f"   Result: {result}%")
    assert isinstance(result, float), "Should return a float"
    assert 0 <= result <= 100, "Should be between 0 and 100"
    assert round(result, 2) == result, "Should be rounded to exactly 2 decimal places"
    
    # Test 2b: No missions case
    print("\n2b. Testing getSuccessRate('DefinitelyNotACompany')")
    result = getSuccessRate("DefinitelyNotACompany")
    print(f"   Result: {result}")
    assert result == 0.0, "Should return 0.0 for non-existent company"
    
    # Test 3: getMissionsByDateRange
    print("\n3. Testing getMissionsByDateRange('1957-10-01', '1957-12-31')")
    result = getMissionsByDateRange("1957-10-01", "1957-12-31")
    print(f"   Result: {result}")
    print(f"   Number of missions: {len(result)}")
    assert isinstance(result, list), "Should return a list"
    
    # Test 3b: Verify chronological ordering
    print("\n3b. Testing chronological ordering of getMissionsByDateRange")
    # Verify the list is sorted chronologically by checking dates (stable mapping)
    if len(result) > 1:
        df = pd.read_csv('space_missions.csv')
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
        # Map each mission to its earliest launch date (avoids duplicates overwriting)
        mission_dates = df.groupby('Mission')['Date'].min().to_dict()
        dates = [mission_dates.get(m, pd.NaT) for m in result]
        # Check that dates are non-decreasing (allowing for same-date missions)
        for i in range(len(dates) - 1):
            if pd.notna(dates[i]) and pd.notna(dates[i+1]):
                assert dates[i] <= dates[i+1], f"Missions not in chronological order at index {i}"
        print("   ✓ Missions are in chronological order")
    
    # Test 3c: Invalid date format
    print("\n3c. Testing getMissionsByDateRange with invalid date format")
    result = getMissionsByDateRange("bad-date", "1957-12-31")
    assert result == [], "Should return empty list for invalid date format"
    
    # Test 3d: Reversed date range
    print("\n3d. Testing getMissionsByDateRange with reversed range")
    result = getMissionsByDateRange("1957-12-31", "1957-10-01")
    assert result == [], "Should return empty list for reversed date range"
    
    # Test 4: getTopCompaniesByMissionCount
    print("\n4. Testing getTopCompaniesByMissionCount(3)")
    result = getTopCompaniesByMissionCount(3)
    print(f"   Result: {result}")
    assert isinstance(result, list), "Should return a list"
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result), "Should return list of tuples"
    
    # Test 4b: Verify tie-breaking (alphabetical when counts are equal)
    print("\n4b. Testing tie-breaking in getTopCompaniesByMissionCount")
    # Compute expected independently to verify tie-breaking logic
    df = pd.read_csv('space_missions.csv')
    company_counts = df['Company'].value_counts().reset_index()
    company_counts.columns = ['Company', 'Count']
    company_counts = company_counts.sort_values(['Count', 'Company'], ascending=[False, True])
    top_3_expected = [(row['Company'], int(row['Count'])) for _, row in company_counts.head(3).iterrows()]
    assert result == top_3_expected, "Should match expected order with alphabetical tie-breaking"
    
    # Test 4c: n = 0 case
    print("\n4c. Testing getTopCompaniesByMissionCount(0)")
    result = getTopCompaniesByMissionCount(0)
    assert result == [], "Should return empty list for n=0"
    
    # Test 5: getMissionStatusCount
    print("\n5. Testing getMissionStatusCount()")
    result = getMissionStatusCount()
    print(f"   Result: {result}")
    assert isinstance(result, dict), "Should return a dictionary"
    assert "Success" in result, "Should contain 'Success' key"
    
    # Test 6: getMissionsByYear
    print("\n6. Testing getMissionsByYear(2020)")
    result = getMissionsByYear(2020)
    print(f"   Result: {result}")
    assert isinstance(result, int), "Should return an integer"
    
    # Test 7: getMostUsedRocket
    print("\n7. Testing getMostUsedRocket()")
    result = getMostUsedRocket()
    print(f"   Result: {result}")
    assert isinstance(result, str), "Should return a string"
    
    # Test 7b: Verify tie-breaking (alphabetical when counts are equal)
    print("\n7b. Testing tie-breaking in getMostUsedRocket")
    # Compute expected independently to verify tie-breaking logic
    df = pd.read_csv('space_missions.csv')
    rocket_counts = df['Rocket'].value_counts().reset_index()
    rocket_counts.columns = ['Rocket', 'Count']
    max_count = rocket_counts['Count'].max()
    top_rockets = rocket_counts[rocket_counts['Count'] == max_count]
    top_rockets = top_rockets.sort_values('Rocket')
    expected = str(top_rockets.iloc[0]['Rocket']) if len(top_rockets) > 0 else ""
    assert result == expected, "Should match expected result with alphabetical tie-breaking"
    
    # Test 8: getAverageMissionsPerYear
    print("\n8. Testing getAverageMissionsPerYear(2010, 2020)")
    result = getAverageMissionsPerYear(2010, 2020)
    print(f"   Result: {result}")
    assert isinstance(result, float), "Should return a float"
    assert round(result, 2) == result, "Should be rounded to exactly 2 decimal places"
    
    # Test 8b: Verify exact formula calculation
    print("\n8b. Testing exact formula for getAverageMissionsPerYear")
    df = pd.read_csv('space_missions.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
    df['Year'] = df['Date'].dt.year
    total = len(df[(df['Year'] >= 2010) & (df['Year'] <= 2020)])
    expected = round(total / (2020 - 2010 + 1), 2)
    assert result == expected, f"Average should match total_missions / num_years: expected {expected}, got {result}"
    
    # Test 8c: Reversed year range
    print("\n8c. Testing getAverageMissionsPerYear with reversed range")
    result = getAverageMissionsPerYear(2020, 2010)
    assert result == 0.0, "Should return 0.0 for reversed year range"
    
    print("\n" + "=" * 50)
    print("All tests passed!")

if __name__ == "__main__":
    test_all_functions()

