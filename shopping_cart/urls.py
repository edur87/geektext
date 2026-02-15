from django.urls import path
from .views import ManageCartView, CartListView, CartSubtotalView

urlpatterns = [
    #POST to add, Delete to remove (expects body parameters)
    path('manage/', ManageCartView.as_view(), name='manage-cart'),

    #GET list of books (expects user_id in URL)
    path('list/<int:user_id>/', CartListView.as_view(), name='list-cart'),

    #GET subtotal (expects user_id in URL)
    path('subtotal/<int:user_id>/', CartSubtotalView.as_view(), name='cart-subtotal'),
]