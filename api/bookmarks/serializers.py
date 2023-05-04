from rest_framework import serializers

from api.bookmarks.models import Bookmark


class BookmarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = (
            "id",
            "url",
            "user",
            "name",
            "description",
        )
