from django.db.models.signals import post_save
from django.dispatch import receiver

from Shop.settings import QUANTITY_SIGNALS_AUTO_ADD_GOODS_IN_STOCK_WHEN_GET_RID
from ishop.models import Good, Purchase


@receiver(post_save, sender=Purchase)
def post_save_add_goods_in_stock(sender, instance, created, **kwargs):
    """This signal adds 12 pcs in stock for goods,
    wich have been run out of stock recently after current purchase"""
    if created:
        if instance.good.in_stock < 1:
            instance.good.in_stock = QUANTITY_SIGNALS_AUTO_ADD_GOODS_IN_STOCK_WHEN_GET_RID
            instance.good.save()
