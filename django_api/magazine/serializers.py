from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, Orders, ProductOrderPosition, ProductReviews


class ProductOrderPositionSerializer(serializers.Serializer):

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product.id"
    )

    name = serializers.CharField(source='product.name', read_only=True)
    quantity = serializers.IntegerField(min_value=1, max_value=5)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price', read_only=True)

class OrderSerializer(serializers.ModelSerializer):

    positions = ProductOrderPositionSerializer(many=True)
    order_sum = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    creator = serializers.CharField(source='creator.username', read_only=True)


    class Meta:
        model = Orders
        fields = ('id', 'status', 'creator', 'order_sum', 'positions')

    def validate(self, attrs):
        positions = attrs.get('positions')
        if not positions:
            raise ValidationError({'products': 'No products'})

        products_ids = {product['product']['id'].id for product in positions}
        if len(products_ids) != len(positions):
            raise ValidationError({'products': 'There are duplicates in the order'})

        return attrs

    def create(self, validated_data):
        products = validated_data.pop('positions')
        validated_data["creator"] = self.context["request"].user
        order = super().create(validated_data)

        for product_pos_data in products:
            ProductOrderPosition.objects.create(
                quantity=product_pos_data['quantity'],
                product=product_pos_data['product']['id'],
                order=order,

            )

        return order


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):

    review = serializers.CharField(source='review.id', read_only=True)
    #review = serializers.RelatedField(read_only=True)
    #reviews = serializers.PrimaryKeyRelatedField(read_only=True)

    creator = serializers.ReadOnlyField(source='creator.id')

    class Meta:
        model = ProductReviews
        fields = ('id', 'review', 'creator', 'text', 'mark')

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)
