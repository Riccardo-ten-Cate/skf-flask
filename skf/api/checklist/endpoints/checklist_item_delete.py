from flask import request
from flask_restplus import Resource
from skf.api.security import security_headers, validate_privilege
from skf.api.checklist.business import delete_checklist_item
from skf.api.checklist.serializers import checklist_update, message
from skf.api.kb.parsers import authorization
from skf.api.restplus import api

ns = api.namespace('checklist', description='Operations related to checklist items')

@ns.route('/delete/item/<string:checklist_id>/type/<int:checklist_type>')
@api.doc(params={'checklist_id': 'The unique identifier of the checklist item (2.1, 10.1.2 etc)', 'checklist_type': 'The checklist type (0: ASVS lvl1, 1: ASVS lvl2, 2: ASVS lvl3, 3: MASVS lvl1, etc)'})
@api.response(404, 'Validation error', message)
class ChecklistItemDelete(Resource):
    
    @api.expect(authorization)
    @api.response(400, 'No results found', message)
    def delete(self, checklist_id, checklist_type):
        """
        Delete a checklist item.
        * Privileges required: **manage**
        """
        validate_privilege(self, 'manage')
        result = delete_checklist_item(checklist_id, checklist_type)
        return result, 200, security_headers()
