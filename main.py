from classes import Category, Resource

cat_ict = Category(
    "ICT",
    "90486ca55805467b81d465bdb3bc3b58&categoryID=38566")

cat_cameras = Category(
    "Cameras",
    "3e4333ba5d8a4071acbd64ca218be245&categoryID=35400")

cat_ipads = Category(
    "iPads",
    "d939505748a7491784179b3f1d76acb4&categoryID=35332")

laptops = Resource("Laptops")
ipads = Resource("iPads")
cameras = Resource("Cameras")

cat_ict.update()
cat_ipads.update()
cat_cameras.update()
