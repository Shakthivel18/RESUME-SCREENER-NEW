import os
import glob
from collections import Counter

PROCESSED_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads', 'processed_text')

def clean_and_verify():
    # 1. Delete HR files (Old data)
    files = glob.glob(os.path.join(PROCESSED_FOLDER, '*_HR.txt'))
    print(f"Found {len(files)} HR files. Deleting...")
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"Error deleting {f}: {e}")

    # 2. Count remaining categories
    all_files = glob.glob(os.path.join(PROCESSED_FOLDER, '*.txt'))
    categories = []
    
    print(f"\nRemaining Files: {len(all_files)}")
    for f in all_files:
        filename = os.path.basename(f)
        # Assuming format: Resume_ID_CATEGORY.txt
        parts = filename.replace('.txt', '').split('_')
        if len(parts) >= 3:
            cat = parts[-1]
            categories.append(cat)
    
    print("Category Distribution:")
    print(Counter(categories))

if __name__ == '__main__':
    clean_and_verify()
