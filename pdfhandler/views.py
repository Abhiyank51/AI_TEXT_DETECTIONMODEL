# pdfhandler/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import pdfplumber

# Load pre-trained BERT model
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def classify_text(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model(**inputs)
    probabilities = torch.softmax(outputs.logits, dim=1).detach().numpy()[0]

    return probabilities[1]  # Probability of being AI text

def calculate_ai_percentage(text):
    ai_probability = classify_text(text)
    return ai_probability * 100

def handle_uploaded_file(f):
    with open('uploaded_file.pdf', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            extracted_text = extract_text_from_pdf('uploaded_file.pdf')
            ai_percentage = calculate_ai_percentage(extracted_text)
            return render(request, 'result.html', {'extracted_text': extracted_text, 'ai_percentage': ai_percentage})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
