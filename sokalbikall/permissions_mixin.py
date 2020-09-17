from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect


# vendor and admin access
class VendorRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'vendor' and not request.user.is_admin:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # redirect same path

        return super(VendorRequiredMixin, self).dispatch(
            request, *args, **kwargs)


# Admin access
class AdminRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # redirect same path

        return super(AdminRequiredMixin, self).dispatch(
            request, *args, **kwargs)


# Same User Required
# class SameUserRequiredMixin(AccessMixin):
#
#     def dispatch(self, request, *args, **kwargs):
#         Klass = request.__class__
#         if not request.user.is_admin:
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # redirect same path
#
#         return super(SameUserRequiredMixin, self).dispatch(
#             request, *args, **kwargs)
