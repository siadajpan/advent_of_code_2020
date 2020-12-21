import re

from utils.utils import read_input


def find_products_of_allergen(allergen, allergens_list):
    # find products that may contain input allergen
    products_groups_that_may_have_allergen = []
    # iterate through the input list, and find if allergen is in the list of allergens
    for products, allergens in allergens_list:
        if allergen in allergens:
            products_groups_that_may_have_allergen.append(products)
    # we couln't find any products that may contain allergens, maybe it has already be found
    if len(products_groups_that_may_have_allergen) == 0:
        return None

    # find intersection between all the products
    products_found = set(products_groups_that_may_have_allergen[0])
    for possible_products in products_groups_that_may_have_allergen:
        products_found = set(possible_products) & products_found

    products_found = list(products_found)
    # if there is only one match, get it
    if len(products_found) == 1:
        print('allergen', allergen, 'product', products_found[0])
        return products_found[0]
    elif len(products_found) == 0:
        raise ValueError(f'Allergen {allergen} could not be matched')
    return None


def remove_product_allergen_from_list(product, allergen, allergens_list):
    # remove product and allergen from our helper list
    for products, allergens in allergens_list:
        if product in products:
            products.remove(product)
        if allergen in allergens:
            allergens.remove(allergen)

    return allergens_list


if __name__ == '__main__':
    data = read_input('input')
    # input list, [((group of products),(group of allergens))]
    allergens_list = []
    # output dictionary: product: allergen
    products_with_allergens = {}
    # only allergens
    all_allergens = []
    for row in data:
        products, contains = re.match(r'([\w\s]+)\(contains ([\w\s,]+)\)', row).groups()
        allergens_list.append([products.split(), contains.split(', ')])
        for contain in contains.split(', '):
            all_allergens.append(contain)
    print('our input:\n', allergens_list)

    # go through list couple time, if there is no update, break
    for _ in range(5):
        old_allergens = allergens_list.copy()
        for allergen in all_allergens:
            # find a product that match the allergen
            found_product = find_products_of_allergen(allergen, allergens_list)
            if not found_product:
                continue
            # remove both from the input list
            remove_product_allergen_from_list(found_product, allergen, allergens_list)
            # update the output dictionary
            products_with_allergens.update(**{found_product: allergen})
        # break if there is no new update
        if old_allergens == allergens_list:
            break
    products_left = [prod for prod, allergen in allergens_list]
    print('left', sum([len(prods) for prods in products_left]))

    print(','.join([p for p, a in sorted(products_with_allergens.items(), key=lambda x: x[1])]))
