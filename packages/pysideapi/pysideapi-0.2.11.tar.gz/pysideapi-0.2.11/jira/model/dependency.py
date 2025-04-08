from jira.model.issue_base import IssueBase
from datetime import datetime

import pytz

tz = pytz.timezone('America/Lima')


class Dependency(IssueBase):
    def __init__(self):
        super().__init__()
        self.petitioner_team_backlog_id = ''
        self.petitioner_team_backlog_name = ''
        self.created_petitioner_team_backlog_id = ''
        self.created_petitioner_team_backlog_name = ''
        self.feature_key = ''
        self.story_points = 0

    def convert_json_dependency(self, json_jira):

        fields = json_jira["fields"]
        changelog = json_jira["changelog"]
        histories = changelog.get('histories')

        self.feature_key = fields.get("customfield_10004")
        '''
        if fields.get('customfield_13301') is not None:
            self.petitioner_team_backlog_id = ', '.join(fields.get("customfield_13301"))
            if self.petitioner_team_backlog_id != '':
                if fields.get('customfield_13302') is not None:
                    self.petitioner_team_backlog_id = ', '.join(fields.get("customfield_13302"))
        '''
        backlog_field_1 = fields.get('customfield_13301')
        backlog_field_2 = fields.get('customfield_13302')

        if backlog_field_1:
            self.petitioner_team_backlog_id = ', '.join(backlog_field_1)
        elif backlog_field_2:  # Solo si 'customfield_13302' tiene un valor, lo actualizamos
            self.petitioner_team_backlog_id = ', '.join(backlog_field_2)

        '''
        backlog_field_1 = fields.get('customfield_13301')
        backlog_field_2 = fields.get('customfield_13302')

        if backlog_field_1:
            self.petitioner_team_backlog_id = ', '.join(backlog_field_1)
        if self.petitioner_team_backlog_id and backlog_field_2:
            self.petitioner_team_backlog_id = ', '.join(backlog_field_2)
        '''
        if fields.get('customfield_10002') is not None:
            self.story_points = fields.get('customfield_10002')
        labels = fields["labels"]

        self.labels = ', '.join(labels)
        self._add_attr_basic(json_jira)
        self._get_attr_from_histories(histories)

        return self
