from src.controllers.FinancialController import FinancialController

def init_routes(app):
    financial_controller = FinancialController.as_view('financial_controller') # Naming is arbitrary
    
    # Create an instance of the FinancialController class
    financial_controller_instance = FinancialController()

    # GET /financial (Retrieve a list of financial resources)
    app.add_url_rule('/financial/', view_func=financial_controller, methods=['GET'])
    
    # GET /financial/create (Display the create form)
    app.add_url_rule('/financial/create/', view_func=financial_controller_instance.create, methods=['GET'])

    # POST /financial/store (Handle the form submission and save to database)
    app.add_url_rule('/financial/store/', view_func=financial_controller_instance.store, methods=['POST'])

    # GET /financial/<id>  (Get details of a specific resource)
    app.add_url_rule('/financial/<int:id>', view_func=financial_controller, methods=['GET'])   

    # PUT /financial/<id>  (Update a resource) 
    app.add_url_rule('/financial/<int:id>', view_func=financial_controller, methods=['PUT']) 

    # DELETE /financial/<id>  (Delete a resource) 
    app.add_url_rule('/financial/<int:id>', view_func=financial_controller, methods=['DELETE'])