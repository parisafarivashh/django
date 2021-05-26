# django rest framework
<< create onlineshop>>

models > 1: custom user[name, email, phone, password] 
         2: profile for each user 
         3: product
         4: category
         5: meson
         6: order
         7: itemorder
         
view > 1: login
       2: signup
       3: the user can see the list of products 
       4: the admin can create product & category & meson
       5: each user can see their own profile
       6: when now user created the order is creted automatically and user can select product
       7: the user just see his own order
       8: we have additional action in view to pay for the order
       
 permission > 1: IsOwn
              2: IsAdmin
              3: ActionPermisiion(custom permission for each action view ['list','create',...])
              

test > 1: test view
       2: test permission
       3: test serializer
              
              
 
       
       
       
         
         
         
