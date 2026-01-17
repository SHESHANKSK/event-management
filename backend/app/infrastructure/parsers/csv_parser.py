import csv
import io
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import UploadFile, HTTPException

def parse_duration_to_minutes(duration_str: str) -> int:
    """
    Parses strings like "54m 13s", "1h 2m", "45s" into integer minutes (rounded).
    """
    if not duration_str:
        return 0
    
    total_minutes = 0.0
    
    # regex for H, M, S
    h_match = re.search(r'(\d+)h', duration_str)
    m_match = re.search(r'(\d+)m', duration_str)
    s_match = re.search(r'(\d+)s', duration_str)
    
    if h_match:
        total_minutes += int(h_match.group(1)) * 60
    if m_match:
        total_minutes += int(m_match.group(1))
    if s_match:
        total_minutes += int(s_match.group(1)) / 60.0
        
    return round(total_minutes)

def parse_timestamp(ts_str: str) -> Optional[datetime]:
    """
    Parses timestamp like "2/6/2022, 10:25:18 AM"
    """
    if not ts_str:
        return None
    try:
        # 2/6/2022, 10:25:18 AM
        return datetime.strptime(ts_str.strip(), "%m/%d/%Y, %I:%M:%S %p")
    except ValueError:
        # Fallback or strict error? User said "validate". Let's try strict first.
        # But maybe different locale? Let's assume the provided format.
        # Try without comma?
        try:
             return datetime.strptime(ts_str.strip(), "%m/%d/%Y %I:%M:%S %p")
        except ValueError:
            return None

async def parse_teams_csv(file: UploadFile) -> List[Dict[str, Any]]:
    content = await file.read()
    decoded = content.decode('utf-8-sig') # Handle potential BOM
    reader = csv.DictReader(io.StringIO(decoded))
    
    parsed_rows = []
    
    # Check headers
    # "Full Name","Join Time","Leave Time","Duration","Email","Role","Participant ID (UPN)"
    # We allow some flexibility or strict match?
    # Let's map strict for now based on screenshot.
    
    for row in reader:
        # normalize keys?
        # DictReader uses keys from first row.
        
        # Map to our model fields
        email = row.get("Email")
        if not email:
            continue # Skip empty rows
            
        duration_str = row.get("Duration", "")
        duration_minutes = parse_duration_to_minutes(duration_str)
        
        if duration_minutes <= 0:
            duration_minutes = 1 # Min 1 minute if it was present but just seconds, or 0? 
            # Model says duration > 0. If "30s", round is 0 or 1? 30/60 = 0.5 -> 0.
            # Maybe ceil? 
            # Let's verify parse logic: 0.5 rounded is 0. 
            # Logic: If attended, at least 1 min credit?
            if duration_str and "s" in duration_str:
                 duration_minutes = 1
        
        join_time = parse_timestamp(row.get("Join Time"))
        leave_time = parse_timestamp(row.get("Leave Time"))
        full_name = row.get("Full Name")
        role = row.get("Role", "Attendee")
        
        parsed_rows.append({
            "email": email,
            "duration": duration_minutes,
            "role": role,
            "full_name": full_name,
            "join_time": join_time,
            "leave_time": leave_time
        })
        
    return parsed_rows
