from daos.product_dao import ProductDAO
from models.product import Product

dao = ProductDAO()


def test_product_select():
    product_list = dao.select_all()
    assert len(product_list) >= 1


def test_product_insert():
    product = Product(
        None,
        "Test Product",
        "Test Brand",
        19.99
    )

    assigned_id = dao.insert(product)

    product_list = dao.select_all()
    names = [p.name for p in product_list]

    assert product.name in names

    # cleanup
    dao.delete(assigned_id)


def test_product_update():
    product = Product(
        None,
        "Test Product",
        "Test Brand",
        19.99
    )

    assigned_id = dao.insert(product)

    product.id = assigned_id
    product.name = "Updated Product"
    product.brand = "Updated Brand"
    product.price = 29.99

    dao.update(product)

    product_list = dao.select_all()

    updated_product = next(
        (p for p in product_list if p.id == assigned_id),
        None
    )

    assert updated_product is not None
    assert updated_product.name == "Updated Product"
    assert updated_product.brand == "Updated Brand"
    assert float(updated_product.price) == 29.99
    # cleanup
    dao.delete(assigned_id)


def test_product_delete():
    product = Product(
        None,
        "Product To Delete",
        "Test Brand",
        9.99
    )

    assigned_id = dao.insert(product)

    dao.delete(assigned_id)

    product_list = dao.select_all()
    ids = [p.id for p in product_list]

    assert assigned_id not in ids