import matplotlib.pyplot as plt
import streamlit as st
import base64
from io import BytesIO
import os
from datetime import datetime

class Visualizer:
    def __init__(self, monitor):
        self.monitor = monitor

    def cli_summary(self):
        print("\n--- AgentMont Summary ---")
        print(f"Total Time: {self.monitor.total_time:.2f} seconds")
        print(f"Input Tokens: {self.monitor.input_tokens}")
        print(f"Output Tokens: {self.monitor.output_tokens}")
        print(f"Total Tokens: {self.monitor.total_tokens}")
        print(f"Cost: ${self.monitor.cost:.6f}")
        print(f"Average Latency: {self.monitor.avg_latency:.4f} seconds")
        print(f"Throughput (Tokens/Sec): {self.monitor.throughput:.2f}")
        avg_cpu = sum(self.monitor.cpu_usage) / len(self.monitor.cpu_usage) if self.monitor.cpu_usage else 0
        avg_mem = sum(self.monitor.memory_usage) / len(self.monitor.memory_usage) if self.monitor.memory_usage else 0
        print(f"Average CPU Usage: {avg_cpu:.2f}%")
        print(f"Average Memory Usage: {avg_mem:.2f} MB")
        print(f"Carbon Emissions: {self.monitor.carbon_emissions:.6f} kg CO2")
        print("----------------------------\n")

    def streamlit_dashboard(self):
        st.title("AgentMont Dashboard")
        st.header("Performance Metrics")
        st.write(f"**Total Time:** {self.monitor.total_time:.2f} seconds")
        st.write(f"**Input Tokens:** {self.monitor.input_tokens}")
        st.write(f"**Output Tokens:** {self.monitor.output_tokens}")
        st.write(f"**Total Tokens:** {self.monitor.total_tokens}")
        st.write(f"**Cost:** ${self.monitor.cost:.6f}")
        st.write(f"**Average Latency:** {self.monitor.avg_latency:.4f} seconds")
        st.write(f"**Throughput (Tokens/Sec):** {self.monitor.throughput:.2f}")
        st.write(f"**Carbon Emissions:** {self.monitor.carbon_emissions:.6f} kg CO2")

        st.header("Resource Utilization")
        if self.monitor.cpu_usage and self.monitor.memory_usage:
            fig, ax = plt.subplots(2, 1, figsize=(10, 6))
            ax[0].plot(self.monitor.cpu_usage, label='CPU Usage (%)', color='blue')
            ax[0].set_xlabel('Time (s)')
            ax[0].set_ylabel('CPU Usage (%)')
            ax[0].legend()

            ax[1].plot(self.monitor.memory_usage, label='Memory Usage (MB)', color='orange')
            ax[1].set_xlabel('Time (s)')
            ax[1].set_ylabel('Memory Usage (MB)')
            ax[1].legend()

            st.pyplot(fig)
        else:
            st.write("No resource usage data available.")

    def generate_html(self, output_path=None):
        """Generate an HTML report with monitoring data and visualizations.
        
        Args:
            output_path (str, optional): Path to save the HTML file. 
                If None, saves to 'agent_mont_report_{timestamp}.html' in current directory.
                
        Returns:
            str: Path to the generated HTML file
        """
        # Create default filename with timestamp if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"agent_mont_report_{timestamp}.html"
        
        # Generate plots as base64 encoded images to embed in HTML
        plots_html = ""
        if self.monitor.cpu_usage and self.monitor.memory_usage:
            # CPU Usage plot
            plt.figure(figsize=(10, 4))
            plt.plot(self.monitor.cpu_usage, label='CPU Usage (%)', color='blue')
            plt.xlabel('Time (s)')
            plt.ylabel('CPU Usage (%)')
            plt.title('CPU Usage Over Time')
            plt.legend()
            plt.tight_layout()
            
            cpu_img = BytesIO()
            plt.savefig(cpu_img, format='png')
            plt.close()
            cpu_img.seek(0)
            cpu_plot_b64 = base64.b64encode(cpu_img.getvalue()).decode('utf-8')
            
            # Memory Usage plot
            plt.figure(figsize=(10, 4))
            plt.plot(self.monitor.memory_usage, label='Memory Usage (MB)', color='orange')
            plt.xlabel('Time (s)')
            plt.ylabel('Memory Usage (MB)')
            plt.title('Memory Usage Over Time')
            plt.legend()
            plt.tight_layout()
            
            mem_img = BytesIO()
            plt.savefig(mem_img, format='png')
            plt.close()
            mem_img.seek(0)
            mem_plot_b64 = base64.b64encode(mem_img.getvalue()).decode('utf-8')
            
            plots_html = f"""
            <div class="charts">
                <div class="chart">
                    <h3>CPU Usage</h3>
                    <img src="data:image/png;base64,{cpu_plot_b64}" alt="CPU Usage">
                </div>
                <div class="chart">
                    <h3>Memory Usage</h3>
                    <img src="data:image/png;base64,{mem_plot_b64}" alt="Memory Usage">
                </div>
            </div>
            """
        else:
            plots_html = """
            <div class="no-data">
                <p>No resource usage data available.</p>
            </div>
            """
        
        # Calculate average CPU and memory usage
        avg_cpu = sum(self.monitor.cpu_usage) / len(self.monitor.cpu_usage) if self.monitor.cpu_usage else 0
        avg_mem = sum(self.monitor.memory_usage) / len(self.monitor.memory_usage) if self.monitor.memory_usage else 0
        
        # Create HTML content
        html_content = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AgentMont Performance Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f7fa;
                }}
                .container {{
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    padding: 30px;
                    margin-bottom: 20px;
                }}
                h1, h2 {{
                    color: #2c3e50;
                    margin-top: 0;
                }}
                h1 {{
                    border-bottom: 2px solid #eaecef;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                .metrics {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .metric-card {{
                    background: #f8f9fa;
                    border-radius: 6px;
                    padding: 15px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                .metric-card h3 {{
                    margin-top: 0;
                    color: #5f6368;
                    font-size: 0.9rem;
                    text-transform: uppercase;
                }}
                .metric-card p {{
                    margin-bottom: 0;
                    font-size: 1.5rem;
                    font-weight: bold;
                    color: #1a73e8;
                }}
                .charts {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                }}
                .chart {{
                    background: white;
                    border-radius: 6px;
                    padding: 15px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                .chart img {{
                    width: 100%;
                    height: auto;
                }}
                .timestamp {{
                    text-align: right;
                    font-size: 0.8rem;
                    color: #666;
                    margin-top: 20px;
                }}
                @media (max-width: 768px) {{
                    .charts {{
                        grid-template-columns: 1fr;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>AgentMont Performance Report</h1>
                
                <h2>Performance Metrics</h2>
                <div class="metrics">
                    <div class="metric-card">
                        <h3>Total Time</h3>
                        <p>{self.monitor.total_time:.2f} seconds</p>
                    </div>
                    <div class="metric-card">
                        <h3>Input Tokens</h3>
                        <p>{self.monitor.input_tokens}</p>
                    </div>
                    <div class="metric-card">
                        <h3>Output Tokens</h3>
                        <p>{self.monitor.output_tokens}</p>
                    </div>
                    <div class="metric-card">
                        <h3>Total Tokens</h3>
                        <p>{self.monitor.total_tokens}</p>
                    </div>
                    <div class="metric-card">
                        <h3>Cost</h3>
                        <p>${self.monitor.cost:.6f}</p>
                    </div>
                    <div class="metric-card">
                        <h3>Average Latency</h3>
                        <p>{self.monitor.avg_latency:.4f} seconds</p>
                    </div>
                    <div class="metric-card">
                        <h3>Throughput</h3>
                        <p>{self.monitor.throughput:.2f} tokens/sec</p>
                    </div>
                    <div class="metric-card">
                        <h3>Average CPU Usage</h3>
                        <p>{avg_cpu:.2f}%</p>
                    </div>
                    <div class="metric-card">
                        <h3>Average Memory Usage</h3>
                        <p>{avg_mem:.2f} MB</p>
                    </div>
                    <div class="metric-card">
                        <h3>Carbon Emissions</h3>
                        <p>{self.monitor.carbon_emissions:.6f} kg CO2</p>
                    </div>
                </div>
                
                <h2>Resource Utilization</h2>
                {plots_html}
                
                <div class="timestamp">
                    Report generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                </div>
            </div>
        </body>
        </html>
        """
        
        # Write the HTML content to the file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML report generated at: {os.path.abspath(output_path)}")
        return os.path.abspath(output_path)
