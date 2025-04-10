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

import json
from typing import Dict, List

import requests


class User:
    def __init__(self):
        self.address = [""]
        self.affiliation = ""
        self.avatar = ""
        self.createdTime = ""
        self.dingtalk = ""
        self.displayName = ""
        self.email = ""
        self.facebook = ""
        self.gitee = ""
        self.github = ""
        self.google = ""
        self.hash = ""
        self.id = ""
        self.isAdmin = False
        self.isForbidden = False
        self.isGlobalAdmin = False
        self.language = ""
        self.name = ""
        self.owner = ""
        self.password = ""
        self.phone = ""
        self.preHash = ""
        self.qq = ""
        self.score = 0
        self.signupApplication = ""
        self.tag = ""
        self.type = ""
        self.updatedTime = ""
        self.wechat = ""
        self.weibo = ""

    @classmethod
    def new(cls, owner, name, created_time, display_name):
        self = cls()
        self.name = name
        self.owner = owner
        self.createdTime = created_time
        self.displayName = display_name
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        user = cls()
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        return user

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _UserSDK:
    def get_users(self) -> List[Dict]:
        """
        Get the users from IAM.

        :return: a list of dicts containing user info
        """
        url = self.endpoint + "/api/get-users"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        users = []
        for user in response["data"]:
            users.append(User.from_dict(user))
        return users

    def get_user(self, user_id: str) -> User:
        """
        Get the user from IAM providing the user_id.

        :param user_id: the id of the user
        :return: User object containing user's info
        :raises ValueError: if user does not exist or is deleted
        """
        url = self.endpoint + "/api/get-user"
        params = {
            "id": f"{self.org_name}/{user_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        
        try:
            r = requests.get(url, params)
            if r.status_code != 200:
                raise ValueError(f"User not found: {user_id}")
                
            try:
                response = r.json()
            except:
                raise ValueError(f"User not found: {user_id}")
                
            if not response or response.get("status") != "ok" or not response.get("data"):
                raise ValueError(f"User not found: {user_id}")
                
            user_data = response.get("data", {})
            if user_data.get("isDeleted", False):
                raise ValueError(f"User not found: {user_id}")
                
            user = User.from_dict(user_data)
            if not user or not user.name:
                raise ValueError(f"User not found: {user_id}")
                
            return user
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get user: {user_id} ({str(e)})")

    def get_user_count(self, is_online: bool = None) -> int:
        """
        Get the count of filtered users for an organization
        :param is_online: True for online users, False for offline users,
                          None for all users
        :return: the count of filtered users for an organization
        """
        url = self.endpoint + "/api/get-user-count"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }

        if is_online is None:
            params["isOnline"] = ""
        else:
            params["isOnline"] = "1" if is_online else "0"

        r = requests.get(url, params)
        count = r.json()
        return count

    def modify_user(self, user: User) -> str:
        """
        Modify a user in IAM.

        :param user: User object to modify
        :return: Response from IAM
        """
        if not user.name:
            raise ValueError("User name cannot be empty")
        if not user.display_name:
            user.display_name = user.name  # Use name as display_name if not provided

        url = self.endpoint + "/api/update-user"
        query_params = {"id": user.name, "clientId": self.client_id, "clientSecret": self.client_secret}

        r = requests.post(url, json=user.to_dict(), params=query_params)
        if r.status_code != 200 or "json" not in r.headers["content-type"]:
            error_str = "IAM response error:\n" + str(r.text)
            raise ValueError(error_str)

        response = r.json()
        if response.get("status") == "error":
            raise ValueError(f"IAM response error:\n{r.text}")
        return response.get("data", "Affected")

    def add_user(self, user: User) -> str:
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

        r = requests.post(url, json=user.to_dict(), params=query_params)
        if r.status_code != 200 or "json" not in r.headers["content-type"]:
            error_str = "IAM response error:\n" + str(r.text)
            raise ValueError(error_str)

        response = r.json()
        if response.get("status") == "error":
            raise ValueError(f"IAM response error:\n{r.text}")
        return response.get("data", "Affected")

    def update_user(self, user: User) -> str:
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

        r = requests.post(url, json=user.to_dict(), params=query_params)
        if r.status_code != 200 or "json" not in r.headers["content-type"]:
            error_str = "IAM response error:\n" + str(r.text)
            raise ValueError(error_str)

        response = r.json()
        if response.get("status") == "error":
            raise ValueError(f"IAM response error:\n{r.text}")
        return response.get("data", "Affected")

    def delete_user(self, user: User) -> str:
        """
        Delete a user from IAM.

        :param user: User object to delete
        :return: Response from IAM
        """
        if not user.name:
            raise ValueError("User name cannot be empty")

        url = self.endpoint + "/api/delete-user"
        query_params = {"id": user.name, "clientId": self.client_id, "clientSecret": self.client_secret}

        r = requests.post(url, json=user.to_dict(), params=query_params)
        if r.status_code != 200 or "json" not in r.headers["content-type"]:
            error_str = "IAM response error:\n" + str(r.text)
            raise ValueError(error_str)

        response = r.json()
        if response.get("status") == "error":
            raise ValueError(f"IAM response error:\n{r.text}")
        return response.get("data", "Affected")
