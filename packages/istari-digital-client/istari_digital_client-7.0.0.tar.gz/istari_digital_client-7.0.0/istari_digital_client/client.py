from __future__ import annotations
import json
import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import Union, TypeAlias, Optional
import uuid
from datetime import datetime, timezone

from istari_digital_client.api.client_api import ClientApi
from istari_digital_client.api_client import ApiClient
from istari_digital_client.configuration import Configuration, ConfigurationError

from istari_digital_client.models.new_source import NewSource
from istari_digital_client.models.artifact import Artifact
from istari_digital_client.models.comment import Comment
from istari_digital_client.models.file import File
from istari_digital_client.models.job import Job
from istari_digital_client.models.model import Model
from istari_digital_client.models.file_revision import FileRevision
from istari_digital_client.models.source import Source
from istari_digital_client.models.token_with_properties import TokenWithProperties
from istari_digital_client.models.function_auth_secret import FunctionAuthSecret
from istari_digital_client.models.new_function_auth_secret import NewFunctionAuthSecret
from istari_digital_client.models.function_auth_type import FunctionAuthType

import istari_digital_core

logger = logging.getLogger("istari-digital-client.client")

PathLike = Union[str, os.PathLike, Path]
JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


class Client(ClientApi):
    """Create a new instance of the Istari client

    Args:
        config (Configuration | None): The configuration for the client

    Returns:
        Client: The Istari client instance
    """

    def __init__(
        self,
        config: Configuration | None = None,
    ) -> None:
        config = config or Configuration()

        if not config.registry_url:
            raise ConfigurationError(
                "Registry URL not set! Must be specified, either via ISTART_REGISTRY_URL env or by explicitly setting "
                "in  'registry_url' parameter in (optional) configuration parameter on client initialization"
            )
        if not config.registry_auth_token:
            logger.warning("registry auth token not set!")

        self.configuration: Configuration = config

        self._api_client = ApiClient(config)

        super().__init__(self.configuration, self._api_client)

    def __del__(self):
        if (
            self.configuration.filesystem_cache_enabled
            and self.configuration.filesystem_cache_clean_on_exit
            and self.configuration.filesystem_cache_root.exists()
            and self.configuration.filesystem_cache_root.is_dir()
        ):
            logger.debug("Cleaning up cache contents for client exit")
            for child in self.configuration.filesystem_cache_root.iterdir():
                if child.is_dir():
                    logger.debug("deleting cache directory - %s", child)
                    shutil.rmtree(
                        self.configuration.filesystem_cache_root, ignore_errors=True
                    )
                elif child.is_file() and not child.is_symlink():
                    logger.debug("deleting cache file - %s", child)
                    child.unlink(missing_ok=True)
                else:
                    logger.debug(
                        "not deleting cache item (is neither a directory nor a regular file) -  %s",
                        child,
                    )

    def create_revision(
        self,
        file_path: PathLike,
        sources: list[NewSource | str] | None = None,
        display_name: str | None = None,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
    ) -> FileRevision:
        storage_revision = self.storage_client.create_revision(
            str(file_path),
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        if sources:
            source_list = []
            for source in sources:
                if isinstance(source, str):
                    revision_id = source
                    relationship_identifier = None
                else:
                    revision_id = source.revision_id
                    relationship_identifier = source.relationship_identifier

                source_list.append(
                    Source(
                        revision_id=revision_id,
                        file_id=None,
                        resource_type=None,
                        resource_id=None,
                        relationship_identifier=relationship_identifier,
                    )
                )

        else:
            source_list = []

        return FileRevision.from_storage_revision(
            storage_revision,
            sources=source_list,
        )

    def update_revision_properties(
        self,
        file: File,
        display_name: str | None = None,
        description: str | None = None,
    ) -> TokenWithProperties:
        file_revision = file.revision

        storage_properties = istari_digital_core.Properties(
            file_name=file_revision.name or "",
            extension=file_revision.extension or "",
            size=file_revision.size or 0,
            description=description,
            mime=file_revision.mime or "",
            version_name=file_revision.version_name or "",
            external_identifier=file_revision.external_identifier or "",
            display_name=display_name,
        )

        updated_properties_token = self.storage_client.update_properties(
            properties=storage_properties,
        )

        return TokenWithProperties(
            id=str(uuid.uuid4()),
            created=datetime.now(timezone.utc),
            sha=updated_properties_token.sha,
            salt=updated_properties_token.salt,
            name=storage_properties.file_name,
            extension=storage_properties.extension,
            size=storage_properties.size,
            description=storage_properties.description,
            mime=storage_properties.mime,
            version_name=storage_properties.version_name,
            external_identifier=storage_properties.external_identifier,
            display_name=storage_properties.display_name,
        )

    def add_artifact(
        self,
        model_id: str,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> Artifact:
        """Add an artifact

        Args:
            model_id (str): The model to add the artifact to
            path (PathLike): The path to the artifact
            sources (List[NewSource]): The sources of the artifact
            description (str | None): The description of the artifact
            version_name (str | None): The version name of the artifact
            external_identifier (str | None): The external identifier of the artifact
            display_name (str | None): The display name of the artifact

        Returns:
            Artifact: The added artifact

        """
        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._create_artifact(
            model_id=model_id,
            file_revision=file_revision,
        )

    def update_artifact(
        self,
        artifact_id: str,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> Artifact:
        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._update_artifact(
            artifact_id=artifact_id,
            file_revision=file_revision,
        )

    def add_comment(
        self,
        resource_id: str,
        path: PathLike,
        description: str | None = None,
    ) -> Comment:
        """Add a comment to a resource

        Args:
            resource_id (str): The resource to add the comment to
            path (PathLike): The path to the comment
            description (str | None): The description of the comment

        Returns:
            Comment: The added comment

        """
        file_revision = self.create_revision(
            file_path=path,
            sources=None,
            display_name=None,
            description=description,
            version_name=None,
            external_identifier=None,
        )

        return self._create_comment(
            resource_id=resource_id,
            file_revision=file_revision,
        )

    def update_comment(
        self,
        comment_id: str,
        path: PathLike,
        description: str | None = None,
    ) -> Comment:
        """Update a comment

        Args:
            comment_id (str | UUID | Comment): The comment to update
            path (PathLike): The path to the comment
            description (str | None): The description of the comment

        Returns:
            Comment: The updated comment

        """
        file_revision = self.create_revision(
            file_path=path,
            sources=None,
            display_name=None,
            description=description,
            version_name=None,
            external_identifier=None,
        )

        return self._update_comment(
            comment_id=comment_id,
            file_revision=file_revision,
        )

    def add_file(
        self,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> File:
        """Add a file

        Args:
            path (PathLike): The path to the file
            sources (List[NewSource] | None): The sources of the file
            description (str | None): The description of the file
            version_name (str | None): The version name of the file
            external_identifier (str | None): The external identifier of the file
            display_name (str | None): The display name of the file

        Returns:
            File: The added file

        """
        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._create_file(
            file_revision=file_revision,
        )

    def update_file(
        self,
        file_id: str,
        path: PathLike | str,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> File:
        """Update a file

        Args:
            file_id (str): The file to update
            path (PathLike): The path to the file
            sources (List[NewSource] | None): The sources of the file
            description (str | None): The description of the file
            version_name (str | None): The version name of the file
            external_identifier (str | None): The external identifier of the file
            display_name (str | None): The display name of the file

        Returns:
            File: The updated file

        """
        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._update_file(
            file_id=file_id,
            file_revision=file_revision,
        )

    def update_file_properties(
        self,
        file: File,
        display_name: str | None = None,
        description: str | None = None,
    ) -> File:
        """Update file properties

        Args:
            file (File): The file to update
            display_name (str | None): The display name of the file
            description (str | None): The description of the file

        Returns:
            File: The updated file

        """
        token_with_properties = self.update_revision_properties(
            file=file,
            display_name=display_name,
            description=description,
        )

        return self._update_file_properties(
            file_id=file.id, token_with_properties=token_with_properties
        )

    def add_job(
        self,
        model_id: str,
        function: str,
        *,
        parameters: JSON | None = None,
        parameters_file: PathLike | None = None,
        tool_name: str | None = None,
        tool_version: str | None = None,
        operating_system: str | None = None,
        agent_identifier: str | None = None,
        sources: list[NewSource | str] | None = None,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
        **kwargs,
    ) -> "Job":
        """Add a job

        Args:
            model_id (str): The model to add the job to
            function (str): The function of the job
            parameters (JSON | None): The parameters of the job
            parameters_file (PathLike | None): The path to the parameters file
            tool_name (str | None): The name of the tool
            tool_version (str | None): The version of the tool
            operating_system (str | None): The operating system of the agent
            agent_identifier (str | None): The identifier of the agent
            sources (List[NewSource] | None): The sources of the job
            description (str | None): The description of the job
            version_name (str | None): The version name of the job
            external_identifier (str | None): The external identifier of the job
            display_name (str | None): The display name of the job

        Returns:
            Job: The added job

        """
        parameters_file_is_temp = False
        if parameters_file and (parameters or kwargs):
            raise ValueError(
                "Can't combine a parameters file with explicit parameters or parameter kwargs"
            )
        if not parameters_file:
            if parameters and kwargs:
                raise ValueError(
                    "Can't combine explicit parameters with parameters kwargs"
                )
            parameters = parameters or kwargs
            parameters_file = Path(
                tempfile.NamedTemporaryFile(
                    prefix="parameters", suffix=".json", delete=False
                ).name
            )
            parameters_file.write_text(json.dumps(parameters, indent=4))
            parameters_file_is_temp = True
        parameters_file = Path(parameters_file)
        try:
            file_revision = self.create_revision(
                file_path=str(parameters_file),
                sources=sources,
                display_name=display_name,
                description=description,
                version_name=version_name,
                external_identifier=external_identifier,
            )

            openapi_job = self._create_model_job(
                model_id=model_id,
                function_name=function,
                file_revision=file_revision,
                tool_name=tool_name,
                tool_version=tool_version,
                operating_system=operating_system,
                agent_identifier=agent_identifier,
            )
        finally:
            if parameters_file_is_temp:
                if parameters_file.exists():
                    parameters_file.unlink(missing_ok=True)

        return openapi_job

    def update_job(
        self,
        job_id: str,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> Job:
        """Update a job

        Args:
            job_id (str): The job to update
            path (PathLike): The path to the job
            sources (List[NewSource] | None): The sources of the job
            description (str | None): The description of the job
            version_name (str | None): The version name of the job
            external_identifier (str | None): The external identifier of the job
            display_name (str | None): The display name of the job

        Returns:
            Job: The updated job

        """
        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._update_job(
            job_id=job_id,
            file_revision=file_revision,
        )

    def add_model(
        self,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> Model:
        """Add a model

        Args:
            path (PathLike): The path to the model
            sources (List[NewSource] | None): The sources of the model
            description (str | None): The description of the model
            version_name (str | None): The version name of the model
            external_identifier (str | None): The external identifier of the model
            display_name (str | None): The display name of the model

        Returns:
            model: The added model

        """
        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )
        return self._create_model(
            file_revision=file_revision,
        )

    def update_model(
        self,
        model_id: str,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> Model:
        """Update a model

        Args:
            model_id (str): The model to update
            path (PathLike): The path to the model
            sources (List[NewSource] | None): The sources of the model
            description (str | None): The description of the model
            version_name (str | None): The version name of the model
            external_identifier (str | None): The external identifier of the model
            display_name (str | None): The display name of the model

        Returns:
            model: The updated model

        """
        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._update_model(
            model_id=model_id,
            file_revision=file_revision,
        )

    def add_function_auth_secret(
        self,
        auth_provider_name: str,
        function_auth_type: FunctionAuthType,
        path: PathLike,
        expiration: Optional[datetime] = None,
    ) -> FunctionAuthSecret:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)

        file_revision = self.create_revision(
            file_path=path,
        )

        secret = NewFunctionAuthSecret(
            auth_provider_name=auth_provider_name,
            revision=file_revision,
            function_auth_type=function_auth_type,
            expiration=expiration,
        )

        return self._add_function_auth_secret(secret)
