from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from post_office import mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Editorial, CryptoAnalysis, PressRelease, News, NewestCourse, Hashtag
from .serializers import SendMessageSerializer
from django.core.paginator import Paginator

# views.py

def index(request):
    editorials = Editorial.objects.all()[:45]
    crypto_analyses = CryptoAnalysis.objects.all()[:9]
    press_releases = PressRelease.objects.all()[:4]
    news = News.objects.all().order_by('-pub_date')[:8]
    featured_news = News.objects.filter(featured=True).order_by('-pub_date')[:3]
    main_articles = News.objects.filter(main_article_position__isnull=False).order_by('main_article_position')[:3]
    newest_courses = NewestCourse.objects.all()[:7]  # Dodajemy 3 najnowsze kursy
    context = {
        'editorials': editorials,
        'crypto_analyses': crypto_analyses,
        'press_releases': press_releases,
        'news': news,
        'featured_news': featured_news,
        'main_articles': main_articles,
        'newest_courses': newest_courses  # Dodajemy nowe kursy do kontekstu
    }
    return render(request, 'articles.html', context)



def editorial(request, slug):
    editorial = get_object_or_404(Editorial, slug=slug)
    return render(request, 'editorial.html', {'editorial': editorial})

def tutorials(request):
    tutorials = Editorial.objects.all()
    return render(request, 'tutorials.html', {'tutorials': tutorials})

def press_release(request, slug):
    press_release = get_object_or_404(PressRelease, slug=slug)
    return render(request, 'press_release.html', {'press_release': press_release})

def news(request, slug):
    news = get_object_or_404(News, slug=slug)
    news.views += 1  # Increase the views by 1
    news.save()  # Don't forget to save the object
    return render(request, 'news.html', {'news': news})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def send_message(request):
    serializer = SendMessageSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        full_message = f"From: {data['name']} <{data['email']}>\n\n{data['message']}"

        mail.send(
            ['office.travilabs@gmail.com'],  
            sender=settings.DEFAULT_FROM_EMAIL,
            subject=data['subject'],
            message=full_message,
            priority='now'
        )
        return Response({"status": "Email sent successfully!"}, status=status.HTTP_200_OK)
    else:
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def all_news(request):
    news_list = News.objects.all().order_by('-pub_date')
    paginator = Paginator(news_list, 25)  # Pokaż 25 newsów na stronę

    page = request.GET.get('page')
    news = paginator.get_page(page)
    
    return render(request, 'all_news.html', {'news': news})

def all_projects(request):
    press_release_list = PressRelease.objects.all()
    paginator = Paginator(press_release_list, 24)  # Show 25 press releases per page

    page = request.GET.get('page')
    press_releases = paginator.get_page(page)
    
    return render(request, 'all_projects.html', {'press_releases': press_releases})

def all_editorials(request):
    editorial_list = Editorial.objects.all()
    paginator = Paginator(editorial_list, 25)  # Pokaż 25 editorials na stronę

    page = request.GET.get('page')
    editorials = paginator.get_page(page)
    
    return render(request, 'all_editorials.html', {'editorials': editorials})

def newest_course(request, slug):
    course = get_object_or_404(NewestCourse, slug=slug)
    return render(request, 'course_details.html', {'course': course})

def all_courses(request):
    course_list = NewestCourse.objects.all()
    paginator = Paginator(course_list, 25)  # Pokaż 25 kursów na stronę

    page = request.GET.get('page')
    courses = paginator.get_page(page)

    return render(request, 'all_courses.html', {'courses': courses})

def web_development_full_courses(request):
    web_development_hashtag = get_object_or_404(Hashtag, name='web-development')
    full_projects_hashtag = get_object_or_404(Hashtag, name='full-projects')
    press_releases = PressRelease.objects.filter(hashtags=web_development_hashtag).filter(hashtags=full_projects_hashtag)
    paginator = Paginator(press_releases, 25)  # Show 25 press releases per page
    page = request.GET.get('page')
    paged_press_releases = paginator.get_page(page)
    
    return render(request, 'web_development_full_courses.html', {'press_releases': paged_press_releases})

def web_development_backend_django(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    django_hashtag = get_object_or_404(Hashtag, name='django')
    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=django_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=django_hashtag)
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_backend_django.html', context)


def web_development_backend_flask(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    flask_hashtag = get_object_or_404(Hashtag, name='flask')
    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=flask_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=flask_hashtag)
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_backend_flask.html', context)

def web_development_backend_express_js(request):
    # Get the hashtags
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    express_js_hashtag = get_object_or_404(Hashtag, name='express-js')
    # Filter the press releases and editorials by hashtags
    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=express_js_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=express_js_hashtag)
    # Combine and paginate
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)
    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_backend_express_js.html', context)

def web_development_backend_php(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    php_hashtag = get_object_or_404(Hashtag, name='php')
    
    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=php_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=php_hashtag)
    
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_backend_php.html', context)

def web_development_frontend_html_css_js(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    html_css_js_hashtag = get_object_or_404(Hashtag, name='html-css-js')
    
    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=html_css_js_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=html_css_js_hashtag)
    
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_frontend_html_css_js.html', context)


def web_development_frontend_react_js(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    react_js_hashtag = get_object_or_404(Hashtag, name='react-js')
    
    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=react_js_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=react_js_hashtag)
    
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_frontend_react.html', context)

def web_development_frontend_vue_js(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    vue_js_hashtag = get_object_or_404(Hashtag, name='vue-js')
    
    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=vue_js_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=vue_js_hashtag)
    
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_frontend_vue.html', context)

def web_development_frontend_next_js(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    next_js_hashtag = get_object_or_404(Hashtag, name='next-js')
    
    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=next_js_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=next_js_hashtag)
    
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_frontend_next_js.html', context)

def web_development_frontend_bootstrap(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    bootstrap_hashtag = get_object_or_404(Hashtag, name='bootstrap')
    
    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=bootstrap_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=bootstrap_hashtag)
    
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_frontend_bootstrap.html', context)

def web_development_frontend_tailwind(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    tailwind_hashtag = get_object_or_404(Hashtag, name='tailwind')
    
    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=tailwind_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=tailwind_hashtag)
    
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_frontend_tailwind.html', context)

def web_development_frontend_three_js(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    three_js_hashtag = get_object_or_404(Hashtag, name='three-js')
    
    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=three_js_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=three_js_hashtag)
    
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_frontend_three_js.html', context)

def web_development_frontend_vite(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    vite_hashtag = get_object_or_404(Hashtag, name='vite')
    
    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=vite_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=vite_hashtag)
    
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_frontend_vite.html', context)

def web_development_wordpress_full_projects(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    wordpress_hashtag = get_object_or_404(Hashtag, name='wordpress')
    full_projects_hashtag = get_object_or_404(Hashtag, name='full-projects')

    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=wordpress_hashtag).filter(hashtags=full_projects_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=wordpress_hashtag).filter(hashtags=full_projects_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_wordpress_full_projects.html', context)


def web_development_wordpress_full_projects(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    wordpress_hashtag = get_object_or_404(Hashtag, name='wordpress')
    full_projects_hashtag = get_object_or_404(Hashtag, name='full-projects')

    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=wordpress_hashtag).filter(hashtags=full_projects_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=wordpress_hashtag).filter(hashtags=full_projects_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_wordpress_full_projects.html', context)

def web_development_wordpress_plugins(request):
    web_dev_hashtag = get_object_or_404(Hashtag, name='web-development')
    wordpress_hashtag = get_object_or_404(Hashtag, name='wordpress')
    plugins_hashtag = get_object_or_404(Hashtag, name='plugins')

    press_releases = PressRelease.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=wordpress_hashtag).filter(hashtags=plugins_hashtag)
    editorials = Editorial.objects.filter(hashtags=web_dev_hashtag).filter(hashtags=wordpress_hashtag).filter(hashtags=plugins_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'web_development_wordpress_plugins.html', context)

def mobile_development_full_projects(request):
    mobile_dev_hashtag = get_object_or_404(Hashtag, name='mobile-development')
    full_projects_hashtag = get_object_or_404(Hashtag, name='full-projects')

    press_releases = PressRelease.objects.filter(hashtags=mobile_dev_hashtag).filter(hashtags=full_projects_hashtag)
    editorials = Editorial.objects.filter(hashtags=mobile_dev_hashtag).filter(hashtags=full_projects_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'mobile_development_fullprojects.html', context)

def mobile_development_java(request):
    mobile_dev_hashtag = get_object_or_404(Hashtag, name='mobile-development')
    java_hashtag = get_object_or_404(Hashtag, name='java')

    press_releases = PressRelease.objects.filter(hashtags=mobile_dev_hashtag).filter(hashtags=java_hashtag)
    editorials = Editorial.objects.filter(hashtags=mobile_dev_hashtag).filter(hashtags=java_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'mobile_development_java.html', context)

def mobile_development_kotlin(request):
    mobile_dev_hashtag = get_object_or_404(Hashtag, name='mobile-development')
    kotlin_hashtag = get_object_or_404(Hashtag, name='kotlin')

    press_releases = PressRelease.objects.filter(hashtags=mobile_dev_hashtag).filter(hashtags=kotlin_hashtag)
    editorials = Editorial.objects.filter(hashtags=mobile_dev_hashtag).filter(hashtags=kotlin_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'mobile_development_kotlin.html', context)

def mobile_development_flutter(request):
    mobile_dev_hashtag = get_object_or_404(Hashtag, name='mobile-development')
    flutter_hashtag = get_object_or_404(Hashtag, name='flutter')

    press_releases = PressRelease.objects.filter(hashtags=mobile_dev_hashtag).filter(hashtags=flutter_hashtag)
    editorials = Editorial.objects.filter(hashtags=mobile_dev_hashtag).filter(hashtags=flutter_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'mobile_development_flutter.html', context)

def mobile_development_react_native(request):
    mobile_dev_hashtag = get_object_or_404(Hashtag, name='mobile-development')
    react_native_hashtag = get_object_or_404(Hashtag, name='react-native')

    press_releases = PressRelease.objects.filter(hashtags=mobile_dev_hashtag).filter(hashtags=react_native_hashtag)
    editorials = Editorial.objects.filter(hashtags=mobile_dev_hashtag).filter(hashtags=react_native_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'mobile_development_react-native.html', context)

def game_development_unity(request):
    game_dev_hashtag = get_object_or_404(Hashtag, name='game-development')
    unity_hashtag = get_object_or_404(Hashtag, name='unity')

    press_releases = PressRelease.objects.filter(hashtags=game_dev_hashtag).filter(hashtags=unity_hashtag)
    editorials = Editorial.objects.filter(hashtags=game_dev_hashtag).filter(hashtags=unity_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'game_development_unity.html', context)

def game_development_unreal_engine(request):
    game_dev_hashtag = get_object_or_404(Hashtag, name='game-development')
    unreal_engine_hashtag = get_object_or_404(Hashtag, name='unreal-engine')

    press_releases = PressRelease.objects.filter(hashtags=game_dev_hashtag).filter(hashtags=unreal_engine_hashtag)
    editorials = Editorial.objects.filter(hashtags=game_dev_hashtag).filter(hashtags=unreal_engine_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'game_development_unreal_engine.html', context)

def game_development_rpg_maker(request):
    game_dev_hashtag = get_object_or_404(Hashtag, name='game-development')
    rpg_maker_hashtag = get_object_or_404(Hashtag, name='rpg-maker')

    press_releases = PressRelease.objects.filter(hashtags=game_dev_hashtag).filter(hashtags=rpg_maker_hashtag)
    editorials = Editorial.objects.filter(hashtags=game_dev_hashtag).filter(hashtags=rpg_maker_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'game_development_rpg_maker.html', context)

def game_development_godot(request):
    game_dev_hashtag = get_object_or_404(Hashtag, name='game-development')
    godot_hashtag = get_object_or_404(Hashtag, name='godot')

    press_releases = PressRelease.objects.filter(hashtags=game_dev_hashtag).filter(hashtags=godot_hashtag)
    editorials = Editorial.objects.filter(hashtags=game_dev_hashtag).filter(hashtags=godot_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'game_development_godot.html', context)

def game_development_phaser(request):
    game_dev_hashtag = get_object_or_404(Hashtag, name='game-development')
    phaser_hashtag = get_object_or_404(Hashtag, name='phaser')

    press_releases = PressRelease.objects.filter(hashtags=game_dev_hashtag).filter(hashtags=phaser_hashtag)
    editorials = Editorial.objects.filter(hashtags=game_dev_hashtag).filter(hashtags=phaser_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'game_development_phaser.html', context)

def game_development_full_projects(request):
    game_dev_hashtag = get_object_or_404(Hashtag, name='game-development')
    full_projects_hashtag = get_object_or_404(Hashtag, name='full-projects')
    press_releases = PressRelease.objects.filter(hashtags=game_dev_hashtag).filter(hashtags=full_projects_hashtag)
    editorials = Editorial.objects.filter(hashtags=game_dev_hashtag).filter(hashtags=full_projects_hashtag)
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'game_development_full_projects.html', context)

def blockchain_full_projects(request):
    blockchain_hashtag = get_object_or_404(Hashtag, name='blockchain')
    full_projects_hashtag = get_object_or_404(Hashtag, name='full-projects')
    
    press_releases = PressRelease.objects.filter(hashtags=blockchain_hashtag).filter(hashtags=full_projects_hashtag)
    editorials = Editorial.objects.filter(hashtags=blockchain_hashtag).filter(hashtags=full_projects_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'blockchain_full-projects.html', context)

def blockchain_solidity(request):
    blockchain_hashtag = get_object_or_404(Hashtag, name='blockchain')
    solidity_hashtag = get_object_or_404(Hashtag, name='solidity')

    press_releases = PressRelease.objects.filter(hashtags=blockchain_hashtag).filter(hashtags=solidity_hashtag)
    editorials = Editorial.objects.filter(hashtags=blockchain_hashtag).filter(hashtags=solidity_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'blockchain_solidity.html', context)

def blockchain_dao(request):
    blockchain_hashtag = get_object_or_404(Hashtag, name='blockchain')
    dao_hashtag = get_object_or_404(Hashtag, name='dao')

    press_releases = PressRelease.objects.filter(hashtags=blockchain_hashtag).filter(hashtags=dao_hashtag)
    editorials = Editorial.objects.filter(hashtags=blockchain_hashtag).filter(hashtags=dao_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'blockchain_dao.html', context)

def blockchain_nft(request):
    blockchain_hashtag = get_object_or_404(Hashtag, name='blockchain')
    nft_hashtag = get_object_or_404(Hashtag, name='nft')

    press_releases = PressRelease.objects.filter(hashtags=blockchain_hashtag).filter(hashtags=nft_hashtag)
    editorials = Editorial.objects.filter(hashtags=blockchain_hashtag).filter(hashtags=nft_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'blockchain_nft.html', context)

def blockchain_dapps(request):
    blockchain_hashtag = get_object_or_404(Hashtag, name='blockchain')
    dapps_hashtag = get_object_or_404(Hashtag, name='dapps')

    press_releases = PressRelease.objects.filter(hashtags=blockchain_hashtag).filter(hashtags=dapps_hashtag)
    editorials = Editorial.objects.filter(hashtags=blockchain_hashtag).filter(hashtags=dapps_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'blockchain_dapps.html', context)

def blockchain_web3_frameworks(request):
    blockchain_hashtag = get_object_or_404(Hashtag, name='blockchain')
    web3_frameworks_hashtag = get_object_or_404(Hashtag, name='web3-frameworks')

    press_releases = PressRelease.objects.filter(hashtags=blockchain_hashtag).filter(hashtags=web3_frameworks_hashtag)
    editorials = Editorial.objects.filter(hashtags=blockchain_hashtag).filter(hashtags=web3_frameworks_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'blockchain_web3_frameworks.html', context)

def automatization_full_projects(request):
    automatization_hashtag = get_object_or_404(Hashtag, name='automatization')
    full_projects_hashtag = get_object_or_404(Hashtag, name='full-projects')
    press_releases = PressRelease.objects.filter(hashtags=automatization_hashtag).filter(hashtags=full_projects_hashtag)
    editorials = Editorial.objects.filter(hashtags=automatization_hashtag).filter(hashtags=full_projects_hashtag)
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)
    context = {
        'items': paged_items,
    }
    return render(request, 'automatization_full_projects.html', context)

def automatization_bots(request):
    automatization_hashtag = get_object_or_404(Hashtag, name='automatization')
    bots_hashtag = get_object_or_404(Hashtag, name='bots')

    press_releases = PressRelease.objects.filter(hashtags=automatization_hashtag).filter(hashtags=bots_hashtag)
    editorials = Editorial.objects.filter(hashtags=automatization_hashtag).filter(hashtags=bots_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'automatization_bots.html', context)

def automatization_scripting_and_automation(request):
    automatization_hashtag = get_object_or_404(Hashtag, name='automatization')
    scripting_and_automation_hashtag = get_object_or_404(Hashtag, name='scripting-and-automation')

    press_releases = PressRelease.objects.filter(hashtags=automatization_hashtag).filter(hashtags=scripting_and_automation_hashtag)
    editorials = Editorial.objects.filter(hashtags=automatization_hashtag).filter(hashtags=scripting_and_automation_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'automatization_scripting_and_automation.html', context)

def automatization_workflow_automation(request):
    automatization_hashtag = get_object_or_404(Hashtag, name='automatization')
    workflow_automation_hashtag = get_object_or_404(Hashtag, name='workflow-automation')
    
    press_releases = PressRelease.objects.filter(hashtags=automatization_hashtag).filter(hashtags=workflow_automation_hashtag)
    editorials = Editorial.objects.filter(hashtags=automatization_hashtag).filter(hashtags=workflow_automation_hashtag)
    
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)
    
    context = {
        'items': paged_items,
    }
    
    return render(request, 'automatization_workflow_automation.html', context)

def automatization_robotic_process_automation(request):
    automatization_hashtag = get_object_or_404(Hashtag, name='automatization')
    rpa_hashtag = get_object_or_404(Hashtag, name='robotic-process-automation')
    
    press_releases = PressRelease.objects.filter(hashtags=automatization_hashtag).filter(hashtags=rpa_hashtag)
    editorials = Editorial.objects.filter(hashtags=automatization_hashtag).filter(hashtags=rpa_hashtag)
    
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)
    
    context = {
        'items': paged_items,
    }
    
    return render(request, 'automatization_robotic_process_automation.html', context)

def automatization_email_automation(request):
    automatization_hashtag = get_object_or_404(Hashtag, name='automatization')
    email_automation_hashtag = get_object_or_404(Hashtag, name='email-automation')

    press_releases = PressRelease.objects.filter(hashtags=automatization_hashtag).filter(hashtags=email_automation_hashtag)
    editorials = Editorial.objects.filter(hashtags=automatization_hashtag).filter(hashtags=email_automation_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'automatization_email_automation.html', context)

def automatization_data_automation(request):
    automatization_hashtag = get_object_or_404(Hashtag, name='automatization')
    data_automation_hashtag = get_object_or_404(Hashtag, name='data-automation')
    press_releases = PressRelease.objects.filter(hashtags=automatization_hashtag).filter(hashtags=data_automation_hashtag)
    editorials = Editorial.objects.filter(hashtags=automatization_hashtag).filter(hashtags=data_automation_hashtag)
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)
    
    context = {
        'items': paged_items,
    }
    
    return render(request, 'automatization_data_automation.html', context)

def automatization_automated_reporting(request):
    automatization_hashtag = get_object_or_404(Hashtag, name='automatization')
    automated_reporting_hashtag = get_object_or_404(Hashtag, name='automated-reporting')

    press_releases = PressRelease.objects.filter(hashtags=automatization_hashtag).filter(hashtags=automated_reporting_hashtag)
    editorials = Editorial.objects.filter(hashtags=automatization_hashtag).filter(hashtags=automated_reporting_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'automatization_automated_reporting.html', context)

def automatization_home_automation(request):
    automatization_hashtag = get_object_or_404(Hashtag, name='automatization')
    home_automation_hashtag = get_object_or_404(Hashtag, name='home-automation')
    
    press_releases = PressRelease.objects.filter(hashtags=automatization_hashtag).filter(hashtags=home_automation_hashtag)
    editorials = Editorial.objects.filter(hashtags=automatization_hashtag).filter(hashtags=home_automation_hashtag)
    
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'automatization_home_automation.html', context)

def databases_mysql(request):
    databases_hashtag = get_object_or_404(Hashtag, name='databases')
    mysql_hashtag = get_object_or_404(Hashtag, name='mysql')

    press_releases = PressRelease.objects.filter(hashtags=databases_hashtag).filter(hashtags=mysql_hashtag)
    editorials = Editorial.objects.filter(hashtags=databases_hashtag).filter(hashtags=mysql_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'databases_mysql.html', context)

def databases_postgresql(request):
    databases_hashtag = get_object_or_404(Hashtag, name='databases')
    postgresql_hashtag = get_object_or_404(Hashtag, name='postgresql')

    press_releases = PressRelease.objects.filter(hashtags=databases_hashtag).filter(hashtags=postgresql_hashtag)
    editorials = Editorial.objects.filter(hashtags=databases_hashtag).filter(hashtags=postgresql_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'databases_postgresql.html', context)

def databases_sqlite(request):
    databases_hashtag = get_object_or_404(Hashtag, name='databases')
    sqlite_hashtag = get_object_or_404(Hashtag, name='sqlite')

    press_releases = PressRelease.objects.filter(hashtags=databases_hashtag).filter(hashtags=sqlite_hashtag)
    editorials = Editorial.objects.filter(hashtags=databases_hashtag).filter(hashtags=sqlite_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'databases_sqlite.html', context)

def databases_realm(request):
    databases_hashtag = get_object_or_404(Hashtag, name='databases')
    realm_hashtag = get_object_or_404(Hashtag, name='realm')

    press_releases = PressRelease.objects.filter(hashtags=databases_hashtag).filter(hashtags=realm_hashtag)
    editorials = Editorial.objects.filter(hashtags=databases_hashtag).filter(hashtags=realm_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'databases_realm.html', context)

def databases_ipfs(request):
    databases_hashtag = get_object_or_404(Hashtag, name='databases')
    ipfs_hashtag = get_object_or_404(Hashtag, name='ipfs')

    press_releases = PressRelease.objects.filter(hashtags=databases_hashtag).filter(hashtags=ipfs_hashtag)
    editorials = Editorial.objects.filter(hashtags=databases_hashtag).filter(hashtags=ipfs_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'databases_ipfs.html', context)

def databases_firebase(request):
    databases_hashtag = get_object_or_404(Hashtag, name='databases')
    firebase_hashtag = get_object_or_404(Hashtag, name='firebase')

    press_releases = PressRelease.objects.filter(hashtags=databases_hashtag).filter(hashtags=firebase_hashtag)
    editorials = Editorial.objects.filter(hashtags=databases_hashtag).filter(hashtags=firebase_hashtag)

    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'databases_firebase.html', context)

def databases_full_projects(request):
    databases_hashtag = get_object_or_404(Hashtag, name='databases')
    full_projects_hashtag = get_object_or_404(Hashtag, name='full-projects')

    press_releases = PressRelease.objects.filter(hashtags=databases_hashtag).filter(hashtags=full_projects_hashtag)
    editorials = Editorial.objects.filter(hashtags=databases_hashtag).filter(hashtags=full_projects_hashtag)

    combined_items = list(press_releases) + list(editorials)
    
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'databases_full_projects.html', context)

def datascience_full_projects(request):
    data_science_hashtag = get_object_or_404(Hashtag, name='data-science')
    full_projects_hashtag = get_object_or_404(Hashtag, name='full-projects')

    press_releases = PressRelease.objects.filter(hashtags=data_science_hashtag).filter(hashtags=full_projects_hashtag)
    editorials = Editorial.objects.filter(hashtags=data_science_hashtag).filter(hashtags=full_projects_hashtag)

    combined_items = list(press_releases) + list(editorials)

    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'datascience_full_projects.html', context)

def datascience_Data_Manipulation_Analysis(request):
    data_science_hashtag = get_object_or_404(Hashtag, name='data-science')
    data_manipulation_analysis_hashtag = get_object_or_404(Hashtag, name='Data-Manipulation-Analysis')

    press_releases = PressRelease.objects.filter(hashtags=data_science_hashtag).filter(hashtags=data_manipulation_analysis_hashtag)
    editorials = Editorial.objects.filter(hashtags=data_science_hashtag).filter(hashtags=data_manipulation_analysis_hashtag)

    combined_items = list(press_releases) + list(editorials)
    
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'datascience_Data_Manipulation_Analysis.html', context)


def datascience_machine_learning(request):
    # Retrieve the desired hashtags
    data_science_hashtag = get_object_or_404(Hashtag, name='data-science')
    machine_learning_hashtag = get_object_or_404(Hashtag, name='machine-learning')

    # Filter PressRelease and Editorial instances based on hashtags
    press_releases = PressRelease.objects.filter(hashtags=data_science_hashtag).filter(hashtags=machine_learning_hashtag)
    editorials = Editorial.objects.filter(hashtags=data_science_hashtag).filter(hashtags=machine_learning_hashtag)

    # Combine the querysets
    combined_items = list(press_releases) + list(editorials)

    # Implement pagination
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'datascience_machine_learning.html', context)

def datascience_data_visualization(request):
    data_science_hashtag = get_object_or_404(Hashtag, name='data-science')
    data_visualization_hashtag = get_object_or_404(Hashtag, name='data-visualization')
    press_releases = PressRelease.objects.filter(hashtags=data_science_hashtag).filter(hashtags=data_visualization_hashtag)
    editorials = Editorial.objects.filter(hashtags=data_science_hashtag).filter(hashtags=data_visualization_hashtag)
    combined_items = list(press_releases) + list(editorials)
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'datascience_data_visualization.html', context)


def datascience_natural_language_processing(request):
    # Retrieve the desired hashtags
    data_science_hashtag = get_object_or_404(Hashtag, name='data-science')
    natural_language_processing_hashtag = get_object_or_404(Hashtag, name='natural-language-processing')

    # Filter PressRelease and Editorial instances based on hashtags
    press_releases = PressRelease.objects.filter(hashtags=data_science_hashtag).filter(hashtags=natural_language_processing_hashtag)
    editorials = Editorial.objects.filter(hashtags=data_science_hashtag).filter(hashtags=natural_language_processing_hashtag)

    # Combine the querysets
    combined_items = list(press_releases) + list(editorials)

    # Implement pagination
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'datascience_natural_language_processing.html', context)

def datascience_big_data_frameworks(request):
    # Retrieve the desired hashtags
    data_science_hashtag = get_object_or_404(Hashtag, name='data-science')
    big_data_frameworks_hashtag = get_object_or_404(Hashtag, name='big-data-frameworks')

    # Filter PressRelease and Editorial instances based on hashtags
    press_releases = PressRelease.objects.filter(hashtags=data_science_hashtag).filter(hashtags=big_data_frameworks_hashtag)
    editorials = Editorial.objects.filter(hashtags=data_science_hashtag).filter(hashtags=big_data_frameworks_hashtag)

    # Combine the querysets
    combined_items = list(press_releases) + list(editorials)

    # Implement pagination
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'datascience_big_data_frameworks.html', context)

def datascience_big_data_frameworks(request):
    # Retrieve the desired hashtags
    data_science_hashtag = get_object_or_404(Hashtag, name='data-science')
    big_data_frameworks_hashtag = get_object_or_404(Hashtag, name='big-data-frameworks')

    # Filter PressRelease and Editorial instances based on hashtags
    press_releases = PressRelease.objects.filter(hashtags=data_science_hashtag).filter(hashtags=big_data_frameworks_hashtag)
    editorials = Editorial.objects.filter(hashtags=data_science_hashtag).filter(hashtags=big_data_frameworks_hashtag)

    # Combine the querysets
    combined_items = list(press_releases) + list(editorials)

    # Implement pagination
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'datascience_big_data_frameworks.html', context)

def datascience_workflow_experiment_management(request):
    # Retrieve the desired hashtags
    data_science_hashtag = get_object_or_404(Hashtag, name='data-science')
    workflow_experiment_management_hashtag = get_object_or_404(Hashtag, name='workflow-experiment-managment')

    # Filter PressRelease and Editorial instances based on hashtags
    press_releases = PressRelease.objects.filter(hashtags=data_science_hashtag).filter(hashtags=workflow_experiment_management_hashtag)
    editorials = Editorial.objects.filter(hashtags=data_science_hashtag).filter(hashtags=workflow_experiment_management_hashtag)

    # Combine the querysets
    combined_items = list(press_releases) + list(editorials)

    # Implement pagination
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'datascience_workflow_experiment_management.html', context)

def ai(request):
    # Retrieve the desired hashtag
    ai_hashtag = get_object_or_404(Hashtag, name='ai')

    # Filter PressRelease and Editorial instances based on the hashtag
    press_releases = PressRelease.objects.filter(hashtags=ai_hashtag)
    editorials = Editorial.objects.filter(hashtags=ai_hashtag)

    # Combine the querysets
    combined_items = list(press_releases) + list(editorials)

    # Implement pagination
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'ai.html', context)

def systems_ubuntu(request):
    # Retrieve the desired hashtags
    systems_hashtag = get_object_or_404(Hashtag, name='systems')
    ubuntu_hashtag = get_object_or_404(Hashtag, name='ubuntu')

    # Filter PressRelease and Editorial instances based on hashtags
    press_releases = PressRelease.objects.filter(hashtags=systems_hashtag).filter(hashtags=ubuntu_hashtag)
    editorials = Editorial.objects.filter(hashtags=systems_hashtag).filter(hashtags=ubuntu_hashtag)

    # Combine the querysets
    combined_items = list(press_releases) + list(editorials)

    # Implement pagination
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'systems_ubuntu.html', context)

def systems_ubuntu_server(request):
    # Retrieve the desired hashtags
    systems_hashtag = get_object_or_404(Hashtag, name='systems')
    ubuntu_server_hashtag = get_object_or_404(Hashtag, name='ubuntu-server')

    # Filter PressRelease and Editorial instances based on hashtags
    press_releases = PressRelease.objects.filter(hashtags=systems_hashtag).filter(hashtags=ubuntu_server_hashtag)
    editorials = Editorial.objects.filter(hashtags=systems_hashtag).filter(hashtags=ubuntu_server_hashtag)

    # Combine the querysets
    combined_items = list(press_releases) + list(editorials)

    # Implement pagination
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'systems_ubuntu_server.html', context)

def systems_windows(request):
    # Retrieve the desired hashtags
    systems_hashtag = get_object_or_404(Hashtag, name='systems')
    windows_hashtag = get_object_or_404(Hashtag, name='windows')

    # Filter PressRelease and Editorial instances based on hashtags
    press_releases = PressRelease.objects.filter(hashtags=systems_hashtag).filter(hashtags=windows_hashtag)
    editorials = Editorial.objects.filter(hashtags=systems_hashtag).filter(hashtags=windows_hashtag)

    # Combine the querysets
    combined_items = list(press_releases) + list(editorials)

    # Implement pagination
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'systems_windows.html', context)

def systems_linux_mint(request):
    # Retrieve the desired hashtags
    systems_hashtag = get_object_or_404(Hashtag, name='systems')
    linux_mint_hashtag = get_object_or_404(Hashtag, name='linux-mint')

    # Filter PressRelease and Editorial instances based on hashtags
    press_releases = PressRelease.objects.filter(hashtags=systems_hashtag).filter(hashtags=linux_mint_hashtag)
    editorials = Editorial.objects.filter(hashtags=systems_hashtag).filter(hashtags=linux_mint_hashtag)

    # Combine the querysets
    combined_items = list(press_releases) + list(editorials)

    # Implement pagination
    paginator = Paginator(combined_items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_items = paginator.get_page(page_number)

    context = {
        'items': paged_items,
    }

    return render(request, 'systems_linux_mint.html', context)

def courses_python(request):
    # Retrieve the desired hashtags
    course_hashtag = get_object_or_404(Hashtag, name='courses')
    python_hashtag = get_object_or_404(Hashtag, name='python')

    # Filter NewestCourse instances based on hashtags
    newest_courses = NewestCourse.objects.filter(hashtags=course_hashtag).filter(hashtags=python_hashtag)

    # Implement pagination
    paginator = Paginator(newest_courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_python.html', context)

def courses_html_css_js(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    html_css_js_hashtag = get_object_or_404(Hashtag, name='html-css-js')

    # Filter NewestCourse instances based on hashtags
    courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=html_css_js_hashtag)

    # Implement pagination
    paginator = Paginator(courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_html_css_js.html', context)

def courses_vue_js(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    vue_js_hashtag = get_object_or_404(Hashtag, name='vue-js')

    # Filter NewestCourse instances based on hashtags
    courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=vue_js_hashtag)

    # Implement pagination
    paginator = Paginator(courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_vue_js.html', context)

def courses_react_js(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    react_js_hashtag = get_object_or_404(Hashtag, name='react-js')

    # Filter NewestCourse instances based on hashtags
    courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=react_js_hashtag)

    # Implement pagination
    paginator = Paginator(courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_react_js.html', context)

def courses_vite(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    vite_hashtag = get_object_or_404(Hashtag, name='vite')

    # Filter NewestCourse instances based on hashtags
    courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=vite_hashtag)

    # Implement pagination
    paginator = Paginator(courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_vite.html', context)

def courses_next_js(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    next_js_hashtag = get_object_or_404(Hashtag, name='next-js')

    # Filter NewestCourse instances based on hashtags
    newest_courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=next_js_hashtag)

    # Implement pagination
    paginator = Paginator(newest_courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_next_js.html', context)

def courses_kotlin(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    kotlin_hashtag = get_object_or_404(Hashtag, name='kotlin')

    # Filter NewestCourse instances based on hashtags
    courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=kotlin_hashtag)

    # Implement pagination
    paginator = Paginator(courses, 10)  # 10 courses per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_kotlin.html', context)

def courses_flutter(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    flutter_hashtag = get_object_or_404(Hashtag, name='flutter')

    # Filter NewestCourse instances based on hashtags
    newest_courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=flutter_hashtag)

    # Implement pagination
    paginator = Paginator(newest_courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_flutter.html', context)

def courses_java(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    java_hashtag = get_object_or_404(Hashtag, name='java')

    # Filter NewestCourse instances based on hashtags
    newest_courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=java_hashtag)

    # Implement pagination
    paginator = Paginator(newest_courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_java.html', context)

def courses_ai(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    ai_hashtag = get_object_or_404(Hashtag, name='ai')

    # Filter NewestCourse instances based on hashtags
    newest_courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=ai_hashtag)

    # Implement pagination
    paginator = Paginator(newest_courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'newest_courses': paged_courses,
    }

    return render(request, 'courses_ai.html', context)

def courses_databases(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    databases_hashtag = get_object_or_404(Hashtag, name='databases')

    # Filter NewestCourse instances based on hashtags
    newest_courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=databases_hashtag)

    # Implement pagination
    paginator = Paginator(newest_courses, 10)  # 10 courses per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_databases.html', context)

def courses_docker(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    docker_hashtag = get_object_or_404(Hashtag, name='docker')

    # Filter NewestCourse instances based on hashtags
    courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=docker_hashtag)

    # Implement pagination
    paginator = Paginator(courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_docker.html', context)

def courses_video_graphic(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    video_graphic_hashtag = get_object_or_404(Hashtag, name='video-graphic')

    # Filter NewestCourse instances based on hashtags
    newest_courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=video_graphic_hashtag)

    # Implement pagination
    paginator = Paginator(newest_courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_video_graphic.html', context)

def courses_cplusplus(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    cplusplus_hashtag = get_object_or_404(Hashtag, name='c++')

    # Filter NewestCourse instances based on hashtags
    newest_courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=cplusplus_hashtag)

    # Implement pagination
    paginator = Paginator(newest_courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_cplusplus.html', context)

def courses_wordpress(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    wordpress_hashtag = get_object_or_404(Hashtag, name='wordpress')

    # Filter NewestCourse instances based on hashtags
    newest_courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=wordpress_hashtag)

    # Implement pagination
    paginator = Paginator(newest_courses, 10)  # 10 courses per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_wordpress.html', context)

def courses_blockchain(request):
    # Retrieve the desired hashtags
    courses_hashtag = get_object_or_404(Hashtag, name='courses')
    blockchain_hashtag = get_object_or_404(Hashtag, name='blockchain')

    # Filter NewestCourse instances based on hashtags
    newest_courses = NewestCourse.objects.filter(hashtags=courses_hashtag).filter(hashtags=blockchain_hashtag)

    # Implement pagination
    paginator = Paginator(newest_courses, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paged_courses = paginator.get_page(page_number)

    context = {
        'courses': paged_courses,
    }

    return render(request, 'courses_blockchain.html', context)