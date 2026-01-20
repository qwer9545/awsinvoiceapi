from flask import Flask, render_template, redirect, url_for, session, request
from flask_session import Session
from datetime import datetime
from config import Config
import aws_utils

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Server-side Session
Session(app)

@app.template_filter('comma')
def comma_filter(value):
    try:
        # Handle string inputs
        val = float(value)
        # Check if it has decimal places
        if val.is_integer():
            return "{:,.0f}".format(val)
        else:
            return "{:,.2f}".format(val)
    except (ValueError, TypeError):
        return value

@app.route('/')
def index():
    invoices = []
    error = None
    account_id = None
    selected_month = request.args.get('month')
    
    # Default to current month if not provided
    if not selected_month:
        selected_month = datetime.now().strftime('%Y-%m')

    # Convert YYYY-MM to year/month for API
    try:
        selected_date = datetime.strptime(selected_month, '%Y-%m')
        
        # Call AWS Utils
        invoices, error_msg, acc_id = aws_utils.list_invoices(
            selected_date.year, 
            selected_date.month
        )
        
        if error_msg:
            # Check if it's a login issue vs actual error
            if 'aws_access_key' not in session:
                # Not logged in, suppress error (just show login form)
                pass
            else:
                error = f"AWS Error: {error_msg}"
        
        account_id = acc_id

    except Exception as e:
        error = str(e)

    is_authenticated = (account_id is not None)
    
    return render_template('index.html', 
                           invoices=invoices, 
                           error=error, 
                           is_authenticated=is_authenticated,
                           account_id=account_id,
                           selected_month=selected_month)

@app.route('/login', methods=['POST'])
def login():
    # Strip whitespace to prevent copy-paste errors
    session['aws_access_key'] = request.form['aws_access_key'].strip()
    session['aws_secret_key'] = request.form['aws_secret_key'].strip()
    
    token = request.form.get('aws_session_token', '').strip()
    if token:
        session['aws_session_token'] = token
    
    # The Invoicing API is in us-east-1.
    session['aws_region'] = 'us-east-1'
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/download/<invoice_id>')
def download_pdf(invoice_id):
    pdf_url, error = aws_utils.get_invoice_pdf_url(invoice_id)
    
    if pdf_url:
        return redirect(pdf_url)
    elif error:
        return f"Error retrieving PDF: {error}", 500
    else:
        return "Could not retrieve PDF URL.", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
