"""
Script to generate and plot triangles using different high-performance libraries
- Matplotlib (good for <100 triangles)
- Plotly (great for 1000s of triangles, interactive)
- Numpy optimized matplotlib (faster than regular matplotlib)
"""

import matplotlib.pyplot as plt
import numpy as np
import random
import time
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Import Plotly for high-performance 3D visualization
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly not available. Install with: pip install plotly")


def generate_random_triangle_3d():
    """Generate a random triangle with 3 vertices in 3D space"""
    # Generate 3 random points (x, y, z coordinates)
    vertices = []
    for _ in range(3):
        x = random.uniform(-10, 10)  # Random x coordinate between -10 and 10
        y = random.uniform(-10, 10)  # Random y coordinate between -10 and 10
        z = random.uniform(-10, 10)  # Random z coordinate between -10 and 10
        vertices.append([x, y, z])
    return np.array(vertices)


def generate_random_color():
    """Generate a random RGB color"""
    return (random.random(), random.random(), random.random())


def generate_multiple_triangles_vectorized(n):
    """Generate n triangles using vectorized numpy operations (much faster)"""
    # Generate all vertices at once: n triangles * 3 vertices * 3 coordinates
    vertices = np.random.uniform(-10, 10, (n, 3, 3))
    colors = np.random.rand(n, 3)  # RGB colors for each triangle
    return vertices, colors


def plot_triangles_plotly(n=2000):
    """Plot triangles using Plotly - much faster for large numbers"""
    if not PLOTLY_AVAILABLE:
        print("Plotly not available. Please install with: pip install plotly")
        return

    print(f"Generating {n} triangles with vectorized operations...")
    start_time = time.time()

    # Generate triangles vectorized
    triangles, colors = generate_multiple_triangles_vectorized(n)

    # Prepare data for Plotly
    x_data = []
    y_data = []
    z_data = []
    i_data = []  # Triangle indices
    j_data = []
    k_data = []
    triangle_colors = []

    vertex_count = 0
    for tri_idx, triangle in enumerate(triangles):
        # Add vertices
        x_data.extend(triangle[:, 0])
        y_data.extend(triangle[:, 1])
        z_data.extend(triangle[:, 2])

        # Define triangle face indices
        i_data.append(vertex_count)
        j_data.append(vertex_count + 1)
        k_data.append(vertex_count + 2)
        vertex_count += 3

        # Color for this triangle
        color = colors[tri_idx]
        triangle_colors.append(f'rgb({int(color[0]*255)}, {int(color[1]*255)}, {int(color[2]*255)})')

    generation_time = time.time() - start_time
    print(f"Triangle generation completed in {generation_time:.3f} seconds")

    # Create Plotly 3D mesh
    fig = go.Figure(data=[
        go.Mesh3d(
            x=x_data,
            y=y_data,
            z=z_data,
            i=i_data,
            j=j_data,
            k=k_data,
            facecolor=triangle_colors,
            opacity=0.8,
            showscale=False
        )
    ])

    fig.update_layout(
        title=f'{n} Random 3D Triangles (Plotly - High Performance)',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        width=1000,
        height=800
    )

    total_time = time.time() - start_time
    print(f"Total visualization time: {total_time:.3f} seconds")

    fig.show()


def plot_triangles_matplotlib_optimized(n=1000):
    """Optimized matplotlib version using vectorized operations"""
    print(f"Generating {n} triangles with optimized matplotlib...")
    start_time = time.time()

    triangles, colors = generate_multiple_triangles_vectorized(n)

    # Create plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Convert to format expected by Poly3DCollection
    poly3d = Poly3DCollection(triangles, alpha=0.7, linewidths=0.5,
                             edgecolors='none')
    poly3d.set_facecolors(colors)
    ax.add_collection3d(poly3d)

    # Set limits
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_zlim(-12, 12)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'{n} Random 3D Triangles (Matplotlib Optimized)')

    total_time = time.time() - start_time
    print(f"Matplotlib optimized visualization time: {total_time:.3f} seconds")

    plt.show()


def plot_triangles_plotly_scatter(n=5000):
    """Alternative Plotly method using scatter3d - very fast for many triangles"""
    if not PLOTLY_AVAILABLE:
        print("Plotly not available.")
        return

    print(f"Generating {n} triangles as scatter plot...")
    start_time = time.time()

    triangles, colors = generate_multiple_triangles_vectorized(n)

    # Flatten all vertices
    all_vertices = triangles.reshape(-1, 3)
    all_colors = np.repeat(colors, 3, axis=0)  # Repeat each color 3 times for 3 vertices

    # Create scatter plot
    fig = go.Figure(data=go.Scatter3d(
        x=all_vertices[:, 0],
        y=all_vertices[:, 1],
        z=all_vertices[:, 2],
        mode='markers',
        marker=dict(
            size=3,
            color=all_colors,
            opacity=0.8
        ),
        text=[f'Triangle {i//3 + 1}, Vertex {i%3 + 1}' for i in range(len(all_vertices))],
        hovertemplate='<b>%{text}</b><br>X: %{x}<br>Y: %{y}<br>Z: %{z}<extra></extra>'
    ))

    fig.update_layout(
        title=f'{n} Random Triangles as Scatter Points (Ultra Fast)',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        width=1000,
        height=800
    )

    total_time = time.time() - start_time
    print(f"Scatter plot visualization time: {total_time:.3f} seconds")

    fig.show()


def benchmark_methods():
    """Benchmark different visualization methods"""
    print("=== VISUALIZATION BENCHMARK ===\n")

    # Test with different sizes
    sizes = [100, 500, 1000]

    for n in sizes:
        print(f"\n--- Testing with {n} triangles ---")

        # Matplotlib optimized
        print("1. Matplotlib (optimized):")
        start = time.time()
        try:
            plot_triangles_matplotlib_optimized(n)
            print(f"   ✓ Completed in {time.time() - start:.3f} seconds")
        except Exception as e:
            print(f"   ✗ Failed: {e}")

        # Plotly mesh (if available)
        if PLOTLY_AVAILABLE:
            print("2. Plotly Mesh3d:")
            start = time.time()
            try:
                plot_triangles_plotly(n)
                print(f"   ✓ Completed in {time.time() - start:.3f} seconds")
            except Exception as e:
                print(f"   ✗ Failed: {e}")

        input("Press Enter to continue to next test...")

    print("\n=== BENCHMARK COMPLETE ===")


def plot_triangles_3d(n=20):
    """Generate and plot n random triangles in 3D"""
    # Create figure and 3D axis
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Store all triangles for batch processing
    triangles = []
    colors = []

    # Generate and collect n triangles
    for i in range(n):
        # Generate random triangle vertices
        triangle_vertices = generate_random_triangle_3d()
        triangles.append(triangle_vertices)
        colors.append(generate_random_color())

    # Create 3D polygon collection
    poly3d = Poly3DCollection(triangles, alpha=0.7, linewidths=2,
                             edgecolors='black')
    poly3d.set_facecolors(colors)
    ax.add_collection3d(poly3d)

    # Set plot properties
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_zlim(-12, 12)
    ax.set_xlabel('X coordinate', fontsize=12)
    ax.set_ylabel('Y coordinate', fontsize=12)
    ax.set_zlabel('Z coordinate', fontsize=12)
    ax.set_title(f'{n} Random 3D Triangles', fontsize=16, fontweight='bold')

    # Add grid
    ax.grid(True, alpha=0.3)

    # Show the plot
    plt.tight_layout()
    plt.show()


def plot_triangles_alternative_3d(n=20):
    """Alternative method using individual triangle plots in 3D"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    for i in range(n):
        # Generate random triangle vertices
        triangle_vertices = generate_random_triangle_3d()

        # Close the triangle by adding the first vertex at the end
        closed_triangle = np.vstack([triangle_vertices, triangle_vertices[0]])

        # Plot triangle outline and surface
        color = generate_random_color()

        # Plot edges
        ax.plot(closed_triangle[:, 0], closed_triangle[:, 1], closed_triangle[:, 2],
                color=color, linewidth=3, marker='o', markersize=6)

        # Plot surface
        ax.plot_trisurf(triangle_vertices[:, 0], triangle_vertices[:, 1],
                       triangle_vertices[:, 2], color=color, alpha=0.6)

    # Set plot properties
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_zlim(-12, 12)
    ax.set_xlabel('X coordinate', fontsize=12)
    ax.set_ylabel('Y coordinate', fontsize=12)
    ax.set_zlabel('Z coordinate', fontsize=12)
    ax.set_title(f'{n} Random 3D Triangles (Alternative Method)',
                 fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def compare_3d_methods(n=10):
    """Show both 3D plotting methods side by side"""
    # Set random seed for consistent comparison
    random.seed(42)
    np.random.seed(42)

    # Create subplot with two 3D plots
    fig = plt.figure(figsize=(20, 8))

    # First method - Poly3DCollection
    ax1 = fig.add_subplot(121, projection='3d')
    triangles = []
    colors = []

    for i in range(n):
        triangle_vertices = generate_random_triangle_3d()
        triangles.append(triangle_vertices)
        colors.append(generate_random_color())

    poly3d = Poly3DCollection(triangles, alpha=0.7, linewidths=2,
                             edgecolors='black')
    poly3d.set_facecolors(colors)
    ax1.add_collection3d(poly3d)

    ax1.set_xlim(-12, 12)
    ax1.set_ylim(-12, 12)
    ax1.set_zlim(-12, 12)
    ax1.set_title('Method 1: Poly3DCollection', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Second method - Individual plot_trisurf
    ax2 = fig.add_subplot(122, projection='3d')

    # Reset random seed for same triangles
    random.seed(42)
    np.random.seed(42)

    for i in range(n):
        triangle_vertices = generate_random_triangle_3d()
        color = generate_random_color()

        ax2.plot_trisurf(triangle_vertices[:, 0], triangle_vertices[:, 1],
                        triangle_vertices[:, 2], color=color, alpha=0.6)

    ax2.set_xlim(-12, 12)
    ax2.set_ylim(-12, 12)
    ax2.set_zlim(-12, 12)
    ax2.set_title('Method 2: Individual Surfaces', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# =====================================================================
# LINE PLOTTING FUNCTIONS
# =====================================================================

def generate_random_line_3d():
    """Generate a random line with start and end points in 3D space"""
    # Generate 2 random points (start and end)
    start_point = [
        random.uniform(-10, 10),  # x
        random.uniform(-10, 10),  # y
        random.uniform(-10, 10)   # z
    ]
    end_point = [
        random.uniform(-10, 10),  # x
        random.uniform(-10, 10),  # y
        random.uniform(-10, 10)   # z
    ]
    return np.array([start_point, end_point])


def generate_multiple_lines_vectorized(n):
    """Generate n lines using vectorized numpy operations (much faster)"""
    # Generate all line endpoints at once: n lines * 2 points * 3 coordinates
    lines = np.random.uniform(-10, 10, (n, 2, 3))
    colors = np.random.rand(n, 3)  # RGB colors for each line
    return lines, colors


def plot_lines_matplotlib_3d(n=1000):
    """Plot random lines using matplotlib 3D"""
    print(f"Plotting {n} lines using Matplotlib 3D...")
    start_time = time.time()

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Generate lines
    for i in range(n):
        line_points = generate_random_line_3d()
        color = generate_random_color()

        # Plot line
        ax.plot(line_points[:, 0], line_points[:, 1], line_points[:, 2],
                color=color, linewidth=1.5, alpha=0.7)

    # Set plot properties
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_zlim(-12, 12)
    ax.set_xlabel('X coordinate', fontsize=12)
    ax.set_ylabel('Y coordinate', fontsize=12)
    ax.set_zlabel('Z coordinate', fontsize=12)
    ax.set_title(f'{n} Random 3D Lines', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)

    total_time = time.time() - start_time
    print(f"Matplotlib line plotting completed in {total_time:.3f} seconds")

    plt.tight_layout()
    plt.show()


def plot_lines_matplotlib_vectorized(n=5000):
    """Plot lines using vectorized matplotlib operations (faster)"""
    print(f"Plotting {n} lines using vectorized Matplotlib...")
    start_time = time.time()

    # Generate all lines at once
    lines, colors = generate_multiple_lines_vectorized(n)

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plot all lines efficiently
    for i, (line, color) in enumerate(zip(lines, colors)):
        ax.plot(line[:, 0], line[:, 1], line[:, 2],
                color=color, linewidth=1, alpha=0.6)

    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_zlim(-12, 12)
    ax.set_xlabel('X coordinate', fontsize=12)
    ax.set_ylabel('Y coordinate', fontsize=12)
    ax.set_zlabel('Z coordinate', fontsize=12)
    ax.set_title(f'{n} Random 3D Lines (Vectorized)', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)

    total_time = time.time() - start_time
    print(f"Vectorized line plotting completed in {total_time:.3f} seconds")

    plt.tight_layout()
    plt.show()


def plot_lines_plotly(n=10000):
    """Plot random lines using Plotly - much faster for large numbers"""
    if not PLOTLY_AVAILABLE:
        print("Plotly not available. Please install with: pip install plotly")
        return

    print(f"Plotting {n} lines using Plotly...")
    start_time = time.time()

    # Generate lines vectorized
    lines, colors = generate_multiple_lines_vectorized(n)

    # Prepare data for Plotly
    fig = go.Figure()

    # Add each line as a separate trace (for different colors)
    for i, (line, color) in enumerate(zip(lines, colors)):
        fig.add_trace(go.Scatter3d(
            x=line[:, 0],
            y=line[:, 1],
            z=line[:, 2],
            mode='lines',
            line=dict(
                color=f'rgb({int(color[0]*255)}, {int(color[1]*255)}, {int(color[2]*255)})',
                width=3
            ),
            name=f'Line {i+1}',
            showlegend=False,  # Hide legend for better performance
            hovertemplate=f'<b>Line {i+1}</b><br>X: %{{x}}<br>Y: %{{y}}<br>Z: %{{z}}<extra></extra>'
        ))

    fig.update_layout(
        title=f'{n} Random 3D Lines (Interactive)',
        scene=dict(
            xaxis_title='X coordinate',
            yaxis_title='Y coordinate',
            zaxis_title='Z coordinate',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        width=1000,
        height=800
    )

    total_time = time.time() - start_time
    print(f"Plotly line plotting completed in {total_time:.3f} seconds")

    fig.show()


def plot_lines_plotly_single_trace(n=50000):
    """Plot lines using single Plotly trace (ultra fast for many lines)"""
    if not PLOTLY_AVAILABLE:
        print("Plotly not available. Please install with: pip install plotly")
        return

    print(f"Plotting {n} lines using Plotly single trace (ultra fast)...")
    start_time = time.time()

    # Generate lines vectorized
    lines, colors = generate_multiple_lines_vectorized(n)

    # Prepare data for single trace with None separators
    x_data = []
    y_data = []
    z_data = []

    for line in lines:
        x_data.extend([line[0, 0], line[1, 0], None])  # start_x, end_x, separator
        y_data.extend([line[0, 1], line[1, 1], None])  # start_y, end_y, separator
        z_data.extend([line[0, 2], line[1, 2], None])  # start_z, end_z, separator

    # Create single trace
    fig = go.Figure(data=go.Scatter3d(
        x=x_data,
        y=y_data,
        z=z_data,
        mode='lines',
        line=dict(color='blue', width=2),
        name='Lines',
        showlegend=False
    ))

    fig.update_layout(
        title=f'{n} Random 3D Lines (Ultra Fast Single Trace)',
        scene=dict(
            xaxis_title='X coordinate',
            yaxis_title='Y coordinate',
            zaxis_title='Z coordinate',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        width=1000,
        height=800
    )

    total_time = time.time() - start_time
    print(f"Ultra fast line plotting completed in {total_time:.3f} seconds")

    fig.show()


def plot_lines_plotly_colored_segments(n=20000):
    """Plot lines with gradient colors along segments"""
    if not PLOTLY_AVAILABLE:
        print("Plotly not available. Please install with: pip install plotly")
        return

    print(f"Plotting {n} gradient-colored line segments...")
    start_time = time.time()

    # Generate lines
    lines, _ = generate_multiple_lines_vectorized(n)

    # Create data with color gradients
    x_data = []
    y_data = []
    z_data = []
    colors_data = []

    for i, line in enumerate(lines):
        # Create multiple points along each line for gradient effect
        t = np.linspace(0, 1, 10)  # 10 points per line
        for j in range(len(t)):
            point = line[0] + t[j] * (line[1] - line[0])
            x_data.append(point[0])
            y_data.append(point[1])
            z_data.append(point[2])
            colors_data.append(i)  # Use line index for color

        # Add separator
        x_data.append(None)
        y_data.append(None)
        z_data.append(None)
        colors_data.append(None)

    fig = go.Figure(data=go.Scatter3d(
        x=x_data,
        y=y_data,
        z=z_data,
        mode='lines',
        line=dict(
            color=colors_data,
            colorscale='Viridis',
            width=3
        ),
        name='Gradient Lines',
        showlegend=False
    ))

    fig.update_layout(
        title=f'{n} Gradient-Colored 3D Lines',
        scene=dict(
            xaxis_title='X coordinate',
            yaxis_title='Y coordinate',
            zaxis_title='Z coordinate'
        ),
        width=1000,
        height=800
    )

    total_time = time.time() - start_time
    print(f"Gradient line plotting completed in {total_time:.3f} seconds")

    fig.show()


def main():
    """Main function with options for different visualization methods"""
    print("=== 3D Visualization Options ===\n")
    print("Choose visualization method:")
    print("\n--- TRIANGLE METHODS ---")
    print("1. Matplotlib Triangles (good for <100 triangles)")
    print("2. Matplotlib Optimized Triangles (good for <1000 triangles)")
    print("3. Plotly Mesh3d Triangles (excellent for 1000s of triangles)")
    print("4. Plotly Scatter Triangles (ultra-fast for 5000+ triangles)")
    print("\n--- LINE METHODS ---")
    print("5. Matplotlib Lines (good for <1000 lines)")
    print("6. Matplotlib Vectorized Lines (good for <5000 lines)")
    print("7. Plotly Interactive Lines (excellent for 10000s of lines)")
    print("8. Plotly Ultra-Fast Lines (single trace, 50000+ lines)")
    print("9. Plotly Gradient Lines (colorful line segments)")
    print("\n--- SPECIAL OPTIONS ---")
    print("10. Benchmark different methods")
    print("11. Quick triangle demo")
    print("12. Quick line demo")

    try:
        choice = input("\nEnter choice (1-12, or press Enter for triangle demo): ").strip()

        # Triangle methods
        if choice == "1":
            n = int(input("Number of triangles (recommended <100): ") or "50")
            plot_triangles_3d(n)

        elif choice == "2":
            n = int(input("Number of triangles (recommended <1000): ") or "500")
            plot_triangles_matplotlib_optimized(n)

        elif choice == "3":
            if PLOTLY_AVAILABLE:
                n = int(input("Number of triangles (can handle 1000s): ") or "2000")
                plot_triangles_plotly(n)
            else:
                print("Plotly not available. Please install with: pip install plotly")

        elif choice == "4":
            if PLOTLY_AVAILABLE:
                n = int(input("Number of triangles (can handle 10000s): ") or "5000")
                plot_triangles_plotly_scatter(n)
            else:
                print("Plotly not available. Please install with: pip install plotly")

        # Line methods
        elif choice == "5":
            n = int(input("Number of lines (recommended <1000): ") or "500")
            plot_lines_matplotlib_3d(n)

        elif choice == "6":
            n = int(input("Number of lines (recommended <5000): ") or "2000")
            plot_lines_matplotlib_vectorized(n)

        elif choice == "7":
            if PLOTLY_AVAILABLE:
                n = int(input("Number of lines (can handle 10000s): ") or "5000")
                plot_lines_plotly(n)
            else:
                print("Plotly not available. Please install with: pip install plotly")

        elif choice == "8":
            if PLOTLY_AVAILABLE:
                n = int(input("Number of lines (can handle 50000+): ") or "20000")
                plot_lines_plotly_single_trace(n)
            else:
                print("Plotly not available. Please install with: pip install plotly")

        elif choice == "9":
            if PLOTLY_AVAILABLE:
                n = int(input("Number of gradient lines (recommended <20000): ") or "5000")
                plot_lines_plotly_colored_segments(n)
            else:
                print("Plotly not available. Please install with: pip install plotly")

        # Special options
        elif choice == "10":
            benchmark_methods()

        elif choice == "12":
            print("\n=== Quick Line Demo ===")
            print("Showing 10000 lines with Plotly ultra-fast method...")
            if PLOTLY_AVAILABLE:
                plot_lines_plotly_single_trace(10000)
            else:
                print("Plotly not available, using matplotlib with 1000 lines...")
                plot_lines_matplotlib_3d(1000)

        else:  # Default triangle demo
            print("\n=== Quick Triangle Demo ===")
            print("Showing 2000 triangles with Plotly (fast method)...")

            if PLOTLY_AVAILABLE:
                plot_triangles_plotly(2000)
            else:
                print("Plotly not available, using matplotlib optimized with 500 triangles...")
                plot_triangles_matplotlib_optimized(500)

    except KeyboardInterrupt:
        print("\nVisualization cancelled.")
    except Exception as e:
        print(f"Error: {e}")
        print("Falling back to basic line visualization...")
        if PLOTLY_AVAILABLE:
            plot_lines_plotly_single_trace(1000)
        else:
            plot_lines_matplotlib_3d(100)


if __name__ == "__main__":
    main()
