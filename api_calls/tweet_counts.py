from builtins import print


def call(name):
    import requests
    import os
    import json

    # To set your environment variables in your terminal run the following line:
    # export 'BEARER_TOKEN'='<your_bearer_token>'
    # bearer_token = os.environ.get("BEARER_TOKEN")

    with open("api_calls/token.txt") as f:
        bearer_token = f.readline() 
    bearer_token = bearer_token[:-1]

    search_url = "https://api.twitter.com/2/tweets/counts/recent"

    # Optional params: start_time,end_time,since_id,until_id,next_token,granularity

    query_params = {'query': 'from:'+name,'granularity': 'day'}


    def bearer_oauth(r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2RecentTweetCountsPython"
        return r


    def connect_to_endpoint(url, params):
        response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()


    json_response = connect_to_endpoint(search_url, query_params)
    return json.dumps(json_response, indent=4, sort_keys=True)

# print(call("_GokulGMenon_"))