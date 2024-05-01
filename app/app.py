
from flask import Flask, render_template, request, make_response
from weasyprint import HTML
import json

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('financial_planning_tool.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict(flat=True)
    data = {key: float(value) if key != 'annuity_type' and key != 'annuity_duration' else value for key, value in data.items()}

    # Annuity calculations
    annuity_payout = calculate_annuity(data['total_assets_at_death'], data['annuity_type'], data['annuity_duration'], data.get('expected_return_rate', 0))

    # Prepare data for the chart
    chart_data = prepare_chart_data(data['total_assets_at_death'], annuity_payout)

    # Render PDF from template
    html = render_template('report.html', data=data, chart_data=json.dumps(chart_data), annuity_payout=annuity_payout)
    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=financial_report.pdf'
    return response

def calculate_annuity(principal, annuity_type, duration, rate=0):
    if duration == 'lifetime':
        years = 20  # default lifetime duration in years
    else:
        years = int(duration)

    if annuity_type == 'fixed':
        return principal / years
    elif annuity_type == 'variable':
        return (principal * (float(rate) / 100)) / years
    else:
        return 0

def prepare_chart_data(total_assets, annuity_payout):
    return {
        'labels': ['Total Assets', 'Annual Annuity Payout'],
        'datasets': [{
            'label': 'Financial Overview',
            'data': [total_assets, annuity_payout],
            'backgroundColor': ['#4CAF50', '#FFCE56']
        }]
    }

if __name__ == '__main__':
    app.run(debug=True)  # Use debug=True for development


