from flask import Flask, request, jsonify, render_template, current_app
from flask.views import MethodView
from fpdf import FPDF
import json
import io
import os
import locale

class FinancialController(MethodView):
    """
    Controller class responsible for handling financial resource requests.
    """
    
    def get(self):
        """
        Handles GET requests to the financial resource endpoint.

        Provides different responses based on the URL path:
         - List financial resources if the path ends with '/'.
         - Retrieve details of a resource if a valid ID is provided.
         - Display the edit form if the path ends with '/edit'.
         - Return an error if the resource ID is invalid.
        """
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
        """
        Processes form submission for creating or updating a financial resource.

        This method extracts financial data, generates a chart, creates a customer 
        information table, constructs a PDF, and returns a success response.
        """
        
        # Extract data from the form submission
        json_data = request.json
        assets = float(json_data.get('total_assets_at_death', 0))
        annuity = float(json_data.get('annuity', 0))  # Ensure 'annuity' key is used here
        
        # Additional data
        age = json_data.get('age')
        annuity_duration = json_data.get('annuity_duration')
        annuity_type = json_data.get('annuity_type')
        email = json_data.get('email')
        expected_return_rate = json_data.get('expected_return_rate')
        formatted_annuity = json_data.get('formatted_annuity')
        formatted_assets = json_data.get('formatted_assets')
        name = json_data.get('name')
        phone = json_data.get('phone')

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
        pdf.set_font("Arial", size=16, style='B')  # Bold title

        # Add title
        pdf.cell(200, 20, txt="Financial Chart", ln=True, align='C')
        pdf.ln(10)  # Add spacing after the title
        
        pdf.set_font("Arial", size=12)

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
            pdf.cell(10, 10, locale.format_string("%.2f", value, grouping=True), align='C')

        # Draw bars
        bar_width = chart_width / (len(data) * 2)  # Adjusted bar width to accommodate boxes
        x_position = x_start + bar_width / 2  # Adjusted x position for centered bars

        for key, value in data.items():
            bar_height = (value / max_value) * chart_height
            # Choose colors for bars and borders
            if key == 'assets':
                pdf.set_fill_color(255, 192, 203)  # Light pink
                pdf.set_draw_color(255, 0, 102)  # Darker pink border
            elif key == 'annuity':
                pdf.set_fill_color(173, 216, 230)  # Light blue
                pdf.set_draw_color(0, 51, 102)  # Darker blue border

            # Draw box around the bar
            pdf.rect(x_position, y_start, bar_width, chart_height, 'D')  # 'D' for drawing the border only

            # Draw bar
            pdf.rect(x_position, y_start + chart_height - bar_height, bar_width, bar_height, 'F')  # 'F' for filling the bar

            # Add value labels on top of bars
            pdf.set_xy(x_position, y_start + chart_height - bar_height - 5)
            formatted_value = locale.format_string("%.2f", value, grouping=True)  # Format value with commas and two decimal places
            pdf.cell(bar_width, 10, formatted_value, align='C')

            # Move x position for next bar
            x_position += bar_width * 2  # Double the bar width for separation

        # Draw vertical line to separate the two sets of bars
        separator_x = x_start + bar_width * 1.5  # X-coordinate for the vertical separator
        pdf.set_draw_color(0, 0, 0)  # Black color for separator line
        pdf.line(separator_x, y_start, separator_x, y_start + chart_height)  # Draw vertical line

        # Add y-axis label
        pdf.set_xy(x_start - 15, y_start + chart_height / 2)
        pdf.cell(10, 10, "Value", align='C')
        
        # Add x-axis label
        pdf.set_xy(x_start + chart_width / 2 - 20, y_start + chart_height)
        pdf.cell(10, 10, "Total Assets and Annuity", align='C')

        # Add legend
        pdf.set_fill_color(255, 192, 203)  # Light pink for assets
        pdf.rect(x_start + 120, y_start + 5, 5, 5, 'F')
        pdf.set_xy(x_start + 128, y_start)
        pdf.cell(10, 10, "Assets", align='L')

        pdf.set_fill_color(173, 216, 230)  # Light blue for annuity
        pdf.rect(x_start + 120, y_start + 15, 5, 5, 'F')
        pdf.set_xy(x_start + 128, y_start + 10)
        pdf.cell(10, 10, "Annuity", align='L')

        # Add customer information table
        pdf.ln(90)  # Add spacing before the table
        pdf.set_font("Arial", size=16, style='B') 
        pdf.cell(60, 10, txt="Customer Information", ln=True, align='L')  # Narrower first column
        pdf.set_font("Arial", size=12)  

        # Table headers
        firstColumnSize = 70
        secondColumnSize = 110
        pdf.set_fill_color(192, 192, 192)  # Light gray background for headers
        pdf.cell(firstColumnSize, 10, txt="Attribute", ln=0, align='L', fill=True)
        pdf.cell(secondColumnSize, 10, txt="Value", ln=1, align='L', fill=True)  # Wider second column

        # Table data (use a loop if you have more attributes)
        pdf.set_fill_color(255, 255, 255)  # White background for data cells
        customer_data = [
            ("Name", name),
            ("Email", email),
            ("Phone", phone),
            ("Age", age),
            ("Annuity", formatted_annuity),
            ("Annuity Duration", annuity_duration),
            ("Annuity Type", annuity_type),
            ("Assets", formatted_assets),
            ("Expected Return Rate", str(expected_return_rate)),
            ("Cash", locale.format_string("%.4f", float(json_data.get('cash', 0)), grouping=True)),  # Format cash with four decimal places
            ("Personal Life Insurance", locale.format_string("%.4f", float(json_data.get('personal_life_insurance', 0)), grouping=True)),  # Format personal life insurance with four decimal places
            ("Group Life Insurance", locale.format_string("%.4f", float(json_data.get('group_life_insurance', 0)), grouping=True)),  # Format group life insurance with four decimal places
            ("CPP Death Benefit", locale.format_string("%.4f", float(json_data.get('cpp_death_benefit', 0)), grouping=True)),  # Format CPP death benefit with four decimal places
            ("RPP Death Benefit", locale.format_string("%.4f", float(json_data.get('rpp_death_benefit', 0)), grouping=True)),  # Format RPP death benefit with four decimal places
            ("RRSP to Liquidate", locale.format_string("%.4f", float(json_data.get('rrsp_to_liquidate', 0)), grouping=True)),  # Format RRSP to liquidate with four decimal places
            ("Investments to Liquidate", locale.format_string("%.4f", float(json_data.get('investments_to_liquidate', 0)), grouping=True)),  # Format investments to liquidate with four decimal places
            ("Other Assets to be Sold", locale.format_string("%.4f", float(json_data.get('other_assets', 0)), grouping=True))  # Format other assets to be sold with four decimal places
        ]
        alternate_color = False  # Variable to toggle row colors
        for attribute, value in customer_data:
            if alternate_color:
                pdf.set_fill_color(240, 240, 240)  # Light gray background for alternate rows
            else:
                pdf.set_fill_color(255, 255, 255)  # White background for data cells
            pdf.cell(firstColumnSize, 10, txt=attribute, ln=0, align='L', fill=True)
            pdf.cell(secondColumnSize, 10, txt=value, ln=1, align='L', fill=True)  # Wider second column
            alternate_color = not alternate_color  # Toggle row colors

        # Save PDF
        pdf_path = current_app.config['APPLICATION_PATH'] + 'app/static/media/financial_chart.pdf'
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