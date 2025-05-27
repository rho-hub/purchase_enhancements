Download a copy of the Odoo platform (18.0) here: https://github.com/odoo/odoo/archive/18.0.zip . Install it using an online tutorial of your choice on a Linux environment. 
I used WSL

Odoo comes with a number of default applications that include a 'Purchases Applications'. The RFQ module however, has some missing functionalities that you're required to implement. You are requested to add a one-to-many relationship between an RFQ and Vendors. Create a customization in the system such that one RFQ could be assigned to several vendors at the model-level. 
Additionally, extend these features to the front-end interfaces such that you make it possible for the end-user to perform such actions.

Clone this repo ino a folder in addons/
creatdb <name of db> (using postgresql)
run ./odoo-bin -d <yourdb> -u purchase_enhancements
