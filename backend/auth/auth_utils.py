import logging
import requests


def get_authenticated_user_details(request_headers):
    user_object = {}

    ## check the headers for the Principal-Id (the guid of the signed in user)
    if "X-Ms-Client-Principal-Id" not in request_headers.keys():
        ## if it's not, assume we're in development mode and return a default user
        from . import sample_user

        raw_user_object = sample_user.sample_user
    else:
        ## if it is, get the user details from the EasyAuth headers
        raw_user_object = {k: v for k, v in request_headers.items()}

    user_object["user_principal_id"] = raw_user_object["X-Ms-Client-Principal-Id"]
    user_object["user_name"] = raw_user_object["X-Ms-Client-Principal-Name"]
    user_object["auth_provider"] = raw_user_object["X-Ms-Client-Principal-Idp"]
    user_object["auth_token"] = raw_user_object["X-Ms-Token-Aad-Id-Token"]
    user_object["client_principal_b64"] = raw_user_object["X-Ms-Client-Principal"]
    user_object["aad_id_token"] = raw_user_object["X-Ms-Token-Aad-Id-Token"]

    return user_object


def ms_graph_authorisation_check(access_token: str, site_id: str, page_id: str):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/pages/{page_id}"
    headers = {"Authorization": "Bearer " + access_token, "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    success = response.status_code == 200
    if not success:
        logging.warn(f"Failed to get page details: {response.text}")
        
    return success
