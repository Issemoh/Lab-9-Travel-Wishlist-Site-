from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm


# Create your views here.
def place_list(request):
    if request.method == "POST":
        form = NewPlaceForm(request.POST)  # receiving data from a page
        place = form.save()
        if form.is_valid():  # checking if entered data is not violating our constraints
            place.save()  # saving data in database
            return redirect("place_list")  # redirecting user to @place_list

    # Rendering places which are not visited
    places = Place.objects.filter(visited=False).order_by("name")
    new_place_form = NewPlaceForm()
    return render(request, "travel_wishlist/wishlist.html", {"places": places, "new_place_form": new_place_form})


def places_visited(request):
    # rendering places which are visited
    visited = Place.objects.filter(visited=True)
    context = {"visited": visited}
    return render(request, "travel_wishlist/visited.html", context=context)


def place_was_visited(request, place_pk):
    # Marking a unvisited place as visited
    if request.method == "POST":
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    return redirect("place_list")