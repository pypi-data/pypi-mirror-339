"""
Main client for iiko.services API
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Any

import requests

from .constants import API_BASE_URL, ENDPOINTS
from .exceptions import AuthenticationError, ApiError, ValidationError, NetworkError
from .utils import filter_none_values, ensure_list
from .models.auth import TokenResponse
from .models.organizations import OrganizationsResponse
from .models.menu import Menu, MenuResponse
from .models.orders import OrderResponse, OrderByIdResponse
from .models.delivery import DeliveryResponse, DeliveryByIdResponse


logger = logging.getLogger(__name__)


class IikoClient:
    """
    Client for iiko.services API
    """

    def __init__(self, api_key: str, base_url: str = API_BASE_URL):
        """
        Initialize client

        Args:
            api_key: API key
            base_url: Base URL for API
        """
        self.api_key = api_key
        self.base_url = base_url
        self.token: Optional[TokenResponse] = None
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _get_token(self) -> str:
        """
        Get token for API requests

        Returns:
            Token string
        """
        if self.token and not self.token.is_expired():
            return self.token.token

        try:
            response = self.session.post(
                f"{self.base_url}{ENDPOINTS['token']}",
                json={"apiLogin": self.api_key}
            )
            response.raise_for_status()
            data = response.json()

            # Create token response with the data from the API
            token_data = {"token": data["token"]}

            # Add correlation_id if present
            if "correlationId" in data:
                token_data["correlationId"] = data["correlationId"]

            # Add expire_seconds if present
            if "expire_seconds" in data:
                token_data["expire_seconds"] = data["expire_seconds"]

            # Create token response and set created_at
            self.token = TokenResponse(**token_data)
            self.token.created_at = datetime.now()

            return self.token.token
        except requests.exceptions.RequestException as e:
            logger.error("Error getting token: %s", e)
            raise NetworkError(f"Error getting token: {e}") from e
        except (KeyError, ValueError) as e:
            logger.error("Error parsing token response: %s", e)
            raise AuthenticationError(f"Error parsing token response: {e}") from e

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Make request to API

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request data

        Returns:
            Response data
        """
        token = self._get_token()
        headers = {"Authorization": f"Bearer {token}"}

        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers, params=data)
            else:
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data
                )

            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            try:
                error_data = e.response.json()
                error_message = error_data.get("errorDescription", str(e))
            except (ValueError, KeyError):
                error_message = str(e)

            logger.error("API error: %s - %s", status_code, error_message)
            raise ApiError(status_code, error_message, e.response) from e
        except requests.exceptions.RequestException as e:
            logger.error("Network error: %s", e)
            raise NetworkError(f"Network error: {e}") from e
        except (ValueError, KeyError) as e:
            logger.error("Error parsing response: %s", e)
            raise ValidationError(f"Error parsing response: {e}") from e

    # Authentication methods
    def get_token(self) -> TokenResponse:
        """
        Get authentication token

        Returns:
            Token response
        """
        self._get_token()
        return self.token

    # Organization methods
    def get_organizations(self, return_additional_info: bool = False,
                          include_disabled: bool = False) -> OrganizationsResponse:
        """
        Get organizations

        Args:
            return_additional_info: Return additional info
            include_disabled: Include disabled organizations

        Returns:
            Organizations response
        """
        data = {
            "returnAdditionalInfo": return_additional_info,
            "includeDisabled": include_disabled
        }

        response = self._make_request("POST", ENDPOINTS["organizations"], data)
        return OrganizationsResponse(organizations=response["organizations"])

    # Menu methods
    def get_menu(self, organization_ids: Union[str, List[str]],
                 price_category_id: Optional[str] = None,
                 include_deleted: bool = False,
                 include_hidden: bool = False) -> MenuResponse:
        """
        Get menu

        Args:
            organization_ids: Organization IDs
            price_category_id: Price category ID
            include_deleted: Include deleted items
            include_hidden: Include hidden items

        Returns:
            Menu response
        """
        organization_ids = ensure_list(organization_ids)

        # Check if we need to use organizationId or organizationIds
        if len(organization_ids) == 1:
            data = {
                "organizationId": organization_ids[0],
                "priceCategoryId": price_category_id,
                "includeDeleted": include_deleted,
                "includeHidden": include_hidden
            }
        else:
            data = {
                "organizationIds": organization_ids,
                "priceCategoryId": price_category_id,
                "includeDeleted": include_deleted,
                "includeHidden": include_hidden
            }

        data = filter_none_values(data)

        response = self._make_request("POST", ENDPOINTS["nomenclature"], data)
        return MenuResponse(**response)

    def get_external_menus(self, organization_ids: Union[str, List[str]]) -> Dict:
        """
        Get external menus

        Args:
            organization_ids: Organization IDs

        Returns:
            Dict with external menus
        """
        organization_ids = ensure_list(organization_ids)

        data = {
            "organizationIds": organization_ids
        }

        response = self._make_request("POST", ENDPOINTS["external_menus"], data)
        return response

    def get_menu_by_id(self, organization_ids: Union[str, List[str]], menu_id: str) -> Menu:
        """
        Get menu by ID

        Args:
            organization_ids: Organization IDs
            menu_id: Menu ID (external menu ID)

        Returns:
            Menu
        """
        organization_ids = ensure_list(organization_ids)

        data = {
            "organizationIds": organization_ids,
            "externalMenuId": menu_id
        }

        response = self._make_request("POST", ENDPOINTS["menu_by_id"], data)
        return Menu(**response["menu"])

    def get_stop_lists(self, organization_ids: Union[str, List[str]]) -> Dict:
        """
        Get stop lists

        Args:
            organization_ids: Organization IDs

        Returns:
            Stop lists
        """
        organization_ids = ensure_list(organization_ids)

        data = {"organizationIds": organization_ids}

        return self._make_request("POST", ENDPOINTS["stop_lists"], data)

    # Order methods
    def create_order(self, organization_id: str, terminal_group_id: str,
                     order: Dict[str, Any]) -> OrderResponse:
        """
        Create order

        Args:
            organization_id: Organization ID
            terminal_group_id: Terminal group ID
            order: Order data

        Returns:
            Order response
        """
        data = {
            "organizationId": organization_id,
            "terminalGroupId": terminal_group_id,
            "order": order
        }

        response = self._make_request("POST", ENDPOINTS["order_create"], data)
        return OrderResponse(**response)

    def get_order_by_id(self, organization_ids: Union[str, List[str]],
                        order_ids: Union[str, List[str]]) -> OrderByIdResponse:
        """
        Get order by ID

        Args:
            organization_ids: Organization IDs
            order_ids: Order IDs

        Returns:
            Order by ID response
        """
        organization_ids = ensure_list(organization_ids)
        order_ids = ensure_list(order_ids)

        data = {
            "organizationIds": organization_ids,
            "orderIds": order_ids
        }

        response = self._make_request("POST", ENDPOINTS["order_by_id"], data)
        return OrderByIdResponse(orders=response["orders"])

    def add_order_items(self, organization_id: str, terminal_group_id: str,
                        order_id: str, items: List[Dict[str, Any]]) -> Dict:
        """
        Add order items

        Args:
            organization_id: Organization ID
            terminal_group_id: Terminal group ID
            order_id: Order ID
            items: Items to add

        Returns:
            Response
        """
        data = {
            "organizationId": organization_id,
            "terminalGroupId": terminal_group_id,
            "orderId": order_id,
            "items": items
        }

        return self._make_request("POST", ENDPOINTS["order_add_items"], data)

    def close_order(self, organization_id: str, order_id: str,
                    payments: List[Dict[str, Any]]) -> Dict:
        """
        Close order

        Args:
            organization_id: Organization ID
            order_id: Order ID
            payments: Payments

        Returns:
            Response
        """
        data = {
            "organizationId": organization_id,
            "orderId": order_id,
            "payments": payments
        }

        return self._make_request("POST", ENDPOINTS["order_close"], data)

    # Delivery methods
    def create_delivery(self, organization_id: str, terminal_group_id: str,
                        delivery: Dict[str, Any]) -> DeliveryResponse:
        """
        Create delivery

        Args:
            organization_id: Organization ID
            terminal_group_id: Terminal group ID
            delivery: Delivery data

        Returns:
            Delivery response
        """
        data = {
            "organizationId": organization_id,
            "terminalGroupId": terminal_group_id,
            "delivery": delivery
        }

        response = self._make_request("POST", ENDPOINTS["delivery_create"], data)
        return DeliveryResponse(**response)

    def get_delivery_by_id(self, organization_ids: Union[str, List[str]],
                           delivery_ids: Union[str, List[str]]) -> DeliveryByIdResponse:
        """
        Get delivery by ID

        Args:
            organization_ids: Organization IDs
            delivery_ids: Delivery IDs

        Returns:
            Delivery by ID response
        """
        organization_ids = ensure_list(organization_ids)
        delivery_ids = ensure_list(delivery_ids)

        data = {
            "organizationIds": organization_ids,
            "orderIds": delivery_ids
        }

        response = self._make_request("POST", ENDPOINTS["delivery_by_id"], data)
        return DeliveryByIdResponse(deliveries=response["orders"])

    def update_delivery_status(self, organization_id: str, order_id: str,
                               status: str) -> Dict:
        """
        Update delivery status

        Args:
            organization_id: Organization ID
            order_id: Order ID
            status: Status

        Returns:
            Response
        """
        data = {
            "organizationId": organization_id,
            "orderId": order_id,
            "status": status
        }

        return self._make_request("POST", ENDPOINTS["delivery_update_order_delivery_status"], data)

    def cancel_delivery(self, organization_id: str, order_id: str,
                        cancel_cause_id: str) -> Dict:
        """
        Cancel delivery

        Args:
            organization_id: Organization ID
            order_id: Order ID
            cancel_cause_id: Cancel cause ID

        Returns:
            Response
        """
        data = {
            "organizationId": organization_id,
            "orderId": order_id,
            "cancelCauseId": cancel_cause_id
        }

        return self._make_request("POST", ENDPOINTS["delivery_cancel"], data)

    # Dictionary methods
    def get_payment_types(self, organization_ids: Union[str, List[str]]) -> Dict:
        """
        Get payment types

        Args:
            organization_ids: Organization IDs

        Returns:
            Payment types
        """
        organization_ids = ensure_list(organization_ids)

        data = {"organizationIds": organization_ids}

        return self._make_request("POST", ENDPOINTS["payment_types"], data)

    def get_order_types(self, organization_ids: Union[str, List[str]]) -> Dict:
        """
        Get order types

        Args:
            organization_ids: Organization IDs

        Returns:
            Order types
        """
        organization_ids = ensure_list(organization_ids)

        data = {"organizationIds": organization_ids}

        return self._make_request("POST", ENDPOINTS["order_types"], data)

    def get_discounts(self, organization_ids: Union[str, List[str]]) -> Dict:
        """
        Get discounts

        Args:
            organization_ids: Organization IDs

        Returns:
            Discounts
        """
        organization_ids = ensure_list(organization_ids)

        data = {"organizationIds": organization_ids}

        return self._make_request("POST", ENDPOINTS["discounts"], data)

    def get_cancel_causes(self, organization_ids: Union[str, List[str]]) -> Dict:
        """
        Get cancel causes

        Args:
            organization_ids: Organization IDs

        Returns:
            Cancel causes
        """
        organization_ids = ensure_list(organization_ids)

        data = {"organizationIds": organization_ids}

        return self._make_request("POST", ENDPOINTS["cancel_causes"], data)

    # Terminal group methods
    def get_terminal_groups(self, organization_ids: Union[str, List[str]]) -> Dict:
        """
        Get terminal groups

        Args:
            organization_ids: Organization IDs

        Returns:
            Terminal groups
        """
        organization_ids = ensure_list(organization_ids)

        data = {"organizationIds": organization_ids}

        return self._make_request("POST", ENDPOINTS["terminal_groups"], data)

    def check_terminal_groups_alive(self, organization_ids: Union[str, List[str]],
                                    terminal_group_ids: Union[str, List[str]]) -> Dict:
        """
        Check if terminal groups are alive

        Args:
            organization_ids: Organization IDs
            terminal_group_ids: Terminal group IDs

        Returns:
            Terminal groups alive status
        """
        organization_ids = ensure_list(organization_ids)
        terminal_group_ids = ensure_list(terminal_group_ids)

        data = {
            "organizationIds": organization_ids,
            "terminalGroupIds": terminal_group_ids
        }

        return self._make_request("POST", ENDPOINTS["terminal_groups_is_alive"], data)

    # Employee methods
    def get_couriers(self, organization_ids: Union[str, List[str]]) -> Dict:
        """
        Get couriers

        Args:
            organization_ids: Organization IDs

        Returns:
            Couriers
        """
        organization_ids = ensure_list(organization_ids)

        data = {"organizationIds": organization_ids}

        return self._make_request("POST", ENDPOINTS["couriers"], data)

    def get_couriers_active_location(self, organization_ids: Union[str, List[str]]) -> Dict:
        """
        Get couriers active location

        Args:
            organization_ids: Organization IDs

        Returns:
            Couriers active location
        """
        organization_ids = ensure_list(organization_ids)

        data = {"organizationIds": organization_ids}

        return self._make_request("POST", ENDPOINTS["couriers_active_location"], data)

    # Address methods
    def get_regions(self, organization_ids: Union[str, List[str]]) -> Dict:
        """
        Get regions

        Args:
            organization_ids: Organization IDs

        Returns:
            Regions
        """
        organization_ids = ensure_list(organization_ids)

        data = {"organizationIds": organization_ids}

        return self._make_request("POST", ENDPOINTS["regions"], data)

    def get_cities(self, organization_ids: Union[str, List[str]],
                   region_ids: Optional[Union[str, List[str]]] = None) -> Dict:
        """
        Get cities

        Args:
            organization_ids: Organization IDs
            region_ids: Region IDs

        Returns:
            Cities
        """
        organization_ids = ensure_list(organization_ids)

        data = {"organizationIds": organization_ids}

        if region_ids:
            data["regionIds"] = ensure_list(region_ids)

        return self._make_request("POST", ENDPOINTS["cities"], data)

    def get_streets_by_city(self, organization_id: str, city_id: str) -> Dict:
        """
        Get streets by city

        Args:
            organization_id: Organization ID
            city_id: City ID

        Returns:
            Streets
        """
        data = {
            "organizationId": organization_id,
            "cityId": city_id
        }

        return self._make_request("POST", ENDPOINTS["streets_by_city"], data)

    # Marketing methods
    def get_marketing_sources(self, organization_ids: Union[str, List[str]]) -> Dict:
        """
        Get marketing sources

        Args:
            organization_ids: Organization IDs

        Returns:
            Marketing sources
        """
        organization_ids = ensure_list(organization_ids)

        data = {"organizationIds": organization_ids}

        return self._make_request("POST", ENDPOINTS["marketing_sources"], data)

    # Customer methods
    def get_customer_info(self, organization_id: str, customer_id: Optional[str] = None,
                          phone: Optional[str] = None, card_track: Optional[str] = None,
                          card_number: Optional[str] = None, email: Optional[str] = None) -> Dict:
        """
        Get customer info

        Args:
            organization_id: Organization ID
            customer_id: Customer ID
            phone: Phone
            card_track: Card track
            card_number: Card number
            email: Email

        Returns:
            Customer info
        """
        data = {
            "organizationId": organization_id,
            "id": customer_id,
            "phone": phone,
            "cardTrack": card_track,
            "cardNumber": card_number,
            "email": email
        }

        data = filter_none_values(data)

        return self._make_request("POST", ENDPOINTS["customer_info"], data)

    def create_or_update_customer(self, organization_id: str, customer: Dict[str, Any]) -> Dict:
        """
        Create or update customer

        Args:
            organization_id: Organization ID
            customer: Customer data

        Returns:
            Customer
        """
        data = {
            "organizationId": organization_id,
            "customer": customer
        }

        return self._make_request("POST", ENDPOINTS["customer_create_or_update"], data)
