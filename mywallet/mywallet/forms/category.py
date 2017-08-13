from wtforms_alchemy import ModelForm

from mywallet import models


class CategoryForm(ModelForm):
    """Category model form"""
    class Meta:
        """WTForm Meta class"""
        model = models.Category
