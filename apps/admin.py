from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.models import (
    User, UserAddress,
    Catalogue, Category, CubCategory,
    Product, ProductSize, ProductValue, ProductColor, ProductImage, ProductComment, ProductLike,
    Order, OrderItem,
    Advertisement,
)


# ===================== INLINES =====================

class UserAddressInline(admin.TabularInline):
    model = UserAddress
    extra = 1
    fields = ('latitude', 'longitude')


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    fields = ('name',)
    show_change_link = True


class CubCategoryInline(admin.TabularInline):
    model = CubCategory
    extra = 1
    fields = ('name', 'image', 'is_active_dashboard')
    show_change_link = True


class ProductValueInline(admin.TabularInline):
    model = ProductValue
    extra = 1
    fields = ('size', 'price', 'quantity', 'characteristics')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'color', 'is_active', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px; border-radius:6px;" />', obj.image.url)
        return '-'
    preview.short_description = "Ko'rinish"


class ProductCommentInline(admin.TabularInline):
    model = ProductComment
    extra = 0
    fields = ('user', 'comment')
    readonly_fields = ('user', 'comment')
    can_delete = True


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'price', 'quantity', 'product_size', 'product_color')


# ===================== USER =====================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserAddressInline]
    list_display = ('username', 'email', 'full_name', 'role', 'phone_number', 'is_active', 'profile_preview')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone_number', 'first_name', 'last_name')
    list_editable = ('role', 'is_active')
    ordering = ('-date_joined',)

    fieldsets = (
        (_('Asosiy ma\'lumotlar'), {
            'fields': ('username', 'password')
        }),
        (_('Shaxsiy ma\'lumotlar'), {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'birthday', 'user_profile_image', 'profile_preview')
        }),
        (_('Rol va ruxsatlar'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Muhim sanalar'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('profile_preview', 'last_login', 'date_joined')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or '-'
    full_name.short_description = 'To\'liq ism'

    def profile_preview(self, obj):
        if obj.user_profile_image:
            return format_html('<img src="{}" style="height:70px; border-radius:50%;" />', obj.user_profile_image.url)
        return '-'
    profile_preview.short_description = 'Rasm'


# ===================== CATEGORY =====================

@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
    list_display = ('name', 'Icon', 'category_count')
    search_fields = ('name',)

    def category_count(self, obj):
        return obj.category_set.count()
    category_count.short_description = 'Kategoriyalar soni'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CubCategoryInline]
    list_display = ('name', 'catalogue', 'subcategory_count')
    list_filter = ('catalogue',)
    search_fields = ('name',)
    autocomplete_fields = ('catalogue',)

    def subcategory_count(self, obj):
        return obj.cubcategory_set.count()
    subcategory_count.short_description = 'Subkategoriyalar'


@admin.register(CubCategory)
class CubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active_dashboard', 'image_preview')
    list_filter = ('is_active_dashboard', 'category__catalogue')
    search_fields = ('name',)
    list_editable = ('is_active_dashboard',)
    autocomplete_fields = ('category',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px; border-radius:6px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Rasm'


# ===================== PRODUCT =====================

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'color_preview')
    search_fields = ('name',)

    def color_preview(self, obj):
        if obj.color:
            return format_html(
                '<div style="width:30px; height:30px; background:{}; border-radius:50%; border:1px solid #ccc;"></div>',
                obj.color
            )
        return '-'
    color_preview.short_description = 'Rang'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductValueInline, ProductCommentInline]
    list_display = ('name', 'brand', 'subcategory', 'is_active', 'main_image')
    list_filter = ('is_active', 'subcategory__category__catalogue', 'subcategory__category', 'subcategory', 'brand')
    search_fields = ('name', 'brand', 'description')
    list_editable = ('is_active',)
    autocomplete_fields = ('subcategory',)
    readonly_fields = ('main_image',)

    fieldsets = (
        ('Mahsulot ma\'lumotlari', {
            'fields': ('name', 'brand', 'subcategory', 'description', 'is_active')
        }),
        ('Asosiy rasm', {
            'fields': ('main_image',),
        }),
    )

    def main_image(self, obj):
        img = obj.product_images.filter(is_active=True).first()
        if img and img.image:
            return format_html('<img src="{}" style="height:80px; border-radius:8px;" />', img.image.url)
        return '-'
    main_image.short_description = 'Asosiy rasm'


@admin.register(ProductLike)
class ProductLikeAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('product__name', 'user__username')
    list_editable = ('is_active',)


# ===================== ORDER =====================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'status', 'created_at', 'item_count', 'address')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__phone_number')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Buyurtma', {
            'fields': ('user', 'address', 'status', 'created_at')
        }),
    )

    def item_count(self, obj):
        return obj.orderitem_set.count()
    item_count.short_description = 'Mahsulotlar soni'


# ===================== ADVERTISEMENT =====================

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'image_preview')
    list_filter = ('category__category__catalogue',)
    search_fields = ('category__name',)
    autocomplete_fields = ('category',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:80px; border-radius:8px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Rasm ko\'rinishi'