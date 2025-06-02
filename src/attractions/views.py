from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from cities.models import City

from .models import Attraction


class AttractionListView(ListView):
    """
    Display a list of attractions with filtering options.
    """

    model = Attraction
    template_name = "attractions/attraction_list.html"
    context_object_name = "attractions"
    paginate_by = 12

    def get_queryset(self):
        queryset = Attraction.objects.filter(is_active=True)

        # Apply category filter
        category = self.request.GET.get("category", "")
        if category:
            queryset = queryset.filter(category=category)

        # Apply city filter
        city_slug = self.request.GET.get("city", "")
        if city_slug:
            queryset = queryset.filter(city__slug=city_slug)

        # Apply featured filter
        featured = self.request.GET.get("featured", "")
        if featured:
            queryset = queryset.filter(is_featured=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add filter choices to context
        context["category_choices"] = Attraction.CATEGORY_CHOICES
        context["cities"] = City.objects.filter(is_active=True)

        # Add current filter values to context
        context["current_category"] = self.request.GET.get("category", "")
        context["current_city"] = self.request.GET.get("city", "")
        context["featured"] = self.request.GET.get("featured", "")

        return context


class AttractionDetailView(DetailView):
    """
    Display details of a specific attraction.
    """

    model = Attraction
    template_name = "attractions/attraction_detail.html"
    context_object_name = "attraction"

    def get_object(self):
        city_slug = self.kwargs.get("city_slug")
        attraction_slug = self.kwargs.get("slug")

        city = get_object_or_404(City, slug=city_slug, is_active=True)
        attraction = get_object_or_404(
            Attraction, slug=attraction_slug, city=city, is_active=True
        )

        return attraction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attraction = self.object

        # Add city to context
        context["city"] = attraction.city

        # Get related attractions (same category or same city)
        related_attractions = Attraction.objects.filter(is_active=True).exclude(
            id=attraction.id
        )

        # First try to get attractions in the same category and city
        same_category_city = related_attractions.filter(
            category=attraction.category, city=attraction.city
        )[:5]

        if same_category_city.count() >= 3:
            context["related_attractions"] = same_category_city
        else:
            # If not enough, get attractions in the same category from any city
            same_category = related_attractions.filter(category=attraction.category)[:5]

            if same_category.count() >= 3:
                context["related_attractions"] = same_category
            else:
                # If still not enough, get attractions from the same city
                same_city = related_attractions.filter(city=attraction.city)[:5]
                context["related_attractions"] = same_city

        return context
