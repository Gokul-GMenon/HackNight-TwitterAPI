from builtins import print
from calendar import prcal


def call(name):
    import requests
    import os
    import json

    # To set your enviornment variables in your terminal run the following line:
    # export 'BEARER_TOKEN'='<your_bearer_token>'
    # bearer_token = os.environ.get("BEARER_TOKEN")
    with open("api_calls/token.txt") as f:
        bearer_token = f.readline() 
    bearer_token = bearer_token[:-1]

    # name = ''

    def create_url():
        # Specify the usernames that you want to lookup below
        # You can enter up to 100 comma-separated values.
        usernames = "usernames=" + name
        user_fields = "user.fields=description,created_at,id"
        # User fields are adjustable, options include:
        # created_at, description, entities, id, location, name,
        # pinned_tweet_id, profile_image_url, protected,
        # public_metrics, url, username, verified, and withheld
        url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
        return url


    def bearer_oauth(r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2UserLookupPython"
        return r


    def connect_to_endpoint(url):
        response = requests.request("GET", url, auth=bearer_oauth,)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()


    # def main():
    url = create_url()
    json_response = connect_to_endpoint(url)
    return json.dumps(json_response, indent=4, sort_keys=True)

# print(call(")
