from src.controllers.FinancialController import FinancialController
import sys

def init_routes(app):
    financial_index_view = FinancialController.as_view('financial-index-view')
    
    app.add_url_rule('/financial', defaults={'action': None}, view_func=financial_index_view, methods=['GET'])
    app.add_url_rule('/financial/<string:action>', view_func=financial_index_view, methods=['POST'])