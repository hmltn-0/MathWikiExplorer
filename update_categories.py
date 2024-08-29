import os
import requests
import pandas as pd

# Constants
API_URL = 'https://en.wikipedia.org/w/api.php'
DATA_FILE = "mathematics_categories.csv"
INITIAL_CATEGORY = "Mathematics"

# Column headers
CATEGORY_COL = "Category"
STATUS_COL = "Status"

def fetch_subcategories(category):
    """Fetch subcategories for a given category using MediaWiki API."""
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtitle': f'Category:{category}',
        'cmlimit': '500',
        'format': 'json'
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    return [member['title'].replace('Category:', '').strip()
            for member in data['query']['categorymembers']]

def create_initial_file():
    """Create the initial CSV file with subcategories of Mathematics."""
    subcategories = fetch_subcategories(INITIAL_CATEGORY)
    df = pd.DataFrame({
        CATEGORY_COL: subcategories,
        STATUS_COL: 'Included'
    })
    df = df.sort_values(CATEGORY_COL)
    df.to_csv(DATA_FILE, index=False)
    print(f"Initial file created with {len(subcategories)} subcategories of Mathematics.")

def update_categories(df):
    """Update the categories dataframe with new subcategories."""
    included_categories = df[df[STATUS_COL] == 'Included'][CATEGORY_COL]
    new_subcategories = []
    for category in included_categories:
        new_subcategories.extend(fetch_subcategories(category))
    
    new_df = pd.DataFrame({CATEGORY_COL: new_subcategories})
    updated_df = pd.merge(df, new_df, on=CATEGORY_COL, how='outer')
    updated_df[STATUS_COL] = updated_df[STATUS_COL].fillna('Included')
    updated_df = updated_df.sort_values(CATEGORY_COL)
    return updated_df

def main():
    if not os.path.exists(DATA_FILE):
        create_initial_file()
    else:
        df = pd.read_csv(DATA_FILE)
        updated_df = update_categories(df)
        updated_df.to_csv(DATA_FILE, index=False)
        print(f"Updated file. Now contains {len(updated_df)} categories.")

if __name__ == "__main__":
    main()
