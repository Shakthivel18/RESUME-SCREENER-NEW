import pandas as pd
import os
import re

# Configuration
CSV_PATH = r'e:/RESUME/resume/Resume.csv'
OUTPUT_DIR = r'e:/RESUME/uploads/processed_text'
LIMIT = 50  # Number of resumes to seed

def seed_resumes():
    print(f"Checking for CSV at: {CSV_PATH}")
    if not os.path.exists(CSV_PATH):
        print("Error: Resume.csv not found.")
        return

    try:
        # Read CSV
        print("Reading CSV file (this might take a moment)...")
        df = pd.read_csv(CSV_PATH)
        
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Iterate and save
        count = 0
        target_categories = ['ENGINEERING', 'INFORMATION-TECHNOLOGY'] # STRICTLY Tech
        
        # Sort or filter df to prioritize these categories
        # We'll just iterate and pick if match
        
        for index, row in df.iterrows():
            if count >= LIMIT:
                break
                
            resume_id = row.get('ID', f'unk_{index}')
            category = str(row.get('Category', 'General')).upper()
            content = row.get('Resume_str', '')
            
            # Filter for specific categories
            if category not in target_categories:
                # Optionally allow others if run out, but for now strict to satisfy user
                # Actually, let's just prioritize. If we don't find enough, we stop.
                continue 
            
            if not isinstance(content, str) or not content.strip():
                continue

            # Sanitize filename
            safe_category = re.sub(r'[^a-zA-Z0-9]', '_', str(category))
            filename = f"Resume_{resume_id}_{safe_category}.txt"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            count += 1
            
        print(f"Successfully seeded {count} resumes to '{OUTPUT_DIR}'.")
        print("You can now go to the Recruiter Dashboard and run a match!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    seed_resumes()
