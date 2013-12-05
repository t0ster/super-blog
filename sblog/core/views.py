from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
from django.shortcuts import redirect

from sblog.core.models import Post, Image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class BlogView(ListView):
    template_name = 'blog.html'
    model = Post
    context_object_name = 'post_list'


class PostView(DetailView):
    template_name = 'post.html'
    model = Post
    context_object_name = 'post'


ImageFormSet = modelformset_factory(Image, ImageForm, extra=1)


class CreatePostView(CreateView):
    template_name = 'edit_post.html'
    model = Post

    def form_valid(self, form):
        context = self.get_context_data()
        form = context['form']
        images_form = context['images_form']
        if form.is_valid() and images_form.is_valid():
            self.object = form.save()
            for data in images_form.cleaned_data:
                if data:
                    image_field = data['image']
                    image = Image()
                    image.image = image_field
                    image.post = self.object
                    image.save()
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreatePostView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = PostForm(**self.get_form_kwargs())
            context['images_form'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['form'] = PostForm()
            context['images_form'] = ImageFormSet(queryset=Image.objects.none())
        return context


class EditPostView(UpdateView):
    template_name = 'edit_post.html'
    model = Post

    def form_valid(self, form):
        context = self.get_context_data()
        form = context['form']
        images_form = context['images_form']
        if form.is_valid() and images_form.is_valid():
            self.object = form.save()
            for data in images_form.cleaned_data:
                if data:
                    image = data['id']
                    image_field = data['image']
                    if not image_field:
                        image.delete()
                    if not image:
                        image = Image()
                        image.image = image_field
                        image.post = self.object
                        image.save()
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(EditPostView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = PostForm(**self.get_form_kwargs())
            context['images_form'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['form'] = PostForm(**self.get_form_kwargs())
            context['images_form'] = ImageFormSet(queryset=Image.objects.filter(post=self.object))
        return context


class DeletePostView(DeleteView):
    model = Post
    success_url = '/'
