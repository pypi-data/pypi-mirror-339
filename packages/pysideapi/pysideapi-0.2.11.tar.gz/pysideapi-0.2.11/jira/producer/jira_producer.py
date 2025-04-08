from typing import List

import pandas as pd

from jira.api_client.jira_api import JiraApi
from jira.model.dependency import Dependency
from jira.model.feature import Feature
from jira.model.story import Story
from jira.model.team_backlog import TeamBacklog
from jira.utils.issue_utils import dividir_lista
from concurrent.futures import ThreadPoolExecutor, as_completed


class JiraProducer:
    def __init__(self, username=None, token=None, proxy=False, max_result=50):
        self._jira_api = JiraApi(username=username, token=token, proxy=proxy, max_result=max_result)

    def get_team_backlog_id(self):
        team_backlog_list =self._jira_api.get_team_backlog_id()
        team_backlog_df = pd.DataFrame(team_backlog_list)
        return team_backlog_df

    def get_feature_by_pi(self, pi_id) -> List[Feature]:
        json_jira = self._jira_api.get_feature_by_pi(pi_id=pi_id)
        '''
        arr_feature = []
        for feature in json_jira:
            current_feature = Feature()
            current_feature.convert_json_to_feature(feature)
            arr_feature.append(current_feature)
        '''
        arr_feature = [Feature().convert_json_to_feature(feature) for feature in json_jira]
        return arr_feature

    def get_feature_data_by_pi(self, pi_id) -> List[Feature]:
        json_jira = self._jira_api.get_feature_data_by_pi(pi_id=pi_id)

        arr_feature = [Feature().convert_json_to_feature(feature) for feature in json_jira]
        return arr_feature
    
    def get_rlb_features_by_pi(self, pi_id) -> List[Feature]:
        json_jira = self._jira_api.get_rlb_features_by_pi(pi_id=pi_id)

        arr_feature = [Feature().convert_json_to_feature(feature) for feature in json_jira]
        return arr_feature

    def get_feature_by_key(self, feature_key) -> Feature:
        json_jira = self._jira_api.get_feature_by_key(feature_id=feature_key)
        current_feature = Feature()
        if len(json_jira) > 0:
            current_feature.convert_json_to_feature(json_jira[0])
        return current_feature

    def get_story_by_features(self, feature_keys: List[str], sublist_size: int = 20) -> List[Story]:

        key_sub_list = dividir_lista(feature_keys, sublist_size)

        arr_json_jira = []
        for keys in key_sub_list:
            arr_json_jira += self._jira_api.get_story_by_feature(feature_id=keys)

        arr_story = [Story().convert_json_story(story) for story in arr_json_jira]
        return arr_story

    def get_story_by_features_task(self, feature_keys: List[str], sublist_size: int = 20) -> List[Story]:
        key_sub_list = dividir_lista(feature_keys, sublist_size)

        arr_story = []

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._jira_api.get_story_by_feature, feature_id=keys) for keys in key_sub_list]

            for future in as_completed(futures):
                arr_story.extend([Story().convert_json_story(story) for story in future.result()])

        return arr_story

    def get_story_by_feature(self, feature_key: str) -> List[Story]:

        json_jira = self._jira_api.get_story_by_feature(feature_id=feature_key)
        arr_story = []
        for story in json_jira:
            current_story = Story()
            current_story.convert_json_story(story)
            arr_story.append(current_story)
        return arr_story

    def get_story_by_key(self, story_key) -> Story:
        json_jira = self._jira_api.get_story_by_key(story_id=story_key)
        current_story = Story()
        if len(json_jira) > 0:
            current_story.convert_json_story(json_jira[0])

        return current_story

    def get_dependency_by_features_task(self, feature_keys: List[str], sublist_size: int = 20) -> List[Dependency]:
        key_sub_list = dividir_lista(feature_keys, sublist_size)

        arr_dependency = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._jira_api.get_dependency_by_feature, feature_id=keys) for keys in
                       key_sub_list]
            for future in as_completed(futures):
                arr_dependency.extend(
                    [Dependency().convert_json_dependency(dependency) for dependency in future.result()])

        return arr_dependency

    def get_dependency_by_feature(self, feature_key: str) -> List[Dependency]:

        json_jira = self._jira_api.get_dependency_by_feature(feature_id=feature_key)
        arr_dependency = []
        for dependency in json_jira:
            current_dependency = Dependency()
            current_dependency.convert_json_dependency(dependency)
            arr_dependency.append(current_dependency)

        return arr_dependency

    def get_team_backlog(self) -> List[TeamBacklog]:
        json_jira = self._jira_api.get_team_backlog()
        arr_backlog = []
        for team_backlog in json_jira:
            current_team_backlog = TeamBacklog()
            current_team_backlog.convert_json_to_team_backlog(team_backlog)
            arr_backlog.append(current_team_backlog)

        return arr_backlog
