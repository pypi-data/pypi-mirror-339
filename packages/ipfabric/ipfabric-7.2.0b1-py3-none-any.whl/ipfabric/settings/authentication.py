import logging
from datetime import datetime
from typing import Optional, Any, Union, ClassVar
from uuid import uuid4

from dateutil import parser
from pydantic import BaseModel, Field, PrivateAttr, field_validator, model_validator, model_serializer

from ipfabric.tools.shared import VALID_IP, validate_ip_network_str, raise_for_status

logger = logging.getLogger("ipfabric")


class Expiration(BaseModel):
    enabled: bool = False
    value: Optional[datetime] = None

    @model_validator(mode="after")
    def _verify(self):
        if self.enabled and not self.value:
            raise ValueError("Enabled Expiration requires a value.")
        elif not self.enabled and self.value:
            raise ValueError("Expiration value requires enabled to be True.")
        return self

    @model_serializer
    def _ser_model(self) -> dict[str, Any]:
        return (
            {"enabled": self.enabled, "value": self.value.strftime("%Y-%m-%d %H:%M:%S")}
            if self.enabled
            else {"enabled": self.enabled}
        )


class BaseCred(BaseModel):
    custom: bool = False
    username: str
    network: list[Union[str, VALID_IP]]  # TODO: Add v6 in 7.3
    excluded: Optional[list[Union[str, VALID_IP]]] = Field(default_factory=list, alias="excludeNetworks")
    expiration: Expiration = Field(None, alias="expirationDate")
    encrypt_password: str = Field(None, alias="password")
    priority: Optional[int] = None
    notes: Optional[str] = None

    @field_validator("network", "excluded")
    @classmethod
    def _verify_valid_networks(cls, v: list[str]) -> list[str]:
        return [validate_ip_network_str(_, ipv6=False) for _ in v]  # TODO: Add v6 in 7.3

    @model_serializer
    def _ser_model(self) -> dict[str, Any]:
        custom = {"custom": self.custom} if self.custom else dict()
        return dict(
            priority=self.priority,
            username=self.username,
            excludeNetworks=self.excluded,
            expirationDate=self.expiration.model_dump(),
            password=self.encrypt_password,
            notes=self.notes or "",
            **custom,
        )


class Credential(BaseCred, BaseModel):
    credential_id: Optional[str] = Field(None, alias="id")
    config_mgmt: bool = Field(False, alias="syslog")

    @model_validator(mode="after")
    def _verify(self):
        if not self.credential_id:
            self.custom = True
        return self

    @model_serializer
    def _ser_cred_model(self) -> dict[str, Any]:
        cred = self._ser_model()
        return dict(
            syslog=self.config_mgmt,
            id=self.credential_id if self.credential_id else str(uuid4()),
            network=self.network,
            **cred,
        )


class Privilege(BaseCred, BaseModel):
    privilege_id: str = Field(None, alias="id")
    network: list[Union[str, VALID_IP]] = Field(None, alias="includeNetworks")

    @model_validator(mode="after")
    def _verify(self):
        if not self.privilege_id:
            self.custom = True
        return self

    @model_serializer
    def _ser_cred_model(self) -> dict[str, Any]:
        cred = self._ser_model()
        return dict(id=self.privilege_id if self.privilege_id else str(uuid4()), includeNetworks=self.network, **cred)


def serialize_list(auth):
    if not auth:
        return list()
    priorities = sorted([_.priority for _ in auth])
    if priorities != list(range(1, len(priorities) + 1)):
        raise ValueError("Priorities are not sequential.")
    return [_.model_dump() for _ in auth]


class CredentialList(BaseModel):
    credentials: list[Credential]

    @model_serializer
    def _verify_priorities(self) -> dict[str, Any]:
        return serialize_list(self.credentials)

    def __bool__(self):
        return bool(self.credentials)


class PrivilegeList(BaseModel):
    privileges: list[Privilege]

    @model_serializer
    def _verify_priorities(self) -> dict[str, Any]:
        return serialize_list(self.privileges)


class Authentication(BaseModel):
    client: Any = Field(exclude=True)
    _credentials: dict[int, Credential] = PrivateAttr(default=dict())
    _enables: dict[int, Privilege] = PrivateAttr(default=dict())
    _cred_url: ClassVar[str] = "settings/credentials"
    _priv_url: ClassVar[str] = "settings/privileges"

    def model_post_init(self, __context: Any) -> None:
        self._credentials = self.get_credentials()
        self._enables = self.get_enables()

    @property
    def credentials(self) -> dict[int, Credential]:
        return self._credentials

    @property
    def enables(self) -> dict[int, Privilege]:
        return self._enables

    @property
    def credentials_by_id(self) -> dict[str, Credential]:
        return {_.credential_id: _ for _ in self._credentials.values()}

    @property
    def enables_by_id(self) -> dict[str, Privilege]:
        return {_.privilege_id: _ for _ in self._enables.values()}

    def get_credentials(self) -> dict[int, Credential]:
        """
        Get all credentials and sets them in the Authentication.credentials
        :return: self.credentials
        """
        res = raise_for_status(self.client.get(self._cred_url))
        self._credentials = {cred["priority"]: Credential(**cred) for cred in res.json()["data"]}
        return self._credentials

    def get_enables(self) -> dict[int, Privilege]:
        """
        Get all privileges (enable passwords) and sets them in the Authentication.enables
        :return:
        """
        res = raise_for_status(self.client.get(self._priv_url))
        self._enables = {priv["priority"]: Privilege(**priv) for priv in res.json()["data"]}
        return self._enables

    @staticmethod
    def _create_payload(username, password, notes, network, excluded, expiration):
        networks = network or ["0.0.0.0/0"]
        excluded = excluded or list()
        if expiration:
            expires = dict(
                enabled=True,
                value=parser.parse(expiration).strftime("%Y-%m-%d %H:%M:%S"),
            )
        else:
            expires = dict(enabled=False)
        payload = {
            "password": password,
            "username": username,
            "notes": notes or username,
            "excludeNetworks": [validate_ip_network_str(e, ipv6=False) for e in excluded],  # TODO: Add v6 in 7.3
            "expirationDate": expires,
            "network": [validate_ip_network_str(e, ipv6=False) for e in networks],
        }
        return payload

    def update_credential(
        self,
        credential: Credential,
        password: Optional[str] = None,
    ) -> Credential:
        """
        Updates a credential. Username cannot be changed, please delete and recreate.

        :param credential: Credential: Modified Credential object to update
        :param password: str: If updating the password then this is the unencrypted password

        :return: Credential: Obj: Credential Obj with ID and encrypted password
        """
        all_creds = {v.credential_id: v.model_dump(by_alias=True) for v in self.credentials.values()}
        if all_creds[credential.credential_id]["username"] != credential.username:
            raise SyntaxError("Cannot change username of credential, please delete and recreate.")
        all_creds[credential.credential_id] = credential.model_dump(by_alias=True)
        if password:
            all_creds[credential.credential_id].update({"password": password, "custom": True})
        raise_for_status(self.client.patch("settings", json={"credentials": list(all_creds.values())}))
        self.get_credentials()
        cred = self.credentials_by_id[credential.credential_id]
        logger.info(f"Updated credential with username {cred.username} and ID of {cred.credential_id}")
        return cred

    def create_credential(
        self,
        username: str,
        password: str,
        networks: list = None,
        notes: str = None,
        excluded: list = None,
        config_mgmt: bool = True,
        expiration: str = None,
    ) -> Credential:
        """
        Creates a new credential. Requires username and password and will default to all networks with no expiration.
        Does not default to use for configuration management, please set to true if needed.
        After creation Authentication.credentials will be updated with new priorities and the new cred is returned.
        :param username: str: Username
        :param password: str: Unencrypted password
        :param networks: list: List of networks defaults to ["0.0.0.0/0"]
        :param notes: str: Optional Note/Description of credential
        :param excluded: list: Optional list of networks to exclude
        :param config_mgmt: bool: Default True - do not use for configuration management
        :param expiration: str: Optional date for expiration, if none then do not expire.
                                To ensure correct date use YYYYMMDD or MM/DD/YYYY formats
        :return: Credential: Obj: Credential Obj with ID and encrypted password
        """
        payload = self._create_payload(username, password, notes, networks, excluded, expiration)
        payload.update({"syslog": config_mgmt})
        res = raise_for_status(self.client.post(self._cred_url, json=payload))
        self.get_credentials()
        cred = Credential(**res.json())
        logger.info(f"Created credential with username {cred.username} and ID of {cred.credential_id}")
        return cred

    def update_enable(
        self,
        enable: Privilege,
        password: Optional[str] = None,
    ) -> Credential:
        """
        Updates a enable privilege password. Username cannot be changed, please delete and recreate.

        :param enable: Privilege: Modified Credential object to update
        :param password: str: If updating the password then this is the unencrypted password

        :return: Privilege: Obj: Privilege Obj with ID and encrypted password
        """
        all_priv = {v.privilege_id: v.model_dump(by_alias=True) for v in self.enables.values()}
        if all_priv[enable.privilege_id]["username"] != enable.username:
            raise SyntaxError("Cannot change username of enable privilege, please delete and recreate.")
        all_priv[enable.privilege_id] = enable.model_dump(by_alias=True)
        if password:
            all_priv[enable.privilege_id].update({"password": password, "custom": True})
        raise_for_status(self.client.patch("settings", json={"privileges": list(all_priv.values())}))
        self.get_credentials()
        priv = self.enables_by_id[enable.privilege_id]
        logger.info(f"Updated enable privilege with username {priv.username} and ID of {priv.privilege_id}")
        return priv

    def create_enable(
        self,
        username: str,
        password: str,
        networks: list = None,
        notes: str = None,
        excluded: list = None,
        expiration: str = None,
    ) -> Privilege:
        """
        Creates a new enable password (privilege account).
        Requires username and password and will default to all networks with no expiration.
        After creation Authentication.enables will be updated with new priorities and the new enable is returned.
        :param username: str: Username
        :param password: str: Unencrypted password
        :param networks: list: List of networks defaults to ["0.0.0.0/0"]
        :param notes: str: Optional Note/Description of credential
        :param excluded: list: Optional list of networks to exclude
        :param expiration: str: Optional date for expiration, if none then do not expire.
                                To ensure correct date use YYYYMMDD or MM/DD/YYYY formats
        :return: Privilege: Obj: Privilege Obj with ID and encrypted password
        """
        payload = self._create_payload(username, password, notes, networks, excluded, expiration)
        payload["includeNetworks"] = payload.pop("network")
        res = raise_for_status(self.client.post(self._priv_url, json=payload))
        self.get_enables()
        priv = Privilege(**res.json())
        logger.info(f"Created enable password with username {priv.username} and ID of {priv.privilege_id}")
        return priv

    def delete_credential(self, credential: Union[Credential, str]) -> bool:
        """
        Deletes a credential and updates Authentication.credentials with new priorities.
        :param credential: Union[Credential, str]: Cred ID in a string or Credential object
        :return:
        """
        cred = credential.credential_id if isinstance(credential, Credential) else credential
        raise_for_status(self.client.request("DELETE", self._cred_url, json=[cred]))
        self.get_credentials()
        logger.warning(f"Deleted credential ID {cred}")
        return True

    def delete_enable(self, enable: Union[Privilege, str]) -> bool:
        """
        Deletes an enable password (privilege account) and updates Authentication.enable with new priorities.
        :param enable: Union[Privilege, str]: Enable ID in a string or Privilege object
        :return:
        """
        priv = enable.privilege_id if isinstance(enable, Privilege) else enable
        raise_for_status(self.client.request("DELETE", self._priv_url, json=[priv]))
        self.get_enables()
        logger.warning(f"Deleted enable password ID {priv}")
        return True

    def update_cred_priority(self, credentials: dict) -> dict:
        """
        Updates the priority of credentials.  Reorder Authentication.credentials dictionary and submit to this method.
        :param credentials: dict: {priority: Credential}
        :return: self.credentials: dict: {priority: Credential}
        """
        payload = [dict(id=c.credential_id, priority=p) for p, c in credentials.items()]
        raise_for_status(self.client.patch(self._cred_url, json=payload))
        self.get_credentials()
        return self.credentials

    def update_enable_priority(self, enables: dict) -> dict:
        """
        Updates the priority of enable passwords.  Reorder Authentication.enables dictionary and submit to this method.
        :param enables: dict: {priority: Privilege}
        :return: self.enables: dict: {priority: Privilege}
        """
        payload = [dict(id=e.privilege_id, priority=p) for p, e in enables.items()]
        raise_for_status(self.client.patch(self._priv_url, json=payload))
        self.get_enables()
        return self.enables
