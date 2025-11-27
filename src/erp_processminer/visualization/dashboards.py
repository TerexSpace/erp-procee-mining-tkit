"""
Provides functions for generating simple dashboards to explore event logs
and performance KPIs.
"""

from erp_processminer.eventlog.structures import EventLog

def generate_dashboard(log: EventLog, output_file: str = 'dashboard.html'):
    """
    Generates a simple HTML dashboard with key process mining statistics.

    This is a basic implementation that generates a static HTML file.
    A more advanced version could use libraries like Dash or Panel.

    :param log: The event log to analyze.
    :param output_file: The path to save the HTML dashboard.
    """
    from erp_processminer.statistics.performance import get_cycle_times
    from erp_processminer.statistics.variants import get_variant_performance
    
    cycle_times = get_cycle_times(log)
    variants = get_variant_performance(log)

    avg_cycle_time = sum(cycle_times) / len(cycle_times) if cycle_times else 0.0
    
    # Sort variants by frequency
    sorted_variants = sorted(variants.items(), key=lambda item: item[1]['frequency'], reverse=True)
    
    # --- HTML Content ---
    html = f"""
    <html>
    <head>
        <title>Process Mining Dashboard</title>
        <style>
            body {{ font-family: sans-serif; }}
            h1, h2 {{ color: #333; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Process Mining Dashboard</h1>
        
        <h2>Log Summary</h2>
        <p>Total Traces: {len(log.traces)}</p>
        <p>Total Events: {len(log.all_events)}</p>
        
        <h2>Performance</h2>
        <p>Average Cycle Time: {avg_cycle_time:.2f} seconds</p>
        
        <h2>Top 10 Process Variants</h2>
        <table>
            <tr>
                <th>Variant</th>
                <th>Frequency</th>
                <th>Avg. Cycle Time (s)</th>
            </tr>
    """
    
    for variant, stats in sorted_variants[:10]:
        variant_str = " &rarr; ".join(variant)
        html += f"""
            <tr>
                <td>{variant_str}</td>
                <td>{stats['frequency']}</td>
                <td>{stats['avg_cycle_time']:.2f}</td>
            </tr>
        """
        
    html += """
        </table>
    </body>
    </html>
    """
    
    with open(output_file, 'w') as f:
        f.write(html)
        
    print(f"Dashboard generated at: {output_file}")
