from django import forms

from user.models import User, Profile


class UserFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'gender', 'birth_year', 'birth_month', 'birth_day', 'location']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_max_distance(self):
        cleaned_data = self.clean()
        max_distance = cleaned_data.get('max_distance')
        min_distance = cleaned_data.get('min_distance')
        if max_distance < min_distance:
            raise forms.ValidationError('max distance 必须大于 min distance')
        return max_distance

    def clean_max_dating_age(self):
        cleaned_data = self.clean()
        max_dating_age = cleaned_data.get('max_dating_age')
        min_dating_age = cleaned_data.get('min_dating_age')
        if max_dating_age < min_dating_age:
            raise forms.ValidationError('max dating age 必须大于 min dating age')
        return max_dating_age
