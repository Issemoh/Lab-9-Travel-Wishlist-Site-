from django.test import TestCase
from django.urls import reverse
from .models import Place


# Create your tests here.
class TestHomePage(TestCase):
    def test_homepage_shows_empty_list_for_empty_database(self):
        home_page = reverse("place_list")  # View name
        response = self.client.get(home_page)  # Getting response
        self.assertTemplateUsed(response, "travel_wishlist/wishlist.html")
        self.assertContains(response, "You have no places in your wishlist")  # checking the contents of response


class TestWishList(TestCase):
    fixtures = ["test_places"]

    def test_wish_list_contains_not_visited_places(self):
        wishlist = reverse("place_list")  # View name
        response = self.client.get(wishlist)  # getting response
        self.assertTemplateUsed(response, "travel_wishlist/wishlist.html")

        # Checking names that has to be in wishlist
        self.assertContains(response, "Tokyo")
        self.assertContains(response, "New York")

        # checking names that are not in wishlist
        self.assertNotContains(response, "San Francisco")
        self.assertNotContains(response, "Moab")


class TestAddNewPlaces(TestCase):
    def test_add_new_unvisited_place_to_wishlist(self):
        add_place = reverse('place_list')
        new_place = {"name": "Japan", "visited": False}  # Adding a new place
        response = self.client.post(add_place, new_place, follow=True)
        self.assertTemplateUsed(response, "travel_wishlist/wishlist.html")
        response_places = response.context["places"]
        self.assertEqual(1, len(response_places))
        japan_response = response_places[0]
        japan_in_database = Place.objects.get(name="Japan", visited=False)

        # Checking if content in database and content in response are equal or not
        self.assertEqual(japan_response, japan_in_database)


class TestVisitPlace(TestCase):
    fixtures = ["test_places"]

    def test_places_visit(self):
        visit_place_url = reverse("place_was_visited", args=(2,))  # making non-visited place to visited
        response = self.client.post(visit_place_url, follow=True)

        self.assertTemplateUsed("travel_wishlist/wishlist.html")

        self.assertNotContains(response, "New York")

        new_york = Place.objects.get(pk=2)

        self.assertTrue(new_york.visited)  # checking if place is in visited list or not

    def test_visit_non_existing_place(self):
        # making non-visited place to visited that are not in database
        visit_place_url = reverse("place_was_visited", args=(198,))
        response = self.client.post(visit_place_url, follow=True)
        self.assertEqual(404, response.status_code)  # Checking if error code 404 is received or not
