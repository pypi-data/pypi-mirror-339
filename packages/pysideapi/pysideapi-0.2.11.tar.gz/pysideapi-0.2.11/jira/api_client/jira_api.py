import concurrent.futures
import json
import math
import os
import urllib.parse

import requests

from jira.api_client.jira_session import get_basic_session
from jira.commons.constants import Constants


def get_response(self, url):
    try:
        response = self.session.get(url, timeout=30)
    except:
        print("Error al conectar a Jira")

    return json.loads(response.text)


class JiraApi:
    def __init__(self, username=None, token=None, proxy=False, max_result=100):
        self.server = Constants.JIRA_SERVER
        self.api_session = Constants.JIRA_API_SESSION
        self.jql_base_url = Constants.JIRA_API_JQL
        self.max_result = max_result
        self.session = get_basic_session(self.api_session, username, token, proxy)
        self.num_cores = os.cpu_count()
        print("Total cores: ", self.num_cores)
    
    def get_team_backlog_id(self, max_results=1000):
        jql = 'project = GTAAS20 AND issuetype = "Gtaas Team Backlog" AND Geography = Peru'
        encoded_jql = requests.utils.quote(jql)
        start_at = 0
        all_issues = []

        while True:
            url = f"https://jira.globaldevtools.bbva.com/rest/api/2/search?jql={encoded_jql}&fields=id,summary&startAt={start_at}&maxResults={max_results}"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            issues = data.get('issues', [])
            if not issues:
                break
            all_issues.extend(issues)
            start_at += max_results

        issues_list = [
            {'team_backlog_id': issue['id'], 'team_backlog_name': issue['fields']['summary']}
            for issue in all_issues if 'id' in issue and 'fields' in issue and 'summary' in issue['fields']
            ]

        return issues_list

    def _get_response(self, url):
        try:
            response = self.session.get(url, timeout=30)
            return json.loads(response.text)
        except Exception as e:
            print(f"Ha ocurrido un error en la clase _get_response, motivo : {e}")


    def __get_all_data_by_jql(self, query, start_at=0):
        jql_final = f"{query}&startAt={start_at}&maxResults={self.max_result}"

        data_current = get_response(self, jql_final)
        start_at_req = data_current["startAt"]
        max_result_req = data_current["maxResults"]
        total_req = data_current["total"]
        data_all = data_current["issues"]

        if start_at_req + max_result_req < total_req:
            start_at_req = start_at_req + max_result_req
            data_all.extend(self.__get_all_data_by_jql(query, start_at_req))

        return data_all

    def __get_all_data_by_jql_task_old(self, query, start_at=0):
        jql_final = f"{query}&startAt={start_at}&maxResults={self.max_result}"
        print(jql_final)
        data_current = self._get_response(jql_final)
        total_req = data_current["total"]

        data_all = data_current["issues"]
        max_request = math.ceil(total_req / self.max_result)
        if max_request > 1:
            start_at_values = [page * self.max_result for page in range(1, max_request)]
            jira_urls = [f"{query}&startAt={start_at_value}&maxResults={self.max_result}" for start_at_value in
                         start_at_values]

            with concurrent.futures.ProcessPoolExecutor(max_workers=self.num_cores) as executor:
                results = list(executor.map(self._get_response, jira_urls))
            [data_all.extend(result["issues"]) for result in results if result is not None]
        return data_all

    def __get_all_data_by_jql_task(self, query, start_at=0):
        jql_final = f"{query}&startAt={start_at}&maxResults={self.max_result}"
        data_current = self._get_response(jql_final)
        total_req = data_current["total"]

        data_all = data_current["issues"]
        max_request = math.ceil(total_req / self.max_result)
        if max_request > 1:
            start_at_values = [page * self.max_result for page in range(1, max_request)]
            jira_urls = [f"{query}&startAt={start_at_value}&maxResults={self.max_result}" for start_at_value in
                         start_at_values]

            with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_cores) as executor:
                results = executor.map(self._get_response, jira_urls)

            [data_all.extend(result["issues"]) for result in results if result is not None]
        return data_all

    def get_feature_by_pi(self, pi_id):
        jql_feature = Constants.JQL_FEATURE.replace("#pi_id", pi_id)
        jql_full_feature = f"{self.jql_base_url}{urllib.parse.quote(jql_feature)}&{Constants.EXTRA_PARAMS_FEATURE}"
        response_feature = self.__get_all_data_by_jql_task(jql_full_feature)
        return response_feature

    def get_feature_data_by_pi(self, pi_id):
        jql_feature = Constants.JQL_FEATURE_DATAENG.replace("#pi_id", pi_id)
        jql_full_feature = f"{self.jql_base_url}{urllib.parse.quote(jql_feature)}&{Constants.EXTRA_PARAMS_FEATURE}"
        response_feature = self.__get_all_data_by_jql_task(jql_full_feature)
        return response_feature
    
    def get_rlb_features_by_pi(self, pi_id):
        jql_feature = Constants.JQL_RLB_DATAENG.replace("#pi_id", pi_id)
        jql_full_feature = f"{self.jql_base_url}{urllib.parse.quote(jql_feature)}&{Constants.EXTRA_PARAMS_FEATURE}"
        response_feature = self.__get_all_data_by_jql_task(jql_full_feature)
        return response_feature

    def get_feature_by_key(self, feature_id):

        jql_feature = f"key={feature_id} AND issuetype in ('Feature' , 'Task L1') "
        jql_full_feature = f"{self.jql_base_url}{urllib.parse.quote(jql_feature)}&{Constants.EXTRA_PARAMS_FEATURE}"
        print(jql_full_feature)
        response_feature = self.__get_all_data_by_jql(jql_full_feature)

        return response_feature

    def get_story_by_feature(self, feature_id):

        jql_story = f"issuetype in ('story' , 'Task L2') AND issueFunction in linkedIssuesOf(\"Key in ({feature_id})\", \"is epic of\")"
        jql_final_story = f"{self.jql_base_url}{urllib.parse.quote(jql_story)}&{Constants.EXTRA_PARAMS_STORY}"
        print(jql_final_story)
        response_story = self.__get_all_data_by_jql_task(jql_final_story)

        return response_story

    def get_story_by_key(self, story_id):
        jql_story = f"key={story_id} AND issuetype in ('story' , 'Task L2') "
        jql_final_story = f"{self.jql_base_url}{urllib.parse.quote(jql_story)}&{Constants.EXTRA_PARAMS_STORY}"
        print(jql_final_story)
        response_story = self.__get_all_data_by_jql(jql_final_story)

        return response_story

    def get_dependency_by_feature(self, feature_id):

        jql_dependency = f"issuetype = dependency AND issueFunction in linkedIssuesOf(\"Key in ({feature_id})\", \"is epic of\")"
        jql_final_dependency = f"{self.jql_base_url}{urllib.parse.quote(jql_dependency)}&{Constants.EXTRA_PARAMS_DEPENDENCY}"
        # print(jql_final_dependency)
        response_dependency = self.__get_all_data_by_jql_task(jql_final_dependency)

        return response_dependency

    def get_team_backlog(self):

        jql_team_backlog = "project%20=%20GTAAS20%20AND%20issuetype%20=%20%22Gtaas%20Team%20Backlog%22%20AND%20Geography%20=%20Peru"
        jql_final = f"{self.jql_base_url}{jql_team_backlog}"
        response_data = self.__get_all_data_by_jql(jql_final)
        return response_data


    def get_pr_mesh_by_PI(self, pi_id):

        jql_malla = f"type =Dependency AND labels = ReleaseMallasDatio AND status =DEPLOYED"
        jql_full_malla = f"{self.jql_base_url}{urllib.parse.quote(jql_malla)}&{Constants.EXTRA_PARAMS_DEPENDENCY}"
        print(jql_full_malla)
        response_malla = self.__get_all_data_by_jql(jql_full_malla)

        return response_malla

    def get_pr_code_by_pi(self, pi_id):

        jql_malla = f"type =Story AND labels = ReleasePRDatio AND status =DEPLOYED"
        jql_full_malla = f"{self.jql_base_url}{urllib.parse.quote(jql_malla)}&{Constants.EXTRA_PARAMS_DEPENDENCY}"
        print(jql_full_malla)
        response_malla = self.__get_all_data_by_jql(jql_full_malla)

        return response_malla

    def get_launchpad_by_pi(self, pi_id):

        jql_launchpad = (f"issuetype = Request AND project = DATASD AND labels IN ('8.-LAUNCHPAD_FINALIZADO') AND "
                         f"Geography = Peru")
        jql_full_launchpad = f"{self.jql_base_url}{urllib.parse.quote(jql_launchpad)}&{Constants.EXTRA_PARAMS_DEPENDENCY}"
        response_launchpad = self.__get_all_data_by_jql(jql_full_launchpad)

        return response_launchpad
