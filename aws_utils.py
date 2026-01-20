import boto3
import botocore.exceptions
from flask import session

def get_boto_clients():
    """
    Establish AWS clients (Invoicing, STS) based on session credentials.
    Priority: Session > Environment
    """
    # Get Invoice PDF API의 엔드포인트(Endpoint)가 us-east-1 리전에만 존재
    region = session.get('aws_region', 'us-east-1')
    
    if 'aws_access_key' in session and 'aws_secret_key' in session:
        boto_session = boto3.Session(
            aws_access_key_id=session['aws_access_key'],
            aws_secret_access_key=session['aws_secret_key'],
            aws_session_token=session.get('aws_session_token'), # Optional
            region_name=region
        )
    else:
        # Fallback to environment/default chain (useful for local dev with ~/.aws/credentials)
        boto_session = boto3.Session(region_name=region)
        
    return boto_session.client('invoicing'), boto_session.client('sts')

def list_invoices(year, month):
    """
    List invoice summaries for a specific billing period.
    """
    try:
        invoicing, sts = get_boto_clients()
        
        # Get Account ID to verify creds work
        account_id = sts.get_caller_identity()['Account']
        
        # List Invoices
        response = invoicing.list_invoice_summaries(
            Selector={
                'ResourceType': 'ACCOUNT_ID',
                'Value': account_id
            },
            Filter={
                'BillingPeriod': {
                    'Month': int(month),
                    'Year': int(year)
                }
            }
        )
        return response.get('InvoiceSummaries', []), None, account_id
        
    except (botocore.exceptions.NoCredentialsError, botocore.exceptions.ClientError) as e:
        return [], str(e), None
    except Exception as e:
        return [], str(e), None

def get_invoice_pdf_url(invoice_id):
    """
    Retrieve the pre-signed URL for an invoice PDF.
    """
    try:
        invoicing, _ = get_boto_clients()
        response = invoicing.get_invoice_pdf(InvoiceId=invoice_id)
        
        invoice_pdf_data = response.get('InvoicePDF', {})
        pdf_url = invoice_pdf_data.get('InvoicePdfUrl') or invoice_pdf_data.get('DocumentUrl')
        
        return pdf_url, None
    except Exception as e:
        return None, str(e)
