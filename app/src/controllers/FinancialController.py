from flask import Flask, request, jsonify, render_template, send_file
from flask.views import MethodView
from weasyprint import HTML
import os
import matplotlib.pyplot as plt
from io import BytesIO
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
        # return render_template('financial/pdf_financial_chart.html', 
        #                         chart_filename='financial_chart.png',
        #                         total_assets_at_death="1,000,000",
        #                         annuity_payout="20,000")
        return render_template('financial/create.html')

    def store(self):
        # Extract data from the form submission
        formatted_assets = request.json.get('formatted_assets')
        formatted_annuity = request.json.get('formatted_annuity')
        
        # Generate the chart
        fig, ax = plt.subplots()
        ax.bar(['Annuity Payout', 'Total Assets at Death'], [formatted_annuity, formatted_assets])
        ax.set_xlabel('Category')
        ax.set_ylabel('Value')
        ax.set_title('Financial Chart')
        
        # Set the minimum value of the y-axis to 0
        ax.set_ylim(bottom=0)

        # Save the chart to a file
        chart_filename = 'financial_chart.png'
        chart_path = os.path.join('/var/www/app/static/media', chart_filename)
        fig.savefig(chart_path)
        
        # Close the figure to release resources
        plt.close(fig)

       # Render the HTML template with the data
        rendered_html = render_template('financial/pdf_financial_chart.html', 
                                chart_filename=chart_filename,
                                total_assets_at_death=formatted_assets,
                                annuity_payout=formatted_annuity)

        # Generate PDF from rendered HTML
        pdf = HTML(string=rendered_html).write_pdf()

        # Save the PDF file
        pdf_filename = 'financial_report.pdf'
        pdf_path = os.path.join('/var/www/app/static/media', pdf_filename)
        with open(pdf_path, 'wb') as f:
            f.write(pdf)

        # Serve the PDF file
        return send_file(pdf_path, as_attachment=True)

        # This block won't be reachable after the return statement above, so you can remove it
        return jsonify({
            'message': 'Resource saved successfully',
            'data': request.json
        }), 200


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