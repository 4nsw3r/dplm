from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, Orders, ProductOrderPosition, ProductReviews, Collections


class ProductOrderPositionSerializer(serializers.Serializer):

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product.id"
    )

    name = serializers.CharField(source='product.name', read_only=True)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price', read_only=True, min_value=1)

class OrderSerializer(serializers.ModelSerializer):

    positions = ProductOrderPositionSerializer(many=True)
    creator = serializers.CharField(source='creator.username', read_only=True)
    # pos_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=False,
    #                                              queryset=Product.objects.all(), source='products')

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

    def update(self, instance, validated_data):
        products = validated_data.pop('positions')
        for prod_data in validated_data:
            if Orders._meta.get_field(prod_data):
                setattr(instance, prod_data, validated_data[prod_data])
        ProductOrderPosition.objects.filter(order=instance).delete()
        for prod in products:
            position = dict(prod)
            ProductOrderPosition.objects.create(order=instance,
                                                product=position['product']['id'],
                                                quantity=prod['quantity'])
        instance.save()
        return instance



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source='creator.id')
    mark = serializers.IntegerField(min_value=1, max_value=5)


    class Meta:
        model = ProductReviews
        fields = ('id', 'review', 'creator', 'text', 'mark', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user

        user_objects = ProductReviews.objects.filter(creator=self.context["request"].user,
                                                     review=validated_data["review"]
                                                     ).count()
        if self.context['request'].method == 'POST' and user_objects >= 1:
            raise ValidationError('Вы уже оставляли отзыв к данному товару.')

        return super().create(validated_data)


class CollectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collections
        fields = '__all__'

