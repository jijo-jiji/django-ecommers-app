from django.contrib import admin
from .models import Category ,Customer,Product,Order,Profile
from django.contrib.auth.models import User
admin.site.register( Category   )

admin.site.register(  Customer  )

admin.site.register(   Product )

admin.site.register(  Order  )
admin.site.register(  Profile  )

# mix profile info and user info
class ProfileIline(admin.StackedInline):
    model = Profile
# extend user models
class UserAdmin(admin.ModelAdmin):
    model = User
    field =["username","first_name","last_name","email"]
    inlines =[ProfileIline]

# unregister the old ways   
admin.site.unregister(User)
# re register the new ways
admin.site.register(User,UserAdmin)
