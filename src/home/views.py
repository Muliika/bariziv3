from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def listings(request):
    return render(request, "home/listings.html")


def single_listing(request):
    return render(request, "home/single-listing.html")


def add_post(request):
    return render(request, "home/add-post.html")
