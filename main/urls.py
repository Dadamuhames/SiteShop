from unicodedata import name
from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required, user_passes_test


urlpatterns = [
    path('', views.home, name='home-page'),
    path('product/<int:pk>', views.ProductsView.as_view(), name='products-page'),
    path('shop', views.CotalogView.as_view(), name='cotalog'),
    path('about', views.about_us, name='about_page'),
    path('contacts', views.contact_page, name='contact_page'),
    path('addproduct', views.addproduct, name='add-page'),
    path('del/<int:c_id>', views.removeFromCart, name='delete'),
    path('subscribe', views.addEmail, name='subscrb'),
    path('feedback', views.feedback, name='feedback'),
    path('like/<int:p_id>', views.like, name='like'),
    path('unlike/<int:p_id>', views.unlike, name='unlike'),
    path('shop/', views.FilterProducts.as_view(), name='cotalog_search'),
    path('addcomment', views.addComents, name='comments'),
    path('search', views.SearchResult.as_view(), name='search'),
    path('FAQ', views.faq, name='faq'),
    path('shipping&return', views.ship_and_returns, name='ship_return'),
    path('storepolicy', views.shop_policy, name='shop_policy'),
    path('addtocart', views.add_to_cart, name='add_to_cart'),
    path('newsletter', views.newsletter_page, name='send_mails'),
    path('get_modal_data/<int:p_id>', views.get_modal_data, name='modal-data'),
    path('get_categories/<int:id>', views.get_postcat, name='get_post_ctg'),
    path('comments-admin', user_passes_test(lambda u: u.is_superuser, login_url='home-page')(views.ControlComments.as_view()), name='comments-admin'),
    path('accept_coment', views.accept_comment, name='accept-comment'),
    path('get_atribut', views.get_atributs, name='get_atribut'),
    path('get_variant', views.get_variant, name='get_var'),
    path('cart/<int:pk>', views.CartDeteilView, name='cart-view')
]
