"""Define the ArgoCD adapter."""

import json
import logging
import os
import shutil
from contextlib import suppress
from typing import Any, Dict, Optional, Union

from argops.adapters.console import Command
from argops.exceptions import (
    ArgoCDConfigurationError,
    ArgoCDDiffError,
    ArgoCDRefreshError,
    ArgoCDSyncError,
)

log = logging.getLogger(__name__)


class ArgoCD(Command):
    """A Python adapter for interacting with the ArgoCD command line interface.

    This adapter provides methods to check ArgoCD configuration, refresh applications,
    show application diffs, and sync applications.
    """

    def check(self) -> None:
        """Check if ArgoCD is well configured.

        This method verifies:
        1. ArgoCD CLI exists

        Raises:
            ArgoCDConfigurationError if it's not well configured
        """
        log.debug("Checking ArgoCD configuration")
        argocd_path = shutil.which("argocd")
        if argocd_path:
            log.debug(f"ArgoCD CLI found at: {argocd_path}")
        else:
            raise ArgoCDConfigurationError("ArgoCD CLI not found in PATH")

    def set_context(self, context: str) -> None:
        """Set the Kubernetes context.

        We're assuming you're using argocd login --core and that you do the context switch at kubectl level. Also that the context name is equal to the environment name plus an optional prefix stored in the environment variable ARGOPS_ENVIRONMENT_PREFIX.

        Args:
            context: the ArgoCD context
        """
        with suppress(KeyError):
            context = f"{os.environ['ARGOPS_ENVIRONMENT_PREFIX']}-{context}"
        log.debug(f"Setting the kubernetes context: {context}")
        cmd = ["kubectl", "config", "use-context", context]

        return_code, _, stderr = self._run_command(cmd)

        if return_code == 0:
            log.debug(f"Successfully set the kubernetes context: {context}")
        else:
            raise ArgoCDConfigurationError(
                f"Failed to set the context {context}: {stderr}"
            )

    def refresh_application(self, app_name: str) -> Dict[str, Any]:
        """Refresh an application.

        Args:
            app_name: The name of the application to refresh.

        Returns:
            the result of the refresh

            status: synced or not
        """
        log.debug(f"Refreshing application: {app_name}")
        cmd = ["argocd", "app", "get", app_name, "--refresh", "--output", "json"]

        return_code, stdout, stderr = self._run_command(cmd, retries=3)

        if return_code == 0:
            try:
                log.debug(f"Successfully refreshed application: {app_name}")
                data = json.loads(stdout)
                state = {
                    "commit": data["status"]["sync"]["revision"],
                    "health": data["status"]["health"]["status"],
                    "sync": data["status"]["sync"]["status"],
                }
                return state
            except json.JSONDecodeError as e:
                log.error(f"Failed to parse JSON response: {e}")
                raise e
        raise ArgoCDRefreshError(f"Failed to refresh application {app_name}: {stderr}")

    def get_application_diff(
        self, app_name: str, revision: Optional[str] = None
    ) -> str:
        """Show the diff for an application.

        Args:
            app_name: The name of the application.
            revision: The commit id to check

        Returns:
            the message of the diff
        """
        log.debug(f"Showing diff for application: {app_name}")
        cmd = ["argocd", "app", "diff", app_name]
        if revision:
            cmd += ["--revision", revision]

        return_code, stdout, stderr = self._run_command(cmd)

        if return_code == 0:
            log.debug(f"No differences found for application: {app_name}")
        elif return_code == 1:
            log.debug(f"Found differences for application: {app_name}")
        else:
            raise ArgoCDDiffError(
                f"Error getting diff for application {app_name}: {stderr}"
            )
        return stdout

    def sync_application(
        self, app_name: str, prune: bool = False
    ) -> Dict[str, Union[bool, str]]:
        """Sync an application.

        Args:
            app_name: The name of the application to sync.
            prune: Whether to prune resources. Defaults to False.
            dry_run: Whether to perform a dry run. Defaults to False.

        Returns:
            A dictionary with the sync results.
        """
        log.debug(f"Syncing application: {app_name} (prune={prune})")
        cmd = ["argocd", "app", "sync", app_name]

        if prune:
            cmd.append("--prune")

        return_code, stdout, stderr = self._run_command(cmd)

        if return_code == 0:
            log.debug(f"Successfully synced application: {app_name}")
            return {"success": True, "output": stdout}
        else:
            raise ArgoCDSyncError(f"Failed to sync application {app_name}: {stderr}")
