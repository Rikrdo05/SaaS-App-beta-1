from flask import Flask, request, render_template_string

app = Flask(__name__)

# Variables to store the selected values
selected_year = None
selected_month = None
selected_revenue_model = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global selected_year, selected_month, selected_revenue_model
    
    if request.method == 'POST':
        # Store the selected values in Python variables
        selected_year = request.form.get('year')
        selected_month = request.form.get('month')
        selected_revenue_model = request.form.get('revenue_model')
        
        # For demonstration, print the selected values
        print(f"Selected Year: {selected_year}")
        print(f"Selected Month: {selected_month}")
        print(f"Selected Revenue Model: {selected_revenue_model}")
    
    # Generate years from 2025 to 2040
    years = list(range(2025, 2041))
    
    # Months list
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Revenue models
    revenue_models = [
        "One-Time Payment",
        "Free Trial (days) + Monthly Subscription",
        "Free Trial (Months) + Monthly Subscription",
        "Free Trial (days) + Annual Subscription",
        "Free Trial (Months) + Annual Subscription",
        "Monthly Subscription (No Free Trial)",
        "Annual Subscription (No Free Trial)"
    ]
    
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Revenue Model Selection</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                form { max-width: 500px; margin: 0 auto; }
                .form-group { margin-bottom: 20px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                select, button { width: 100%; padding: 10px; font-size: 16px; }
                button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
                button:hover { background-color: #45a049; }
            </style>
        </head>
        <body>
            <h1>Select Revenue Model Parameters</h1>
            <form method="POST">
                <div class="form-group">
                    <label for="year">Year:</label>
                    <select id="year" name="year" required>
                        <option value="">-- Select Year --</option>
                        {% for year in years %}
                            <option value="{{ year }}">{{ year }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="month">Month:</label>
                    <select id="month" name="month" required>
                        <option value="">-- Select Month --</option>
                        {% for month in months %}
                            <option value="{{ month }}">{{ month }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="revenue_model">Revenue Model:</label>
                    <select id="revenue_model" name="revenue_model" required>
                        <option value="">-- Select Revenue Model --</option>
                        {% for model in revenue_models %}
                            <option value="{{ model }}">{{ model }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <button type="submit">Submit</button>
            </form>
            
            {% if selected_year and selected_month and selected_revenue_model %}
                <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa;">
                    <h3>Selected Values:</h3>
                    <p><strong>Year:</strong> {{ selected_year }}</p>
                    <p><strong>Month:</strong> {{ selected_month }}</p>
                    <p><strong>Revenue Model:</strong> {{ selected_revenue_model }}</p>
                </div>
            {% endif %}
        </body>
        </html>
    ''', years=years, months=months, revenue_models=revenue_models,
       selected_year=selected_year, selected_month=selected_month, 
       selected_revenue_model=selected_revenue_model)

if __name__ == '__main__':
    app.run(debug=True)
