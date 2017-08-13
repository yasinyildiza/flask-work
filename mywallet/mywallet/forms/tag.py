from wtforms_alchemy import ModelForm

from mywallet import models


class TagForm(ModelForm):
    """Tag model form"""
    class Meta:
        """WTForm Meta class"""
        model = models.Tag
