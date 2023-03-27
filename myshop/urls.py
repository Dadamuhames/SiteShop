from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf.urls import handler400, handler403, handler404, handler500

 
urlpatterns = [
    path('admin-panel/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('account.urls')),
    path('orders/', include('palpay.urls')),
    path('admin/', include('admins.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "myshop.views.page_not_found_view"
handler500 = "myshop.views.page_not_found_view_500"
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]