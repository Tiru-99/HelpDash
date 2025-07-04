from tools.dashboard_tools.client.client_dashboard_tool import (
    ClientStatusCountTool,
    NewClientsThisMonthTool,
    BirthdayReminderTool,
)

from tools.dashboard_tools.revenue.revenue_dashboard_tools import (
    TotalRevenueTool,
    OutstandingPaymentsTool,
)

from tools.dashboard_tools.attendance.attendance_dashboard_tools import (
    AttendancePercentageTool,
    DropOffRateTool,
)

from tools.dashboard_tools.service.service_dashboard_tools import (
    EnrollmentTrendsTool,
    CourseCompletionRateTool,
)

DASHBOARD_TOOLS = [
    # Client Tools
    ClientStatusCountTool,
    NewClientsThisMonthTool,
    BirthdayReminderTool,

    # Revenue Tools
    TotalRevenueTool,
    OutstandingPaymentsTool,

    # Attendance Tools
    AttendancePercentageTool,
    DropOffRateTool,

    # Service Tools
    EnrollmentTrendsTool,
    CourseCompletionRateTool,
]
