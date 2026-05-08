from django.db.models import Model, CharField, ImageField, BooleanField, ForeignKey, CASCADE


class Catalogue(Model):
    name = CharField(unique=True)
    Icon = CharField(max_length=255)

class Category(Model):
    catalogue = ForeignKey(Catalogue, on_delete=CASCADE)
    name = CharField(unique=True)

class CubCategory(Model):
    category = ForeignKey(Category,on_delete=CASCADE)
    name   = CharField(max_length=255)
    image = ImageField(upload_to='categories/',null=True,blank=True)
    is_active_dashboard = BooleanField(default=True)