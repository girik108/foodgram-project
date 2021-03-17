from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class LoginPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):

    def has_permission(self):
        obj = self.get_object()
        return self.request.user == obj.author


class ShopListPermission(PermissionRequiredMixin):

    def has_permission(self):
        obj = self.get_object()
        if self.request.user.is_authenticated:
            return self.request.user == obj.user

        return obj.session_key == self.request.session.session_key