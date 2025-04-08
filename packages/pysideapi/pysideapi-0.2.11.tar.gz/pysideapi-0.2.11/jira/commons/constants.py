class Constants:
    CRITERIA_TO_FIND_TABLE = "|\r\n|"
    CRITERIA_TO_FIND_START_TEAM_BACKLOG = 'Peru'
    CRITERIA_TO_FIND_END_TEAM_BACKLOG = '</span>\n  </button>'
    PIPE_ID = "|"
    CRITERIA_TO_FIND_GS = "spreadsheets/d/"
    SLASH_ID = "/"
    JIRA_SERVER = "https://jira.globaldevtools.bbva.com"
    JIRA_API_SESSION = f"{JIRA_SERVER}/rest/auth/1/session"
    JIRA_API_JQL = f"{JIRA_SERVER}/rest/api/2/search?jql="

    JQL_FEATURE = "issueFunction in linkedIssuesOf(\"issuetype = Enterprise and 'Country Sponsor' = Peru \") AND " \
                  "issuetype = Feature  AND 'SDA Project' is not EMPTY AND 'Program " \
                  "Increment' in (#pi_id)"

    JQL_FEATURE_DATAENG_OLD = "issueFunction in linkedIssuesOf(\"issuetype = Enterprise and 'Country Sponsor' = Peru \") AND "\
                "issuetype = Feature AND project in ('DEDATIOCIB','DEDATIOCI2','DEDATIOCI1','DEDRRR','DEDRRDT', "\
                "'DEDRRA','DEDRRCM','DEDFANPYDT','DEDFBASESI','DEDFMISYS','DEDFMODELO','DEDFRORC','DEDFTRANSV','DEDATIOENG', " \
                "'DEDATIOEN3','DEDATIOEN4','DEDATIOEN1','DEDATIOEN2','DEDATIOCLI','DEDATIOCL1','DEDATIOCL2','DEDATIOCL3','DEDATIOCL4') " \
                "AND 'SDA Project' is not EMPTY AND 'Program Increment' in (#pi_id)"

    JQL_FEATURE_DATAENG_20241028 = "issuetype in (Feature , Task L1) AND (project in ('DEDATIOCIB','DEDATIOCI2','DEDATIOCI1','DEDRRR','DEDRRDT', " \
                          "'DEDRRA','DEDRRCM','DEDFANPYDT','DEDFBASESI','DEDFMISYS','DEDFMODELO','DEDFRORC','DEDFTRANSV','DEDATIOENG', " \
                          "'DEDATIOEN3','DEDATIOEN4','DEDATIOEN1','DEDATIOEN2','DEDATIOCLI','DEDATIOCL1','DEDATIOCL2','DEDATIOCL3','DEDATIOCL4') OR labels IN ('#proyDatio')) " \
                          "AND 'Program Increment' in (#pi_id)"

    JQL_FEATURE_DATAENG = "issuetype in ('Feature' , 'Task L1') AND project in ('DEDATIOCIB','DEDATIOCI2','DEDATIOCI1'," \
                          "'DEDRRR','DEDRRDT','DEDRRA','DEDRRCM'," \
                          "'DEDFANPYDT','DEDFBASESI','DEDFMISYS','DEDFMODELO','DEDFRORC','DEDFTRANSV'," \
                          "'DEDATIOENG','DEDATIOEN3','DEDATIOEN4','DEDATIOEN1','DEDATIOEN2'," \
                          "'DEDATIOCLI','DEDATIOCL1','DEDATIOCL2','DEDATIOCL3','DEDATIOCL4'," \
                          "'PAD3')" \
                          " AND 'Program Increment' in (#pi_id)"
    
    JQL_RLB_DATAENG = "issuetype = 'Feature' AND labels in ('EvolutivoRLB') AND 'Program Increment' in (#pi_id)"

    EXTRA_PARAMS_FEATURE = "expand=changelog&fields=changelog,description,created,updated,customfield_10006,project," \
                           "customfield_13300,customfield_13702,customfield_10264,labels,customfield_10260," \
                           "customfield_10003,customfield_10272,customfield_10004,customfield_12900,creator,status," \
                           "issuelinks,summary,issuetype,customfield_19001,customfield_10400,customfield_10265,assignee"

    EXTRA_PARAMS_STORY = "expand=changelog&fields=changelog,assignee,description,created,updated,customfield_10006," \
                         "project,customfield_13702,customfield_10264,labels,customfield_10260,customfield_10003," \
                         "customfield_10272,resolution,customfield_10004,status,customfield_12900,creator,issuelinks," \
                         "summary,issuetype,customfield_19001,customfield_10400,customfield_13300,customfield_10265," \
                         "labels,comment,customfield_10002"

    EXTRA_PARAMS_DEPENDENCY = "expand=changelog&fields=changelog,created,updated,customfield_10006,project," \
                              "customfield_13702,customfield_10264,labels,customfield_10260,customfield_10003," \
                              "customfield_10272,resolution,customfield_10004,status,customfield_12900,creator," \
                              "issuelinks,summary,issuetype,customfield_19001,customfield_10400,customfield_13300," \
                              "customfield_10265,labels,comment,customfield_10002,customfield_13301,customfield_13302"


