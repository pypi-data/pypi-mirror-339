import os
import json
import mimetypes

import requests

def get_subscribed_apps(whatsapp_business_id: str, access_token: str):
    """
    Documentation: https://stackoverflow.com/questions/77766798/meta-cloud-api-is-triggering-every-webhook-for-multiple-apps
    """
    url = f"https://graph.facebook.com/v21.0/{whatsapp_business_id}/subscribed_apps"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(response.json())

def add_subscribed_apps(whatsapp_business_id: str, access_token: str):
    """
    Documentation: https://stackoverflow.com/questions/77766798/meta-cloud-api-is-triggering-every-webhook-for-multiple-apps
    """
    url = f"https://graph.facebook.com/v21.0/{whatsapp_business_id}/subscribed_apps"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    print(response.json())

def delete_subscribed_app(whatsapp_business_id: str, access_token: str):
    """
    Documentation: https://stackoverflow.com/questions/77766798/meta-cloud-api-is-triggering-every-webhook-for-multiple-apps
    """
    url = f"https://graph.facebook.com/v21.0/{whatsapp_business_id}/subscribed_apps"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    print(response.json())

def info_phone_number(whatsapp_phone_number_id: str, access_token: str):
    """
    Documentation: https://developers.facebook.com/docs/whatsapp/business-management-api/manage-phone-numbers#get-a-single-phone-number
    """
    
    url = f"https://graph.facebook.com/{whatsapp_phone_number_id}"
    headers = {
    "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(url, headers=headers)
    print(response.json())
    
    url = f"https://graph.facebook.com/{whatsapp_phone_number_id}"
    headers = {
    "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(url, headers=headers)
    print(response.json())

def register_phone_number(whatsapp_phone_number_id: str, access_token: str):
    url = f"https://graph.facebook.com/{whatsapp_phone_number_id}/register"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    json = {
        "messaging_product": "whatsapp",
        "pin": "123456"
    }
    response = requests.post(url, headers=headers, json=json)
    print(response.json())

def get_templates(whatsapp_business_id: str, access_token: str, next_page: str = None):
    """
    Documentation: https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates/#retrieve-templates
    """
    try:
        url = f"https://graph.facebook.com/v22.0/{whatsapp_business_id}/message_templates"
        if next_page:
            url = next_page
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(e)

def get_template_format(template_name: str, whatsapp_business_id: str, access_token: str):
    try: 
        templates = get_templates(whatsapp_business_id, access_token)
        while templates:
            for template in templates['data']:
                if template['name'] == template_name:
                    template = {
                        "category": template['category'],
                        "parameter_format": template['parameter_format'],
                        "components": template['components']
                    }
                    template = json.dumps(template, indent=4, ensure_ascii=False)
                    template = f'\"{template_name}\": {template}'
                    print(template)
                    return
            next_page = templates['paging'].get('next')
            templates = None
            if next_page:
                templates = get_templates(whatsapp_business_id, access_token, next_page)
        raise Exception("Template not found")
    except Exception as e:
        print(e)

def cloud_api_upload_media(file_name: str, whatsapp_phone_number_id: str, access_token: str):
    """
    Documentation: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media/
    """
    
    file_path = os.path.join("media", file_name)
    file_type = mimetypes.guess_type(file_name)[0]
    
    url = f"https://graph.facebook.com/v22.0/{whatsapp_phone_number_id}/media"
    headers = {
        "Authorization": f"Bearer {access_token}",
        }
    files = {
        'file': (file_name, open(file_path, 'rb'), file_type),
        }
    data = {
        "messaging_product" : "whatsapp"
        }
    response = requests.post(url, headers=headers, files=files, data=data)
    print(response.json())

def cloud_api_get_image(image_id: str, access_token: str):
    """
    Documentation: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media/
    """
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            }
        
        # Step 1: Get image download URL
        url = f"https://graph.facebook.com/v22.0/{image_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        download_url = response.json().get('url')
        file_type = response.json().get('mime_type').split("/")[1]
        file_path = os.path.join("media", f"{image_id}.{file_type}")

        
        # Step 2: Download image
        response = requests.get(download_url, headers=headers)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content) 
        print(f"Image {image_id} downloaded successfully.")
        
    except Exception as e:
        print(e)

def resumable_upload_file(file_name: str, app_id: str, access_token: str):
    """
    Documentation: https://developers.facebook.com/docs/graph-api/guides/upload
    """
    file_path = os.path.join("media", file_name)
    file_length = os.path.getsize(file_path)
    file_type = mimetypes.guess_type(file_name)[0]

    try:
        # Step 1
        url = f"https://graph.facebook.com/v22.0/{app_id}/uploads"
        params = {
            'file_name': file_name,
            'file_length': file_length,
            'file_type': file_type,
            'access_token': access_token
            }
        response = requests.post(url, params=params)
        response.raise_for_status()
        print(response.json())

        # Step 2
        upload_session_id = response.json().get('id').split("upload:")[1]
        url = f"https://graph.facebook.com/v22.0/upload:{upload_session_id}"
        headers = {
            "Authorization": f"OAuth {access_token}",
            "file_offset": "0"
            }
        with open(file_path, 'rb') as file_data:
            response = requests.post(url, headers=headers, data=file_data)
        response.raise_for_status()
        print(response.json())
    except Exception as e:
        print(e)
