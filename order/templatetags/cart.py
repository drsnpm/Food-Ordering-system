from django import template
register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        try:
            id_int = int(id)
            if id_int == product.id:
                return True
        except ValueError:
            pass
    return False


@register.filter(name='card_quantity')
def card_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        try:
            id_int = int(id)
            if id_int == product.id:
                return cart.get(id)
        except ValueError:
            pass
    return 0

@register.filter(name='price_toatal')
def price_toatal(product, cart):
    return product.price * card_quantity(product, cart)

@register.filter(name='cart_toatal_price')
def cart_toatal_price(products, cart):
    sum = 0
    for i in products:
        sum += price_toatal(i, cart)
    return sum

@register.filter(name='currency')
def currency(number):
    return '₹ '+str(number)

@register.filter(name='multiply')
def multiply(number, number1):
    return number * number1