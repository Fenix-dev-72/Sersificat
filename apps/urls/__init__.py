from .profile import urlpatterns as profile_urls
from .category import urlpatterns as category_urls
from .product import urlpatterns as product_urls
from .auth import urlpatterns as auth_urls
from .ads import urlpatterns as ads_urls
from .order import urlpatterns as order_urls

urlpatterns = []

urlpatterns += product_urls
urlpatterns += auth_urls
urlpatterns += category_urls
urlpatterns += profile_urls
urlpatterns += ads_urls
urlpatterns += order_urls
