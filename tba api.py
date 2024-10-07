from __future__ import print_function

import time
import tbaapiv3client
from tbaapiv3client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://www.thebluealliance.com/api/v3
# See configuration.py for a list of all supported configuration parameters.
configuration = tbaapiv3client.Configuration(
    host="https://www.thebluealliance.com/api/v3"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration = tbaapiv3client.Configuration(
    host="https://www.thebluealliance.com/api/v3",
    api_key={
        'X-TBA-Auth-Key': '8xnOPBtV3yQxLNOgLWciKJI946VjkoqrKH2HkGnZerFwqhVZhcCkXrYtlXIKbYKd'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TBA-Auth-Key'] = 'Bearer'


# Enter a context with an instance of the API client
with tbaapiv3client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tbaapiv3client.TBAApi(api_client)
    if_modified_since = 'if_modified_since_example'  # str | Value of the `Last-Modified` header in the most recently cached response by the client. (optional)

    try:
        api_response = api_instance.get_status(if_modified_since=if_modified_since)
        print(api_response)
    except ApiException as e:
        print("Exception when calling TBAApi->get_status: %s\n" % e)
