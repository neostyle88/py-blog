from django.shortcuts import redirect
from django.views import generic

from blog.forms import CommentaryForm
from blog.models import Post


class IndexView(generic.ListView):
    template_name = "blog/index.html"
    paginate_by = 5
    queryset = Post.objects.all()


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentaryForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()  # Get the post
        comment_form = CommentaryForm(request.POST)
        if comment_form.is_valid():
            # Save the comment
            new_comment = comment_form.save(commit=False)
            new_comment.user = (
                self.request.user
            )  # Assuming your Comment model has a 'user' field
            new_comment.post = post
            new_comment.save()
            return redirect(
                "blog:post-detail", pk=post.pk
            )  # Redirect to the post detail page
        else:
            # Handle form errors
            # You can also re-render the page with the form and errors here
            pass
