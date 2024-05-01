from flask import Flask, request, jsonify, render_template
from flask.views import MethodView
from weasyprint import HTML
import json

class FinancialController(MethodView):
    def get(self):
        if request.path.endswith('/'):  # List all financial resources
            return jsonify({'message': 'List of financial resources'})
        
        resource_id = request.path.split('/')[-1]  # Extract ID
        if resource_id.isdigit():
            return jsonify({'message': f'Details of resource {resource_id}'}), 200
        
        elif request.path.endswith('/edit'):
            return jsonify({'message': 'Edit form for resource'}), 200
        
        return jsonify({'error': 'Invalid resource ID'}), 400

    def create(self):
        # Display the create form
        return render_template('financial/create.html')

    def store(self):
        # Handle the form submission and save to database
        data = request.get_json()
        print(data)
        # Logic to save the data to the database
        return jsonify({'message': 'Resource saved successfully'}), 201

    def put(self):
        resource_id = request.path.split('/')[-1]
        if resource_id.isdigit():
            # Logic to update resource with given ID
            return jsonify({'message': f'Resource {resource_id} updated'}), 200
        return jsonify({'error': 'Invalid resource ID'}), 400

    def delete(self):
        resource_id = request.path.split('/')[-1]
        if resource_id.isdigit():
            # Logic to delete resource with given ID
            return jsonify({'message': f'Resource {resource_id} deleted'}), 200
        return jsonify({'error': 'Invalid resource ID'}), 400