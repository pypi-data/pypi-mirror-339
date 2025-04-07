from datetime import datetime, timezone
from empyrebase.types.firestore import Document
from empyrebase.utils import raise_detailed_error, replace_all


class Firestore:
    """Firebase Firestore"""

    SERVER_TIMESTAMP = type("SERVER_TIMESTAMP", (), {})()

    def __init__(self, requests, project_id, firebase_path, database_name="(default)", auth_id=None):
        self.project_id = project_id
        self.firebase_path = firebase_path
        self.database_name = database_name
        self.base_path = f"firestore.googleapis.com/v1/projects/{project_id}/databases/{database_name}/documents/{firebase_path}"
        self.headers = {}
        self.requests = requests
        if auth_id:
            self.headers["Authorization"] = f"Bearer {auth_id}"

    def authorize(self, auth_id: str):
        self.headers["Authorization"] = f"Bearer {auth_id}"

    def collection(self, collection: str):
        """Returns a collection reference

        Args:
            collection (str): Collection path relative to the base path passed on initialization
        """

        path_parts = self.firebase_path.strip("/").split("/")
        current_len = len(path_parts)
        if current_len > 0 and path_parts[0] and current_len % 2 != 0:
            raise ValueError(
                "Collection must be an odd child. Did you mean to get a document ref?")

        new_path = f"{self.firebase_path}/{collection}"
        new_path = replace_all(new_path, '//', '/')

        return Firestore(self.requests, self.project_id, new_path, self.database_name, self.headers.get("Authorization", "").replace("Bearer ", ""))

    def document(self, document: str):
        """Returns a document reference

        Args:
            document (str): Document path relative to the base path passed on initialization
        """

        path_parts = self.firebase_path.strip("/").split("/")
        current_len = len(path_parts)
        if current_len > 0 and path_parts[0] and current_len % 2 == 0:
            raise ValueError(
                "Document must be an even child. Did you mean to get a collection ref?")

        new_path = f"{self.firebase_path}/{document}"
        new_path = replace_all(new_path, '//', '/')
        return Firestore(self.requests, self.project_id, new_path, self.database_name, self.headers.get("Authorization", "").replace("Bearer ", ""))

    def create_document(self, document="", data={}):
        """
        Creates a new document in the Firestore database.

        Args:
            document (str): Document path relative to the base path passed on initialization
            data (dict): Data to be stored in the document
        """

        return self.update_document(document, data, _new=True)

    def get_document(self, document: str = "", _during_update: bool = False):
        """Fetches the document from firestore database

        Args:
            document (str): document path relative to the base path passed on initialization
        """

        if not document and not self.firebase_path:
            raise ValueError("Document path is required")

        path_parts = "/".join([self.firebase_path, document]).strip().strip("/").split("/")
        current_len = len(path_parts)
        if current_len > 0 and path_parts[0] and current_len % 2 != 0:
            raise ValueError("Document ref must be an even child.")

        request_url = f"{self.base_path}"
        if document:
            request_url += f"/{document}"

        request_url = replace_all(request_url, '//', '/')
        request_url = "https://" + request_url

        response = self.requests.get(request_url, headers=self.headers)

        if response.status_code == 200:
            data = response.json().get('fields', {})
            cleaned = self._doc_to_dict(data)
            return Document(cleaned, True)
        elif response.status_code == 404:
            return Document({}, False)
        else:
            if _during_update:
                return {}
            raise_detailed_error(response)

    def batch_get_documents(self, documents: list):
        """Fetches multiple documents in a batch

        Args:
            documents (list): List of document paths relative to the base path passed on initialization
        """
        request_url = f"{self.base_path}:batchGet"
        request_url = replace_all(request_url, '//', '/')
        request_url = "https://" + request_url

        response = self.requests.post(request_url, headers=self.headers, json={
            "documents": [
                f"projects/{self.project_id}/databases/{self.database_name}/documents/{document.lstrip('/')}"
                for document in documents
            ]
        })
        if response.status_code == 200:
            results = response.json()
            return [self._doc_to_dict(result['found']['fields']) for result in results if 'found' in result]
        else:
            raise_detailed_error(response)

    def run_query(self, collection: str, structured_query: dict):
        """Runs a structured query against the collection

        Args:
            collection (str): Collection path relative to the base path passed on initialization
            structured_query (dict): Firestore structured query object
        """
        request_url = f"{self.base_path}/{collection}:runQuery"
        request_url = replace_all(request_url, '//', '/')
        response = self.requests.post(
            request_url, headers=self.headers, json=structured_query)
        if response.status_code == 200:
            results = response.json()
            return [self._doc_to_dict(result['document']['fields']) for result in results if 'document' in result]
        else:
            raise_detailed_error(response)

    def update_document(self, document="", data={}, _new=False):
        if not _new:
            existing_data = self.get_document(document, True)
            data = {**existing_data, **data}

        firestore_data = self._dict_to_doc(data)

        firestore_data = {k: v for k,
                          v in firestore_data.items() if v is not None}

        request_url = f"{self.base_path}/{document}"
        request_url = replace_all(request_url, '//', '/')
        request_url = "https://" + request_url

        response = self.requests.patch(
            request_url, headers=self.headers, json={"fields": firestore_data})

        if response.status_code != 200:
            raise_detailed_error(response)

    def delete_document(self, document):
        """Deletes the document from the Firestore database

        Args:
            document (str): Document path relative to the base path passed on initialization
        """
        request_url = f"{self.base_path}/{document}"
        request_url = replace_all(request_url, '//', '/')
        request_url = "https://" + request_url

        response = self.requests.delete(request_url, headers=self.headers)
        if response.status_code != 200:
            raise_detailed_error(response)

    def list_documents(self, collection: str=""):
        """Lists all documents in a collection

        Args:
            collection (str): Collection path relative to the base path passed on initialization
        """
        
        request_url = self.base_path
        if collection:
            request_url += f"/{collection}"
            
        request_url = replace_all(request_url, '//', '/')
        request_url = f"https://{request_url}"

        response = self.requests.get(request_url, headers=self.headers)
        if response.status_code == 200:
            documents = response.json().get('documents', [])
            return {doc['name']: self._doc_to_dict(doc['fields']) if doc.get('fields') else {} for doc in documents}
        else:
            raise_detailed_error(response)

    def __process_value(self, dtype, value):
        processed = None
        match dtype:
            case 'stringValue':
                processed = str(value)
            case 'integerValue':
                processed = int(value)
            case 'booleanValue':
                processed = bool(value)
            case 'mapValue':
                processed = self._doc_to_dict(value.get('fields', {}))
            case 'timestampValue':
                processed = datetime.fromisoformat(
                    value.replace("Z", "+00:00"))
            case 'arrayValue':
                processed = [
                    self.__process_value(v_type, v_value)
                    for item in value.get('values', [])
                    for v_type, v_value in item.items()
                ]
            case _:
                print("WARNING: Unsupported dtype, defaulting to NoneType:", dtype)

        return processed

    def __convert_to_fb(self, value):
        return ({"stringValue": value} if isinstance(value, str)
                else {"timestampValue": datetime.now().replace(tzinfo=timezone.utc).isoformat(timespec="seconds")} if value == self.SERVER_TIMESTAMP
                else {"booleanValue": value} if isinstance(value, bool)
                else {"integerValue": value} if isinstance(value, int)
                else {"timestampValue": value.replace(tzinfo=timezone.utc).isoformat(timespec="seconds")} if isinstance(value, datetime)
                else {"mapValue": {"fields": self._dict_to_doc(value)}} if isinstance(value, dict)
                else {"arrayValue": {"values": [self.__convert_to_fb(v) for v in value]}} if isinstance(value, list)
                else {"nullValue": None} if value == None
                else None)

    def _dict_to_doc(self, data: dict):
        return {key: self.__convert_to_fb(value) for key, value in data.items()}

    def _doc_to_dict(self, data: dict) -> dict:
        clean = {}
        for key in data:
            dtype = list(data[key].keys())[0]
            clean[key] = self.__process_value(dtype, data[key][dtype])

        return clean
