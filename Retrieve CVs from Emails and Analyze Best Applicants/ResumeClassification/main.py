import sys
import torch
import google.auth.transport.requests
from google.oauth2 import service_account
from transformers import BertTokenizer, BertForSequenceClassification
import re  # For regular expressions operations


service_account_file = 'acc.json'
scopes = ['https://www.googleapis.com/auth/datastore']

# Load the trained model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')  # Adjust with actual path if needed
model = BertForSequenceClassification.from_pretrained("model")  # Adjust with actual path if needed
model.eval()

# Define category labels
category_labels = ['ACCOUNTANT',
                   'ADVOCATE',
                   'APPAREL',
                   'ARTS',
                   'BANKING',
                   'BUSINESS-DEVELOPMENT',
                   'CHEF',
                   'CONSTRUCTION',
                   'CONSULTANT',
                   'DESIGNER',
                   'DIGITAL-MEDIA',
                   'ENGINEERING',
                   'FINANCE',
                   'FITNESS',
                   'HEALTHCARE',
                   'HR',
                   'INFORMATION-TECHNOLOGY',
                   'PUBLIC-RELATIONS',
                   'SALES',
                   'TEACHER']

def clean(text):
    """
    Clean the input text by removing URLs, emails, special characters, and stop words.
    
    :param text: The string to be cleaned
    :return: The cleaned string
    """

    # Compile patterns for URLs and emails to speed up cleaning process
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    
    # Remove URLs
    clean_text = url_pattern.sub('', text)
    
    clean_text = clean_text.lower()
    
    # Remove emails
    clean_text = email_pattern.sub('', clean_text)
    
    # Remove special characters (keeping only words and whitespace)
    clean_text = re.sub(r'[^\w\s]', '', clean_text)
    
    
    return clean_text

# Function to predict resume category
def predict_resume_category(resume_text):

    resume_text = clean(resume_text)

    inputs = tokenizer(resume_text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    predicted_class_id = torch.argmax(logits, dim=1).item()
    # Save the resume text to a file

    return category_labels[predicted_class_id]

def get_access_token():
    # Create a credentials object from the service account file
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes)

    # Request an access token
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)

    # Return the access token
    return credentials.token

# Main function to handle command-line input
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No resume text provided.")
        sys.exit(1)
    
    # The resume text is passed as a command-line argument
    resume_text = sys.argv[1]
    predicted_category = predict_resume_category(resume_text)
    print(f"Predicted Job Category: {predicted_category}")