from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import City, CityAttraction, District


# Class-based views (CBVs)
class DistrictListView(ListView):
    model = District
    template_name = "cities/district_list.html"
    context_object_name = "districts"
    paginate_by = 12

    def get_queryset(self):
        queryset = District.objects.filter(is_active=True)
        query = self.request.GET.get("q", "")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["total_results"] = self.get_queryset().count()
        return context


class DistrictDetailView(DetailView):
    model = District
    template_name = "cities/district_detail.html"
    context_object_name = "district"

    def get_queryset(self):
        return District.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cities = self.object.cities.filter(is_active=True)

        # Pagination for cities
        paginator = Paginator(cities, 9)
        page = self.request.GET.get("page", 1)

        try:
            cities_page = paginator.page(page)
        except PageNotAnInteger:
            cities_page = paginator.page(1)
        except EmptyPage:
            cities_page = paginator.page(paginator.num_pages)

        context["cities"] = cities_page
        context["total_cities"] = cities.count()
        return context


class CityListView(ListView):
    model = City
    template_name = "cities/city_list.html"
    context_object_name = "cities"
    paginate_by = 9

    def get_queryset(self):
        queryset = City.objects.filter(is_active=True).select_related("district")

        # Filter by keyword
        keyword = self.request.GET.get("keyword", "")
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(district__name__icontains=keyword)
            )

        # Filter by district
        district_slug = self.request.GET.get("district", "")
        if district_slug:
            queryset = queryset.filter(district__slug=district_slug)

        # Filter by featured status
        featured = self.request.GET.get("featured", "")
        if featured == "true":
            queryset = queryset.filter(is_featured=True)

        # Sort results
        sort_by = self.request.GET.get("sort", "name")
        if sort_by == "name":
            queryset = queryset.order_by("name")
        elif sort_by == "population_high":
            queryset = queryset.order_by("-population")
        elif sort_by == "population_low":
            queryset = queryset.order_by("population")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all districts for filter dropdown
        context["districts"] = District.objects.filter(is_active=True)

        # Pass current filter values to template
        context["keyword"] = self.request.GET.get("keyword", "")
        context["current_district"] = self.request.GET.get("district", "")
        context["current_sort"] = self.request.GET.get("sort", "name")
        context["featured"] = self.request.GET.get("featured", "")

        # Check if any filters were applied
        filters_applied = bool(
            context["keyword"] or context["current_district"] or context["featured"]
        )
        context["filters_applied"] = filters_applied

        # Total results count
        context["total_results"] = self.get_queryset().count()

        return context


class CityDetailView(DetailView):
    model = City
    template_name = "cities/city_detail.html"
    context_object_name = "city"

    def get_queryset(self):
        return City.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get attractions for this city
        attractions = self.object.attractions.filter(is_active=True)

        # Filter by category if specified
        category = self.request.GET.get("category", "")
        if category:
            attractions = attractions.filter(category=category)

        # Count attractions by category for sidebar
        category_counts = (
            self.object.attractions.filter(is_active=True)
            .values("category")
            .annotate(count=Count("id"))
        )

        # Convert to dictionary for easy access in template
        categories = {item["category"]: item["count"] for item in category_counts}

        context["attractions"] = attractions
        context["categories"] = categories
        context["current_category"] = category

        return context


class AttractionDetailView(DetailView):
    model = CityAttraction
    template_name = "cities/attraction_detail.html"
    context_object_name = "attraction"

    def get_queryset(self):
        city_slug = self.kwargs.get("city_slug")
        city = get_object_or_404(City, slug=city_slug, is_active=True)
        return CityAttraction.objects.filter(city=city, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the city
        city_slug = self.kwargs.get("city_slug")
        city = get_object_or_404(City, slug=city_slug, is_active=True)

        # Get related attractions (same category in same city)
        related_attractions = CityAttraction.objects.filter(
            city=city, category=self.object.category, is_active=True
        ).exclude(id=self.object.id)[:3]

        context["city"] = city
        context["related_attractions"] = related_attractions

        return context
