import os
import pandas as pd
from ultralytics import YOLO
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Database Connection
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def categorize_image(detections):
    """
    Classify image based on detected objects.
    Logic:
    - promotional: Contains person + product
    - product_display: Contains product, no person
    - lifestyle: Contains person, no product
    - other: Neither detected
    """
    # Get set of all class names detected in this image
    labels = set([d['class_name'] for d in detections])
    
    has_person = 'person' in labels
    
    # Common product-like objects found in medical/retail context
    # (YOLOv8n classes: bottle, cup, bowl, box-like items)
    product_objects = {'bottle', 'cup', 'wine glass', 'bowl', 'vase', 'suitcase', 'handbag', 'backpack'}
    
    # Check if any product object is in the labels
    has_product = not labels.isdisjoint(product_objects)

    if has_person and has_product:
        return 'promotional'
    elif has_product and not has_person:
        return 'product_display'
    elif has_person:
        return 'lifestyle'
    else:
        return 'other'

def run_yolo():
    print("Initializing YOLOv8 model...")
    model = YOLO('yolov8n.pt') 
    image_dir = "data/raw/images"
    
    # Dictionary to store results per image
    image_data = {} 

    print(f"Scanning images in {image_dir}...")
    
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(root, file)
                # Filename without extension is the message_id
                msg_id = os.path.splitext(file)[0]
                
                try:
                    # Run inference
                    results = model(img_path, verbose=False)
                    
                    # Extract detections
                    current_detections = []
                    for r in results:
                        for box in r.boxes:
                            cls_id = int(box.cls[0])
                            name = model.names[cls_id]
                            conf = float(box.conf[0])
                            
                            current_detections.append({
                                "class_name": name,
                                "confidence": conf
                            })
                    
                    # Determine Category
                    category = categorize_image(current_detections)
                    
                    # Prepare rows for DB (One row per detected object)
                    if not current_detections:
                         # Log 'other' if nothing detected
                         if msg_id not in image_data:
                             image_data[msg_id] = []
                         image_data[msg_id].append({
                             "message_id": msg_id,
                             "image_path": img_path,
                             "detected_class": "none",
                             "confidence": 0.0,
                             "image_category": "other"
                         })
                    else:
                        for d in current_detections:
                            if msg_id not in image_data:
                                image_data[msg_id] = []
                            image_data[msg_id].append({
                                "message_id": msg_id,
                                "image_path": img_path,
                                "detected_class": d['class_name'],
                                "confidence": d['confidence'],
                                "image_category": category
                            })
                            
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    # Flatten the dictionary into a list
    final_rows = []
    for mid, items in image_data.items():
        final_rows.extend(items)

    # Save to Database
    if final_rows:
        df = pd.DataFrame(final_rows)
        engine = create_engine(DB_URL)
        # Save to raw schema
        df.to_sql('yolo_detections', engine, schema='raw', if_exists='replace', index=False)
        print(f"✅ Success! Saved {len(df)} detection rows to 'raw.yolo_detections'.")
    else:
        print("No images processed.")

if __name__ == "__main__":
    run_yolo()