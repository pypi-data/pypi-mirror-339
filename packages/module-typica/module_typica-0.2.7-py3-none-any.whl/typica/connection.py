import re
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class EndpointMeta(BaseModel):
    host: Optional[str] = Field("localhost", description="Connection host")
    port: Optional[str | int] = Field(8000, description="Connection port")

    @property
    def port_int(self) -> int | None:
        if self.port and isinstance(self.port, str):
            return int(self.port)
        return self.port or None


class AuthMeta(BaseModel):
    username: Optional[str] = Field(None, description="Database username")
    password: Optional[str] = Field(None, description="Database password")


class URIConnectionMeta(BaseModel):
    uri: Optional[str] = Field("", description="Database connection URI")


class DBConnectionMeta(EndpointMeta, AuthMeta, URIConnectionMeta):
    database: Optional[str] = Field(None, description="Database name")
    space: Optional[str] = Field(None, description="Database schema / space name")

    def uri_string(self, base: str = "http", with_db: bool = True) -> str:
        """
        Return a URI string for the database connection.

        :param base: The base of the URI (e.g. "http", "postgresql", etc.).
        :param with_db: Whether to include the database name in the URI.
        :return: A string representing the URI.
        """
        if self.host:
            meta = f"{self.host}:{self.port}"
            if self.username:
                return f"{base}://{self.username}:{self.password}@{meta}/{self.database if with_db and self.database else ''}"
            return (
                f"{base}://{meta}/{self.database if with_db and self.database else ''}"
            )
        return ""

    @model_validator(mode="after")
    def extract_uri(self):
        """
        Extracts and parses the URI to populate the connection metadata fields.

        This method processes the `uri` attribute to extract authentication and
        connection details such as username, password, host, port, and database.
        It modifies the respective attributes of the instance based on the parsed
        URI components.

        Steps involved:
        - Strips the scheme from the URI.
        - Splits the URI into metadata and additional query parameters.
        - Extracts database name from query parameters if present.
        - Parses authentication info and host details from the metadata.
        - Converts the port to an integer.

        Returns:
            The instance with populated connection metadata fields.
        """
        if self.uri:
            uri = re.sub(r"\w+:(//|/)", "", self.uri)
            metadata, others = (
                re.split(r"\/\?|\/", uri) if re.search(r"\/\?|\/", uri) else [uri, None]
            )
            if others and not self.database:
                if "&" in others:
                    for other in others.split("&"):
                        if "=" in other and re.search(r"authSource", other):
                            self.database = other.split("=")[-1]
                        elif "=" not in other:
                            self.database = other
                else:
                    self.database = others
            if "@" in metadata:
                self.username, self.password, self.host, self.port = re.split(
                    r"\@|\:", metadata
                )
            else:
                self.host, self.port = re.split(r"\:", metadata)
            if self.port:
                self.port = int(self.port)
        return self


class ClusterConnectionMeta(AuthMeta, URIConnectionMeta):
    cluster_uri: Optional[list[EndpointMeta]] = Field(
        [], description="List of clusters endpoint"
    )
    database: Optional[str] = Field(None, description="Database name")
    space: Optional[str] = Field(None, description="Database schema / space name")

    def uri_string(self, base: str = "http", with_db: bool = True) -> str:
        """
        Return a URI string for the database connection.

        :param base: The base of the URI (e.g. "http", "postgresql", etc.).
        :param with_db: Whether to include the database name in the URI.
        :return: A string representing the URI.
        """
        if self.cluster_uri:
            meta = ",".join([f"{c.host}:{c.port}" for c in self.cluster_uri])
            if self.username:
                return f"{base}://{self.username}:{self.password}@{meta}/{self.database if with_db and self.database else ''}"
            return (
                f"{base}://{meta}/{self.database if with_db and self.database else ''}"
            )
        return ""

    @model_validator(mode="after")
    def extract_uri(self):
        """
        Extract URI from connection string and fill in the respective fields.

        If the connection string is in the format of mongodb://user:password@host:port/database,
        the respective fields will be filled in. If the connection string is in the format of
        mongodb://host:port,host:port/database, the hosts will be split into a list of
        EndpointMeta objects.

        :return: The modified ClusterConnectionMeta object.
        :rtype: ClusterConnectionMeta
        """
        if self.uri:
            uri = re.sub(r"\w+:(//|/)", "", self.uri)
            clean_meta, others = (
                re.split(r"\/\?|\/", uri) if re.search(r"\/\?|\/", uri) else [uri, None]
            )
            cluster_uri = []
            if others and not self.database:
                if "&" in others:
                    for other in others.split("&"):
                        if "=" in other and re.search(r"authSource", other):
                            self.database = other.split("=")[-1]
                        elif "=" not in other:
                            self.database = other
                else:
                    self.database = others
            if "@" in clean_meta:
                auth_meta, clean_meta = re.split(r"\@", clean_meta)
                self.username, self.password = re.split(r"\:", auth_meta)

            for cluster in clean_meta.split(","):
                hostData = re.split(r"\:", cluster)
                cluster_uri.append(
                    EndpointMeta(host=hostData[0], port=int(hostData[1]))
                )
            self.cluster_uri = cluster_uri
        return self


class S3ConnectionMeta(EndpointMeta):
    access_key: Optional[str] = Field(None, description="S3 access key")
    secret_key: Optional[str] = Field(None, description="S3 secret key")
    bucket: str = Field(..., description="S3 bucket name")
    base_path: Optional[str] = Field("/", description="S3 base path")

    @property
    def json_meta(self) -> dict:
        """
        Return a dictionary of metadata for connecting to S3.

        :return: A dictionary with the endpoint_url, access_key, and secret_key.
        """
        return {
            "endpoint_url": f"http://{self.host}:{self.port}",
            "key": self.access_key,
            "secret": self.secret_key,
        }


class RedisConnectionMeta(EndpointMeta, AuthMeta):
    database: int = Field(..., description="Database name")


class RMQConnectionMeta(EndpointMeta, AuthMeta):
    vhost: Optional[str] = Field(None, description="Virtual host")
