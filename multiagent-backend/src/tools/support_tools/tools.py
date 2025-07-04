from tools.support_tools.client.client_support_tools import SearchClient, GetClientEnrolledService
from tools.support_tools.orders.get_order_by_id import GetOrderByClient, GetOrderByIdTool
from tools.support_tools.orders.get_order_by_status import GetOrderByStatus
from tools.support_tools.payment.payment_support_tools import (
    GetPaymentByOrderTool,
    CalculatePendingDuesTool,
)
from tools.support_tools.sessions.session_support_tools import (
    ListUpcomingServicesTool,
    FilterByInstructorTool,
    FilterByStatusTool,
)
from tools.support_tools.external_api.create_enquiry_tool import (
    CreateEnquiryTool
)
from tools.support_tools.external_api.create_order_tool import (
    SmartCreateOrderTool
)


SUPPORT_TOOLS = [
    SearchClient,
    GetClientEnrolledService,
    GetOrderByClient,
    GetOrderByIdTool,
    GetOrderByStatus,
    GetPaymentByOrderTool,
    CalculatePendingDuesTool,
    ListUpcomingServicesTool,
    FilterByInstructorTool,
    FilterByStatusTool,
    CreateEnquiryTool , 
    SmartCreateOrderTool
]
