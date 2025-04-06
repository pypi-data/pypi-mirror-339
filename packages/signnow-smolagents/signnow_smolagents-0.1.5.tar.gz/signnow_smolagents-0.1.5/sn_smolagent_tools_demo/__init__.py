import time

from typing import List, Dict

import requests as requests
import json as json

from smolagents import CodeAgent, Tool, ToolCallingAgent, ToolCollection
from abc import ABC, abstractmethod


class TokenProvider(ABC):
    @abstractmethod
    def get_token(self) -> str:
        pass


class LoginPasswordTokenProvider(TokenProvider):
    def __init__(self, login: str, password: str, app_key: str):
        self.login = login
        self.password = password
        self.app_key = app_key

    def get_token(self) -> str:
        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {self.app_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "username": self.login,
            "password": self.password,
            "grant_type": "password"
        }

        response = requests.post("https://api.signnow.com/oauth2/token", headers=headers, data=data)
        return response.json().get("access_token")


def access_token_from_login_password(login: str, password: str, app_key: str) -> str:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic " + app_key,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "username": login,
        "password": password,
        "grant_type": "password"
    }

    response = requests.post("https://api.signnow.com/oauth2/token", headers=headers, data=data)
    return response.json().get("access_token")


class SignNowSmolagentsCodeAgent(CodeAgent):
    def __init__(
            self,
            access_token: str,
            **kwargs,
    ):
        snTools = SignNowSmolagentsToolset(access_token=access_token)
        tools = kwargs.get("tools", []) + snTools.tools
        super().__init__(
            tools=tools,
            name=kwargs.get("name", "SignNowAgent"),
            description=kwargs.get(
                "description",
                (
                    'This agent integrates with the SignNow API to handle electronic signatures.'
                    'It can send documents for signing, retrieve their signing status, manage templates, and coordinate contacts—all within a streamlined workflow.'
                )
            ),
            **kwargs
        )


class SignNowSmolagentsToolCallingAgent(ToolCallingAgent):
    def __init__(
            self,
            access_token: str,
            **kwargs,
    ):
        snTools = SignNowSmolagentsToolset(access_token=access_token)
        tools = kwargs.get("tools", []) + snTools.tools
        super().__init__(
            tools=tools,
            name=kwargs.get("name", "SignNowAgent"),
            description=kwargs.get(
                "description",
                (
                    'This agent integrates with the SignNow API to handle electronic signatures.'
                    'It can send documents for signing, retrieve their signing status, manage templates, and coordinate contacts—all within a streamlined workflow.'
                )
            ),
            **kwargs
        )


class SignNowSmolagentsToolset(ToolCollection):
    def __init__(self, access_token: str):
        get_templates_list = GetTemplateListTool(access_token=access_token)
        upload_document = UploadLocalFileTool(access_token=access_token)
        get_contacts = GetContactsTool(access_token=access_token)
        create_document_from_template = CreateDocumentFromTemplateTool(access_token=access_token)
        get_document_info = GetDocumentInfoTool(access_token=access_token)
        send_invite = SendInviteTool(access_token=access_token)
        prefill_fields = PrefillFieldsTool(access_token=access_token)
        super().__init__(tools=[
            get_templates_list,
            upload_document,
            get_contacts,
            create_document_from_template,
            get_document_info,
            send_invite,
            prefill_fields
        ])


class GetTemplateListTool(Tool):
    name = "get_template_list"
    description = """
    Retrieves a list of templates from the SignNow platform.
    Returns:
        str: A JSON-formatted string containing the list of templates. Each template is structured as follows:
            [
                {
                    "id": str,              # Unique identifier of the template
                    "name": str,            # Name of the template
                    "roles": [              # List of roles assigned for signing
                        {
                            "unique_id": str,        # Unique identifier of the role
                            "signing_order": str,    # Order of signing
                            "name": str              # Name of the role (e.g., "Recipient 1")
                        },
                        ...
                    ]
                },
                ...
            ]
    """

    inputs = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        access_token = kwargs.pop("access_token", None)
        if not access_token:
            raise ValueError("Missing access token")
        self.access_token = access_token

    output_type = "string"

    def forward(self):
        import requests
        import json

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        folder_ids = []

        try:
            response = requests.get("https://api.signnow.com/v1/folder", headers=headers, params={
                'subfolder-data': 'true',
                'with_team_documents': 'true',
                'include_documents_subfolders': 'false',
                'entity_type': 'all',
                'is_document_sl': 'false',
            })
            response.raise_for_status()
            folders = response.json().get('folders', [])
            folder_ids.extend(folder['id'] for folder in folders if int(folder['template_count']) > 0)
        except Exception as e:
            print(f"Error fetching folders")

        try:
            response = requests.get("https://api.signnow.com/user", headers=headers)
            response.raise_for_status()

            userId = response.json().get('id')

            response = requests.get("https://api.signnow.com/user/" + userId + "/shared_with_me", headers=headers,
                                    params={
                                        'subfolder-data': 'true',
                                        'with_team_documents': 'true',
                                        'include_documents_subfolders': 'false',
                                        'entity_type': 'all',
                                        'is_document_sl': 'false',
                                    })
            response.raise_for_status()
            folders = response.json().get('folders', [])
            folder_ids.extend(folder['id'] for folder in folders if int(folder['template_count']) > 0)
        except Exception as e:
            print(f"Error fetching sharedFolders")

        templates = []

        for folder_id in folder_ids:
            try:
                response = requests.get(
                    f"https://api.signnow.com/folder/{folder_id}",
                    headers=headers,
                    params={'entity_type': 'template'}
                )
                response.raise_for_status()
                documents = response.json().get('documents', [])
                for doc in documents:
                    templates.append({
                        'id': doc['id'],
                        'name': doc['document_name'],
                        'roles': doc['roles']
                    })
            except requests.RequestException as e:
                raise Exception(f"Error get template list: {e.response.text}")
            except Exception as e:
                print(f"Error fetching templates from folder {folder_id}: {e}")

        # $response = $this->request('GET', '/user', [
        #     RequestOptions::HEADERS = > ['Authorization' = > 'Bearer '. $accessToken]
        # ], 'getUserInfo');
        #
        # $response = json_decode($response->getBody()->getContents(), true);
        #
        # return new
        # User(
        # $response['id'],
        # $response['first_name'],
        # $response['last_name'],
        # $response['primary_email']
        # );

        return json.dumps(templates, ensure_ascii=False)


class UploadLocalFileTool(Tool):
    name = "upload_local_file_to_signnow"
    description = """
    Upload local file to signnow documents and return documentId
    Returns:
        Id of created document
    """

    inputs = {
        "file_path": {
            "type": "string",
            "description": "path to local file",
        },
        "filename": {
            "type": "string",
            "description": "name of document",
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        access_token = kwargs.pop("access_token", None)
        if not access_token:
            raise ValueError("Missing access token")
        self.access_token = access_token

    output_type = "string"

    def forward(self, file_path: str, filename: str):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }

        try:
            with open(file_path, 'rb') as file:
                files = {
                    'file': (filename, file),
                    'check_fields': (None, 'true')
                }

                response = requests.post('https://api.signnow.com/document', headers=headers, files=files)
                response.raise_for_status()

        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
        except requests.RequestException as e:
            raise Exception(f"Error uploading document: {e.response.text}")

        data = response.json()

        if 'id' not in data:
            raise Exception("Response has no documentId")

        return data['id']


class GetContactsTool(Tool):
    name = "get_contacts_from_signnow"
    description = """
    Retrieves a list of contacts from SignNow
    Returns:
        str: A JSON string containing the list of contacts.
        in the following JSON format:
        [
            {
                "name": "{first_name} {last_name}",
                "email": "{email}",
                "description": "{description}"
            },
        ]
    """

    inputs = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        access_token = kwargs.pop("access_token", None)
        if not access_token:
            raise ValueError("Missing access token")
        self.access_token = access_token

    output_type = "string"

    def forward(self):
        url = "https://app.signnow.com/snapi/v2/crm/contacts?limit=50"

        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Error get contacts: {e.response.text}")

        res = []
        for contact in response.json().get('data'):
            res.append({
                'name': str(contact['first_name']) + " " + str(contact['last_name']),
                'email': contact['email'],
                'description': str(contact['description'])
            })

        return json.dumps(res, ensure_ascii=False)


class CreateDocumentFromTemplateTool(Tool):
    name = "create_document_from_template"
    description = """
    Create document from template
    Returns:
        Id of created document
    """

    inputs = {
        "template_id": {
            "type": "string",
            "description": "The template ID from which the document will be created. You can get it from get_templates_list tool.",
        },
        "document_name": {
            "type": "string",
            "description": "The name of the newly created document.",
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        access_token = kwargs.pop("access_token", None)
        if not access_token:
            raise ValueError("Missing access token")
        self.access_token = access_token

    output_type = "string"

    def forward(self, template_id: str, document_name: str):
        url = "https://api.signnow.com/template/" + template_id + "/copy"

        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Accept": "application/json"
        }

        data = {
            "document_name": document_name
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Error create document from template: {e.response.text}")

        return response.json().get('id')


class GetDocumentInfoTool(Tool):
    name = "get_document_info"
    description = """
    Get document info, with a lot of usefull information about roles and fields
    Args:
        document_id: document id
    Returns:
        document info in json format
    """

    inputs = {
        "document_id": {
            "type": "string",
            "description": "document id",
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        access_token = kwargs.pop("access_token", None)
        if not access_token:
            raise ValueError("Missing access token")
        self.access_token = access_token

    output_type = "string"

    def forward(self, document_id: str):
        url = "https://api.signnow.com/document/" + document_id

        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Error get document info: {e.response.text}")

        return json.dumps(response.json(), ensure_ascii=False)


class PrefillFieldsTool(Tool):
    name = "prefill_fields"
    description = """
    This tool should only use values already present in the context. 
    To retrieve such values, you may use tools like 'get_document_info'. 

    This tool **MUST NOT** generate, assume, or guess any values. Use ONLY values you are confident in,
    based on the current context or direct user input. If the value is uncertain, leave the field unfilled
    unless the user explicitly instructs you otherwise.

    If you are not 100% certain about a value — DO NOT fill that field. Do not assume anything. Use only direct inputs or verified context.

    It is not required to prefill all fields in the document — you may prefill only a subset of fields
    if only some values are known or relevant.

    ⚠️ It is BETTER to leave a field empty than to fill it with an incorrect or assumed value.

    Example of incorrect usage:
    - {"field_name": "Address", "prefilled_text": "His Address"},  # Assuming "His Address" as the adress
    - {"field_name": "Full Name", "prefilled_text": "John Doe"},  # guessed based on email address
    This is NOT allowed.

    You can obtain the list of available fields by inspecting the document through 'get_document_info'.
    Raises:
        Exception: If the API request fails.
    """

    inputs = {
        "document_id": {
            "type": "string",
            "description": "The ID of the document whose fields you want to prefill."
        },
        "fields": {
            "type": "array",
            "description": "A list of field name and value pairs to prefill.",
            "items": {
                "type": "object",
                "properties": {
                    "field_name": {
                        "type": "string",
                        "description": "The name of the field to prefill."
                    },
                    "prefilled_text": {
                        "type": "string",
                        "description": "The text to prefill in the field."
                    }
                },
                "required": ["field_name", "prefilled_text"]
            }
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        access_token = kwargs.pop("access_token", None)
        if not access_token:
            raise ValueError("Missing access token")
        self.access_token = access_token

    output_type = "null"

    def forward(self, document_id: str, fields: List[Dict[str, str]]):
        url = f"https://api.signnow.com/v2/documents/{document_id}/prefill-texts"

        payload = {
            "fields": fields
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.put(url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Error pre-filling fields: {e.response.text}")


class SendInviteTool(Tool):
    name = "send_invite"
    description = """
    Send an invitation to sign a document to recipients.
    Args:
        document_id: The ID of the document to invite recipients to sign.
        subject: The subject of the invitation email.
        message: The message included in the invitation.
        recipients: A list of recipient dictionaries with the following structure:
            - role (str): The role of the recipient in the signing process.
            - email (str): The email address of the recipient.
            - role_id (str): The unique ID of the recipient's role in the document. You MUST get this ID from the document info from get_document_info tool.
            - order (int, optional): The signing order for the recipient (default is 1).
    Raises:
        Exception: If the API request fails.
    """

    inputs = {
        "document_id": {
            "type": "string",
            "description": "The ID of the document to invite recipients to sign.",
        },
        "subject": {
            "type": "string",
            "description": "The subject of the invitation email.",
        },
        "message": {
            "type": "string",
            "description": "The message included in the invitation.",
        },
        "recipients": {
            "type": "array",
            "description": """
            A list of recipient dictionaries
            """,
            "items": {
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string",
                        "description": "The role of the recipient in the signing process."
                    },
                    "email": {
                        "type": "string",
                        "description": "The email address of the recipient."
                    },
                    "role_id": {
                        "type": "string",
                        "description": "The unique ID of the recipient's role in the document."
                    },
                    "order": {
                        "type": "integer",
                        "description": "The signing order for the recipient (default is 1).",
                        "default": 1
                    }
                },
                "required": ["role", "email", "role_id"]
            },
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        access_token = kwargs.pop("access_token", None)
        if not access_token:
            raise ValueError("Missing access token")
        self.access_token = access_token

    output_type = "null"

    def forward(self, document_id: str, subject: str, message: str, recipients: List[Dict]):
        url = f'https://api.signnow.com/document/{document_id}/invite'

        to_list = [
            {
                "role": recipient["role"],
                "order": recipient.get("order", 1),
                "email": recipient["email"],
                "message": message,
                "subject": subject,
                "role_id": recipient["role_id"],
                "expiration_days": 30,
                "reminder": {
                    "remind_before": 0,
                    "remind_after": 0,
                    "remind_repeat": 0
                },
                "authentication": {
                    "type": None
                },
                "reassign": "0",
                "decline_by_signature": "0"
            } for recipient in recipients
        ]

        payload = {
            "cc": [],
            "document_id": document_id,
            "from": "lebedev.mikhail@pdffiller.team",
            "message": message,
            "on_complete": "document_and_attachments",
            "subject": subject,
            "to": to_list,
            "cc_step": [],
            "client_timestamp": int(time.time()),
            "template": False,
            "email_groups": [],
            "viewers": []
        }

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Error sending invite: {e.response.text}")