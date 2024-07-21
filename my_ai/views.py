from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView
from django_htmx.http import HttpResponseClientRedirect

from api import ai_response, GeminiChat
from memberships.views import is_valid_subscription
from my_ai.forms import ProductDescriptionForm
from my_ai.models import ProductDescriptionModel, Templates, TemplateCategory, Language

DEFAULT_PROJECT_NAME = "Untitled"
all_templates = Templates.objects.all()
all_template_categories = TemplateCategory.objects.all()
most_common_templates = Templates.objects.annotate(num_projects=Count('productdescriptionmodel')).order_by(
    '-num_projects')[:8]
blank_projects = ProductDescriptionModel.objects.filter(aidescription__isnull=True)


def get_default_template():
    default_template, _ = Templates.objects.get_or_create(name="Product Descriptions")
    return default_template


def search_templates(request):
    if template_searched := request.GET.get("search"):
        return Templates.objects.filter(name__icontains=template_searched), template_searched
    else:
        return Templates.objects.none(), template_searched


@login_required(login_url='/accounts/login')
def index(request):
    context = {"all_templates": all_templates,
               "most_common_templates": most_common_templates,
               'all_template_categories': all_template_categories,
               "results": search_templates(request)[0],
               "searched": search_templates(request)[1],
               }
    return render(request, 'index.html', context)


@login_required(login_url='/accounts/login')
def create_product_copy(request):
    user_template_name = request.GET.get("q", get_default_template().name)
    request.session["user_template_name"] = user_template_name
    template_object = Templates.objects.get(name=user_template_name)

    project = ProductDescriptionForm(
        initial={"project_name": DEFAULT_PROJECT_NAME}).save(commit=False)
    project.client_id = request.user.id
    project.project_name = DEFAULT_PROJECT_NAME
    project.template_name = template_object
    project.save()
    return redirect("update-project", project.id)


def answer_and_save_word_count(request,
                                     user_prompt: str,
                                     model: str, max_tokens: int = 256, temperature: float = 0.7,
                                     number_of_variants: int = 1,
                                     frequency_penalty: float = 0.0):
    """THIS FUNCTION counts and saves tokens in database then RETURN A TUPLE OF (AI_ANSWER,TOTAL_TOKENS)"""
    """ai_answers = [ai_response(user_prompt, max_tokens, model,
                              temperature, frequency_penalty) for _ in
                  range(number_of_variants)]"""
    # chat_answers = [chat_completion(user_prompt) for _ in range(number_of_variants)]

    gemini = GeminiChat(prompt=user_prompt)
    total_tokens = gemini.gemini_token_count()

    chat_gemini = [(gemini.gemini_chat_completion(), total_tokens) for _ in range(number_of_variants)]
    # user = get_user(request)
    # user.number_of_words += sum(total_tokens for _, total_tokens in chat_gemini)
    # user.save()
    print(chat_gemini)
    return chat_gemini


@login_required(login_url='/accounts/login')
def create_product_description(request):
    if request.method != "POST":
        return handle_not_post_request()
    product_form = ProductDescriptionForm(request.POST)
    if not product_form.is_valid():
        return handle_invalid_form(product_form)
    if not is_valid_subscription(request):
        return handle_expired_subscription()

    user_template = get_user_template(request)
    context = get_context_from_form(request, product_form)
    context["ai_answers"] = get_ai_answers(request, user_template, context, product_form)

    print(context)

    return render(request, "my_ai/generate_prod_descript.html", context)


def handle_not_post_request():
    return HttpResponse("Please enter the valid data")


def handle_invalid_form(form):
    return HttpResponse(form.errors)


def handle_expired_subscription():
    return HttpResponse("Your subscription is ended ! subscribe")


def get_user_template(request):
    user_template_name = request.session["user_template_name"]
    return get_object_or_404(Templates, name=user_template_name)


def get_context_from_form(request, form):
    project_name = request.session['project_name'] = form.cleaned_data['project_name']
    product_name = request.session['product_name'] = form.cleaned_data['product_name']
    user_product_description = request.session['user_description'] = form.cleaned_data['user_description']
    return {
        "product_name": product_name,
        'project_name': project_name,
        "user_product_description": user_product_description,
    }


def get_ai_answers(request, user_template, context: dict, form):
    number_of_variants = int(request.POST.get("number_of_variant", '1'))
    user_prompt = get_user_prompt(user_template, context, form)
    return answer_and_save_word_count(
        request,
        user_prompt=user_prompt,
        max_tokens=user_template.max_token,
        number_of_variants=number_of_variants,
        model=user_template.model,
        temperature=user_template.temperature,
        frequency_penalty=user_template.frequency_penalty,
    )


def get_user_prompt(user_template: Templates, context: dict, form):
    return user_template.prompt.format(
        product_name=context["product_name"],
        output_language=form.cleaned_data['output_language'],
        user_template_name=user_template.name,
        tone=form.cleaned_data['tone'],
        user_product_description=context["user_product_description"],
    )


@login_required(login_url='/accounts/login')
def save_answer(request):
    ai_answer = request.POST.get("ai_answer", '')
    user_description = request.session['user_description']
    user_template_name = request.session["user_template_name"]
    template_object = get_object_or_404(Templates, name=user_template_name)
    project_id = request.session['project_id']
    answer = get_object_or_404(ProductDescriptionModel, id=project_id)
    answer.user_description = user_description
    answer.product_name = request.session['product_name']
    answer.template_name = template_object
    answer.save()
    ai_description = answer.aidescription_set.create(ai_answer=ai_answer, template_name=user_template_name)
    context = {"project": answer, "ai_description": ai_description,
               "template_object": template_object}
    return render(request, "my_ai/saved_answer_responses.html", context)


@login_required(login_url='/accounts/login')
def productProjectListView(request):
    user = request.user
    all_projects = ProductDescriptionModel.objects.filter(client=user).order_by('-updated')
    searched = request.GET.get("project_search", '')
    if searched:
        all_projects = all_projects.filter(Q(project_name__icontains=searched)
                                           | Q(product_name__icontains=searched)
                                           | Q(template_name__name__icontains=searched))
    paginator = Paginator(all_projects, 12)
    page_number = request.GET.get('page', "1")
    projects = paginator.get_page(page_number)
    context = {"projects": projects, "searched": searched,
               'most_common_templates': most_common_templates,
               "all_projects": all_projects}
    return render(request, "my_ai/all_projects.html", context)


class ProjectUpdateView(UpdateView):
    model = ProductDescriptionModel
    form_class = ProductDescriptionForm
    context_object_name = 'project'
    template_name = "my_ai/update_product_project.html"

    def get_success_url(self):
        return reverse_lazy('update-project', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['project_id'] = self.object.pk
        user_template_name = self.request.GET.get('q')
        if user_template_name:
            self.request.session['user_template_name'] = user_template_name
        else:
            user_template_name = self.request.session.get('user_template_name',
                                                          get_default_template().name)
        context["user_template_name"] = user_template_name
        context['template_object'] = get_object_or_404(Templates, name=user_template_name)
        context['all_template_categories'] = all_template_categories
        context['results'] = search_templates(self.request)[0]
        context['searched'] = search_templates(self.request)[1]
        return context

    def get_form(self, form_class=None):

        user_template_name = self.request.GET.get('q',
                                                  self.request.session.get(
                                                      "user_template_name",
                                                      get_default_template().name))
        template_object = get_object_or_404(Templates, name=user_template_name)

        if form_class is None:
            form_class = self.get_form_class()
        form = super().get_form(form_class)
        form.fields['product_name'].widget.attrs['placeholder'] = template_object.product_name_placeholder
        form.fields['user_description'].widget.attrs['placeholder'] = template_object.user_description_placeholder
        return form


@login_required(login_url='/accounts/login')
def delete_project(request, pk):
    answer = ProductDescriptionModel.objects.filter(id=pk)
    answer.delete()
    return HttpResponseClientRedirect(reverse("home"))


def templates_View(request):
    user_favorite_templates = Templates.objects.filter(
        productdescriptionmodel__client=request.user).annotate(
        num_projects=Count('productdescriptionmodel')
    ).order_by('-num_projects')[:8]
    context = {"all_templates": all_templates,
               "all_template_categories": all_template_categories,
               "most_common_templates": most_common_templates,
               "user_favorite_templates": user_favorite_templates}
    return render(request, 'my_ai/all_templates.html', context)


def remove_not_committed_answer(request):
    return HttpResponse("")


def check_user_description(request):
    user_description = request.POST.get("user_description", "")
    return HttpResponse(f"{len(user_description.split())} words ")


def delete_blank_projects(request):
    user_blank_projects = blank_projects.filter(client=request.user)
    user_blank_projects.delete()
    return HttpResponseClientRedirect(reverse("home"))