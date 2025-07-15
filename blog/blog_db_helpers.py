from .models import BlogPost

def get_blog_data(request):
    try:
        title = request.data.get("title", None)
        author_id = request.data.get("author_id", None)
        created_at = request.data.get("created_at", None)
        limit = request.data.get("limit", 10)
        offset = request.data.get("offset", 0)

        kwargs = {}
        if title:
            kwargs["title__iexact"] = title
        if author_id:
            kwargs["author_id"] = author_id
        if created_at:
            kwargs["created_at__date"] = created_at
        records = BlogPost.objects.filter(**kwargs).order_by("-id")[offset:offset+limit]
        return records
    except Exception as ex:
        return False
