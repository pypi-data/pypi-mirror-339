from jira.model.issue_base import IssueBase
from datetime import datetime

import pytz

tz = pytz.timezone('America/Lima')


class TeamBacklog:
    def __init__(self):
        self.id = ''
        self.key = ''
        self.summary = ''

    def convert_json_to_team_backlog(self, json_jira):

        self.id = json_jira["id"]
        self.key = json_jira["key"]
        fields = json_jira["fields"]
        self.summary = fields["summary"]