import os
import json
import requests
import pudb

from schemas.event import EventSchema

from config import MICRO_APPOINTMENTS_URL, MICRO_DOCTORS_URL, MICRO_ADDRESS_URL

#POST
def handle_create(item: dict, base_url: str) -> dict:
    data = item.get("data")
    if item.get("domain") == "appointment":
        try:
            validated_data = EventSchema.model_validate(data)
            data = validated_data.model_dump(mode="json")
        except Exception as e:
            print("Erro na validação do EventSchema:", e, flush=True)
            return {"id": item.get("id"), "error": f"EventSchema validation error: {str(e)}"}
    try:
        response = requests.post(base_url, json=data)
    except Exception as e:
        print("Erro na requisição POST:", e, flush=True)
        return {"id": item.get("id"), "error": str(e)}
    if response.status_code != 200:
        try:
            error_data = response.json()
        except Exception:
            error_data = {"message": response.text}
        return {
            "id": item.get("id"),
            "status_code": response.status_code,
            "msg": error_data.get("msg", ""),
            "status": error_data.get("status", "error"),
            "data": error_data.get("data", None)
        }
    json_response = response.json() 
    return {
        "id": item.get("id"),
        "status_code": response.status_code,
        "msg": json_response.get("msg", ""),
        "status": json_response.get("status", ""),
        "data": json_response.get("data", None)
    }

#PUT
def handle_update(item: dict, base_url: str, item_id: str) -> dict:
    data = item.get("data")
    if item.get("domain") == "appointment":
        if not data or not data.get("user_id"):
            return {"id": item.get("id"), "error": "Missing 'user_id' field in data for update action."}
        user_id = data.get("user_id")
        url = f"{base_url}?id={item_id}&user_id={user_id}"
    else:
        url = f"{base_url}/{item_id}"
    try:
        response = requests.put(url, json=data)
    except Exception as e:
        print("Erro na requisição PUT:", e, flush=True)
        return {"id": item.get("id"), "error": str(e)}
    if response.status_code != 200:
        try:
            error_data = response.json()
        except Exception:
            error_data = {"message": response.text}
        if "unique" in error_data.get("msg", "").lower() or "duplicate" in error_data.get("msg", "").lower():
            error_data["msg"] = "Já existe um appointment com o mesmo nome."
        return {
            "id": item.get("id"),
            "status_code": response.status_code,
            "msg": error_data.get("msg", ""),
            "status": error_data.get("status", "error"),
            "data": error_data.get("data", None)
        }
    json_response = response.json() 
    return {
        "id": item.get("id"),
        "status_code": response.status_code,
        "msg": json_response.get("msg", ""),
        "status": json_response.get("status", ""),
        "data": json_response.get("data", None)
    }

#DELETE
def handle_delete(item: dict, base_url: str, item_id: str) -> dict:
    data = item.get("data")
    if item.get("domain") == "appointment":
        if not data or not data.get("user_id"):
            return {"id": item.get("id"), "error": "Missing 'user_id' field in data for delete action."}
        user_id = data.get("user_id")
        url = f"{base_url}?id={item_id}&user_id={user_id}"
    else:
        url = f"{base_url}/{item_id}"
    try:
        response = requests.delete(url)
    except Exception as e:
        print("Erro na requisição DELETE:", e, flush=True)
        return {"id": item.get("id"), "error": str(e)}
    if response.status_code != 200:
        try:
            error_data = response.json()
        except Exception:
            error_data = {"message": response.text}
        return {
            "id": item.get("id"),
            "status_code": response.status_code,
            "msg": error_data.get("msg", ""),
            "status": error_data.get("status", "error"),
            "data": error_data.get("data", None)
        }
    json_response = response.json() 
    return {
        "id": item.get("id"),
        "status_code": response.status_code,
        "msg": json_response.get("msg", ""),
        "status": json_response.get("status", ""),
        "data": json_response.get("data", None)
    }

## Route_item
## responsible for defining the operation between create (POST), update (PUT) and delete (DELETE)
## which calls the micro appointment service passing the parameters
## currently, the domains "doctor" and "address" have not been implemented
def route_item(item: dict) -> dict:
    domain = item.get("domain")
    action = item.get("action")
    data = item.get("data")
    item_id = item.get("id", "")
    
    if not domain:
        return {"id": item.get("id"), "error": "Missing 'domain' field."}
    if not action:
        return {"id": item.get("id"), "error": "Missing 'action' field."}
    
    # sets the URL based on the domain, this domain comes from payload request
    if domain == "appointment":
        base_url = MICRO_APPOINTMENTS_URL.rstrip("/") + "/appointment"
    elif domain == "doctor":
        base_url = MICRO_DOCTORS_URL
    elif domain == "address":
        base_url = MICRO_ADDRESS_URL
    else:
        return {"id": item.get("id"), "error": f"Domain '{domain}' not recognized."}
    
    if action in ["create", "update"] and not data:
        return {"id": item.get("id"), "error": f"Missing 'data' field for action '{action}'."}
    
    if action in ["update", "delete"] and not item.get("id"):
        return {"id": None, "error": f"Missing 'id' field for action '{action}'."}
    
    try:
        if action == "create":
            return handle_create(item, base_url)
        elif action == "update":
            return handle_update(item, base_url, item_id)
        elif action == "delete":
            return handle_delete(item, base_url, item_id)
        else:
            return {"id": item.get("id"), "error": f"Action '{action}' not supported."}
    except Exception as e:
        print("Erro na request:", e, flush=True)
        return {"id": item.get("id"), "error": str(e)}

def process_items(items: list) -> list:
    results = []
    for item in items:
        if hasattr(item, "dict"):
            item = item.dict()
        result = route_item(item)
        results.append(result)
    return results
