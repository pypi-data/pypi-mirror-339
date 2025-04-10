"""Define program exceptions."""

# ArgoCD


class ArgoCDConfigurationError(Exception):
    """Custom exception for ArgoCD configuration errors."""

    pass


class ArgoCDRefreshError(Exception):
    """Custom exception for ArgoCD refresh errors."""

    pass


class ArgoCDDiffError(Exception):
    """Custom exception for ArgoCD diff errors."""

    pass


class ArgoCDSyncError(Exception):
    """Custom exception for ArgoCD sync errors."""

    pass


# Gitea


class TeaConfigurationError(Exception):
    """Custom exception for gitea tea configuration errors."""

    pass


class TeaRuntimeError(Exception):
    """Custom exception for gitea tea runtime errors."""

    pass
