"""
Constants for iiko.services API
"""

# API Base URL
API_BASE_URL = "https://api-ru.iiko.services"

# API Endpoints
ENDPOINTS = {
    # Authentication
    "token": "/api/1/access_token",

    # Organizations
    "organizations": "/api/1/organizations",

    # Terminal groups
    "terminal_groups": "/api/1/terminal_groups",
    "terminal_groups_is_alive": "/api/1/terminal_groups/is_alive",

    # Menu
    "nomenclature": "/api/1/nomenclature",
    "menu": "/api/2/menu",
    "menu_by_id": "/api/2/menu/by_id",
    "external_menus": "/api/2/menu/external_menus",
    "stop_lists": "/api/1/stop_lists",
    "combo": "/api/1/combo",
    "combo_calculate": "/api/1/combo/calculate",

    # Dictionaries
    "cancel_causes": "/api/1/cancel_causes",
    "order_types": "/api/1/deliveries/order_types",
    "discounts": "/api/1/discounts",
    "payment_types": "/api/1/payment_types",
    "removal_types": "/api/1/removal_types",
    "tips_types": "/api/1/tips_types",

    # Orders
    "order_create": "/api/1/order/create",
    "order_by_id": "/api/1/order/by_id",
    "order_by_table": "/api/1/order/by_table",
    "order_add_items": "/api/1/order/add_items",
    "order_close": "/api/1/order/close",
    "order_change_payments": "/api/1/order/change_payments",
    "order_init_by_table": "/api/1/order/init_by_table",

    # Deliveries: Create and update
    "delivery_create": "/api/1/deliveries/create",
    "delivery_update_order_problem": "/api/1/deliveries/update_order_problem",
    "delivery_update_order_delivery_status": "/api/1/deliveries/update_order_delivery_status",
    "delivery_update_order_courier": "/api/1/deliveries/update_order_courier",
    "delivery_add_items": "/api/1/deliveries/add_items",
    "delivery_close": "/api/1/deliveries/close",
    "delivery_cancel": "/api/1/deliveries/cancel",
    "delivery_change_complete_before": "/api/1/deliveries/change_complete_before",
    "delivery_change_delivery_point": "/api/1/deliveries/change_delivery_point",
    "delivery_change_service_type": "/api/1/deliveries/change_service_type",
    "delivery_change_payments": "/api/1/deliveries/change_payments",
    "delivery_change_comment": "/api/1/deliveries/change_comment",
    "delivery_print_delivery_bill": "/api/1/deliveries/print_delivery_bill",
    "delivery_confirm": "/api/1/deliveries/confirm",
    "delivery_cancel_confirmation": "/api/1/deliveries/cancel_confirmation",
    "delivery_change_operator": "/api/1/deliveries/change_operator",

    # Deliveries: Retrieve
    "delivery_by_id": "/api/1/deliveries/by_id",
    "delivery_by_date_and_status": "/api/1/deliveries/by_delivery_date_and_status",
    "delivery_by_revision": "/api/1/deliveries/by_revision",
    "delivery_by_date_and_phone": "/api/1/deliveries/by_delivery_date_and_phone",
    "delivery_by_date_and_source_key_and_filter": "/api/1/deliveries/by_delivery_date_and_source_key_and_filter",

    # Addresses
    "regions": "/api/1/regions",
    "cities": "/api/1/cities",
    "streets_by_city": "/api/1/streets/by_city",

    # Employees
    "couriers": "/api/1/employees/couriers",
    "couriers_by_role": "/api/1/employees/couriers/by_role",
    "couriers_active_location": "/api/1/employees/couriers/active_location",
    "couriers_active_location_by_terminal": "/api/1/employees/couriers/active_location/by_terminal",
    "couriers_locations_by_time_offset": "/api/1/employees/couriers/locations/by_time_offset",
    "employees_info": "/api/1/employees/info",

    # Marketing sources
    "marketing_sources": "/api/1/marketing_sources",

    # Customers
    "customer_info": "/api/1/loyalty/iiko/customer/info",
    "customer_create_or_update": "/api/1/loyalty/iiko/customer/create_or_update",
    "customer_program_add": "/api/1/loyalty/iiko/customer/program/add",
    "customer_card_add": "/api/1/loyalty/iiko/customer/card/add",
    "customer_card_remove": "/api/1/loyalty/iiko/customer/card/remove",
    "customer_wallet_hold": "/api/1/loyalty/iiko/customer/wallet/hold",
    "customer_wallet_topup": "/api/1/loyalty/iiko/customer/wallet/topup",
    "customer_wallet_chargeoff": "/api/1/loyalty/iiko/customer/wallet/chargeoff",
}

# Order statuses
class OrderStatus:
    NEW = "New"
    BILL = "Bill"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"

# Delivery statuses
class DeliveryStatus:
    NEW = "New"
    WAITING = "Waiting"
    ON_WAY = "OnWay"
    DELIVERED = "Delivered"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"

# Payment types
class PaymentType:
    CASH = "Cash"
    CARD = "Card"
    CREDIT = "Credit"
    GIFT_CARD = "GiftCard"
    EXTERNAL = "External"
