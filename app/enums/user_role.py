from enum import Enum


class UserRole(str,Enum):
    CUSTOMER = 'customer'
    SELLER = 'seller'
    ADMIN = 'admin'
    SUPER_ADMIN = 'super_admin'