def lazy_imports():
    global main_menu, graph_menu, line_menu, time_spent_chart, time_spent_all_chart
    global run_simulation, save_data, delete_files, restore_files, get_SS

    from .menu import main_menu, graph_menu, line_menu
    from .chart_generator import time_spent_chart, time_spent_all_chart
    from .simulation import run_simulation
    from .data_handler import save_data, delete_files, restore_files, get_SS


lazy_imports()
