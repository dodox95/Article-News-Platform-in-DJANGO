from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from backend1 import views as backend1_views

from backend1 import views
import os

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    path('api/', include('backend1.urls')),
    path('', backend1_views.index, name='index'),
    
    path('web-development/full-projects/', views.web_development_full_courses, name='web_development_full_courses'),
    path('web-development/backend/django/', views.web_development_backend_django, name='web_development_backend_django'),
    path('web-development/backend/flask/', views.web_development_backend_flask, name='web_development_backend_flask'),
    path('web-development/backend/express-js/', views.web_development_backend_express_js, name='web_development_backend_express_js'),
    path('web-development/backend/php/', views.web_development_backend_php, name='web_development_backend_php'),
    path('web-development/frontend/html-css-js/', views.web_development_frontend_html_css_js, name='web_development_frontend_html_css_js'),
    path('web-development/frontend/react-js/', views.web_development_frontend_react_js, name='web_development_frontend_react'),
    path('web-development/frontend/vue-js/', views.web_development_frontend_vue_js, name='web_development_frontend_vue'),
    path('web-development/frontend/next-js/', views.web_development_frontend_next_js, name='web_development_frontend_next_js'),
    path('web-development/frontend/bootstrap/', views.web_development_frontend_bootstrap, name='web_development_frontend_bootstrap'),
    path('web-development/frontend/tailwind/', views.web_development_frontend_tailwind, name='web_development_frontend_tailwind'),
    path('web-development/frontend/three-js/', views.web_development_frontend_three_js, name='web_development_frontend_three_js'),
    path('web-development/frontend/vite/', views.web_development_frontend_vite, name='web_development_frontend_vite'),
    path('web-development/wordpress/full-projects/', views.web_development_wordpress_full_projects, name='web_development_wordpress_full_projects'),
    path('web-development/wordpress/plugins/', views.web_development_wordpress_plugins, name='web_development_wordpress_plugins'),


    path('mobile-development/full-projects/', views.mobile_development_full_projects, name='mobile_development_full_projects'),
    path('mobile-development/java/', views.mobile_development_java, name='mobile_development_java'),
    path('mobile-development/kotlin/', views.mobile_development_kotlin, name='mobile_development_kotlin'),
    path('mobile-development/flutter/', views.mobile_development_flutter, name='mobile_development_flutter'),
    path('mobile-development/react-native/', views.mobile_development_react_native, name='mobile_development_react_native'),
    
    path('game-development/unity/', views.game_development_unity, name='game_development_unity'),
    path('game-development/unreal-engine/', views.game_development_unreal_engine, name='game_development_unreal_engine'),
    path('game-development/rpg-maker/', views.game_development_rpg_maker, name='game_development_rpg_maker'),
    path('game-development/godot/', views.game_development_godot, name='game_development_godot'),
    path('game-development/phaser/', views.game_development_phaser, name='game_development_phaser'),
    path('game-development/full-projects/', views.game_development_full_projects, name='game_development_full_projects'),

    path('blockchain/full-projects/', views.blockchain_full_projects, name='blockchain_full_projects'),
    path('blockchain/solidity/', views.blockchain_solidity, name='blockchain_solidity'),
    path('blockchain/dao/', views.blockchain_dao, name='blockchain_dao'),
    path('blockchain/nft/', views.blockchain_nft, name='blockchain_nft'),
    path('blockchain/dapps/', views.blockchain_dapps, name='blockchain_dapps'),
    path('blockchain/web3-frameworks/', views.blockchain_web3_frameworks, name='blockchain_web3_frameworks'),
    
    
    path('automatization/full-projects/', views.automatization_full_projects, name='automatization_full_projects'),
    path('automatization/bots/', views.automatization_bots, name='automatization_bots'),
    path('automatization/scripting-and-automation/', views.automatization_scripting_and_automation, name='automatization_scripting_and_automation'),
    path('automatization/workflow-automation/', views.automatization_workflow_automation, name='automatization_workflow_automation'),
    path('automatization/robotic-process-automation/', views.automatization_robotic_process_automation, name='automatization_rpa'),
    path('automatization/email-automation/', views.automatization_email_automation, name='automatization_email_automation'),
    path('automatization/data-automation/', views.automatization_data_automation, name='automatization_data_automation'),
    path('automatization/automated-reporting/', views.automatization_automated_reporting, name='automatization_automated_reporting'),
    path('automatization/home-automation/', views.automatization_home_automation, name='automatization_home_automation'),
    
    path('databases/mysql/', views.databases_mysql, name='databases_mysql'),
    path('databases/postgresql/', views.databases_postgresql, name='databases_postgresql'),
    path('databases/sqlite/', views.databases_sqlite, name='databases_sqlite'),
    path('databases/realm/', views.databases_realm, name='databases_realm'),
    path('databases/ipfs/', views.databases_ipfs, name='databases_ipfs'),
    path('databases/firebase/', views.databases_firebase, name='databases_firebase'),
    path('databases/full-projects/', views.databases_full_projects, name='databases_full_projects'),
    
    path('data-science/full-projects/', views.datascience_full_projects, name='datascience_full_projects'),    
    path('data-science/data-manipulation-analysis/', views.datascience_Data_Manipulation_Analysis, name='datascience_Data_Manipulation_Analysis'),
    path('data-science/machine-learning-deep-learning/', views.datascience_machine_learning, name='datascience_machine_learning'),
    path('data-science/data-visualization/', views.datascience_data_visualization, name='datascience_data_visualization'),
    path('data-science/natural-language-processing/', views.datascience_natural_language_processing, name='datascience_nlp'),
    path('data-science/big-data-frameworks/', views.datascience_big_data_frameworks, name='datascience_big_data_frameworks'),
    path('data-science/workflow-experiment-management/', views.datascience_workflow_experiment_management, name='datascience_workflow_experiment_management'),
    
    path('ai/', views.ai, name='ai'),
    
    path('systems/ubuntu/', views.systems_ubuntu, name='systems_ubuntu'),
    path('systems/ubuntu-server/', views.systems_ubuntu_server, name='systems_ubuntu_server'),
    path('systems/windows/', views.systems_windows, name='systems_windows'),
    path('systems/linux-mint/', views.systems_linux_mint, name='systems_linux_mint'),
    
    path('courses/python/', views.courses_python, name='courses_python'),
    path('courses/html-css-js/', views.courses_html_css_js, name='courses_html_css_js'),
    path('courses/vue-js/', views.courses_vue_js, name='courses_vue_js'),
    path('courses/react-js/', views.courses_react_js, name='courses_react_js'),
    path('courses/vite/', views.courses_vite, name='courses_vite'),
    path('courses/next-js/', views.courses_next_js, name='courses_next_js'),
    path('courses/kotlin/', views.courses_kotlin, name='courses_kotlin'),
    path('courses/flutter/', views.courses_flutter, name='courses_flutter'),
    path('courses/java/', views.courses_java, name='courses_java'),
    path('courses/ai/', views.courses_ai, name='courses_ai'),
    path('courses/docker/', views.courses_docker, name='courses_docker'),
    path('courses/databases/', views.courses_databases, name='courses_databases'),
    path('courses/video-graphic/', views.courses_video_graphic, name='courses_video_graphic'),
    path('courses/blockchain/', views.courses_blockchain, name='courses_blockchain'),
    path('courses/c++/', views.courses_cplusplus, name='courses_cplusplus'),
    path('courses/wordpress/', views.courses_wordpress, name='courses_wordpress'),

]

if settings.DEBUG:
    urlpatterns += static('/_next/static/', document_root=os.path.join(settings.BASE_DIR, 'static/.next/static'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
