import unittest
import sys
import io
from contextlib import redirect_stdout

import bfs_output
from graph import create_graph
from graph_lists import all_lists_dict
from graph_matrix import all_matrix_dict


def create_adjacency_list(img_graph):
    """
    Create and store the adjacency list as a dictionary.
    Each vertex is represented as a tuple (color, x, y, edges).
    """
    adjacency_list = {}
    for vertex in img_graph.vertices:
        adjacency_list[vertex.index] = (vertex.color, vertex.x, vertex.y, vertex.edges)
    return adjacency_list


def check_graph(actual_graph, correct_graph):
    """
    Helper function that checks if the student graph is correct given the correct graph.

    Parameters:
        actual_graph (dict): Graph produced by the student's code, with the same format as correct_graph.
        correct_graph (dict): The correct graph to compare against.

    Returns:
        bool: True if the graphs match, False otherwise.
        str: Error message if graphs do not match.
    """
    # Check if both graphs have the same number of vertices
    if set(actual_graph.keys()) != set(correct_graph.keys()):
        return (
            False,
            "Mismatch in vertices: keys in student graph do not match correct graph.",
        )

    for vertex, (color, x, y, edges) in correct_graph.items():
        if vertex not in actual_graph:
            return False, f"Vertex {vertex} missing in the student graph."

        student_vertex = actual_graph[vertex]
        student_color, student_x, student_y, student_edges = student_vertex

        # Check color, x, and y values
        if student_color != color:
            return (
                False,
                f"Mismatch in color for vertex {vertex}: expected {color}, got {student_color}.",
            )
        if student_x != x:
            return (
                False,
                f"Mismatch in x for vertex {vertex}: expected {x}, got {student_x}.",
            )
        if student_y != y:
            return (
                False,
                f"Mismatch in y for vertex {vertex}: expected {y}, got {student_y}.",
            )

        # Check edges (ensure they are sorted)
        if sorted(student_edges) != sorted(edges):
            return (
                False,
                f"Mismatch in edges for vertex {vertex}: expected {sorted(edges)}, got {sorted(student_edges)}.",
            )

    # If all checks pass
    return True, "Graphs match successfully."


class TestCreateGraph(unittest.TestCase):
    """Test Suite for create_graph Function"""

    def test_create_graph_1(self):
        """Test chess graph: Validates adjacency list creation."""
        with open("chess.in", encoding="utf-8") as f:
            data = f.read()
            actual_graph, search_start, search_color = create_graph(data)
            actual_graph_adjacency_list = create_adjacency_list(actual_graph)
            result, message = check_graph(
                actual_graph_adjacency_list, all_lists_dict["chess"]
            )
            self.assertTrue(result, message)
            self.assertEqual(search_start, 34)
            self.assertEqual(search_color, "white")

    def test_create_graph_2(self):
        """Test f1 graph: Checks Validates adjacency list creation."""
        with open("f1.in", encoding="utf-8") as f:
            data = f.read()
            actual_graph, search_start, search_color = create_graph(data)
            actual_graph_adjacency_list = create_adjacency_list(actual_graph)
            result, message = check_graph(
                actual_graph_adjacency_list, all_lists_dict["f1"]
            )
            self.assertTrue(result, message)
            self.assertEqual(search_start, 78)
            self.assertEqual(search_color, "red")

    def test_create_graph_3(self):
        """Test flags graph: Validates adjacency list creation."""
        with open("flags.in", encoding="utf-8") as f:
            data = f.read()
            actual_graph, search_start, search_color = create_graph(data)
            actual_graph_adjacency_list = create_adjacency_list(actual_graph)
            result, message = check_graph(
                actual_graph_adjacency_list, all_lists_dict["flags"]
            )
            self.assertTrue(result, message)
            self.assertEqual(search_start, 9)
            self.assertEqual(search_color, "white")

    def test_create_graph_4(self):
        """Test heart graph: Validates adjacency list creation."""
        with open("heart.in", encoding="utf-8") as f:
            data = f.read()
            actual_graph, search_start, search_color = create_graph(data)
            actual_graph_adjacency_list = create_adjacency_list(actual_graph)
            result, message = check_graph(
                actual_graph_adjacency_list, all_lists_dict["heart"]
            )
            self.assertTrue(result, message)
            self.assertEqual(search_start, 45)
            self.assertEqual(search_color, "magenta")

    def test_create_graph_5(self):
        """Test horns graph: Validates adjacency Validates adjacency list creation."""
        with open("horns.in", encoding="utf-8") as f:
            data = f.read()
            actual_graph, search_start, search_color = create_graph(data)
            actual_graph_adjacency_list = create_adjacency_list(actual_graph)
            result, message = check_graph(
                actual_graph_adjacency_list, all_lists_dict["horns"]
            )
            self.assertTrue(result, message)
            self.assertEqual(search_start, 93)
            self.assertEqual(search_color, "green")

    def test_create_graph_6(self):
        """Test small graph: Validates adjacency list creation."""
        with open("small.in", encoding="utf-8") as f:
            data = f.read()
            actual_graph, search_start, search_color = create_graph(data)
            actual_graph_adjacency_list = create_adjacency_list(actual_graph)
            result, message = check_graph(
                actual_graph_adjacency_list, all_lists_dict["small"]
            )
            self.assertTrue(result, message)
            self.assertEqual(search_start, 2)
            self.assertEqual(search_color, "green")


class TestAdjacencyMatrix(unittest.TestCase):
    """create_adjacency_matrix Test Suite"""

    def test_create_adjacency_matrix_1(self):
        """Test chess matrix: Validates the adjacency matrix creation for a chessboard-like graph."""
        with open("chess.in", encoding="utf-8") as f:
            data = f.read()
            actual_graph, _, _ = create_graph(data)
            student_adjancey_matrix = actual_graph.create_adjacency_matrix()
            self.assertEqual(student_adjancey_matrix, all_matrix_dict["chess"])

    def test_create_adjacency_matrix_2(self):
        """Test f1 matrix: Validates the adjacency matrix creation for a check-like graph."""
        with open("check.in", encoding="utf-8") as f:
            data = f.read()
            actual_graph, _, _ = create_graph(data)
            student_adjancey_matrix = actual_graph.create_adjacency_matrix()
            self.assertEqual(student_adjancey_matrix, all_matrix_dict["check"])

    def test_create_adjacency_matrix_3(self):
        """Test flags matrix: Validates the adjacency matrix creation for a f1-like graph."""
        with open("flags.in", encoding="utf-8") as f:
            data = f.read()
            actual_graph, _, _ = create_graph(data)
            student_adjancey_matrix = actual_graph.create_adjacency_matrix()
            self.assertEqual(student_adjancey_matrix, all_matrix_dict["flags"])

    def test_create_adjacency_matrix_4(self):
        """Test heart matrix: Validates the adjacency matrix creation for a heart-like graph."""
        with open("heart.in", encoding="utf-8") as f:
            data = f.read()
            actual_graph, _, _ = create_graph(data)
            student_adjancey_matrix = actual_graph.create_adjacency_matrix()
            self.assertEqual(student_adjancey_matrix, all_matrix_dict["heart"])

    def test_create_adjacency_matrix_5(self):
        """Test horns matrix: Validates the adjacency matrix creation for a random-like graph."""
        with open("random.in", encoding="utf-8") as f:
            data = f.read()
            actual_graph, _, _ = create_graph(data)
            student_adjancey_matrix = actual_graph.create_adjacency_matrix()
            self.assertEqual(student_adjancey_matrix, all_matrix_dict["random"])

    def test_create_adjacency_matrix_6(self):
        """Test small matrix: Validates the adjacency matrix creation for a small-like graph."""
        with open("small.in", encoding="utf-8") as f:
            data = f.read()
            actual_graph, _, _ = create_graph(data)
            student_adjancey_matrix = actual_graph.create_adjacency_matrix()
            self.assertEqual(student_adjancey_matrix, all_matrix_dict["small"])


class TestBFS(unittest.TestCase):
    """BFS Test Suite"""

    def check_bfs(self, filename, levels, visited):
        # read input
        with open(filename, encoding="utf-8") as f:
            data = f.read()
            actual_graph, search_start, search_color = create_graph(data)

            # Validate that the correct graph is created before continuing.
            actual_graph_adjacency_list = create_adjacency_list(actual_graph)
            result, message = check_graph(
                actual_graph_adjacency_list,
                all_lists_dict[filename.split("/")[-1].rstrip(".in")],
            )
            self.assertTrue(result, message)

            # Capture print statements as a string.
            print_output = io.StringIO()
            with redirect_stdout(print_output):
                actual_graph.bfs(search_start, search_color)
            print_output = print_output.getvalue()

            actual_visited_order = []

            # Extract order of visited vertices.
            for line in print_output.split("\n"):
                if line.startswith("Visited vertex "):
                    actual_visited_order.append(int(line.split("Visited vertex ")[-1]))

            # Check if vertices were visited twice.
            visited_set = list(set(actual_visited_order))
            if len(visited_set) != len(actual_visited_order):
                actual_visited_order.sort()

                for i in range(1, len(actual_visited_order)):
                    if actual_visited_order[i] == actual_visited_order[i - 1]:
                        self.fail(
                            f"Vertex {actual_visited_order[i]} was visited twice."
                        )

            # Make sure vertices that are further are not visited while closer ones
            # haven't been visited
            for vertex in actual_visited_order:
                # make sure levels is not empty
                if len(levels) < 1:
                    self.fail(
                        f"Visited vertex {vertex}"
                        " even though there are no more vertices that need to be visited."
                    )
                    return False

                # Remove current level if every vertex has been visited
                if len(levels[0]) < 1:
                    levels.pop(0)

                # make sure again levels is not empty
                if len(levels) < 1:
                    print(
                        f"Visited vertex {vertex}"
                        + " even though there are no more vertices that need to be visited."
                    )

                # check that vertex should actually be visited
                if not vertex in visited:
                    self.fail(
                        f"Vertex {vertex}"
                        " was visited even though it is not the right color."
                    )

                # check that the vertex is in the current level
                if not vertex in levels[0]:
                    self.fail(f"Vertex {vertex} was visited too early.")

                # if all tests pass: remove vertex from level
                levels[0].remove(vertex)

            # check if all vertices were visited
            while (len(levels) > 0) and (len(levels[0]) < 1):
                levels.pop(0)

            if len(levels) > 0:
                print("vertex " + str(levels[0][0]) + " was never visited.")
                return False

            return True

    def test_bfs_1(self):
        """Test BFS on chess graph: Validates BFS traversal on the chess graph input."""
        levels, visited = bfs_output.chess_levels, bfs_output.chess_visited
        self.check_bfs("chess.in", levels, visited)

    def test_bfs_2(self):
        """Test BFS on F1 graph: Validates BFS traversal on the F1 circuit layout graph."""
        levels, visited = bfs_output.f1_levels, bfs_output.f1_visited
        self.check_bfs("f1.in", levels, visited)

    def test_bfs_3(self):
        """Test BFS on flags graph: Validates BFS traversal on the flags graph input."""
        levels, visited = bfs_output.flags_levels, bfs_output.flags_visited
        self.check_bfs("flags.in", levels, visited)

    def test_bfs_4(self):
        """Test BFS on heart graph: Validates BFS traversal on the heart-shaped graph."""
        levels, visited = bfs_output.heart_levels, bfs_output.heart_visited
        self.check_bfs("heart.in", levels, visited)

    def test_bfs_5(self):
        """Test BFS on horns graph: Validates BFS traversal on the horns-shaped graph."""
        levels, visited = bfs_output.horns_levels, bfs_output.horns_visited
        self.check_bfs("horns.in", levels, visited)

    def test_bfs_6(self):
        """Test BFS on small graph: Validates BFS traversal on a small, simple graph."""
        levels, visited = bfs_output.small_levels, bfs_output.small_visited
        self.check_bfs("small.in", levels, visited)


class TestDFS(unittest.TestCase):
    """DFS Test Suite"""

    def check_dfs(self, filename, visited):
        """Validates that the search order is depth first search"""
        # read input
        with open(filename, encoding="utf-8") as f:
            data = f.read()
            actual_graph, search_start, search_color = create_graph(data)

            # Validate that the correct graph is created before continuing.
            actual_graph_adjacency_list = create_adjacency_list(actual_graph)
            result, message = check_graph(
                actual_graph_adjacency_list,
                all_lists_dict[filename.split("/")[-1].rstrip(".in")],
            )
            self.assertTrue(result, message)

            # Capture print statements as a string.
            print_output = io.StringIO()
            with redirect_stdout(print_output):
                actual_graph.dfs(search_start, search_color)
            print_output = print_output.getvalue()

            actual_visited_order = []

            # Extract order of visited vertices.
            for line in print_output.split("\n"):
                if line.startswith("Visited vertex "):
                    actual_visited_order.append(int(line.split("Visited vertex ")[-1]))

            # Check if vertices were visited twice.
            visited_set = list(set(actual_visited_order))
            if len(visited_set) != len(actual_visited_order):
                actual_visited_order.sort()

                for i in range(1, len(actual_visited_order)):
                    if actual_visited_order[i] == actual_visited_order[i - 1]:
                        self.fail(
                            f"Vertex {actual_visited_order[i]} was visited twice."
                        )

            if set(visited) != set(actual_visited_order):
                # Check if all vertices were visited
                for vertex in visited:
                    if not vertex in actual_visited_order:
                        self.fail(f"Vertex {vertex} has not been visited.")

                # Check if more than all vertices were visited
                for vertex in actual_visited_order:
                    if not vertex in visited:
                        self.fail(f"Vertex {vertex} should not have been visited.")

            # Reset graph
            actual_graph, search_start, search_color = create_graph(data)
            print_output = io.StringIO()

            # Verify that the visited order is DFS
            with redirect_stdout(print_output):
                self.check_visited_order(
                    actual_graph, search_start, search_color, actual_visited_order, 1
                )

    def check_visited_order(self, graph, vertex_index, color, visit_list, list_index):
        """Recursive check to verify depth first search order"""
        # color the visited vertex
        graph.vertices[vertex_index].visit_and_set_color(color)

        # check if the vertex that was visited next is a neighbor of this vertex
        while (list_index < len(visit_list)) and (
            visit_list[list_index] in graph.vertices[vertex_index].edges
        ):
            # keep going there
            list_index = self.check_visited_order(
                graph, visit_list[list_index], color, visit_list, list_index + 1
            )

        # check if there is a neightbor we could still visit
        for neighbor in graph.vertices[vertex_index].edges:
            # check if the vertex has the correct color and is not already visited; visit
            if (not graph.vertices[neighbor].visited) and (
                graph.vertices[neighbor].color
                == graph.vertices[vertex_index].prev_color
            ):
                self.fail(
                    f"vertex {neighbor} wasn't visited after vertex"
                    f" {vertex_index} (maximum depth not reached)."
                )

        return list_index

    def test_dfs_1(self):
        """Test DFS on the chess graph using visited order of vertices"""
        visited = bfs_output.chess_visited
        self.check_dfs("chess.in", visited)

    def test_dfs_2(self):
        """Test DFS on the f1 graph using visited order of vertices"""
        visited = bfs_output.f1_visited
        self.check_dfs("f1.in", visited)

    def test_dfs_3(self):
        """Test DFS on the flags graph using visited order of vertices"""
        visited = bfs_output.flags_visited
        self.check_dfs("flags.in", visited)

    def test_dfs_4(self):
        """Test DFS on the heart graph using visited order of vertices"""
        visited = bfs_output.heart_visited
        self.check_dfs("heart.in", visited)

    def test_dfs_5(self):
        """Test DFS on the horns graph using visited order of vertices"""
        visited = bfs_output.horns_visited
        self.check_dfs("horns.in", visited)

    def test_dfs_6(self):
        """Test DFS on the small graph using visited order of vertices"""
        visited = bfs_output.small_visited
        self.check_dfs("small.in", visited)


def main():
    """Main function to run tests based on command-line arguments."""
    test_cases = {
        "graph": TestCreateGraph,
        "matrix": TestAdjacencyMatrix,
        "bfs": TestBFS,
        "dfs": TestDFS,
    }

    usage_string = (
        "Usage: python3 test_graph.py [test_method_or_function] [test_number]\n"
        "Examples:\n"
        "    python3 test_graph.py matrix 1\n"
        "    python3 test_reducible.py dfs 4\n"
        "Valid options for [test_method_or_function]: "
        + ", ".join(test_cases.keys())
        + "\n"
        "Test cases range 1-6 for all methods and functions."
    )
    if len(sys.argv) > 3:
        print(usage_string)
        return
    if len(sys.argv) == 1:
        unittest.main()
        return
    sys.argv = sys.argv[1:]
    test_name = sys.argv[0]
    if test_name not in test_cases:
        print(
            f"Invalid test name: {test_name}. Valid options are: {', '.join(test_cases.keys())}"
        )
        return
    if len(sys.argv) == 1:
        # Extract test case based on the first command-line argument
        suite = unittest.TestLoader().loadTestsFromTestCase(test_cases[test_name])
    else:
        test_num = sys.argv[1]
        loader = unittest.TestLoader()

        # Load all tests from the test case class
        all_tests = loader.loadTestsFromTestCase(test_cases[test_name])
        suite = unittest.TestSuite()
        # Filter tests that end with 'test_num'
        for test in all_tests:
            if test.id().split(".")[-1].split("_")[-1] == test_num:
                suite.addTest(test)
        if not suite.countTestCases():
            print(usage_string)
            return
    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    main()
