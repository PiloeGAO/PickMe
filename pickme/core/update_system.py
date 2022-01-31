'''
    :package:   PickMe
    :file:      update_system.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Update System.
'''
import json
from urllib import request

from pickme.core.exceptions import CoreError

from pickme.core.logger import get_logger
logger = get_logger()

class UpdateVersion():
    def __init__(self, name="", description="", number="", release_date="", url=""):
        self.__name = name
        self.__description = description
        self.__version = number
        self.__release_date = release_date
        self.__url = url
    
    @classmethod
    def create(cls, raw_version={}, service=""):
        """Create an UpdateVersion from online service.

        Args:
            raw_version (dict, optional): Dict from the API. Defaults to {}.
            service (str, optional): Service name. Defaults to "".

        Raises:
            CoreError: Online Update Service not supported

        Returns:
            updateVersion: The update version from raw_version
        """
        if(service == "github"):
            version_name = raw_version["name"]
            version_description = raw_version["body"]
            version_number = raw_version["tag_name"]
            version_release_date = raw_version["published_at"]
            version_url = raw_version["html_url"]

            return cls(
                name=version_name,
                description=version_description,
                number=version_number,
                release_date=version_release_date,
                url=version_url
            )
        
        # Other services can be implemented here.
        raise CoreError("Online Update Service not supported.")

    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self.__description

    @property
    def version(self):
        return self.__version

    @property
    def version_id(self):
        major, minor, patch = self.__version.split(".")
        return major * 1000000 + minor * 10000 + patch * 10
    
    @property
    def url(self):
        return self.__url

def get_update_versions(url):
    """Get onlive versions from a github API URL.

    Args:
        url (str): URL to request

    Returns:
        list: List of online versions
    """
    version_request = request.Request(url)
    service = ""

    if("https://api.github.com/" in url):
        service = "github"
    
    try:
        with request.urlopen(version_request) as f:
            result =  f.read().decode('utf-8')
    except request.HTTPError:
        logger.error(f"Version check failed - \"{url}\" not reachable.")
        return []
    
    versions = []

    for item in json.loads(result):
        versions.append(UpdateVersion.create(raw_version=item, service=service))
    
    sorted_versions = sorted(versions, key=lambda item: item.version_id)

    return sorted_versions