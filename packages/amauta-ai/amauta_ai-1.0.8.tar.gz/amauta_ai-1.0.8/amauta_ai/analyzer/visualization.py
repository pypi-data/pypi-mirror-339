"""Visualization module for code analysis results."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class VisualizationGenerator:
    """
    Generator for visualizations of code analysis results.

    This class generates various visualizations based on analysis results,
    including dependency graphs, complexity charts, and file type distributions.
    """

    def __init__(self, output_dir: str = "."):
        """
        Initialize the visualization generator.

        Args:
            output_dir: Directory to save visualizations
        """
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def generate_dependency_graph(
        self, analysis_result: Dict[str, Any], filename: str = "dependency_graph.html"
    ) -> str:
        """
        Generate an interactive dependency graph visualization.

        Args:
            analysis_result: Analysis result dictionary
            filename: Output filename

        Returns:
            Path to the generated HTML file
        """
        if "file_dependencies" not in analysis_result:
            return "No dependency data available"

        dependencies = analysis_result["file_dependencies"]

        # Create a D3.js visualization
        nodes = []
        links = []
        node_ids = {}

        # Create nodes
        node_id = 0
        for file_path in dependencies:
            # Skip files with very long paths to keep visualization manageable
            if len(file_path) > 100:
                continue

            # Determine node group (type) based on file extension
            extension = os.path.splitext(file_path)[1].lower()
            if extension in [".py"]:
                group = 1
            elif extension in [".js", ".jsx", ".ts", ".tsx"]:
                group = 2
            elif extension in [".css", ".scss", ".sass", ".less"]:
                group = 3
            elif extension in [".html", ".htm"]:
                group = 4
            else:
                group = 5

            # Add node
            nodes.append({"id": node_id, "name": file_path, "group": group})

            node_ids[file_path] = node_id
            node_id += 1

        # Create links
        for source, targets in dependencies.items():
            if source not in node_ids:
                continue

            source_id = node_ids[source]

            for target in targets:
                # Convert relative import paths to full paths (simplified)
                if target.startswith("."):
                    # Skip relative imports for simplicity
                    continue

                # For package imports, we create dummy nodes
                if target not in node_ids:
                    nodes.append(
                        {
                            "id": node_id,
                            "name": target,
                            "group": 6,  # External dependency
                        }
                    )
                    node_ids[target] = node_id
                    node_id += 1

                target_id = node_ids[target]

                links.append({"source": source_id, "target": target_id, "value": 1})

        # Generate HTML with D3.js
        html = self._generate_d3_html(
            title="Dependency Graph",
            nodes=nodes,
            links=links,
            description="Visualization of file dependencies in the codebase. Hover over nodes to see file paths.",
        )

        # Write to file
        output_path = self.output_dir / filename
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return str(output_path)

    def generate_complexity_chart(
        self, analysis_result: Dict[str, Any], filename: str = "complexity_chart.html"
    ) -> str:
        """
        Generate a chart visualizing code complexity metrics.

        Args:
            analysis_result: Analysis result dictionary
            filename: Output filename

        Returns:
            Path to the generated HTML file
        """
        if "complexity_metrics" not in analysis_result:
            return "No complexity data available"

        complexity_metrics = analysis_result["complexity_metrics"]
        summary = complexity_metrics["summary"]

        # Extract data for visualization
        labels = []
        complexities = []
        functions = []

        # If we have file-specific metrics, extract them
        if "files" in complexity_metrics:
            # Create a list of (file_path, complexity) tuples
            file_complexities = []

            for file_path, file_data in complexity_metrics["files"].items():
                # Calculate total complexity for the file
                file_funcs = file_data.get("functions", [])
                total_complexity = sum(func.get("complexity", 1) for func in file_funcs)
                num_functions = len(file_funcs)

                if num_functions > 0:
                    avg_complexity = total_complexity / num_functions
                    file_complexities.append((file_path, avg_complexity, num_functions))

            # Sort by average complexity and take top 10
            file_complexities.sort(key=lambda x: x[1], reverse=True)
            top_files = file_complexities[:10]

            # Extract data for chart
            for file_path, avg_complexity, num_funcs in top_files:
                # Use basename to shorten the display
                base_name = os.path.basename(file_path)
                labels.append(base_name)
                complexities.append(avg_complexity)
                functions.append(num_funcs)

        # If we don't have any file data, show summary data
        if not labels and summary.get("total_functions", 0) > 0:
            labels = ["All Files"]
            complexities = [summary.get("avg_complexity", 0)]
            functions = [summary.get("total_functions", 0)]

        # Create the chart HTML
        chart_html = self._generate_chart_html(
            title="Code Complexity",
            chart_type="bar",
            labels=labels,
            datasets=[
                {
                    "label": "Average Complexity",
                    "data": complexities,
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "borderWidth": 1,
                },
                {
                    "label": "Number of Functions",
                    "data": functions,
                    "backgroundColor": "rgba(153, 102, 255, 0.2)",
                    "borderColor": "rgba(153, 102, 255, 1)",
                    "borderWidth": 1,
                    "yAxisID": "y1",
                },
            ],
            options={
                "responsive": True,
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "title": {"display": True, "text": "Complexity"},
                    },
                    "y1": {
                        "beginAtZero": True,
                        "position": "right",
                        "grid": {"drawOnChartArea": False},
                        "title": {"display": True, "text": "Number of Functions"},
                    },
                },
            },
            description=f"""
                <p>This chart shows the average cyclomatic complexity of files in the codebase.</p>
                <p><strong>Total Functions</strong>: {summary.get('total_functions', 0)}</p>
                <p><strong>Average Complexity</strong>: {summary.get('avg_complexity', 0):.2f}</p>
                <p><strong>Maximum Complexity</strong>: {summary.get('max_complexity', 0)}</p>
            """,
        )

        # Write the chart HTML to a file
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(chart_html)

        return output_path

    def generate_file_type_chart(
        self, analysis_result: Dict[str, Any], filename: str = "file_types_chart.html"
    ) -> str:
        """
        Generate a chart visualizing file type distribution.

        Args:
            analysis_result: Analysis result dictionary
            filename: Output filename

        Returns:
            Path to the generated HTML file
        """
        if (
            "file_summary" not in analysis_result
            or "by_extension" not in analysis_result["file_summary"]
        ):
            return "No file data available"

        by_extension = analysis_result["file_summary"]["by_extension"]

        # Prepare data for pie chart
        labels = []
        data = []
        background_colors = []

        # List of colors for the chart (can be extended)
        colors = [
            "rgba(255, 99, 132, 0.8)",
            "rgba(54, 162, 235, 0.8)",
            "rgba(255, 206, 86, 0.8)",
            "rgba(75, 192, 192, 0.8)",
            "rgba(153, 102, 255, 0.8)",
            "rgba(255, 159, 64, 0.8)",
            "rgba(199, 199, 199, 0.8)",
            "rgba(83, 102, 255, 0.8)",
            "rgba(40, 159, 64, 0.8)",
            "rgba(210, 199, 199, 0.8)",
        ]

        # Sort extensions by file count
        sorted_extensions = sorted(
            by_extension.items(), key=lambda x: x[1], reverse=True
        )

        # Generate chart data
        other_count = 0
        for i, (ext, count) in enumerate(sorted_extensions):
            if i < 9:  # Show top 9 extensions individually
                labels.append(ext)
                data.append(count)
                background_colors.append(colors[i % len(colors)])
            else:  # Group remaining extensions as "Other"
                other_count += count

        # Add "Other" category if there are more than 9 extensions
        if other_count > 0:
            labels.append("Other")
            data.append(other_count)
            background_colors.append("rgba(169, 169, 169, 0.8)")

        # Generate HTML with Chart.js
        html = self._generate_chart_html(
            title="File Type Distribution",
            chart_type="pie",
            labels=labels,
            datasets=[
                {
                    "label": "File Types",
                    "data": data,
                    "backgroundColor": background_colors,
                    "borderColor": "rgba(255, 255, 255, 1)",
                    "borderWidth": 1,
                }
            ],
            options={
                "responsive": True,
                "plugins": {
                    "legend": {"position": "right"},
                    "tooltip": {
                        "callbacks": {
                            "label": "function(context) { return context.label + ': ' + context.raw + ' files'; }"
                        }
                    },
                },
            },
            description=f"""
                <p>This chart shows the distribution of file types in the codebase.</p>
                <p><strong>Total Files</strong>: {analysis_result['file_summary'].get('total_files', 0)}</p>
                <p><strong>Total Lines</strong>: {analysis_result['file_summary'].get('total_lines', 0)}</p>
            """,
        )

        # Write to file
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return output_path

    def generate_all_visualizations(
        self, analysis_result: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Generate all available visualizations.

        Args:
            analysis_result: Analysis result dictionary

        Returns:
            Dictionary mapping visualization types to file paths
        """
        visualizations = {}

        # Generate dependency graph
        try:
            dep_graph_path = self.generate_dependency_graph(analysis_result)
            if (
                dep_graph_path
                and isinstance(dep_graph_path, str)
                and not dep_graph_path.startswith("No")
            ):
                visualizations["dependency_graph"] = dep_graph_path
        except Exception as e:
            print(f"Error generating dependency graph: {str(e)}")

        # Generate complexity chart
        try:
            complexity_chart_path = self.generate_complexity_chart(analysis_result)
            if (
                complexity_chart_path
                and isinstance(complexity_chart_path, str)
                and not complexity_chart_path.startswith("No")
            ):
                visualizations["complexity_chart"] = complexity_chart_path
        except Exception as e:
            print(f"Error generating complexity chart: {str(e)}")

        # Generate file type chart
        try:
            file_type_chart_path = self.generate_file_type_chart(analysis_result)
            if (
                file_type_chart_path
                and isinstance(file_type_chart_path, str)
                and not file_type_chart_path.startswith("No")
            ):
                visualizations["file_type_chart"] = file_type_chart_path
        except Exception as e:
            print(f"Error generating file type chart: {str(e)}")

        return visualizations

    def _generate_d3_html(
        self,
        title: str,
        nodes: List[Dict[str, Any]],
        links: List[Dict[str, Any]],
        description: str = "",
    ) -> str:
        """
        Generate HTML with D3.js for graph visualization.

        Args:
            title: Chart title
            nodes: List of node objects with id, name, and group
            links: List of link objects with source, target, and value
            description: Description of the visualization

        Returns:
            HTML content as string
        """
        # Serialize nodes and links to JSON
        nodes_json = json.dumps(nodes)
        links_json = json.dumps(links)

        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        #description {{
            margin: 20px 0;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }}
        #chart {{
            width: 100%;
            height: 700px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .node circle {{
            stroke: #fff;
            stroke-width: 1.5px;
        }}
        .link {{
            stroke: #999;
            stroke-opacity: 0.6;
        }}
        .tooltip {{
            position: absolute;
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            pointer-events: none;
        }}
    </style>
    <script src="https://d3js.org/d3.v5.min.js"></script>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div id="description">{description}</div>
        <div id="chart"></div>
    </div>
    
    <script>
        // Graph data
        const graph = {{
            nodes: {nodes_json},
            links: {links_json}
        }};
        
        // Set up D3 visualization
        const width = document.getElementById('chart').clientWidth;
        const height = document.getElementById('chart').clientHeight;
        
        // Create SVG
        const svg = d3.select('#chart')
            .append('svg')
            .attr('width', width)
            .attr('height', height);
            
        // Create tooltip
        const tooltip = d3.select('body').append('div')
            .attr('class', 'tooltip')
            .style('opacity', 0);
            
        // Set up force simulation
        const simulation = d3.forceSimulation(graph.nodes)
            .force('link', d3.forceLink(graph.links).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .on('tick', ticked);
            
        // Define color scale for node groups
        const color = d3.scaleOrdinal(d3.schemeCategory10);
        
        // Create links
        const link = svg.append('g')
            .selectAll('line')
            .data(graph.links)
            .enter().append('line')
            .attr('class', 'link')
            .attr('stroke-width', d => Math.sqrt(d.value));
            
        // Create nodes
        const node = svg.append('g')
            .selectAll('circle')
            .data(graph.nodes)
            .enter().append('circle')
            .attr('class', 'node')
            .attr('r', 8)
            .attr('fill', d => color(d.group))
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended))
            .on('mouseover', function(d) {{
                tooltip.transition()
                    .duration(200)
                    .style('opacity', .9);
                tooltip.html(d.name)
                    .style('left', (d3.event.pageX + 5) + 'px')
                    .style('top', (d3.event.pageY - 28) + 'px');
            }})
            .on('mouseout', function(d) {{
                tooltip.transition()
                    .duration(500)
                    .style('opacity', 0);
            }});
            
        // Update positions on tick
        function ticked() {{
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
                
            node
                .attr('cx', d => d.x)
                .attr('cy', d => d.y);
        }}
        
        // Drag functions
        function dragstarted(d) {{
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(d) {{
            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }}
        
        function dragended(d) {{
            if (!d3.event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
    </script>
</body>
</html>
"""

    def _generate_chart_html(
        self,
        title: str,
        chart_type: str,
        labels: List[str],
        datasets: List[Dict[str, Any]],
        options: Dict[str, Any] = None,
        description: str = "",
    ) -> str:
        """
        Generate HTML with Chart.js for data visualization.

        Args:
            title: Chart title
            chart_type: Chart.js chart type (bar, line, pie, etc.)
            labels: Labels for data points
            datasets: List of dataset objects with data and styling
            options: Additional Chart.js options
            description: Description text for the visualization

        Returns:
            HTML content as string
        """
        # Convert Python structures to JSON for JavaScript
        labels_json = json.dumps(labels)
        datasets_json = json.dumps(datasets)
        options_json = json.dumps(options or {})

        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        .description {{
            margin: 20px 0;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }}
        .chart-container {{
            width: 100%;
            height: 600px;
            margin-top: 20px;
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="description">
            {description}
        </div>
        <div class="chart-container">
            <canvas id="myChart"></canvas>
        </div>
    </div>

    <script>
        // Get the canvas element
        const ctx = document.getElementById('myChart').getContext('2d');
        
        // Create the chart
        const myChart = new Chart(ctx, {{
            type: '{chart_type}',
            data: {{
                labels: {labels_json},
                datasets: {datasets_json}
            }},
            options: {options_json}
        }});
    </script>
</body>
</html>
"""

    def generate_network_graph(
        self,
        dependencies: Dict[str, List[str]],
        output_file: str = "dependency_graph.html",
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Generate a network graph visualization of dependencies.

        Args:
            dependencies: Dictionary of file dependencies
            output_file: Output filename
            options: Additional options for the visualization
        """
        # Implementation of the method
        pass
