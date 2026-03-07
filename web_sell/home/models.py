from django.db import models

# Create your models here.
class Product(models.Model):
    Id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100, db_column='name')
    Image_path = models.CharField(max_length=255, db_column='imge_path')
    cost = models.IntegerField(db_column='cost')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    class Meta:
        db_table = 'users'  # <-- tên bảng có sẵn
        managed = False  # không cho Django tạo/migrate bảng này

    def __str__(self):
        return self.name
    def get_img_path_and_cost(self, name):
        try:
            product = Product.objects.get(name=name)
            return product.Image_path, product.cost
        except Product.DoesNotExist:
            return None, None


        