from awesomeNations.connection import WrapperConnection, URLManager
from awesomeNations.customMethods import join_keys, format_key
from awesomeNations.internalTools import NationAuth
from awesomeNations.exceptions import HTTPError
from pprint import pprint as pp
from datetime import datetime
from typing import Optional
from urllib3 import Timeout
from typing import Literal
from pathlib import Path
from logging import WARNING
import logging

logger = logging.getLogger("AwesomeLogger")
logging.basicConfig(level=logging.WARNING, format="[%(asctime)s] %(levelname)s: %(message)s")

wrapper = WrapperConnection()
url_manager = URLManager("https://www.nationstates.net/cgi-bin/api.cgi")

class AwesomeNations():
    """
    # 🚩 AwesomeNations 🚩

    Welcome! I'm the main class of this library and can't wait to collaborate with you!
    Feel free to explore my [GitHub repository](https://github.com/Stalot/AwesomeNations)
    and report any issues [here](https://github.com/Stalot/AwesomeNations/issues).

    # 📚 Useful References 📚
    
    If you want to make things right, I highly recommend you to **read documentation**.
    Yes, I know, it sounds as thrilling as watching paint dry... But you really should!
    Here are some helpful links for coding guidelines and references. Please note that
    these resources may change over time:

    - 📖 [NationStates API Documentation](https://www.nationstates.net/pages/api.html)  
    - ⚖️ [NationStates Script Rules for HTML site](https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966)
    
    ---
    
    ### user_agent:

    > Sets a User-Agent. Whenever possible, your tool should identify itself by setting
    > the User-Agent header with relevant data.

    > - `<application name>/<version> <comments>`
    > - `ExampleScript/1.2 (by:Testlandia; usedBy:Maxtopia)`
    
    ### request_timeout:

    > Defines a timeout (in seconds) for requests.

    > - `request_timeout: tuple = (10, 5)` -> 10 seconds for connecting, 5 seconds for reading.
    > - `request_timeout: int = 10` -> 10 seconds for both.
    
    ### ratelimit_sleep:
    
    > This allows to automatically "sleep" if the API ratelimit is reached, prevents temporary
    > lockouts due to excessive requests in a short span of time.

    ### ratelimit_reset_time:
    
    > Defines the reset time (in seconds) to wait when the API ratelimit is reached.
    
    ### api_version:
    
    > This setting allows you to specify the NationStates API version your script uses.

    ### log_level:
    
    > Sets logging log level, if None is given, disables logging.
    """

    def __init__(self,
                 user_agent: str,
                 request_timeout: int | tuple = (15, 10),
                 ratelimit_sleep: bool = True,
                 ratelimit_reset_time: int = 30,
                 api_version: int = 12,
                 log_level: Optional[int] = WARNING):
        self.user_agent: str = user_agent
        self.request_timeout: int | tuple = request_timeout
        self.ratelimit_sleep: bool = ratelimit_sleep
        self.ratelimit_reset_time: int = ratelimit_reset_time
        self.api_version: int = api_version
        self.log_level: Optional[int] = log_level

        headers: dict = {
        "User-Agent": self.user_agent,
        "Cache-Control": "no-cache",
        }
        
        wrapper.headers = headers
        wrapper.request_timeout = Timeout(connect=self.request_timeout[0], read=self.request_timeout[1]) if type(self.request_timeout) is tuple else int(self.request_timeout)
        wrapper.ratelimit_sleep = self.ratelimit_sleep
        wrapper.ratelimit_reset_time = self.ratelimit_reset_time
        wrapper.api_version = self.api_version
        
        if self.log_level is None:
            logger.disabled = True
        elif type(self.log_level) is int:
            logger.level = self.log_level
        else:
            raise ValueError(f"Invalid {type(self.log_level).__name__} '{self.log_level}', log_level must be an int (to change level) or None (to disable logging)")

    def __repr__(self):
        return f"AwesomeNations(user_agent={self.user_agent}, request_timeout={self.request_timeout}, ratelimit_sleep={self.ratelimit_sleep}, ratelimit_reset_time={self.ratelimit_reset_time}, api_version={self.api_version}, log_level={self.log_level})"

    def today_is_nationstates_birthday(self) -> bool:
        "Today is 11/13?"
        today = datetime.today()
        date: str = today.strftime('%D')
        birthday: bool = False
        if '11/13' in date:
            birthday = True
        return birthday

    def get_nationstates_age(self) -> int:
        "Current year - NationStates year of creation (NationStates was created in 2002)."
        created = 2002
        today = datetime.today().year
        age = today - created
        return age

    def get_daily_data_dumps(self, filepath: str | Path = "./datadump.gz", type: Literal["nation", "region"] = "nation") -> None:
        """
        Dowloads NationStates daily data dumps.
        
        ### type: str
        
        - "nation": Dowloads the nation data dump.
        - "region": Dowloads the region data dump.
        """
        nation_url: str = "https://www.nationstates.net/pages/nations.xml.gz"
        region_url: str = "https://www.nationstates.net/pages/regions.xml.gz"

        match type:
            case "nation":
                wrapper.fetch_file(nation_url, filepath)
            case "region":
                wrapper.fetch_file(region_url, filepath)
            case _:
                raise ValueError(type)

    def get_world_shards(self, shards: str | tuple[str] | list[str], **kwargs) -> dict:
        """
        Gets one or more shards from the World API.
        """
        for kwarg in kwargs:
            kwargs[kwarg] = join_keys(kwargs[kwarg])
        params: Optional[str] = join_keys([f"{kwarg}={kwargs[kwarg]}" for kwarg in kwargs], ";") if kwargs else None
        url: str = url_manager.generate_shards_url("world", shards, params)
        response: dict = wrapper.fetch_api_data(url)
        return response

    def get_world_assembly_shards(self, shards: str | tuple[str] | list[str], **kwargs) -> dict:
        """
        Gets one or more shards from the World Assembly API.
        """
        for kwarg in kwargs:
            kwargs[kwarg] = join_keys(kwargs[kwarg])
        params: Optional[str] = join_keys([f"{kwarg}={kwargs[kwarg]}" for kwarg in kwargs], ";") if kwargs else None
        url: str = url_manager.generate_shards_url("wa",
                                                   shards,
                                                   params,
                                                   council_id=kwargs["council_id"])
        response: dict = wrapper.fetch_api_data(url)
        return response

    def get_api_latest_version(self) -> int:
        """Gets NationStates API latest version"""
        url = "https://www.nationstates.net/cgi-bin/api.cgi?a=version"
        latest_version: int = int(wrapper.fetch_raw_data(url))
        return latest_version

    class Nation:
        """
        Class dedicated to NationStates nation API.
        """
        def __init__(self,
                     nation_name: str,
                     password: str = None,
                     autologin: str = None) -> None:
            self.nation_name: str = format_key(nation_name, False, '%20') # Name is automatically parsed.
            wrapper._auth = NationAuth(password, autologin) if any((password, autologin)) else None

        def __repr__(self):
            return f"Nation(nation_name={self.nation_name})"

        def exists(self) -> bool:
            """
            Checks if nation exists.
            """
            url = url_manager.generate_shards_url("nation",
                                                  None,
                                                  None,
                                                  nation_name=self.nation_name)
            status_code: int = wrapper.connection_status_code(url)
            match status_code:
                case 200:
                    return True
                case 404:
                    return False
                case _:
                    raise HTTPError(status_code)

        # DEPRECATED METHOD
        def get_public_shards(self, shards: Optional[str | tuple[str] | list[str]] = None, **kwargs) -> dict:
            """
            # THIS METHOD IS DEPRECATED
            ## Use ```get_shards()``` instead!
            
            ***
            
            Gets one or more shards from the requested nation, returns the standard API if no shards provided.
            
            ### Standard:
            
            > A compendium of the most commonly sought information.
            
            ### Shards:
            > If you don't need most of this data, please use shards instead. Shards allow you to request
            > exactly what you want and can be used to request data not available from the Standard API!
            """
            for kwarg in kwargs:
                kwargs[kwarg] = join_keys(kwargs[kwarg])
            params: Optional[str] = join_keys([f"{kwarg}={kwargs[kwarg]}" for kwarg in kwargs], ";") if kwargs else None
            url: str = url_manager.generate_shards_url("nation",
                                                       shards,
                                                       params,
                                                       nation_name=self.nation_name)
            logger.warning("get_public_shards() is deprecated.")
            response: dict = wrapper.fetch_api_data(url)
            return response

        # Replacing get_public_shards()
        def get_shards(self, shards: Optional[str | tuple[str] | list[str]] = None, **kwargs) -> dict:
            """
            Gets one or more shards from the requested nation, returns the standard API if no shards provided.
            
            ### Standard:
            
            > A compendium of the most commonly sought information.
            
            ### Shards:
            > If you don't need most of this data, please use shards instead. Shards allow you to request
            > exactly what you want and can be used to request data not available from the Standard API!
            """
            for kwarg in kwargs:
                kwargs[kwarg] = join_keys(kwargs[kwarg])
            params: Optional[str] = join_keys([f"{kwarg}={kwargs[kwarg]}" for kwarg in kwargs], ";") if kwargs else None
            url: str = url_manager.generate_shards_url("nation",
                                                       shards,
                                                       params,
                                                       nation_name=self.nation_name)
            response: dict = wrapper.fetch_api_data(url)
            return response

    class Region: 
        """
        Class dedicated to NationStates region API.
        """
        def __init__(self, region_name: str) -> None:
            # self.pretty_name: str = prettify_string(str(region_name))
            self.region_name = format_key(region_name, False, '%20')
        
        def __repr__(self):
            return f"Region(region_name={self.region_name})"
        
        def exists(self) -> bool:
            """
            Checks if region exists.
            """
            url = url_manager.generate_shards_url("region",
                                                  None,
                                                  None,
                                                  region_name=self.region_name)
            status_code: int = wrapper.connection_status_code(url)
            match status_code:
                case 200:
                    return True
                case 404:
                    return False
                case _:
                    raise HTTPError(status_code)

        def get_shards(self, shards: Optional[str | tuple[str] | list[str]] = None, **kwargs) -> dict:
            """
            Gets one or more shards from the requested region, returns the standard API if no shards provided.
            
            ### Standard:
            
            A compendium of the most commonly sought information.
            
            ### Shards:
            If you don't need most of this data, please use shards instead. Shards allow you to request exactly what you want and can be used to request data not available from the Standard API!
            """
            for kwarg in kwargs:
                kwargs[kwarg] = join_keys(kwargs[kwarg])
            params: Optional[str] = join_keys([f"{kwarg}={kwargs[kwarg]}" for kwarg in kwargs], ";") if kwargs else None
            url: str = url_manager.generate_shards_url("region",
                                                       shards,
                                                       params,
                                                       region_name=self.region_name)
            response: dict = wrapper.fetch_api_data(url)
            return response

if __name__ == "__main__":
    api = AwesomeNations("AwesomeNations/Test", log_level=0)
    print(api)
    print(api.Nation("testlandia").get_public_shards("name"))
    print(api.Region("the pacific"))