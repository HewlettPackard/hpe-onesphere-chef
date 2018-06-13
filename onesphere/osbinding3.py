# (C) Copyright 2018 Hewlett Packard Enterprise Development LP.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# onesphere/osbinding3.py

import requests
import json


# Module level decorators

def notimplementedyet(func):
    def new_func(*args):
        msg = func.__name__ + " is not implemented yet."
        print(msg)
        return msg
    return new_func

def stringnotempty(arguments):
    def check_wrapper(func):
        def check_args(*args, **kwargs):
            code = func.__code__
            names = list(code.co_varnames[:code.co_argcount])
            print(names)
            print(args)
            for argument in arguments:
                num = names.index(argument)
                value = args[num]
                #if isinstance(value, str) and value.strip(): # not change user's input
                if isinstance(value, str) and value:
                    return func(*args, **kwargs)
                else:
                    raise Exception(argument + " should be a non-empty string.")
        return check_args
    return check_wrapper


# Class OSClient

class OSClient:

    URI_ACCOUNT                     = "/account"
    URI_APPLIANCES                  = "/appliances"
    URI_CATALOG_TYPES               = "/catalog-types"
    URI_CATALOGS                    = "/catalogs"
    URI_CONNECT_APP                 = "/connect-app"
    URI_DEPLOYMENTS                 = "/deployments"
    URI_EVENTS                      = "/events"
    URI_KEYPAIRS                    = "/keypairs"
    URI_MEMBERSHIP_ROLES            = "/membership-roles"
    URI_MEMBERSHIPS                 = "/memberships"
    URI_METRICS                     = "/metrics"
    URI_NETWORKS                    = "/networks"
    URI_PASSWORD_RESET              = "/password-reset"
    URI_PROJECTS                    = "/projects"
    URI_PROVIDER_TYPES              = "/provider-types"
    URI_PROVIDERS                   = "/providers"
    URI_RATES                       = "/rates"
    URI_REGIONS                     = "/regions"
    URI_ROLES                       = "/roles"
    URI_SERVICE_TYPES               = "/service-types"
    URI_SERVICES                    = "/services"
    URI_SESSION                     = "/session"
    URI_SESSION_IDP                 = "/session/idp"
    URI_STATUS                      = "/status"
    URI_TAG_KEYS                    = "/tag-keys"
    URI_TAGS                        = "/tags"
    URI_USERS                       = "/users"
    URI_VIRTUAL_MACHINE_PROFILES    = "/virtual-machine-profiles"
    URI_VOLUMES                     = "/volumes"
    URI_WORKSPACES                  = "/workspaces"
    URI_ZONE_TYPES                  = "/zone-types"
    URI_ZONES                       = "/zones"

    HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def __init__(self, host_url, username, password):
        self.host_url = host_url
        self.rest_prefix = host_url + "/rest"
        self.username = username
        self.password = password
        self.Connect()

    def __del__(self):
        # raising exception in the destructor will be ignored
        # raise Exception("raising exception in OSClient destructor")
        #pass
        self.Disconnect()

    def Connect(self):
        full_url = self.rest_prefix + OSClient.URI_SESSION
        data = {'userName': self.username, 'password': self.password}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        r_json = r.json()
        if r.status_code != 200:
            raise Exception(r_json["message"])
        else:
            self.token = r_json["token"]
            self.user_uri = r_json["userUri"]
            OSClient.HEADERS["Authorization"] = r_json["token"]

    def Disconnect(self):
        full_url = self.rest_prefix + OSClient.URI_SESSION
        r = requests.delete(full_url, headers=OSClient.HEADERS)

    # Account APIs

    @notimplementedyet
    def GetAccount(self, view="full"):
        full_url = self.rest_prefix + OSClient.URI_ACCOUNT
        params = {"view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # Appliances APIs

    def GetAppliances(self, name="", region_uri=""):
        full_url = self.rest_prefix + OSClient.URI_APPLIANCES
        params = {}
        if name.strip():
            params["name"] = name
        if region_uri.strip():
            params["regionUri"] = region_uri
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    def CreateAppliance(self, ep_address, ep_username, ep_password,
                        name, region_uri, appliance_type):
        full_url = self.rest_prefix + OSClient.URI_APPLIANCES
        end_point = {"address": ep_address,
                     "password": ep_password,
                     "username": ep_username}
        data={"endpoint": end_point,
              "name": name,
              "regionUri": region_uri,
              "type": appliance_type}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['appliance_id'])
    def GetAppliance(self, appliance_id):
        full_url = self.rest_prefix + OSClient.URI_APPLIANCES + "/" + appliance_id
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    @stringnotempty(['appliance_id'])
    def DeleteAppliance(self, appliance_id):
        full_url = self.rest_prefix + OSClient.URI_APPLIANCES + "/" + appliance_id
        r = requests.delete(full_url, headers=OSClient.HEADERS)
        return r.json()

    # info_array: [{op, path, value}]
    # op: "replace|remove"
    @stringnotempty(['appliance_id'])
    def UpdateAppliance(self, appliance_id, info_array):
        if (len(info_array) == 0):
            raise Exception("info_array should be a non-empty array.")
        try:
            json.loads(info_array)
        except ValueError:
            raise Exception("info_array should be in JSON format.")
        full_url = self.rest_prefix + OSClient.URI_APPLIANCES + "/" + appliance_id
        r = requests.put(full_url, headers=OSClient.HEADERS, json=info_array)
        return r.json()

    # Catalog Types APIs

    def GetCatalogTypes(self):
        full_url = self.rest_prefix + OSClient.URI_CATALOG_TYPES
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Catalogs APIs

    # view: "full" - return related content
    def GetCatalogs(self, user_query="", view=""):
        full_url = self.rest_prefix + OSClient.URI_CATALOGS
        params = {}
        if user_query.strip():
            params["userQuery"] = user_query.strip()
        if view.strip():
            params["view"] = view.strip()
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['access_key', 'catalog_type_uri', 'name', 'password', 'region_name', 'secret_key', 'url', 'username'])
    def CreateCatalog(self, access_key, catalog_type_uri, name, password, region_name, secret_key, url, username):
        full_url = self.rest_prefix + OSClient.URI_CATALOGS
        data = {"accessKey": access_key,
                "catalogTypeUri": catalog_type_uri,
                "name": name,
                "password": password,
                "regionName": region_name,
                "secretKey": secret_key,
                "url": url,
                "username": username}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['catalog_id'])
    def GetCatalog(self, catalog_id, view):
        full_url = self.rest_prefix + OSClient.URI_CATALOGS + "/" + catalog_id
        params = {"view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @notimplementedyet
    @stringnotempty(['catalog_id'])
    def DeleteCatalog(self, catalog_id):
        full_url = self.rest_prefix + OSClient.URI_CATALOGS + "/" + catalog_id
        r = requests.delete(full_url, headers=OSClient.HEADERS)
        return r.json()

    @stringnotempty(['catalog_id', 'name', 'password', 'access_key', 'secret_key', 'region_name', 'state'])
    def UpdateCatalog(self, catalog_id, name, password, access_key, secret_key, region_name, state):
        full_url = self.rest_prefix + OSClient.URI_CATALOGS + "/" + catalog_id
        data = {"name": name, "password": password, "accessKey": access_key,
                "secretKey": secret_key, "regionName": region_name, "state": state}
        r = requests.put(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    # Connect App APIs

    # os: windows or mac
    @stringnotempty(['os'])
    def GetConnectApp(self, os="windows"):
        full_url = self.rest_prefix + OSClient.URI_CONNECT_APP
        params = {"os": os}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # Deployments APIs

    # view: "full" - get related resources of zone, service and volume details.
    def GetDeployments(self, query="", user_query="", view=""):
        full_url = self.rest_prefix + OSClient.URI_DEPLOYMENTS
        params = {}
        if query.strip():
            params["query"] = query
        if user_query.strip():
            params["userQuery"] = user_query
        if view.strip():
            params["view"] = view
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    def CreateDeployment(self, info):
        full_url = self.rest_prefix + OSClient.URI_DEPLOYMENTS
        r = requests.post(full_url, headers=OSClient.HEADERS, json=info)
        return r

    @stringnotempty(['deployment_id'])
    def GetDeployment(self, deployment_id, view="full"):
        full_url = self.rest_prefix + OSClient.URI_DEPLOYMENTS + "/" + deployment_id
        params = {"view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['deployment_id'])
    def UpdateDeployment(self, deployment_id, info):
        try:
            json.loads(info)
        except ValueError:
            raise Exception("info should be in JSON format.")
        full_url = self.rest_prefix + OSClient.URI_DEPLOYMENTS + "/" + deployment_id
        r = requests.put(full_url, headers=OSClient.HEADERS, json=info)
        return r.json()

    @stringnotempty(['deployment_id'])
    def DeleteDeployment(self, deployment_id):
        full_url = self.rest_prefix + OSClient.URI_DEPLOYMENTS + "/" + deployment_id
        r = requests.delete(full_url, headers=OSClient.HEADERS)
        return r.json()

    # action_type: one of restart|resume|start|stop|suspend.
    @stringnotempty(['deployment_id', 'action_type'])
    def ActionOnDeployment(self, deployment_id, action_type, force=True):
        if action_type not in ["restart", "resume", "start", "stop", "suspend"]:
            raise Exception("action type must be one of restart|resume|start|stop|suspend.")
        full_url = self.rest_prefix + OSClient.URI_DEPLOYMENTS + "/" + deployment_id + "/actions"
        data = {"force": force, "type": action_type}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['deployment_id'])
    def GetDeploymentConsole(self, deployment_id):
        full_url = self.rest_prefix + OSClient.URI_DEPLOYMENTS + "/" + deployment_id + "/console"
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Events APIs

    @notimplementedyet
    def GetEvents(self, resource_uri):
        full_url = self.rest_prefix + OSClient.URI_EVENTS
        params = {"resourceUri": resource_uri}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # Keypairs APIs

    @stringnotempty(['region_uri', 'project_uri'])
    def GetKeyPair(self, region_uri, project_uri):
        full_url = self.rest_prefix + OSClient.URI_KEYPAIRS
        params = {"regionUri": region_uri, "projectUri": project_uri}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # Membership Roles APIs

    def GetMembershipRoles(self):
        full_url = self.rest_prefix + OSClient.URI_MEMBERSHIP_ROLES
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Memberships APIs

    @stringnotempty(['query'])
    def GetMemberships(self, query):
        full_url = self.rest_prefix + OSClient.URI_MEMBERSHIPS
        params = {"query": query}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['user_uri, role_uri, project_uri'])
    def CreateMembership(self, user_uri, role_uri, project_uri):
        full_url = self.rest_prefix + OSClient.URI_MEMBERSHIPS
        data = {"userUri": user_uri, "membershipRoleUri": role_uri, "projectUri": project_uri}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['user_uri, role_uri, project_uri'])
    def DeleteMembership(self, user_uri, role_uri, workspace_uri):
        full_url = self.rest_prefix + OSClient.URI_MEMBERSHIPS
        data = {"userUri": user_uri, "membershipRoleUri": role_uri, "projectUri": project_uri}
        r = requests.delete(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    # Metrics APIs

    def GetMetrics(self, resource_uri, category, group_by, query, name,
                   period_start, period, period_count, view, start, count):
        full_url = self.rest_prefix + OSClient.URI_METRICS
        params = {"resourceUri": resource_uri,
                "category": category,
                "groupBy": group_by,
                "query": query,
                "name": name,
                "periodStart": period_start,
                "period": period,
                "periodCount": period_count,
                "view": view,
                "start": start,
                "count": count}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # Networks APIs

    def GetNetworks(self, query):
        full_url = self.rest_prefix + OSClient.URI_NETWORKS
        params = {"query": query}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['network_id'])
    def GetNetwork(self, network_id):
        full_url = self.rest_prefix + OSClient.URI_NETWORKS + "/" + network_id
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # info_array: [{op, path, value}]
    @stringnotempty(['network_id'])
    def UpdateNetwork(self, network_id, info_array):
        if (len(info_array) == 0):
            raise Exception("info_array should be a non-empty array.")
        try:
            json.loads(info_array)
        except ValueError:
            raise Exception("info_array should be in JSON format.")
        full_url = self.rest_prefix + OSClient.URI_NETWORKS + "/" + network_id
        r = requests.put(full_url, headers=OSClient.HEADERS, json=info_array)
        return r.json()

    # Password Reset APIs

    @stringnotempty(['email'])
    def ResetSingleUsePassword(email):
        full_url = self.rest_prefix + OSClient.URI_PASSWORD_RESET
        data = {"email": email}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['password', 'token'])
    def ChangePassword(password, token):
        full_url = self.rest_prefix + OSClient.URI_PASSWORD_RESET + "/change"
        data = {"password": password, "token": token}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    # Projects APIs

    # view: "full" - return related content
    def GetProjects(self, user_query="", view=""):
        full_url = self.rest_prefix + OSClient.URI_PROJECTS
        params = {}
        if user_query.strip():
            params["userQuery"] = user_query.strip()
        if view.strip():
            params["view"] = view.strip()
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['name', 'description', 'tag_uris'])
    def CreateProject(self, name, description, tag_uris):
        full_url = self.rest_prefix + OSClient.URI_PROJECTS
        data = {"name": name,
                "description": description,
                "tagUris": tag_uris}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['project_id'])
    def GetProject(self, project_id, view):
        full_url = self.rest_prefix + OSClient.URI_PROJECTS + "/" + project_id
        params = {"view", view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @notimplementedyet
    @stringnotempty(['project_id'])
    def DeleteProject(self, project_id):
        full_url = self.rest_prefix + OSClient.URI_PROJECTS + "/" + project_id
        r = requests.delete(full_url, headers=OSClient.HEADERS)
        return r.json()

    @stringnotempty(['project_id', 'name', 'description', 'tag_uris'])
    def UpdateProject(self, project_id, name, description, tag_uris):
        full_url = self.rest_prefix + OSClient.URI_PROJECTS + "/" + project_id
        data = {"name": name,
                "description": description,
                "tagUris": tag_uris}
        r = requests.put(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    # Provider Types APIs

    def GetProviderTypes(self):
        full_url = self.rest_prefix + OSClient.URI_PROVIDER_TYPES
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Providers APIs

    # query supports providerTypeUri and projectUri
    def GetProviders(self, query=""):
        full_url = self.rest_prefix + OSClient.URI_PROVIDERS
        params = {"query": query}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # payment_provider: True|False
    # state: "Enabled|Disabled"
    @stringnotempty(['provider_id', 'provider_type_uri',
                     'access_key', 'secret_key',
                     'payment_provider', 's3_cost_bucket',
                     'master_uri', 'state'])
    def CreateProvider(self, provider_id, provider_type_uri,
                       access_key, secret_key,
                       payment_provider, s3_cost_bucket,
                       master_uri, state):
        full_url = self.rest_prefix + OSClient.URI_PROVIDERS
        data={"id": provider_id,
              "providerTypeUri": provider_type_uri,
              "accessKey": access_key,
              "secretKey": secret_key,
              "paymentProvider": payment_provider,
              "s3CostBucket": s3_cost_bucket,
              "masterUri": master_uri,
              "state": state}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['provider_id'])
    def GetProvider(self, provider_id, view="full", discover=False):
        full_url = self.rest_prefix + OSClient.URI_PROVIDERS + "/" + provider_id
        params={"view": view, "discover": discover}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['provider_id'])
    def DeleteProvider(self, provider_id):
        full_url = self.rest_prefix + OSClient.URI_PROVIDERS + "/" + provider_id
        r = requests.delete(full_url, headers=OSClient.HEADERS)
        return r.json()

    # info_array: [{op, path, value}]
    # op: "add|replace|remove"
    @stringnotempty(['provider_id'])
    def UpdateProvider(self, provider_id, info_array):
        if (len(info_array) == 0):
            raise Exception("info_array should be a non-empty array.")
        try:
            json.loads(info_array)
        except ValueError:
            raise Exception("info_array should be in JSON format.")
        full_url = self.rest_prefix + OSClient.URI_PROVIDERS + "/" + provider_id
        r = requests.put(full_url, headers=OSClient.HEADERS, json=info_array)
        return r.json()

    # Rates APIs

    # resource_uri: "default" - skeleton set of the default rates
    # active: boolean
    # start: integer
    # count: integer
    def GetRates(self, resource_uri="",
                 effective_for_date="", effective_date="",
                 metric_name="", active=True,
                 start=0, count=0):
        full_url = self.rest_prefix + OSClient.URI_RATES
        params = {"effectiveForDate": effective_for_date,
                  "effectiveDate": effective_date,
                  "metricName": metric_name,
                  "active": active}
        if resource_uri.strip():
            params["resourceUri"] = resource_uri.strip()
        if start > 0:
            params["start"] = start
        if count > 0:
            params["count"] = count
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['rate_id'])
    def GetRate(self, rate_id):
        full_url = self.rest_prefix + OSClient.URI_RATES + "/" + rate_id
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Regions APIs

    def GetRegions(self, query="", view=""):
        full_url = self.rest_prefix + OSClient.URI_REGIONS
        params={"query": query, "view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['name', 'provider_uri', 'loc_latitude', 'loc_longitude'])
    def CreateRegion(self, name, provider_uri, loc_latitude, loc_longitude):
        full_url = self.rest_prefix + OSClient.URI_REGIONS
        data = {"name": name,
                "providerUri": provider_uri,
                "location": {
                    "latitude": loc_latitude,
                    "longitude": loc_longitude}}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['region_id'])
    def GetRegion(self, region_id, view, discover=True):
        full_url = self.rest_prefix + OSClient.URI_REGIONS + "/" + region_id
        params = {"view": view, "discover": discover}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['region_id'])
    def DeleteRegion(self, region_id, force=False):
        full_url = self.rest_prefix + OSClient.URI_REGIONS + "/" + region_id
        params = {"force": force}
        r = requests.delete(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # info_array: [{op, path, value}]
    # op: "add|replace"
    # path: "/name|/location"
    @stringnotempty(['region_id'])
    def PatchRegion(self, region_id, info_array):
        if (len(info_array) == 0):
            raise Exception("info_array should be a non-empty array.")
        try:
            json.loads(info_array)
        except ValueError:
            raise Exception("info_array should be in JSON format.")
        full_url = self.rest_prefix + OSClient.URI_REGIONS + "/" + region_id
        r = requests.put(full_url, headers=OSClient.HEADERS, json=info_array)
        return r.json()

    @notimplementedyet
    @stringnotempty(['region_id'])
    def UpdateRegion(self, region_id, region):
        try:
            json.loads(region)
        except ValueError:
            raise Exception("region should be in JSON format.")
        full_url = self.rest_prefix + OSClient.URI_REGIONS + "/" + region_id
        r = requests.put(full_url, headers=OSClient.HEADERS, json=region)
        return r.json()

    @stringnotempty(['region_id'])
    def GetRegionConnection(self, region_id):
        full_url = self.rest_prefix + OSClient.URI_REGIONS + "/" + region_id + "/connection"
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # state: "Enabling|Enabled|Disabling|Disabled"
    @stringnotempty(['region_id', 'endpoint_uuid', 'name',
                     'loc_ipaddress', 'loc_username', 'loc_password', 'loc_port',
                     'state', 'uri'])
    def CreateRegionConnection(self, region_id, endpoint_uuid, name,
                               loc_ipaddress, loc_username, loc_password, loc_port,
                               state, uri):
        full_url = self.rest_prefix + OSClient.URI_REGIONS + "/" + region_id + "/connection"
        data = {"endpointUuid": endpoint_uuid,
                "name": name,
                "location": {
                    "ipAddress": loc_ipaddress,
                    "username": loc_username,
                    "password": loc_password,
                    "port": loc_port},
                "state": state,
                "uri": uri}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['region_id'])
    def DeleteRegionConnection(self, region_id):
        full_url = self.rest_prefix + OSClient.URI_REGIONS + "/" + region_id + "/connection"
        r = requests.delete(full_url, headers=OSClient.HEADERS)
        return r.json()

    @stringnotempty(['region_id'])
    def GetRegionConnectorImage(self, region_id):
        full_url = self.rest_prefix + OSClient.URI_REGIONS + "/" + region_id + "/connector-image"
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Roles APIs

    def GetRoles(self):
        full_url = self.rest_prefix + OSClient.URI_ROLES
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Service Types APIs

    def GetServiceTypes(self):
        full_url = self.rest_prefix + OSClient.URI_SERVICE_TYPES
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    @stringnotempty(['service_type_id'])
    def GetServiceType(self, service_type_id):
        full_url = self.rest_prefix + OSClient.URI_SERVICE_TYPES + "/" + service_type_id
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Services APIs

    # view: full
    def GetServices(self, query="", user_query="", view="full"):
        full_url = self.rest_prefix + OSClient.URI_SERVICES
        params = {"query": query, "userQuery": user_query, "view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # view: "full|deployment"
    @stringnotempty(['service_id'])
    def GetService(self, service_id, view="full"):
        full_url = self.rest_prefix + OSClient.URI_SERVICES + "/" + service_id
        params = {"view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # Session APIs

    def GetSession(self, view="full"):
        full_url = self.rest_prefix + OSClient.URI_SESSION
        params = {"view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @notimplementedyet
    @stringnotempty(['user_name'])
    def GetSessionIdp(self, user_name):
        full_url = self.rest_prefix + OSClient.URI_SESSION_IDP
        params = {"userName": user_name}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # Status APIs

    def GetStatus(self):
        full_url = self.rest_prefix + OSClient.URI_STATUS
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Tag Keys APIs

    # view: "full"
    def GetTagKeys(self, view="full"):
        full_url = self.rest_prefix + OSClient.URI_TAG_KEYS
        params = {"view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['name'])
    def CreateTagKey(self, name):
        full_url = self.rest_prefix + OSClient.URI_TAG_KEYS
        data = {"name": name}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    # view: "full"
    @stringnotempty(['tag_key_id'])
    def GetTagKey(self, tag_key_id, view="full"):
        full_url = self.rest_prefix + OSClient.URI_TAG_KEYS + "/" + tag_key_id
        params = {"view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['tag_key_id'])
    def DeleteTagKey(self, tag_key_id):
        full_url = self.rest_prefix + OSClient.URI_TAG_KEYS + "/" + tag_key_id
        r = requests.delete(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Tags APIs

    # view: "full"
    def GetTags(self, view="full"):
        full_url = self.rest_prefix + OSClient.URI_TAGS
        params = {"view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['name', 'tag_key_uri'])
    def CreateTag(self, name, tag_key_uri):
        full_url = self.rest_prefix + OSClient.URI_TAGS
        data = {"name": name, "tagKeyUri": tag_key_uri}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    # view: "full"
    @stringnotempty(['tag_id'])
    def GetTag(self, tag_id, view="full"):
        full_url = self.rest_prefix + OSClient.URI_TAGS + "/" + tag_id
        params = {"view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['tag_id'])
    def DeleteTag(self, tag_id):
        full_url = self.rest_prefix + OSClient.URI_TAGS + "/" + tag_id
        r = requests.delete(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Users APIs

    def GetUsers(self, user_query=""):
        full_url = self.rest_prefix + OSClient.URI_USERS
        params = {"userQuery": user_query}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # role: "administrator|analyst|consumer|project-creator"
    @stringnotempty(['email', 'name', 'password', 'role'])
    def CreateUser(self, email, name, password, role):
        full_url = self.rest_prefix + OSClient.URI_USERS
        data = {"email": email, "name": name, "password": password, "role": role}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['user_id'])
    def GetUser(self, user_id):
        full_url = self.rest_prefix + OSClient.URI_USERS + "/" + user_id
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # role: "administrator|analyst|consumer|project-creator"
    @stringnotempty(['user_id', 'email', 'name', 'password', 'role'])
    def UpdateUser(self, user_id, email, name, password, role):
        full_url = self.rest_prefix + OSClient.URI_USERS + "/" + user_id
        data = {"email": email, "name": name, "password": password, "role": role}
        r = requests.put(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['user_id'])
    def DeleteUser(self, user_id):
        full_url = self.rest_prefix + OSClient.URI_USERS + "/" + user_id
        r = requests.delete(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Virtual Machine Profiles APIs

    def GetVirtualMachineProfiles(self, zone_uri="", service_uri=""):
        full_url = self.rest_prefix + OSClient.URI_VIRTUAL_MACHINE_PROFILES
        params = {"zoneUri": zone_uri, "serviceUri": service_uri}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    @stringnotempty(['vm_profile_id'])
    def GetVirtualMachineProfile(self, vm_profile_id):
        full_url = self.rest_prefix + OSClient.URI_VIRTUAL_MACHINE_PROFILES + "/" + vm_profile_id
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Volumes APIs

    # view: "full"
    def GetVolumes(self, query="", view="full"):
        full_url = self.rest_prefix + OSClient.URI_VOLUMES
        params = {"query": query, "view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    def CreateVolume(self, name, size_gib, zone_uri, project_uri):
        full_url = self.rest_prefix + OSClient.URI_VOLUMES
        data = {"name": name, "sizeGiB": size_gib, "zoneUri": zone_uri, "projectUri": project_uri}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['volume_id'])
    def GetVolume(self, volume_id):
        full_url = self.rest_prefix + OSClient.URI_VOLUMES + "/" + volume_id
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    @stringnotempty(['volume_id'])
    def UpdateVolume(self, volume_id, name, size_gib):
        full_url = self.rest_prefix + OSClient.URI_VOLUMES + "/" + volume_id
        data = {"name": name, "sizeGiB": size_gib}
        r = requests.put(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['volume_id'])
    def DeleteVolume(self, volume_id):
        full_url = self.rest_prefix + OSClient.URI_VOLUMES + "/" + volume_id
        r = requests.delete(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Zone Types APIs

    def GetZoneTypes(self):
        full_url = self.rest_prefix + OSClient.URI_ZONE_TYPES
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    def GetZoneTypeResourceProfiles(self, zone_type_id):
        full_url = self.rest_prefix + OSClient.URI_ZONE_TYPES + "/" + zone_type_id + "resource-profiles"
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    # Zones APIs

    def GetZones(self, query="", region_uri="", appliance_uri=""):
        full_url = self.rest_prefix + OSClient.URI_ZONES
        params = {"query": query, "regionUri": region_uri, "applianceUri": appliance_uri}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    def CreateZone(self, zone_data):
        full_url = self.rest_prefix + OSClient.URI_ZONES
        try:
            json.loads(zone_data)
        except ValueError:
            raise Exception("zone_data should be in JSON format.")
        r = requests.post(full_url, headers=OSClient.HEADERS, json=zone_data)
        return r.json()

    # view: "full"
    @stringnotempty(['zone_id'])
    def GetZone(self, zone_id, view="full"):
        full_url = self.rest_prefix + OSClient.URI_ZONES + "/" + zone_id
        params = {"view": view}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # op: "add|replace|remove"
    @stringnotempty(['zone_id'])
    def UpdateZone(self, zone_id, op, path, value):
        full_url = self.rest_prefix + OSClient.URI_ZONES + "/" + zone_id
        data = {"op": op, "path": path, "value": value}
        r = requests.put(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['zone_id'])
    def DeleteZone(self, zone_id, force=True):
        full_url = self.rest_prefix + OSClient.URI_ZONES + "/" + zone_id
        params = {"force": force}
        r = requests.delete(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # action_type: "reset|add-capacity|reduce-capacity"
    # resource_type: "compute|storage"
    @stringnotempty(['zone_id'])
    def ActionOnZone(self, zone_id, action_type, resource_type, resource_capacity):
        full_url = self.rest_prefix + OSClient.URI_ZONES + "/" + zone_id + "/actions"
        data = {"type": action_type,
                "resourceOps": {
                    "resourceType": resource_type,
                    "resourceCapacity": resource_capacity}}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['zone_id'])
    def GetZoneApplianceImage(self, zone_id):
        full_url = self.rest_prefix + OSClient.URI_ZONES + "/" + zone_id + "/appliance-image"
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    @stringnotempty(['zone_id'])
    def GetZoneTaskStatus(self, zone_id):
        full_url = self.rest_prefix + OSClient.URI_ZONES + "/" + zone_id + "/task-status"
        r = requests.get(full_url, headers=OSClient.HEADERS)
        return r.json()

    @stringnotempty(['zone_id', 'uuid'])
    def GetZoneConnections(self, zone_id, uuid):
        full_url = self.rest_prefix + OSClient.URI_ZONES + "/" + zone_id + "/connections"
        params = {"uuid": uuid}
        r = requests.get(full_url, headers=OSClient.HEADERS, params=params)
        return r.json()

    # state: "Enabling|Enabled|Disabling|Disabled"
    @stringnotempty(['zone_id'])
    def CreateZoneConnection(self, zone_id, uuid, name, ip_address, username, password, port, state):
        full_url = self.rest_prefix + OSClient.URI_ZONES + "/" + zone_id + "/connections"
        data = {"uuid": uuid,
                "name": name,
                "location": {
                    "ipAddress": ip_address,
                    "username": username,
                    "password": password,
                    "port": port},
                "state": state}
        r = requests.post(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

    @stringnotempty(['zone_id', 'uuid'])
    def DeleteZoneConnection(self, zone_id, uuid):
        full_url = self.rest_prefix + OSClient.URI_ZONES + "/" + zone_id + "/connections/" + uuid
        r = requests.delete(full_url, headers=OSClient.HEADERS)
        return r.json()

    # op: "add|replace|remove"
    @stringnotempty(['zone_id'])
    def UpdateZoneConnection(self, zone_id, uuid, op, path, value):
        full_url = self.rest_prefix + OSClient.URI_ZONES + "/" + zone_id + "/connections/" + uuid
        data = {"op": op, "path": path, "value": value}
        r = requests.put(full_url, headers=OSClient.HEADERS, json=data)
        return r.json()

