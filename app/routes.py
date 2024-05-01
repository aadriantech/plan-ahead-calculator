from src.controllers.FinancialController import FinancialController
import sys

# def init_routes(app):
#     financial_index_view = FinancialController.as_view('financial-index-view')
    
#     app.add_url_rule('/financial', defaults={'action': None}, view_func=financial_index_view, methods=['GET'])
#     app.add_url_rule('/financial/<string:action>', view_func=financial_index_view, methods=['POST'])

def init_routes(app):
    financial_controller = FinancialController.as_view('financial-controller')  # Naming is arbitrary

    # GET /financial (Retrieve a list of financial resources?)
    app.add_url_rule('/financial', view_func=financial_controller, methods=['GET'])

    # POST /financial (Create a new financial resource?)
    app.add_url_rule('/financial/create', view_func=financial_controller, methods=['GET'])
    app.add_url_rule('/financial/store', view_func=financial_controller, methods=['POST'])

    # GET /financial/<id>  (Get details of a specific resource)
    app.add_url_rule('/financial/<int:id>', view_func=financial_controller, methods=['GET'])   

    # PUT /financial/<id>  (Update a resource) 
    app.add_url_rule('/financial/<int:id>', view_func=financial_controller, methods=['PUT']) 

    # DELETE /financial/<id>  (Delete a resource) 
    app.add_url_rule('/financial/<int:id>', view_func=financial_controller, methods=['DELETE']) 
