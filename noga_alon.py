import math

def divide_graph(edges: list) -> list:
  '''
  Make a 2k-regular bipartite graph into two k-regular bipartite graphs
  '''

  # step 1: Find the circles from the edges.
  list_circles = []
  while len(edges) > 0:
    list_edges_of_circle = [edges.pop(0)]
    while len(edges) > 0:
      index_next_edge = None
      for i in range(len(edges)):
        if len(list_edges_of_circle) % 2 == 0:
          if edges[i]["v_x"] == list_edges_of_circle[-1]["v_x"]:
            index_next_edge = i
            break
        else:
          if edges[i]["v_y"] == list_edges_of_circle[-1]["v_y"]:
            index_next_edge = i
            break
      if index_next_edge is None:
        break
      list_edges_of_circle.append(edges.pop(i))
    list_circles.append(list_edges_of_circle)

  # step 2: Connect the circles into an Euler circuit.
  euler_circuit = list_circles.pop(0)
  while len(list_circles) > 0:
    for i in range(len(list_circles)):
      bool_find_next_edge = False
      for j in range(len(list_circles[i])):
        for k in range(len(euler_circuit)):
          if j % 2 != 0:
            if euler_circuit[k]["v_x"] == list_circles[i][j]["v_x"]:
              bool_find_next_edge = True
              break
          else:
            if euler_circuit[k]["v_y"] == list_circles[i][j]["v_y"]:
              bool_find_next_edge = True
              break
        if bool_find_next_edge:
          break
      if bool_find_next_edge:
        break
    circle_added_to_circuit = list_circles.pop(i)
    if bool_find_next_edge:
      euler_circuit = euler_circuit[:k] + circle_added_to_circuit[j:] + circle_added_to_circuit[:j] + euler_circuit[k:]
    else:
      euler_circuit += circle_added_to_circuit

  # step 3: Make two k-regular bipartite graphs.
  return_edges0 = []
  return_edges1 = []
  for i in range(len(euler_circuit)):
    if i % 2 == 1:
      return_edges0.append(euler_circuit[i])
    else:
      return_edges1.append(euler_circuit[i])
  return [return_edges0, return_edges1]

def bipartite_graph_coloring(part_x: list, part_y: list, edges: list) -> list:
  """
  A simple algorithm for edge-coloring bipartite multigraphs by Noga Alon (UNOFFICIAL)).

  Reference
  ---------
  https://www.tau.ac.il/~nogaa/PDFS/lex2.pdf

  Parameters
  ----------
  part_x: list of str
    The partition X of vertex.
  part_y: list of str
    The partition Y of vertex.
  edges : list of tuple of str
    Edges. : [(vertex in part_x, vertex in part_y), ...]

  Returns
  -------
  matchings: list
    Return the edge colors as list of matching.
  """

  # step0: Check parameters and convert.
  for vertex in part_x:
    part_x_without_vertex = list(part_x)
    part_x_without_vertex.remove(vertex)
    if not isinstance(vertex, str):
      raise TypeError(f"This vertex is not str: {vertex}")
    if vertex in part_x_without_vertex:
      raise ValueError(f"This is duplicate vertex in X: {vertex}")
  for vertex in part_y:
    part_y_without_vertex = list(part_y)
    part_y_without_vertex.remove(vertex)
    if not isinstance(vertex, str):
      raise TypeError(f"This vertex is not str: {vertex}")
    if vertex in part_y_without_vertex:
      raise ValueError(f"This is duplicate vertex in Y: {vertex}")
  for edge in edges:
    if not isinstance(edge, tuple):
      raise TypeError(f"This edge is not tuple: {edge}")
    if not isinstance(edge[0], str) or not isinstance(edge[1], str):
      raise TypeError(f"The vertex of this edge is not str: {edge}")
    if edge[0] not in part_x or edge[1] not in part_y:
      raise ValueError(f"The vertex of this edge is not in part: {edge}")
  part_x = {vertex: True for vertex in part_x}
  part_y = {vertex: True for vertex in part_y}
  edges  = [{"v_x": edge[0], "v_y": edge[1], "dummy": False} for edge in edges]

  # step1: Add isolated vertices to equalize the number of vertices in the partition.
  for i in range(abs(len(part_x) - len(part_y))):
    if len(part_x) < len(part_y):
      part_x[f"dummy_{i}"] = False
    else:
      part_y[f"dummy_{i}"] = False
  
  # step2: Make the graph k-regular by adding some edges
  max_degree_of_part_x = max([len([edge for edge in edges if edge["v_x"] == vertex]) for vertex in part_x.keys()])
  max_degree_of_part_y = max([len([edge for edge in edges if edge["v_y"] == vertex]) for vertex in part_y.keys()])
  max_degree = max(max_degree_of_part_x, max_degree_of_part_y)
  degree_of_part_x = {vertex: len([edge for edge in edges if edge["v_x"] == vertex]) for vertex in part_x.keys()}
  degree_of_part_y = {vertex: len([edge for edge in edges if edge["v_y"] == vertex]) for vertex in part_y.keys()}
  for vertex_x in degree_of_part_x.keys():
    for i in range(max_degree - degree_of_part_x[vertex_x]):
      while degree_of_part_y[list(degree_of_part_y.keys())[0]] == max_degree:
        del degree_of_part_y[list(degree_of_part_y.keys())[0]]
      edges.append({"v_x": vertex_x, "v_y": list(degree_of_part_y.keys())[0], "dummy": False})
      degree_of_part_y[list(degree_of_part_y.keys())[0]] += 1

  # step3: Make the edge colors as list of matching.
  list_of_edges_to_be_divided = [edges]
  matchings = []
  times_loop = 0
  while len(list_of_edges_to_be_divided) > 0:
    times_loop += 1
    print(times_loop)
    edges_to_be_divided = list_of_edges_to_be_divided.pop(0)
    degree = len([edge for edge in edges_to_be_divided if edge["v_x"] == edges_to_be_divided[0]["v_x"]])
    if degree % 2 == 0:
      return_edges = divide_graph(edges_to_be_divided)
      if degree == 2:
        matchings.append([(edge["v_x"], edge["v_y"]) for edge in return_edges[0] if part_x[edge["v_x"]] and part_y[edge["v_y"]]])
        matchings.append([(edge["v_x"], edge["v_y"]) for edge in return_edges[1] if part_x[edge["v_x"]] and part_y[edge["v_y"]]])
      else:
        list_of_edges_to_be_divided.append(return_edges[0])
        list_of_edges_to_be_divided.append(return_edges[1])
    else:
      t = int(math.log2(degree * len(part_x))) + 1
      matching = list(edges_to_be_divided)
      matching *= ((2 ** t) // degree)
      matching += [{"v_x": list(part_x.keys())[i], "v_y": list(part_y.keys())[i], "dummy": True} for i in range(len(part_x)) for j in range((2 ** t) % degree)]
      while len(matching) > len(part_x):
        return_edges = divide_graph(matching)
        numbers_of_dummy = [len([edge for edge in return_edges[i] if edge["dummy"]]) for i in range(2)]
        if numbers_of_dummy[0] < numbers_of_dummy[1]:
          matching = return_edges[0]
        else:
          matching = return_edges[1]
      matchings.append([(edge["v_x"], edge["v_y"]) for edge in matching if part_x[edge["v_x"]] and part_y[edge["v_y"]]])
      for edge in matching:
        edges_to_be_divided.remove(edge)
      list_of_edges_to_be_divided.append(edges_to_be_divided)
  return matchings
