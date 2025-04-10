# Copyright 2021 The IAM Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
from typing import Dict, List, Optional, Any

import aiohttp
import jwt
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from yarl import URL
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from .user import User


class AioHttpClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = None

    async def fetch(self, path, method="GET", **kwargs):
        url = self.base_url + path
        async with self.session.request(method, url, **kwargs) as response:
            if response.status != 200:
                raise ValueError(f"IAM response error: {await response.text()}")
            
            # Try to parse as JSON first
            try:
                return await response.json()
            except:
                # If not JSON, return text
                return await response.text()

    async def get(self, path, **kwargs):
        return await self.fetch(path, method="GET", **kwargs)

    async def post(self, path, **kwargs):
        return await self.fetch(path, method="POST", **kwargs)

    async def __aenter__(self):
        self.session = await aiohttp.ClientSession().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                raise exc_val
        finally:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)


class AsyncIAMSDK:
    def __init__(
        self,
        endpoint: str,
        client_id: str,
        client_secret: str,
        certificate: str,
        org_name: str,
        application_name: str,
        front_endpoint: str = None,
    ):
        self.endpoint = endpoint
        if front_endpoint:
            self.front_endpoint = front_endpoint
        else:
            self.front_endpoint = endpoint.replace(":8000", ":7001")
        self.client_id = client_id
        self.client_secret = client_secret
        self.certificate = certificate
        self.org_name = org_name
        self.application_name = application_name
        self.grant_type = "authorization_code"

        self.algorithms = ["RS256"]
        self._session = AioHttpClient(base_url=self.endpoint)

    @property
    def headers(self) -> Dict:
        basic_auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("utf-8")
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Basic {basic_auth}",
        }

    @property
    def certification(self) -> bytes:
        if not isinstance(self.certificate, str):
            raise TypeError("certificate field must be str type")
        return self.certificate.encode("utf-8")

    async def get_auth_link(
        self,
        redirect_uri: str,
        response_type: str = "code",
        scope: str = "read",
    ) -> str:
        url = self.front_endpoint + "/login/oauth/authorize"
        params = {
            "client_id": self.client_id,
            "response_type": response_type,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": self.application_name,
        }
        return str(URL(url).with_query(params))

    async def get_oauth_token(
        self,
        code: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Dict:
        """
        Request the IAM server to get OAuth token.
        Must be set code or username and password for grant type.
        If nothing is set then client credentials grant will be used.

        :param code: the code that sent from IAM using redirect url
                     back to your server.
        :param username: IAM username
        :param password: username password
        :return: OAuth token
        """
        return await self.oauth_token_request(code, username, password)

    def _get_payload_for_access_token_request(
        self,
        code: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Dict:
        """
        Return payload for request body which was selecting by strategy.
        """
        if code:
            return self.__get_payload_for_authorization_code(code=code)
        elif username and password:
            return self.__get_payload_for_password_credentials(username=username, password=password)
        else:
            return self.__get_payload_for_client_credentials()

    def __get_payload_for_authorization_code(self, code: str) -> Dict:
        """
        Return payload for auth request with authorization code
        """
        return {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
        }

    def __get_payload_for_password_credentials(self, username: str, password: str) -> Dict:
        """
        Return payload for auth request with resource owner password
        credentials.
        """
        return {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": username,
            "password": password,
        }

    def __get_payload_for_client_credentials(self) -> Dict:
        """
        Return payload for auth request with client credentials.
        """
        return {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

    async def oauth_token_request(
        self,
        code: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Dict:
        """
        Request the IAM server to get access_token.
        Must be set code or username and password for grant type.
        If nothing is set then client credentials grant will be used.
        Returns full response as dict.

        :param code: the code that sent from IAM using redirect url
                     back to your server.
        :param username: IAM username
        :param password: username password
        :return: Response from IAM
        """
        params = self._get_payload_for_access_token_request(code=code, username=username, password=password)
        return await self._oauth_token_request(payload=params)

    async def _oauth_token_request(self, payload: Dict) -> Dict:
        """
        Request the IAM server to get access_token.

        :param payload: Body for POST request.
        :return: Response from IAM
        """
        path = "/api/login/oauth/access_token"
        async with self._session as session:
            return await session.post(path, data=payload)

    async def refresh_token_request(self, refresh_token: str, scope: str = "") -> Dict:
        """
        Request the IAM server to get access_token.

        :param refresh_token: refresh_token for send to IAM
        :param scope: OAuth scope
        :return: Response from IAM
        """
        path = "/api/login/oauth/refresh_token"
        params = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": scope,
            "refresh_token": refresh_token,
        }
        async with self._session as session:
            return await session.post(path, data=params)

    async def refresh_oauth_token(self, refresh_token: str, scope: str = "") -> str:
        """
        Request the IAM server to get access_token.

        :param refresh_token: refresh_token for send to IAM
        :param scope: OAuth scope
        :return: Response from IAM
        """
        token = await self.refresh_token_request(refresh_token, scope)
        return token.get("access_token")

    def parse_jwt_token(self, token: str) -> Dict[str, Any]:
        """
        Parse JWT token

        :param token: JWT token
        :return: JWT token claims
        """
        if not self.certification:
            raise ValueError("No certification provided")

        certificate_bytes = self.certification.encode() if isinstance(self.certification, str) else self.certification
        try:
            # Try to load as a certificate first
            cert = x509.load_pem_x509_certificate(certificate_bytes)
            public_key = cert.public_key()
        except Exception:
            try:
                # If not a certificate, try to load as a public key
                public_key = load_pem_public_key(certificate_bytes)
            except Exception as e:
                raise ValueError(f"Failed to load certificate or public key: {str(e)}")

        try:
            # First decode without verification to get the audience
            unverified = jwt.decode(token, options={"verify_signature": False})
            audience = unverified.get("aud")
            if isinstance(audience, list) and len(audience) == 1:
                audience = audience[0]

            # Now decode with verification and the correct audience
            decoded = jwt.decode(token, public_key, algorithms=["RS256"], audience=audience)
            # Convert audience to string if it's a list with a single value
            if "aud" in decoded and isinstance(decoded["aud"], list) and len(decoded["aud"]) == 1:
                decoded["aud"] = decoded["aud"][0]
            return decoded
        except Exception as e:
            raise ValueError(f"Failed to parse JWT token: {str(e)}")

    async def enforce(
        self,
        permission_model_name: str,
        sub: str,
        obj: str,
        act: str,
        v3: Optional[str] = None,
        v4: Optional[str] = None,
        v5: Optional[str] = None,
    ) -> bool:
        """
        Send data to IAM enforce API
        # https://iam.org/docs/permission/exposed-casbin-apis#enforce

        :param permission_model_name: Name permission model (e.g. "permission-built-in")
        :param sub: sub from Casbin
        :param obj: obj from Casbin
        :param act: act from Casbin
        :param v3: v3 from Casbin
        :param v4: v4 from Casbin
        :param v5: v5 from Casbin
        """
        path = "/api/enforce"
        params = {
            "id": permission_model_name,
            "v0": sub,
            "v1": obj,
            "v2": act,
            "v3": v3,
            "v4": v4,
            "v5": v5,
        }
        async with self._session as session:
            response = await session.post(path, headers=self.headers, json=params)
            if hasattr(response, 'json'):
                result = await response.json()
                if isinstance(result, dict):
                    if "status" in result and result["status"] == "error":
                        raise ValueError(f"IAM response error: {result}")
                    if "data" in result:
                        return bool(result["data"])
            return False

    async def batch_enforce(self, permission_model_name: str, permission_rules: List[List[str]]) -> List[bool]:
        """
        Send data to IAM enforce API

        :param permission_model_name: Name permission model
        :param permission_rules: permission rules to enforce
                        [][0] -> sub: subject (user)
                        [][1] -> obj: object (resource)
                        [][2] -> act: action (permission)
        :return: List of boolean values indicating whether each rule is allowed
        """
        path = "/api/batch-enforce"
        
        # Format the request as expected by the server: [[model_name, sub, obj, act], [model_name, sub, obj, act], ...]
        formatted_rules = []
        for rule in permission_rules:
            if not isinstance(rule, list) or len(rule) < 3:
                raise ValueError("Each permission rule must be a list containing at least [subject, object, action]")
            formatted_rules.append([permission_model_name] + rule)

        async with self._session as session:
            response = await session.post(path, headers=self.headers, json=formatted_rules)
            # Handle both dictionary and response object cases
            result = response if isinstance(response, dict) else await response.json()
            
            if isinstance(result, dict):
                if "status" in result and result["status"] == "error":
                    raise ValueError(f"IAM response error: {result}")
                if "data" in result and isinstance(result["data"], list):
                    return [bool(x) for x in result["data"]]
                raise ValueError(f"Unexpected response format from IAM server: {result}")
            return [bool(x) for x in result]

    async def get_users(self) -> Dict:
        """
        Get the users from IAM.

        :return: a list of dicts containing user info
        """
        path = "/api/get-users"
        params = {"owner": self.org_name}
        async with self._session as session:
            users = await session.get(path, headers=self.headers, params=params)
            return users["data"]

    async def get_user(self, user_id: str) -> User:
        """
        Get the user from IAM providing the user_id.

        :param user_id: the id of the user
        :return: User object containing user's info
        :raises ValueError: if user does not exist or is deleted
        """
        path = "/api/get-user"
        params = {"id": f"{self.org_name}/{user_id}"}
        async with self._session as session:
            response = await session.get(path, headers=self.headers, params=params)
            if isinstance(response, dict):
                if response.get("status") != "ok" or not response.get("data"):
                    raise ValueError(f"User not found: {user_id}")
                    
                user_data = response.get("data", {})
                if user_data.get("isDeleted", False):
                    raise ValueError(f"User not found: {user_id}")
                    
                user = User.from_dict(user_data)
                if not user or not user.name:
                    raise ValueError(f"User not found: {user_id}")
                    
                return user
            raise ValueError(f"User not found: {user_id}")

    async def get_user_count(self, is_online: bool = None) -> int:
        """
        Get the count of filtered users for an organization
        :param is_online: True for online users, False for offline users,
                          None for all users
        :return: the count of filtered users for an organization
        """
        path = "/api/get-user-count"
        params = {
            "owner": self.org_name,
        }

        if is_online is None:
            params["isOnline"] = ""
        else:
            params["isOnline"] = "1" if is_online else "0"

        async with self._session as session:
            count = await session.get(path, headers=self.headers, params=params)
            return count["data"]

    async def modify_user(self, method: str, user: User, params=None) -> Dict:
        path = f"/api/{method}"
        async with self._session as session:
            return await session.post(path, params=params, headers=self.headers, json=user.to_dict())

    async def add_user(self, user: User) -> str:
        """
        Add a new user to IAM.

        :param user: User object to add
        :return: Response from IAM
        """
        if not user.name:
            raise ValueError("User name cannot be empty")
        if not user.display_name:
            user.display_name = user.name  # Use name as display_name if not provided

        url = self.endpoint + "/api/add-user"
        query_params = {"id": user.name, "clientId": self.client_id, "clientSecret": self.client_secret}

        async with self._session as session:
            response = await session.post(path="/api/add-user", headers=self.headers, json=user.to_dict(), params=query_params)
            if isinstance(response, dict):
                if response.get("status") == "error":
                    raise ValueError(f"IAM response error:\n{response}")
                return "Affected"
            return "Affected"

    async def update_user(self, user: User) -> str:
        """
        Update an existing user in IAM.

        :param user: User object with updated fields
        :return: Response from IAM
        """
        if not user.name:
            raise ValueError("User name cannot be empty")
        if not user.display_name:
            user.display_name = user.name  # Use name as display_name if not provided

        url = self.endpoint + "/api/update-user"
        query_params = {"id": user.name, "clientId": self.client_id, "clientSecret": self.client_secret}

        async with self._session as session:
            response = await session.post(path="/api/update-user", headers=self.headers, json=user.to_dict(), params=query_params)
            if isinstance(response, dict):
                if response.get("status") == "error":
                    raise ValueError(f"IAM response error:\n{response}")
                return "Affected"
            return "Affected"

    async def delete_user(self, user: User) -> str:
        """
        Delete a user from IAM.

        :param user: User object to delete
        :return: Response from IAM
        """
        if not user.name:
            raise ValueError("User name cannot be empty")

        url = self.endpoint + "/api/delete-user"
        query_params = {"id": user.name, "clientId": self.client_id, "clientSecret": self.client_secret}

        async with self._session as session:
            response = await session.post(path="/api/delete-user", headers=self.headers, json=user.to_dict(), params=query_params)
            if isinstance(response, dict):
                if response.get("status") == "error":
                    raise ValueError(f"IAM response error:\n{response}")
                return "Affected"
            return "Affected"
