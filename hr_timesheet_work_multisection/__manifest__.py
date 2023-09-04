{
    'name': 'Timesheet Work Multisection',
    'version': '16.0.1.0.0',
    'category': '',
    'description': u"""
Add sale line section in timesheet.work.todo and done to allow filtering and grouping by.
""",
    'author': 'Serincloud',
    'depends': [
        'sale_order_multisection',
        'hr_timesheet_work',
    ],
    'data': [
        'views/timesheet_line_todo_views.xml',
        'views/timesheet_line_done_views.xml',
    ],
    'installable': True,
}
