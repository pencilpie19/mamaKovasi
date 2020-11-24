from django.db import models

# Create your models here.
class CoverPhotos(models.Model):
    file = models.ImageField(upload_to="cover",blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    first_sentence=models.CharField(max_length=80,verbose_name="İlk açıklama",blank=True,null=True,default="")
    second_sentence=models.CharField(max_length=80,verbose_name="İkinci açıklama",blank=True,null=True,default="")
    def get_path(self):
        return self.file.path