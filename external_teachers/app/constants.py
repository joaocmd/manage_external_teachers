def_password = '0'

JSON_FILE = 'departmentMembers_prod.json'

ENCODING = 'utf-8'

EXPORT_ACTION = 'export_action'
CLOSE_ACTION = 'close_action'
DELETE_ACTION = 'delete_action'

POSSIBLE_ACTIONS = {
  'dep_opened' : {EXPORT_ACTION : True,
                  CLOSE_ACTION : False,
                  DELETE_ACTION : True},
  'dep_closed' : {EXPORT_ACTION : True,
                  CLOSE_ACTION : False,
                  DELETE_ACTION : False},
  'sc_opened' : {EXPORT_ACTION : True,
                  CLOSE_ACTION : True,
                  DELETE_ACTION : True},
  'sc_closed' : {EXPORT_ACTION : True,
                  CLOSE_ACTION : False,
                  DELETE_ACTION : True},
}
