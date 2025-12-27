import json
import os
from datetime import datetime
from app.extensions.postgres import db
from app.models.event import Event
from config import Config

def generate_timeline_json():
    """Generate TimelineJS JSON from database events"""
    
    # Query published events
    events = Event.query.filter_by(is_published=True).order_by(Event.start_date).all()
    
    timeline_data = {
        "events": [],
        "title": {
            "text": {
                "headline": "时间线故事",
                "text": "基于 TimelineJS 创建的时间线展示"
            }
        },
        "eras": [],
        "scale": "human"
    }
    
    for event in events:
        # Convert to TimelineJS slide format
        slide = {
            "unique_id": event.unique_id or f"event-{event.id}",
            "start_date": {
                "year": event.start_date.year,
                "month": event.start_date.month,
                "day": event.start_date.day
            },
            "text": {
                "headline": event.headline or "",
                "text": event.text or ""
            }
        }
        
        # Add optional fields
        if event.end_date:
            slide["end_date"] = {
                "year": event.end_date.year,
                "month": event.end_date.month,
                "day": event.end_date.day
            }
        
        if event.display_date:
            slide["display_date"] = event.display_date
        
        if event.media_url:
            slide["media"] = {
                "url": event.media_url,
                "caption": event.media_caption or "",
                "credit": event.media_credit or ""
            }
        
        if event.group:
            slide["group"] = event.group
        
        if event.background_url or event.background_color:
            slide["background"] = {}
            if event.background_url:
                slide["background"]["url"] = event.background_url
            if event.background_color:
                slide["background"]["color"] = event.background_color
        
        if event.autolink is not None:
            slide["autolink"] = event.autolink
        
        timeline_data["events"].append(slide)
    
    # Ensure output directory exists
    output_path = Config.JSON_OUTPUT_PATH
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(timeline_data, f, ensure_ascii=False, indent=2)
    
    print(f"JSON文件已生成: {output_path}")
    return True

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        generate_timeline_json()