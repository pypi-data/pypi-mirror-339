from typing import Any
from dataclasses import dataclass, field

import requests

from dahua.utils import generate_password_hash
from dahua.exceptions import DahuaRequestError
from dahua.rpc._global import GlobalRPC
from dahua.rpc.magic_box import MagicBoxRPC
from dahua.rpc.user_manager import UserManagerRPC


@dataclass
class DahuaRpc:
    host: str
    port: int
    
    # Methods
    _global: GlobalRPC = field(init=False)
    magic_box: MagicBoxRPC = field(init=False)
    user_manager: UserManagerRPC = field(init=False)

    def __post_init__(self) -> None:
        self.session: requests.Session = requests.Session()
        self.session_id: str | None = None
        self.request_id: int = 0
        self.base_url: str = f"http://{self.host}:{self.port}"

        # Initialize RPC classes
        self._global = GlobalRPC(client=self)
        self.magic_box = MagicBoxRPC(client=self)
        self.user_manager = UserManagerRPC(client=self)

    def _request(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        endpoint: str = 'RPC2',
        verify: bool = True
    ) -> dict[str, Any]:
        """Send an RPC request."""
        self.request_id += 1
        data: dict[str, Any] = {'method': method, 'id': self.request_id}
        if params is not None:
            data['params'] = params
        if self.session_id:
            data['session'] = self.session_id

        response = self.session.post(f'{self.base_url}/{endpoint}', json=data)
        json_response = response.json()

        if verify:
            if not json_response.get('result'):
                raise DahuaRequestError(f"Request failed: {json_response}")

        return json_response

    def login(self, username: str, password: str) -> None:
        """Login to the camera using the provided username and password."""
        initial_request = self._global.login(
            params={
                'userName': username,
                'password': password,
                'clientType': "Web3.0"
            },
            verify = False # Can't verify first request, as it doesn't have a session yet.
        )

        self.session_id = initial_request.get('session')
        realm = initial_request.get('params', {}).get('realm', '')
        random_value = initial_request.get('params', {}).get('random', '')
        pass_hash = generate_password_hash(username, password, realm, random_value)

        login_params = {
            'userName': username,
            'password': pass_hash,
            'clientType': "Web3.0",
            'authorityType': "Default",
            'passwordType': "Default"
        }

        self._global.login(params=login_params)
