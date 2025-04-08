class Trading212Error(Exception):
    """Generic exception"""

class Trading212InvalidParameter(Trading212Error):
    """When an invalid parameter is provided"""

class Trading212BadApiKey(Trading212Error):
    """When there is a bad api key provided"""

class Trading212NotFound(Trading212Error):
    """When the requested resource isn't found"""

class Trading212TimeOut(Trading212Error):
    """When there is a timeout"""

class Trading212Limited(Trading212Error):
    """When you have hit the rate limit"""

class Trading212ScopeError(Trading212Error):
    """When the scope is missing for the api key"""