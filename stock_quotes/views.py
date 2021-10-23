from django.shortcuts import render, redirect
from django.contrib import messages 
from .models import Stock
from .forms import StockForm
import requests
import json
# "token=pk_ef194b10c0024af8b98e6f8e064da4c5"

def home(request):

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_ef194b10c0024af8b98e6f8e064da4c5")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."

		return render(request, 'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'ticker': 'Enter a ticker symbol above...'})

def about(request):
	return render(request, 'about.html', {})

def add_stock(request):
	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added"))
			return redirect('add_stock')

	else:
		tickers = Stock.objects.all()
		output = []

		for ticker in tickers:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker) + "/quote?token=pk_ef194b10c0024af8b98e6f8e064da4c5")
			try:
				api = json.loads(api_request.content)
				# api.id = ticker.id
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'add_stock.html', { 'output': output })

def delete(request, stock_id):
	ticker = Stock.objects.get(pk=stock_id)
	ticker.delete()
	messages.success(request, ("Ticker has been deleted"))
	return redirect(delete_stock)

def delete_stock(request):
	tickers = Stock.objects.all()
	return render(request, 'delete_stock.html', { 'tickers': tickers })