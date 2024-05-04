from flask import Flask, request, jsonify, render_template, send_file
from flask.views import MethodView
from fpdf import FPDF
import json
import io
import os

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
        # Extract data from the form submission
        formatted_assets = request.json.get('formatted_assets')
        formatted_annuity = request.json.get('formatted_annuity')
        assets = int(request.json.get('assets'))
        annuity = int(request.json.get('annuity'))
        
        data = {
            'assets': assets,
            'annuity': annuity
        }

        # Calculate y-axis range
        max_value = max(data.values()) * 1.3  # Additional 30% to the max value
        num_guidelines = 5  # Number of guidelines on the y-axis
        guideline_values = [max_value * (i / num_guidelines) for i in range(num_guidelines + 1)]

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add title
        pdf.cell(200, 10, txt="Financial Chart", ln=True, align='C')
        pdf.ln(10)  # Add spacing after the title

        # Draw chart
        chart_width = 160
        chart_height = 80
        x_start = 30
        y_start = 40
        pdf.rect(x_start, y_start, chart_width, chart_height)  # Outer rectangle

        # Draw guidelines on y-axis
        pdf.set_line_width(0.2)
        for value in guideline_values[1:]:
            y = y_start + (chart_height * (1 - value / max_value))
            pdf.line(x_start, y, x_start + chart_width, y)
            # Add y-axis labels
            pdf.set_xy(x_start - 10, y - 3)
            pdf.cell(10, 10, str(int(value)), align='C')

        # Draw bars
        bar_width = chart_width / len(data)
        x_position = x_start + bar_width / 4  # Adjust x position for centered bars
        for key, value in data.items():
            bar_height = (value / max_value) * chart_height
            # Choose colors for bars
            if key == 'assets':
                pdf.set_fill_color(0, 102, 204)  # Dark blue
            elif key == 'annuity':
                pdf.set_fill_color(51, 204, 51)  # Dark green
            pdf.rect(x_position, y_start + chart_height - bar_height, bar_width / 2, bar_height, 'F')
            # Add value labels on top of bars
            pdf.set_xy(x_position, y_start + chart_height - bar_height - 5)
            pdf.cell(bar_width / 2, 10, str(value), align='C')
            x_position += bar_width  # Increase x position for next bar

        # Add y-axis label
        pdf.set_xy(x_start - 15, y_start + chart_height / 2)
        pdf.cell(10, 10, "Value", align='C')
        # Add x-axis label
        pdf.set_xy(x_start + chart_width / 2 - 20, y_start + chart_height + 10)
        pdf.cell(10, 10, "Total Assets and Annuity", align='C')

        # Add legend
        pdf.set_fill_color(0, 102, 204)  # Dark blue for assets
        pdf.rect(x_start + 120, y_start + 5, 5, 5, 'F')
        pdf.set_xy(x_start + 128, y_start)
        pdf.cell(10, 10, "Assets", align='L')

        pdf.set_fill_color(51, 204, 51)  # Dark green for annuity
        pdf.rect(x_start + 120, y_start + 15, 5, 5, 'F')
        pdf.set_xy(x_start + 128, y_start + 10)
        pdf.cell(10, 10, "Annuity", align='L')

        # Save PDF
        pdf_path = '/var/www/app/static/media/financial_chart.pdf'  # Customize the path
        pdf.output(pdf_path)

        # Return response
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