from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from . import database, schemas

app = FastAPI(title="Medical Data Warehouse API")

# Endpoint 1: Top Products (Frequency analysis)
@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def get_top_products(limit: int = 10, db: Session = Depends(database.get_db)):
    # Counts identical messages (proxy for shared posts/products)
    query = text("""
        SELECT message_text as product_name, count(*) as count 
        FROM dbt_prod.fct_messages 
        GROUP BY message_text 
        ORDER BY count DESC 
        LIMIT :limit
    """)
    result = db.execute(query, {"limit": limit}).fetchall()
    return [{"product_name": row[0][:50] + "..." if len(row[0]) > 50 else row[0], "count": row[1]} for row in result]

# Endpoint 2: Channel Activity
@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity])
def get_channel_activity(channel_name: str, db: Session = Depends(database.get_db)):
    query = text("""
        SELECT d.full_date, COUNT(*) as post_count
        FROM dbt_prod.fct_messages f
        JOIN dbt_prod.dim_channels c ON f.channel_key = c.channel_key
        JOIN dbt_prod.dim_dates d ON f.date_key = d.date_key
        WHERE c.channel_name = :channel_name
        GROUP BY d.full_date
        ORDER BY d.full_date
    """)
    result = db.execute(query, {"channel_name": channel_name}).fetchall()
    
    if not result:
        # If no results, check if channel exists to give better error
        return []
        
    return [{"date": str(row[0]), "post_count": row[1]} for row in result]

# Endpoint 3: Search Messages
@app.get("/api/search/messages", response_model=List[schemas.MessageResponse])
def search_messages(query: str, limit: int = 20, db: Session = Depends(database.get_db)):
    sql = text("""
        SELECT message_id, message_text, view_count 
        FROM dbt_prod.fct_messages 
        WHERE message_text ILIKE :q 
        LIMIT :limit
    """)
    result = db.execute(sql, {"q": f"%{query}%", "limit": limit}).fetchall()
    return [{"message_id": int(row[0]), "text": row[1], "views": row[2]} for row in result]

# Endpoint 4: Visual Content Stats (YOLO Data)
@app.get("/api/reports/visual-content", response_model=List[schemas.VisualStats])
def get_visual_content_stats(db: Session = Depends(database.get_db)):
    sql = text("""
        SELECT image_category, count(*) 
        FROM dbt_prod.fct_image_detections 
        GROUP BY image_category
    """)
    result = db.execute(sql).fetchall()
    return [{"category": row[0], "count": row[1]} for row in result]