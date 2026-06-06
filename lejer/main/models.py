from django.db import models

# Create your models here.
from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY_CHOICES = [('APP', 'Apparatus'), ('REA', 'Reagent')]
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_stock_threshold = models.PositiveIntegerField(default=5)

    @property
    def total_stock(self):
        # Sums all quantities from associated batches
        return sum(batch.quantity for batch in self.batches.all())

    def __str__(self):
        return f"{self.name} ({self.sku})"

class Batch(models.Model):
    product = models.ForeignKey(Product, related_name='batches', on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.batch_number}"

class Order(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    invoice_no = models.CharField(max_length=20, unique=True)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.invoice_no} - {self.school.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price_at_order
