from rest_framework import serializers
class CountryInfoSerializer(serializers.Serializer):
    flag_link = serializers.URLField()
    capital = serializers.CharField()
    largest_city = serializers.ListField(child=serializers.CharField())
    official_languages = serializers.ListField(child=serializers.CharField())
    area_total = serializers.IntegerField()
    population = serializers.IntegerField()
    GDP_nominal = serializers.DecimalField(max_digits=20, decimal_places=2)