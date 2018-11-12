## This README is written to clarify a few points about Django REST views.

### Question: So what are these elegant generic views that are all the rage?

``` shell
class DistrictList(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
```

``` shell
class DistrictDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
```

## Answer: They are a concise way to handle a variety of common HTTP requests!
The definitions below correspond to the generic views for the District class in that were just listed above. Notice how many more lines of code there are! Beyond consolidating code and allowing for a few lines to express GET, POST, and PUT protocols, generic views are also tailor made to allow users to directly interact with a table in the gsndb database instance via the Django REST API endpoints, all from the comfort of their own browser. Hot dog!

The first block of code corresponds to the DistrictList generic view:

``` shell
@csrf_exempt
def district_list(request):

    if request.method == 'GET':
        districts = District.objects.all()
        serializer = DistrictSerializer(districts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DistrictSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error, status=400)
```

And this second block of code corresponds to the DistrictDetail generic view:

``` shell
@csrf_exempt
def district_detail(request, pk):

    try:
        district = District.objects.get(pk=pk)
    except District.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DistrictSerializer(district)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DistrictSerializer(district, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        district.delete()
        return HttpResponse(status=204)
  ```
