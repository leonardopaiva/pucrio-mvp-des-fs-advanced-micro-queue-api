from flask_openapi3 import OpenAPI, Info, Tag
from flask import jsonify, redirect
from flask_cors import CORS
from schemas.queue import ProcessSyncSchema
from services.route_handler import process_items
from pydantic import ValidationError
import pudb

info = Info(
    title="Micro Queue API",
    version="1.0.0",
    description="API responsible for processing the synchronization queue of items."
)
app = OpenAPI(__name__, info=info)
CORS(app)

@app.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    return jsonify({
        "status": "error",
        "msg": "Validation error",
        "data": e.errors()
    }), 422

queue_tag = Tag(name="Queue", description="Endpoints for synchronization queue processing")

@app.get('/', tags=[queue_tag])
def home():
    """Redirects to the OpenAPI documentation."""
    return redirect('/openapi')

@app.post('/process-sync', tags=[queue_tag])
def process_sync(body: ProcessSyncSchema):
    """
    Receives a list of items for synchronization and processes each one, forwarding
    them to the appropriate microservice.

    The purpose of this function is to synchronize the user's data stored in
    local storage with the database.
    
    Example body:
    {
      "items": [
         {
           "id": "1",
           "domain": "appointment",
           "action": "create",
           "data": { ... }
         },
         {
           "id": "2",
           "domain": "doctor",
           "action": "update",
           "data": { ... }
         }
      ]
    }
    Another example:
    {
        "items": [
          {
            "action": "update",
            "domain": "appointment",
            "id": "5c526994-cea3-4b68-9d2e-145b42e64c31",
            "data": {
              "id": "5c526994-cea3-4b68-9d2e-145b42e64c31",
              "name": "Urgent Service 2",
              "date": "2025-04-07T14:47:26.034479",
              "description": "Consultation updated for exam",
              "observation": "Updated observation",
              "doctor_id": 1,
              "doctor_name": "Doctor Matheus",
              "location_id": 1,
              "location_name": "Memorial São José Recife 83",
              "type": 1,
              "user_id": "54e8a4a8-5001-7018-8eec-ce6b634cded9"
            }
          }
        ]
      }
    """
    results = process_items(body.items)
    error_present = any("error" in item for item in results)
    
    if error_present:
        return jsonify({
            "status": "error",
            "msg": "Some items failed to process.",
            "data": results
        }), 400
    else:
        return jsonify({
            "status": "ok",
            "msg": "Items processed successfully.",
            "data": results
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
